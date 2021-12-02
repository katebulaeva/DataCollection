import requests
from pprint import pprint
import json

api_key = "368bcaa66a5d98471cd43a4a9461bf4fd1ee8526"
city = 'munich'

url = 'https://api.waqi.info/search/'


params = {'token': api_key, 'keyword': city}

response = requests.get(url, params=params)


j_data = response.json()
pprint(j_data)

#AQI	Air Pollution Level	Health Implications	Cautionary Statement (for PM2.5)
#0 - 50	Good	Air quality is considered satisfactory, and air pollution poses little or no risk	None
#51 -100	Moderate	Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.	Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.
#101-150	Unhealthy for Sensitive Groups	Members of sensitive groups may experience health effects. The general public is not likely to be affected.	Active children and adults, and people with respiratory disease, such as asthma, should limit prolonged outdoor exertion.
#151-200	Unhealthy	Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects	Active children and adults, and people with respiratory disease, such as asthma, should avoid prolonged outdoor exertion; everyone else, especially children, should limit prolonged outdoor exertion
#201-300	Very Unhealthy	Health warnings of emergency conditions. The entire population is more likely to be affected.	Active children and adults, and people with respiratory disease, such as asthma, should avoid all outdoor exertion; everyone else, especially children, should limit outdoor exertion.
#300+	Hazardous	Health alert: everyone may experience more serious health effects	Everyone should avoid all outdoor exertion