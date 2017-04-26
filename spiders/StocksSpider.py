import scrapy
from items import FinassistItem
from pymongo.mongo_client import MongoClient
from scrapy.utils.project import get_project_settings


class StocksSpider(scrapy.Spider):
    name = "stocks"
    allowed_domains = ["moneycontrol.com"]
    start_urls = [
        "http://www.moneycontrol.com/india/stockpricequote/paints-varnishes/bergerpaintsindia/BPI02",
        "http://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/jbchemicalspharmaceuticals/JBC01",
        "http://www.moneycontrol.com/india/stockpricequote/infrastructure-general/larsentoubro/LT",
        "http://www.moneycontrol.com/india/stockpricequote/banks-public-sector/statebankindia/SBI",
        "http://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/sunpharmaceuticalindustries/SPI",
        "http://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/unichemlaboratories/UL02",
        "http://www.moneycontrol.com/india/stockpricequote/banks-private-sector/yesbank/YB",
        "http://www.moneycontrol.com/india/stockpricequote/engineering-heavy/prajindustries/PI17",
        "http://www.moneycontrol.com/india/stockpricequote/electric-equipment/technoelectricengineeringcompany/TEE",
        "http://www.moneycontrol.com/india/stockpricequote/power-generation-distribution/torrentpower/TP14",
        "http://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/aartidrugs/AD",
        "http://www.moneycontrol.com/india/stockpricequote/transport-logistics/containercorporationindia/CCI",
        "http://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/hikal/H05",
        "http://www.moneycontrol.com/india/stockpricequote/computers-software-medium-small/kelltontechsolutions/VMF",
        "http://www.moneycontrol.com/india/stockpricequote/plastics/nilkamal/NP08",
        "http://www.moneycontrol.com/india/stockpricequote/engineering-heavy/sanghvimovers/SM10",
        "http://www.moneycontrol.com/india/stockpricequote/auto-lcvs-hcvs/tatamotors/TM03",
        "http://www.moneycontrol.com/india/stockpricequote/finance-housing/gichousingfinance/GIC",
        "http://www.moneycontrol.com/india/stockpricequote/construction-contracting-civil/gayatriprojects/GP10",
        "http://www.moneycontrol.com/india/stockpricequote/textiles-readymade-apparels/gokaldasexports/GE05",
        "http://www.moneycontrol.com/india/stockpricequote/textiles-readymade-apparels/indianterrainfashions/ITF",
        "http://www.moneycontrol.com/india/stockpricequote/cigarettes/itc/ITC",
        "http://www.moneycontrol.com/india/stockpricequote/textiles-spinning-cotton-blended/nitinspinners/NS12",
        "http://www.moneycontrol.com/india/stockpricequote/finance-general/capitalfirst/FCH",
        "http://www.moneycontrol.com/india/stockpricequote/construction-contracting-real-estate/godrejproperties/GP11",
        "http://www.moneycontrol.com/india/stockpricequote/dyes-pigments/kiriindustries/KDC01",
        "http://www.moneycontrol.com/india/stockpricequote/petrochemicals/goacarbon/GC04",
        "http://www.moneycontrol.com/india/stockpricequote/auto-lcvs-hcvs/tatamotorsdvr/TMD",
        "http://www.moneycontrol.com/india/stockpricequote/media-entertainment/jagranprakashan/JP12",
        "http://www.moneycontrol.com/india/stockpricequote/cables-power-others/keiindustries/KEI",
        "http://www.moneycontrol.com/india/stockpricequote/miscellaneous/greenplyindustries/GI19",
        "http://www.moneycontrol.com/india/stockpricequote/personal-care/daburindia/DI"
    ]

    def getDB(self):
        settings = get_project_settings()
        client = MongoClient(settings.get("MONGODB_HOST"), settings.getint("MONGODB_PORT"))
        #db = client[settings.get('MONGODB_DATABASE', 'TestDB')]
        db = client[settings.get('MONGODB_DATABASE')]
        return db
    
    
    def saveData(self, item):
        db = self.getDB()
        db.stockDetails.update({"name" : item['name']}, item, upsert=True )

    def parse(self, response):
        item = FinassistItem()
        item['name'] = response.xpath('//div[@id="nChrtPrc"]//h1[@class="b_42"]/text()').extract()[0]
        item['price'] = response.xpath('//div[@class="stockDtl PB30"]//div[@id="Nse_Prc_tick_div"]//span[@class="PA2"]/strong/text()').extract()[0]

        self.saveData(item)
        return item
