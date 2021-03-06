# Find Store

Find Store is a python package for searching the closest store from the data store to either provided address or zipcode.

# Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Find Store.

```bash
pip install git+https://github.com/MarHelen/find_store.git

```
or...
```bash
sudo pip3 install git+https://github.com/MarHelen/find_store.git

```
Otherwise you can also make repository clone and install or run it from the local copy.
```bash
git clone https://github.com/MarHelen/find_store.git
pip install -U googlemaps
python3 find_store/store/main.py --zip=94158 --units=km
```

## Usage

```bash
  find_store --address="<address>"
  find_store --address="<address>" [--units=(mi|km)] [--output=text|json]
  find_store --zip=<zip>
  find_store --zip=<zip> [--units=(mi|km)] [--output=text|json]
```


 Options:
```bash
  --zip=<zip>            Find nearest store to this zip code. If there are multiple best-matches, return the first.
  --address="<address>"  Find nearest store to this address. If there are multiple best-matches, return the first.
  --units=(mi|km)        Display units in miles or kilometers [default: mi]
  --output=(text|json)   Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]
```
 Example 1
```bash
  find_store --zip=94158 --units=km
```
 Output
```bash
  Here's the nearest store details:
 	store name: San Francisco Central, 
 	store address: SEC 4th & Mission St 789 Mission St San Francisco CA 94103-3132, 			
 	distance from requested address: 1.815950km
```

Example 2
```bash
  find_store --address=94158 --output="json"
```

Output
```bash
	{"store_name": "San Francisco Central", "store_location": "SEC 4th & Mission St", "address": "789 Mission St", "city": "San Francisco", "state": "CA", "zip_code": "94103-3132", "latitude": "37.7847358", "longitude": "-122.4036914", "county": "San Francisco County", "distance": 1.1283786342129303, "units": "mi"}
```

# Details

The implementation is pretty much strainforward. Every time when a new address or zipcode is being requsted the algorithm is looking through all the stores in the data storage and call ```calc_distance(...)``` function to retrieve the exact distance beetween two pairs of coordinates. Eventually the main function return closest store details with this minimum distance. 

For the location trasformation Google Maps Geolocation API used, - python3 package. The library is using for converting address string to exact latitude and longitude.

For the distance calculation uses [haversine formula](https://www.movable-type.co.uk/scripts/latlong.html)

# Testing

To cover the main functionality, added unit tests for ```search_store()``` and ```calc_distance()``` with mocking calls to Google API.

To run the test:
```bash
python3 -m unittest store/tests/test_find_store.py
```

