from pymongo import MongoClient
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
client = MongoClient(settings.get("MONGODB_HOST"),settings.getint("MONGODB_PORT"))
db = client[settings.get('MONGODB_DATABASE')]

stocksPrice={}
for stk in db['stockDetails'].find({}):
	stocksPrice[stk['name']] = stk['price']

amountMap={}
for stk in db['investments'].aggregate([{"$group":{"_id":"$stock","totalAmount":{"$sum":{"$multiply":["$price","$units"]}}}}]):
	amountMap[stk['_id']] = stk['totalAmount']

unitsMap = {}
for stk in db['investments'].aggregate([{"$group":{"_id":"$stock","totalUnits":{"$sum":"$units"}}}]):
	unitsMap[stk['_id']] = stk['totalUnits']

print "StockName, AveragePrice, CurrentPrice, Percentage"
for name,totalAmount in amountMap.items():
	avgPrice = (totalAmount / unitsMap[name])
	percentage = ( (float(stocksPrice[name]) - avgPrice) / avgPrice ) * 100
	print name, avgPrice, stocksPrice[name], int(percentage),"%"
	print
	