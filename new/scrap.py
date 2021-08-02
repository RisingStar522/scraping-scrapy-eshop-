import os
import sys
import json
import re
import boto3


from scrapy import signals
# from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
import scrapy

from .target import Targetcom
from .sears import Searscom
from .sephora import Sephoracom
from .dicks import Dickscom



# dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# TABLE_NAME = "deciders"

# response = dynamodb.get_item(
#     TableName=TABLE_NAME,
#     Key={
#         'name': {'S':'search_sort'},
#     }
# )
 
# if response["Item"] is not None:
#     SHOULD_SORT = response['Item']["enabled"]["BOOL"]
# else:
#     SHOULD_SORT = True

SHOULD_SORT = True
def search(searchkey):
    print(f'SEARCHING FOR {searchkey}')
    productlist = []
    

    # bestbuyObj = Bestbuycom(searchkey)
    # bestbuyObj.start()

    # neweggObj = Neweggcom(searchkey)
    # neweggObj.start()

    searsObj = Searscom(searchkey)
    searsObj.start()

    # walmartObj = Walmartcom(searchkey)
    # walmartObj.start()

    # amazonObj = Amazoncom(searchkey)
    # amazonObj.start()

    sephoraObj = Sephoracom(searchkey)
    sephoraObj.start()
    
    targetObj = Targetcom(searchkey)
    targetObj.start()

    # barnObj = Barncom(searchkey)
    # barnObj.start()

    # ultaObj = Ultacom(searchkey)
    # ultaObj.start()

    # costcoObj = Costcocom(searchkey)
    # costcoObj.start()
    
    # dicksObj = Dickscom(searchkey)
    # dicksObj.start()
    # print("Searchkey-------", searchkey)
    # bedbatObj = Bedbatcom(searchkey)
    # bedbatObj.start()
  
    targetObj.join()
    # bestbuyObj.join()
    # neweggObj.join()
    searsObj.join()
    # walmartObj.join()
    # amazonObj.join()
    sephoraObj.join()
    # barnObj.join()
    # ultaObj.join()
    # costcoObj.join()
    # dicksObj.join()
    # bedbatObj.join()

    productlist += targetObj.goodlist
    # productlist += bestbuyObj.goodlist
    # productlist += neweggObj.goodlist
    productlist += searsObj.goodlist
    # productlist += walmartObj.goodlist
    # productlist += amazonObj.goodlist
    productlist += sephoraObj.goodlist
    # productlist += barnObj.goodlist
    # productlist += ultaObj.goodlist
    # productlist += costcoObj.goodlist
    # productlist += dicksObj.goodlist
    
    # productlist += bedbatObj.goodlist

  
    if SHOULD_SORT is True:
        print("SORTING")
        for x in productlist:
            if ( x.get('price') == None): 
                x["price"] = ""

            x['price'] = re.sub('[^0-9|.]',"", x['price'])
            pos = x['price'].find(".")
            if ( pos != -1 ): x['price'] = x['price'][:pos+3]

        productlist = sorted(productlist, key=lambda x: (len(x['price']), x['price'] ), reverse = True )
    
    del targetObj
    # del bestbuyObj
    # del neweggObj
    del searsObj
    # del walmartObj
    # del amazonObj
    del sephoraObj
    # del barnObj
    # del ultaObj
    # del costcoObj
    # del dicksObj
    # del bedbatObj


    return json.dumps(productlist)
    # return "asdfasdfasfdasdf"