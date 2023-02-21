import pymysql.cursors
import settings as cfg
#import pandas as pd
from datetime import datetime

# Connect to the database
connection = pymysql.connect(
							host=cfg.database['host'],
                            user=cfg.database['username'],
                            password=cfg.database['password'],
                            database=cfg.database['database'],
                            cursorclass=pymysql.cursors.DictCursor
                            )
cursor=connection.cursor()


cdate=datetime.now().strftime("%Y-%m-%d")

def Inserthistoricdata(data):
	# # Insert a single record
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



def EarningEstimates(nullrec,data):
	try:
		checkdata="select * from earningestimate where ticker="+f"'{data['ticker']}'"+\
		"and (quarter is null or quarter="+f"'{data['Quarter']}'"+")"
		#print(checkdata)
		cursor.execute(checkdata)
		result = cursor.fetchone()
		#print(result)
		if (not result):
			if(nullrec):
				sql="""INSERT INTO earningestimate (ticker,date) values(%s,%s)"""
				values=(data['ticker'],cdate)
				print('Inserting a null rec')
			else:
				sql="""INSERT INTO earningestimate (ticker,quarter,noofanalyst,\
				avgestimate,lowestimate,highestimate,yearagoeps,date) values (%s,%s,%s,%s,%s,\
				%s,%s,%s) """
				values=(data['ticker'],data['Quarter'],data['No. of Analysts'],\
				data['Avg. Estimate'],data['Low Estimate'],data['High Estimate'],\
				data['Year Ago EPS'],data['date'])
			#print(sql)
			cursor.execute(sql,values)
			connection.commit()
		else:
			print("Record Already exists")
		status=True
	except Exception as e:
		print("An error occured while pushing the record",e)
		status=False
	return status



