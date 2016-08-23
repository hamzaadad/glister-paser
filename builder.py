import urllib, requests, random, json, time, os
from os.path import join, getsize

MyKey = 'AIzaSyAl2O8R9k03nCeLqSgLs6nkfXU-sakI_P4'


for root, dirs, files in os.walk('meknes'):
    for f in files:
        link =  "meknes/"+f
        type_name = f.replace("_"+f.replace(".json", "").split("_")[-1], "").replace(".json", "")
        f_data = open(link, 'r').read()
        j_data = json.loads(f_data)
        if "results" in j_data:
            for result in j_data["results"]:
                js_resp = requests.get("https://maps.googleapis.com/maps/api/place/details/json?placeid="+result["place_id"]+"&key="+MyKey)
                if js_resp.status_code == 200:
                    if not os.path.exists("places_folder/"+result["place_id"]):
                        os.makedirs("places_folder/"+result["place_id"])
                        open("places_folder/"+result["place_id"]+"/result.json", "w").write(json.dumps(json.loads(js_resp.text)))
                print result["place_id"]
