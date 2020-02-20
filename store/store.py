
import googlemaps
import csv
import math
import json
import logging
import codecs
import pkg_resources

# not safe way to keep an api-key, should be only temporary
gmaps = googlemaps.Client(key='AIzaSyA1UUqu_5mZBvmvu2oEvPAPkq_WgNVa4Ac')

# Earth radius
R = 6371

# main function for getting closest to requested address store details from the data storage
# args [address_string]
# returns [colum_names, distance, store_details]
def search_store(address):
	geocode_result = gmaps.geocode(str(address))
	
	# check if google geolocation is able to find geometry for requested address
	if not geocode_result or 'error' in geocode_result[0] or 'geometry' not in geocode_result[0]:
		message = "Please, use valid address or zipcode"
		if geocode_result and 'error' in geocode_result[0]:
			message = message + ":" + geocode_result[0]['message']
		logging.error(message)
		return

	coordinates = geocode_result[0]['geometry']['location']
	lat = coordinates['lat']
	lng = coordinates['lng']
	[column_names, distance, store] = nearest_adr_search(lat, lng)
	return [column_names, distance, store]


# function for searching through *.csv file with stores and look nearest from requested address
# args [latitude, longitude, units]
# returns [[csv_column_name_list], distance, [store_list]]
def nearest_adr_search(lat, lng):
	# read csv file line by line and calc the distance to requested, save min
	min_store = None
	min_distance = 100000

	resource_package = __name__
	resource_path = '/'.join(('data', 'store-locations.csv'))
	with pkg_resources.resource_stream(resource_package, resource_path) as csv_file:
		utf8_reader = codecs.getreader("utf-8")
		csv_reader = csv.reader(utf8_reader(csv_file), delimiter=',')
		line_count = 0
		column_names = []
		for row in csv_reader:
			if line_count == 0:
				column_names = row
				line_count += 1
			else:
				current_lat, current_lng = float(row[6]), float(row[7])
				current_distance = calc_distance(lat, lng, current_lat, current_lng)
				if current_distance < min_distance:
					min_store = row
					min_distance = current_distance

	return column_names, min_distance, min_store


# function for calculating absolute distanse between two coordinate points
# uses haversine formula, link: https://www.movable-type.co.uk/scripts/latlong.html
# args [latitude1, longitude1, latitude2, longitude2, unit]
# returns absolute distanse in requested units (mi/km)
def calc_distance(lat1, lng1, lat2, lng2):
	lat1_rad = math.radians(lat1)
	lat2_rad = math.radians(lat2)

	delta_fi = math.radians(lat2-lat1)
	delta_lambda = math.radians(lng2-lng1)
	a = math.sin(delta_fi/2) * math.sin(delta_fi/2) + \
		math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	return R * c

