import pprint
import requests

base_url = "https://api.themoviedb.org/3"
api_key = "api_key=c3d5cd287179507f4783766b3ff53e0f"
api_url = base_url + '/tv/456?' + api_key
# tv_id = Show.objects.all().order_by('id')
# endpoint_path = f"/tv/{tv_id}"
# endpoint = base_url + endpoint_path + api_key
   
     
response = requests.get(api_url)
data = response.json()
poster = data["poster_path"]
pprint.pprint(poster)
