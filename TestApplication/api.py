from flask_restful import reqparse, abort, Api, Resource
import requests
import json

parser=reqparse.RequestParser()
parser.add_argument('zip')
api_key="2af827ed3f9867ad2cee000d60426cfd"
class GetWeather():
    def __init__(self):
        self.filters="";

    def search(self,data):
        query="http://api.openweathermap.org/data/2.5/weather?zip={0}&units=imperial&appid={1}".format(data, api_key)

        response=requests.request("GET", query)
        json_object=json.loads(response.text.encode('utf8'))
        print(json_object)
        return json_object

class API_getWeather(Resource):
    def get(self):
        print("doing search")
        args=parser.parse_args()
        api=GetWeather()
        user_zip=args['zip']
        print(user_zip)
        weather=api.search(user_zip)
        return json.dumps(weather)

