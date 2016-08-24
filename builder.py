import urllib, requests, random, json, time, os
from os.path import join, getsize

MyKey = 'AIzaSyCSP0xOu_wMiCABpVUugtRxSutpN8lgRaM'


for root, dirs, files in os.walk('meknes'):
    for f in files:
        link =  "meknes/"+f
        type_name = f.replace("_"+f.replace(".json", "").split("_")[-1], "").replace(".json", "")
        f_data = open(link, 'r').read()
        j_data = json.loads(f_data)
        if "results" in j_data:
            for result in j_data["results"]:
                if not os.path.exists("places_folder/"+type_name+"/"+result["place_id"]):
                    print type_name
                    js_resp = requests.get("https://maps.googleapis.com/maps/api/place/details/json?placeid="+result["place_id"]+"&key="+MyKey)
                    if js_resp.status_code == 200:
                        if not os.path.exists("places_folder/"+type_name+"/"+result["place_id"]):
                            os.makedirs("places_folder/"+type_name+"/"+result["place_id"])
                            open("places_folder/"+type_name+"/"+result["place_id"]+"/result.json", "w").write(json.dumps(json.loads(js_resp.text)))
                            if "photos" in result:
                                for photo in result["photos"]:
                                    photo_url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth="+str(photo["width"])+"&photoreference="+photo["photo_reference"]+"&key=" + MyKey
                                    photo_data = requests.get(photo_url, stream=True)
                                    if photo_data.status_code == 200:
                                        with open("places_folder/"+type_name+"/"+result["place_id"]+"/"+str(random.randint(0,999999))+".png", "wb") as f:
                                            for chunk in photo_data.iter_content(1024):
                                                f.write(chunk)
                                    else:
                                        print "cant get image", photo_data.status_code
                            else:
                                print "has no images", result["place_id"]
                    else:
                        print "error request:", js_resp.status_code
                else:
                    print "error:" ,type_name, result["place_id"]