def RevenueEstimate(nullrec,data):
	try:
		checkdata="select * from revenueestimates where ticker="+f"'{data['ticker']}'"+\
		"and (quarter is null or quarter="+f"'{data['Quarter']}'"+")"
		#print(checkdata)
		cursor.execute(checkdata)
		result = cursor.fetchone()
		#print(result)
		if (not result):
			if(nullrec):
				sql="""INSERT INTO revenueestimates (ticker,date) values(%s,%s)"""
				values=(data['ticker'],cdate)
				print('Inserting a null rec')
			else:
				sql="""INSERT INTO revenueestimates (ticker,quarter,noofanalyst,\
				avgestimate,lowestimate,highestimate,yearagosales,date,Salesgrowthpercent)\
				 values (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
				values=(data['ticker'],data['Quarter'],data['No. of Analysts'],\
				data['Avg. Estimate'],data['Low Estimate'],data['High Estimate'],\
				data['Year Ago Sales'],data['date'],data['Sales Growth (year/est)'])
			#print(sql)
			cursor.execute(sql,values)
			connection.commit()
		else:
			print("Record Already exists")
		status=True
	except Exception as e:
		print("An error occured while pushing the record",e)
		status=False
	return status


def EarningHistory(nullrec,data):
	try:
		checkdata="select * from earninghistory where ticker="+f"'{data['ticker']}'"+\
		"and (quarter is null or quarter="+f"'{data['Quarter']}'"+")"
		#print(checkdata)
		cursor.execute(checkdata)
		result = cursor.fetchone()
		#print(result)
		if (not result):
			if(nullrec):
				sql="""INSERT INTO earninghistory (ticker,date) values(%s,%s)"""
				values=(data['ticker'],cdate)
				print('Inserting a null rec')
			else:
				sql="""INSERT INTO earninghistory (ticker,quarter,esteps,\
				actualeps,difference,surprise,date)\
				 values (%s,%s,%s,%s,%s,%s,%s) """
				values=(data['ticker'],data['Quarter'],data['EPS Est.'],\
				data['EPS Actual'],data['Difference'],data['Surprise %'],data['date'])
			#print(sql)
			cursor.execute(sql,values)
			connection.commit()
		else:
			print("Record Already exists")
		status=True
	except Exception as e:
		print("An error occured while pushing the record",e)
		status=False
	return status



def EPSTrend(nullrec,data):
	try:
		checkdata="select * from epstrend where ticker="+f"'{data['ticker']}'"+\
		"and (quarter is null or quarter="+f"'{data['Quarter']}'"+")"
		#print(checkdata)
		cursor.execute(checkdata)
		result = cursor.fetchone()
		#print(result)
		if (not result):
			if(nullrec):
				sql="""INSERT INTO epstrend (ticker,date) values(%s,%s)"""
				values=(data['ticker'],cdate)
				print('Inserting a null rec')
			else:
				sql="""INSERT INTO epstrend (ticker,quarter,currentestimate,7daysago,\
				30daysago,60daysago,90daysago,date)\
				 values (%s,%s,%s,%s,%s,%s,%s,%s) """
				values=(data['ticker'],data['Quarter'],data['Current Estimate'],\
				data['7 Days Ago'],data['30 Days Ago'],data['60 Days Ago'],\
				data['90 Days Ago'],data['date'])
			#print(sql)
			cursor.execute(sql,values)
			connection.commit()
		else:
			print("Record Already exists")
		status=True
	except Exception as e:
		print("An error occured while pushing the record",e)
		status=False
	return status



def EPSRevisions(nullrec,data):
	try:
		checkdata="select * from epsrevisions where ticker="+f"'{data['ticker']}'"+\
		"and (quarter is null or quarter="+f"'{data['Quarter']}'"+")"
		#print(checkdata)
		cursor.execute(checkdata)
		result = cursor.fetchone()
		#print(result)
		if (not result):
			if(nullrec):
				sql="""INSERT INTO epsrevisions (ticker,date) values(%s,%s)"""
				values=(data['ticker'],cdate)
				print('Inserting a null rec')
			else:
				sql="""INSERT INTO epsrevisions (ticker,quarter,uplast7days,\
				uplast30days,downlast7days,downlast30days,date)\
				 values (%s,%s,%s,%s,%s,%s,%s) """
				values=(data['ticker'],data['Quarter'],data['Up Last 7 Days'],\
				data['Up Last 30 Days'],data['Down Last 7 Days'],data['Down Last 30 Days'],\
				data['date'])
			#print(sql)
			cursor.execute(sql,values)
			connection.commit()
		else:
			print("Record Already exists")
		status=True
	except Exception as e:
		print("An error occured while pushing the record",e)
		status=False
	return status

def GrowthEstimates(nullrec,data):
	try:
		checkdata="select * from growthestimates where ticker="+f"'{data['ticker']}'"+\
		"and (division is null or division="+f"'{data['Quarter']}'"+")"
		#print(checkdata)
		cursor.execute(checkdata)
		result = cursor.fetchone()
		#print(result)
		if (not result):
			if(nullrec):
				sql="""INSERT INTO growthestimates (ticker,date) values(%s,%s)"""
				values=(data['ticker'],cdate)
				print('Inserting a null rec')
			else:
				sql="""INSERT INTO growthestimates (ticker,division,currqtr,\
				nextqtr,curryear,nextyear,next5years,past5years,date)\
				 values (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
				values=(data['ticker'],data['Quarter'],data['Current Qtr.'],\
				data['Next Qtr.'],data['Current Year'],data['Next Year'],\
				data['Next 5 Years (per annum)'],data['Past 5 Years (per annum)'],\
				data['date'])
			#print(sql)
			cursor.execute(sql,values)
			connection.commit()
		elif len(data)>3:
			print("Updating the growth estimates tables")
			cursor.execute("""UPDATE growthestimates SET currqtr=%s,nextqtr=%s,curryear=%s,nextyear=%s,\
			next5years=%s,past5years=%s,date=%s""",(data['Current Qtr.'],data['Next Qtr.'],data['Current Year'],data['Next Year'],\
			data['Next 5 Years (per annum)'],data['Past 5 Years (per annum)'],data['date']))

		else:
			print("GrowthEstimate record already exists")
		status=True

	except Exception as e:
		print("An error occured while Updating the record",e)
		print("Data which is to be updated",data)
		status=False
	return status





def EarningCalender(data):
	try:
		checkdata="select * from earningcalender where ticker="+f"'{data['ticker']}'"+\
		"and (startdatetime is null or startdatetime="+f"'{data['startdatetime']}'"+")"
		#print(checkdata)
		cursor.execute(checkdata)
		result = cursor.fetchone()
		#print(result)
		if (not result):
			sql="""INSERT INTO earningcalender (ticker,company,startdatetime,\
			datetimetype,epsestimate,epsactual,epssurpricepct,timezone,\
			gmtoffsetmilliseconds,quotetype,date)\
			 values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
			values=(data['ticker'],data['companyshortname'],data['startdatetime'],\
			data['startdatetimetype'],data['epsestimate'],data['epsactual'],\
			data['epssurprisepct'],data['timeZoneShortName'],data['gmtOffsetMilliSeconds'],\
			data['quoteType'],cdate)
			#print(sql)
			cursor.execute(sql,values)
			connection.commit()
		else:
			print("Record Already exists")
		status=True
	except Exception as e:
		print("An error occured while pushing the record",e)
		status=False
	return status












# df=pd.read_excel(r"C:\Users\DELL\Music\Stockripper\earningcalender.xlsx")

# # data={'ticker':'umar','Quarter':''}
# # RevenueEstimate(True,data)
# for idx,data in df.iterrows():
# 	status=EarningCalender(data)
# 	print(status,idx)
	
	

