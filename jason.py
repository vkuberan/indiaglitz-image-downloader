import time
import json
import shutil
import requests

data = """
{
   "name":"Shivani Narayanan",
   "recs":180,
   "currentitem":3126820,
   "currentpage":177,
   "totalpages":2,
   "category":"Actress",
   "language":"tamil",
   "type":"gallery",
   "catid":"1",
   "cid":"8859",
   "imgSrvr":"https:\/\/1847884116.rsc.cdn77.org\/tamil\/gallery\/actress\/shivaninarayanan\/",
   "baseurl":"http:\/\/www.indiaglitz.com\/shivani-narayanan-gallery-images-tamil-1-",
   "images":[
      {
         "id":3126820,
         "image":"shivaninarayanan090620_4.jpg",
         "clicks":"0"
      },
      {
         "id":3126819,
         "image":"shivaninarayanan090620_3.jpg",
         "clicks":"0"
      },
      {
         "id":3126818,
         "image":"shivaninarayanan090620_2.jpg",
         "clicks":"0"
      },
      {
         "id":3126817,
         "image":"shivaninarayanan090620_1.jpg",
         "clicks":"0"
      }
   ]
}
"""
process_data = json.loads(data)

if 'images' in process_data:
    for image in process_data['images']:
        url = 'https://1847884116.rsc.cdn77.org/tamil/gallery/actress/shivaninarayanan/' + \
            image['image']
        imagename = image['image']
        print(url)

        response = requests.get(url, stream=True)
        with open(imagename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        time.sleep(3)
