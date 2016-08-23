from bs4 import BeautifulSoup
import urllib, requests, random, json, time

MyKey = 'AIzaSyAl2O8R9k03nCeLqSgLs6nkfXU-sakI_P4'

Myatt = {
    "lat":"33.9006096",
    "lon":"-5.5471761",
    "rad":"50000"
}

def loadPlaces(file):
    places = []
    for pl in open(file, 'r').readlines():
        places.append(pl.replace("\n", ""))
    return places


def GoogPlac(lat,lng,radius,types,key, pagetoken):

    AUTH_KEY = key
    LOCATION = str(lat) + "," + str(lng)
    RADIUS = radius
    TYPES = types
    if pagetoken == False:
        print "im in first page"
        MyUrl = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=%s&types=%s&sensor=false&key=%s') % (LOCATION, RADIUS, TYPES, AUTH_KEY)
    else:
        print "lets get the next"
        MyUrl = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=%s&types=%s&sensor=false&key=%s&pagetoken=%s') % (LOCATION, RADIUS, TYPES, AUTH_KEY, pagetoken)
        print MyUrl
    response = urllib.urlopen(MyUrl);
    jsonRaw = response.read()
    print len(jsonRaw)
    if len(jsonRaw) > 0:
        jsonData = json.loads(jsonRaw)
    else:
        jsonData = {"status":"EMPTY"}
    return jsonData



MyType = loadPlaces('places')

for place in MyType:
    print place
    data = GoogPlac(Myatt["lat"], Myatt["lon"], Myatt["rad"], place, MyKey, False)

    if "status" in data and data["status"] == "OK":
        open(place+"_"+str(random.randint(0,999999))+ ".json", "w").write(json.dumps(data))

    while "status" in data and data["status"] == "OK" and "next_page_token" in data:

        if len(data["next_page_token"]) > 0:
            print "sleeping for 5s"
            time.sleep(5)
            print "woke up"
            data = GoogPlac(Myatt["lat"], Myatt["lon"], Myatt["rad"], place, MyKey, data["next_page_token"])
        if "status" in data and data["status"] == "OK":
            open(place+"_"+str(random.randint(0,999999))+ ".json", "w").write(json.dumps(data))
        if "status" in data and data["status"] == "INVALID_REQUEST":
            print "invalid"
