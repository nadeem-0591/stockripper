import requests,os,time,datetime
from lxml import html
import pandas as pd
from selenium import webdriver
from yahoo_earnings_calendar import YahooEarningsCalendar
import settings as cfg
import mysql as db
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from tqdm import tqdm

pwd=os.getcwd()
chromedriver=os.path.join(pwd,"chromedriver.exe")

##driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

def GetCompanieslist():
	print("@"*20+"  Pls Hang on getting data from YahooEarningsCalendar API  "+"@"*20)
	yec = YahooEarningsCalendar()

	date_from=pd.to_datetime(cfg.defaults["startdate"])  ##convert str to date format
	date_to=pd.to_datetime(cfg.defaults["enddate"])
	data=yec.earnings_between(date_from,date_to)  ### Pull the data
	print('\n'*2)
	print("Successfully Fetched the data for time range",date_from,date_to)
	print('\n'*2)
	df=pd.DataFrame(data) 						  ### Convert into DataFrame												
	df=df.sort_values(by=['epsestimate'],ascending=False) ## Sort in Asc order by epsestimate
	#df=df[df.epsestimate>cfg.defaults["epsestimate_threshold"]] ## Filter the records
	df.startdatetime=df.startdatetime.apply(lambda a: pd.to_datetime(a).strftime("%Y-%m-%d %H:%M:%S"))
	df.fillna(0,inplace=True)
	for idx,data in df.iterrows():
		status=db.EarningCalender(data)
		#print(status,idx)
	companies=df.ticker.tolist()    ### Get the companies list
	#print(df.head())
	if companies:
		output={"companies":companies,"status":True}
	else:
		output={"companies":companies,"status":False}
	return output

def GetAnalysisdata(company):
	res=requests.get(f'https://finance.yahoo.com/quote/{company}/analysis?p={company}')
	tree=html.fromstring(res.text)
	columns=[]
	table_data=[]
	if(tree.xpath('//*[@id="Col1-0-AnalystLeafPage-Proxy"]/section/table')):
	    for table in tree.xpath('//*[@id="Col1-0-AnalystLeafPage-Proxy"]/section/table'):
	        col=[]
	        for head in table.xpath('./thead'):
	            for span in head.xpath('./tr/th'): 
	                col.append(span.text_content())
	                #print(span.text_content())
	        columns.append(col)
	        for row in table.xpath('./tbody/tr'):
	            roww=[]
	            for td in row.xpath('./td'):
	                roww.append(td.text_content())
	            table_data.append(roww)
	else:
	    pass
	    #print(f"No Data Found {company}")
	return columns,table_data


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


def GetFinancialdata(company):
	pass



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

def ProcessAnalysisData(columns,table_data,company):
	df_list=[]
	col_count=[5,6,4,5,4,6]
	a,b=0,0
	for j,colcnt in enumerate(col_count):
	    mcols=[]
	    b=colcnt+a
	    sdata=table_data[a:b]  
	    for i in range(b-a):
	        mcols.append(sdata[i][0])
	    #print(",".join(mcols))
	    test=pd.DataFrame(columns=mcols)
	    test.insert(0,'Quarter',columns[j][1:])
	    for idx,colm in enumerate(mcols):
	    	test[colm]=sdata[idx][1:]
	    	try:
	    		test[colm].replace({'%':''}, regex=True,inplace=True)
	    		test.replace('N/A',0,inplace=True)
	    		test[colm]=test[colm].astype(float)
	    	except:
	    		pass
	    test['date']=datetime.datetime.now().strftime("%Y-%m-%d")
	    test['ticker']=company
	    for eachcol in test.columns:
	    	try:
	    		test[eachcol]=test[eachcol].apply(lambda x: float(str(x).replace(',','')))
	    	except:
	    		pass

	    df_list.append(test)
	    #print(test)
	    a=b
	return df_list


output=GetCompanieslist()
print("@"*100)
print(f"Found {len(output['companies'])} companies")
print("@"*100)

if(output['status']):
	driver=initWebdriver()
	for company in tqdm(output['companies']):
		print(f"Getting Analysis data for company code {company}")
		columns,table_data=GetAnalysisdata(company)
		if(columns):
			tables_list=ProcessAnalysisData(columns,table_data,company)
			for tableno,tabledf in enumerate(tables_list):
				#print(f"Inserting into table no{tableno} with length")
				if tableno==0:
					for idx,data in tabledf.iterrows():
						db.EarningEstimates(False,data)
				elif tableno==1:
					for idx,data in tabledf.iterrows():
						db.RevenueEstimate(False,data)
				elif tableno==2:
					for idx,data in tabledf.iterrows():
						db.EarningHistory(False,data)
				elif tableno==3:
					for idx,data in tabledf.iterrows():
						db.EPSTrend(False,data)
				elif tableno==4:
					for idx,data in tabledf.iterrows():
						db.EPSRevisions(False,data)
				elif tableno==5:
					for idx,data in tabledf.iterrows():
						db.GrowthEstimates(False,data)
		else:
			data={'ticker':company,'Quarter':''}
			db.EarningEstimates(True,data)
			db.RevenueEstimate(True,data)
			db.EarningHistory(True,data)
			db.EPSTrend(True,data)
			db.EPSRevisions(True,data)
			db.GrowthEstimates(True,data)
		print(f"Getting historical data for company code {company}")
		historicdata=GetHistoricaldata(company,driver)
		historicdata.fillna(0,inplace=True)
		print(f"Inserting historical data for company code {company}")
		for index,rdata in historicdata.iterrows():
			status=db.Inserthistoricdata(rdata)
		

	driver.close()
else:
	Print("No Companies found for your TimeRange,\
		Please expand the time range")

