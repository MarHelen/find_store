#!/usr/bin/env python3

import json
import argparse
import logging

from store import search_store


def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("--zip", type=int, help="Find nearest store to this zip code. If there are multiple best-matches, return the first.")
	parser.add_argument("--address", type=str, help="Find nearest store to this address. If there are multiple best-matches, return the first.")
	parser.add_argument("--output", type=str, help="Output in human-readable text, or in JSON (e.g. machine-readable) [default: text]", default='text')
	parser.add_argument("--units", type=str, help="Display units in miles or kilometers [default: mi]", default='mi')
	args = parser.parse_args()

	if args.zip is None and args.address is None:
		logging.error("You need to request at least one location parameter: zip or address.")
		return None

	if args.units not in ["mi", "km"]:
		logging.error("Please, specify correct unit formate. Available formates: 'km' and 'mi'.")
		return None

	if args.output not in ["text", "json"]:
		logging.error("Please, specify correct output formate. Available formates: 'text' and 'json'.")
		return None

	return args


def main():
	args = get_arguments()
	record = search_store(args.address or args.zip, args.google_api_key)
	if not record:
		return

	print_output(record, args.output, args.units)

# function for printing the output in requested formate
# default: text Here's the nearest store details:
# 					store name: San Francisco West, 
# 					store address: SEC Geary Blvd. and Masonic Avenue 2675 Geary Blvd San Francisco CA 94118-3400,
# 					distance from requested address: 1.449589mi
# optional: json {"store_name": "San Francisco West", "store_location": "SEC Geary Blvd. and Masonic Avenue", 
# 					"address": "2675 Geary Blvd", "city": "San Francisco", "state": "CA", "zip_code": "94118-3400", 
#					"latitude": "37.7820964", "longitude": "-122.4464697", "county": "San Francisco County", 
#					"distance": 1.4495892592265038}
def print_output(record, output, units):
	[column_names, distance, store] = record
	# coeficient to convert km to mi
	km_to_miles = 0.621371
	distance = distance if units == "km" else distance * km_to_miles
	if output == 'text':
		print('Here\'s the nearest store details:\n store name: %s, \n store address: %s, \
			\n distance from requested address: %f%s' %(store[0], ' '.join(store[1:6]), distance, units))
	else:
		result = {column_names[i].lower().replace(' ', '_') : store[i] for i in range(len(column_names))}
		result['distance'] = distance
		result['units'] = units
		result_json = json.dumps(result)
		print (result_json)


if __name__== "__main__":
	main()
