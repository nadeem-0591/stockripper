import time,datetime
from lxml import html
import pandas as pd
from selenium import webdriver
from yahoo_earnings_calendar import YahooEarningsCalendar
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import pymysql.cursors
import settings as cfg

### Current date 
cdate=datetime.datetime.now().strftime("%Y-%m-%d")

########### Initialise webdriver
def initWebdriver():
    options = webdriver.ChromeOptions()
    print("Headless Mode",cfg.defaults['headless'])
    if(cfg.defaults['headless']):
        options.add_argument('headless')
    else:
    	print("Running in Normal Mode")
    driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),options=options)
    #webdriver.Chrome(executable_path=chromedriver, options=options)
    return driver


###### Get historical Data
def GetHistoricaldata(company,driver):
	driver.get(f'https://in.finance.yahoo.com/quote/{company}/history?p={company}')
	for i in range(10):
		time.sleep(1)     ### Scroll the webpage to load data dynamically
		driver.execute_script("window.scrollBy(0,1000)","")
		tree=html.fromstring(driver.page_source)
		#print('Scrolling')
	### Get the Column Names
	columnNames=['Date', 'Open', 'High', 'Low', 'Close*', 'Adj. close**', 'Volume']
	#for header in tree.xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/thead/tr'):
	#    for column in header.xpath('./th'):
	#        columnNames.append(column.text_content())
	### get the row data
	finalrows=[]
	for row in tree.xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]/table/tbody/tr'):
	    row_data=[]
	    for col in row.xpath('./td'):
	        row_data.append(col.text_content())
	    if(len(row_data)==len(columnNames)):
	        finalrows.append(row_data)
	df2=pd.DataFrame(finalrows,columns=columnNames)
	df2=df2.astype(str)
	df2.replace('-',0,inplace=True)
	df2.Volume=df2.Volume.apply(lambda x: float(str(x).replace(',','')))
	df2['Date']=df2.Date.apply(lambda x:pd.to_datetime(x,format='%d-%b-%Y').strftime("%Y-%m-%d"))#
	for i in ['Open', 'High', 'Low', 'Close*', 'Adj. close**']:
		df2[i]=df2[i].apply(lambda x: float(str(x).replace(',','')))
		df2[i]=df2[i].astype(float)

	df2['Difference_close_price']=df2['Close*'].diff()
	df2['close_status']=df2.Difference_close_price.apply(lambda x:1 if x>0 else 0)
	df2['Difference_volume_price']=df2['Volume'].diff()
	df2['volume_status']=df2.Difference_volume_price.apply(lambda x:1 if x>0 else 0)
	print("Shape",df2.shape)
	n=cfg.defaults['meancount']
	mean=[]
	for index,data in df2.iterrows():
	    mean.append(df2.loc[index+1:n+1+index].Volume.mean())
	df2.insert(len(df2.columns),'MeanVolume',mean)
	df2.insert(0,'ticker',company)
	if(len(df2)==0):
		#print("Before",df2.head())
		rowa=["" for i in range(len(df2.columns))]
		rowa[0]=company
		df2.loc[0]=rowa
		df2['Date']=datetime.datetime.now().strftime("%Y-%m-%d")
		print("Empty DataFrame Farooq Pls check")
		#print(df2.head())
	#df2.to_excel("Test.xlsx",index=False)
	return df2

### Insert into database
def Inserthistoricdata(connection,data):
	# # Insert a single record
	cursor=connection.cursor()
	try:
		checkdata="select * from history where Ticker="+f"'{data['ticker']}'"+\
		"and (Date is null or Date="+f"'{data['Date']}'"+")"
		cursor.execute(checkdata)
		result = cursor.fetchone()

		if(not result ):
			sql="""INSERT INTO history (Ticker,Date,open,Close,High,Low,\
			Adj_close,Volume,dffrnc_btn_prvsdy_cls,is_prvsdy_dffrnc_cls_pstv,\
			dffrnc_btn_prvsdy_volume,is_prvsdy_dffrnc_vlme_pstv,cdate,meanvolume) values (%s,%s,%s,%s,%s,\
			%s,%s,%s,%s,%s,%s,%s,%s,%s) """
			values=(data['ticker'],data['Date'],data['Open'],data['Close*'],\
			data['High'],data['Low'],data['Adj. close**'],data['Volume'],\
			data['Difference_close_price'],data['close_status'],data['Difference_volume_price'],\
			data['volume_status'],cdate,data['MeanVolume'])

			emptyrecord="""INSERT INTO history (Ticker,cdate) values(%s,%s)"""
			if(data['Open']):
				pass
			else:
				sql=emptyrecord
				values=(data['ticker'],cdate)
			cursor.execute(sql,values)
			connection.commit()
		else:
			pass
			#print("Record Already Exists")
		status=True
	except Exception as e:
		print("An error occured while committing to Database",e)
		status=False
	return status

#### Get db Connection
def getdbconnection():
	# Connect to the database
	connection = pymysql.connect(
								host=cfg.database['host'],
	                            user=cfg.database['username'],
	                            password=cfg.database['password'],
	                            database=cfg.database['database'],
	                            cursorclass=pymysql.cursors.DictCursor
	                            )
	return connection

### Get daily tickers from database
def GetCompanies(connection):
	cursor=connection.cursor()
	sql="select * from dailyruns"
	cursor.execute(sql)
	result=cursor.fetchall()
	return result

dbconnection=getdbconnection()
tickerdata=GetCompanies(dbconnection)
if(tickerdata):
	df=pd.DataFrame(tickerdata)
	print(df)
	driver=initWebdriver()
	for index,data in df.iterrows():
		totaldata=GetHistoricaldata(data['ticker'],driver)
		totaldata.fillna(0,inplace=True)
		#print(totaldata)
		required_data=totaldata[(pd.to_datetime(totaldata['Date']).dt.date>data['startdate'])\
		&(pd.to_datetime(totaldata['Date']).dt.date<data['enddate'])]
		print(f"Inserting ticker {data['ticker']} into database")
		for inde,rdata in required_data.iterrows():
			status=Inserthistoricdata(dbconnection,rdata)
	driver.close()
else:
	print("No Data is available from the dailyruns table")



