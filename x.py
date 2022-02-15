# import imp
import pprint
# import time
# import googlemaps


# Api_key='fcedcc5b15678ad9a5764177740f2536'

# gmaps=googlemaps.Client(key=Api_key)

# places_result=gmaps.place_nearby(location='26.8010238,75.7976769', radius=4000,type='cafe')
# pprint.pprint(places_result)



# http://apis.mapmyindia.com/advancedmaps/v1/<licence_key>/geo_code?place_detail?place_id=<eLoc> 



import requests
import json

# set up the request parameters
params = {
  'api_key': '2D7F91CEBBD14C53A953EA7DD3197902',
  'q':['-8.705833, 115.261377'],
  'keywords':'restaurant',
  'radius':'1000'


}

# make the http GET request to SerpWow
api_result = requests.get('https://api.serpwow.com/search', params)

# print the JSON response from SerpWow
data=json.dumps(api_result.json())
pprint.pprint(data)

