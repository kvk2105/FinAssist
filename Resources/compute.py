from pymongo import MongoClient
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
client = MongoClient(settings.get("MONGODB_HOST"),settings.getint("MONGODB_PORT"))
db = client['tempdb']

stocksPrice={}
for stk in db['tab2'].find({}):
	stocksPrice[stk['name']] = stk['price']	
print	

amountMap={}
for stk in db['tab1'].aggregate([{"$group":{"_id":"$name","totalAmount":{"$sum":{"$multiply":["$price","$units"]}}}}]):
	amountMap[stk['_id']] = stk['totalAmount']

unitsMap = {}
for stk in db['tab1'].aggregate([{"$group":{"_id":"$name","totalUnits":{"$sum":"$units"}}}]):
	unitsMap[stk['_id']] = stk['totalUnits']

print "StockName, CurrentPrice, AveragePrice, Percentage"
for name,totalAmount in amountMap.items():
	avgPrice = (totalAmount / unitsMap[name])
	percentage = ( (stocksPrice[name] - avgPrice) / avgPrice ) * 100
	print name, stocksPrice[name], avgPrice, percentage, "%"
