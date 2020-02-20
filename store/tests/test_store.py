import unittest
from unittest.mock import MagicMock

import json
import store

class TestFindStore(unittest.TestCase):

	def test_search_store_by_zip(self):

		store.gmaps.geocode = MagicMock(return_value=[{'address_components': [{'long_name': '94158', \
			'short_name': '94158', 'types': ['postal_code']}, {'long_name': 'San Francisco', \
			'short_name': 'SF', 'types': ['locality', 'political']}, {'long_name': 'San Francisco County', \
			'short_name': 'San Francisco County', 'types': ['administrative_area_level_2', 'political']}, \
			{'long_name': 'California', 'short_name': 'CA', 'types': ['administrative_area_level_1', 'political']}, \
			{'long_name': 'United States', 'short_name': 'US', 'types': ['country', 'political']}], \
			'formatted_address': 'San Francisco, CA 94158, USA', 'geometry': {'bounds': {'northeast': \
			{'lat': 37.7835291, 'lng': -122.3796809}, 'southwest': {'lat': 37.7640839, 'lng': -122.401657}}, \
			'location': {'lat': 37.7748363, 'lng': -122.3872576}, 'location_type': 'APPROXIMATE', 'viewport': \
			{'northeast': {'lat': 37.7835291, 'lng': -122.3796809}, 'southwest': {'lat': 37.7640839, 'lng': -122.401657}}}, \
			'place_id': 'ChIJTayi3tN_j4ARIwuQJy7-etE', 'types': ['postal_code']}])

		[columns, distance, found_store] = store.search_store("94158")

		self.assertEqual(distance, 1.8159499465101046)
		self.assertEqual(found_store[0], "San Francisco Central")


	def  test_search_store_by_address(self):
		expected_result = "Here's the nearest store details: store name: Mountain View, \
			store address: NEC Showers Dr & Latham St 555 Showers Dr Mountain View CA 94040-1432, \
			distance from requested address: 2.937272km"

		store.gmaps.geocode = MagicMock(return_value=[{'address_components': [{'long_name': '1600', 'short_name': '1600', \
			'types': ['street_number']}, {'long_name': 'Amphitheatre Parkway', 'short_name': 'Amphitheatre Pkwy', \
			'types': ['route']}, {'long_name': 'Mountain View', 'short_name': 'Mountain View', \
			'types': ['locality', 'political']}, {'long_name': 'Santa Clara County', 'short_name': 'Santa Clara County', \
			'types': ['administrative_area_level_2', 'political']}, {'long_name': 'California', 'short_name': 'CA', \
			'types': ['administrative_area_level_1', 'political']}, {'long_name': 'United States', 'short_name': 'US', \
			'types': ['country', 'political']}, {'long_name': '94043', 'short_name': '94043', 'types': ['postal_code']}], \
			'formatted_address': '1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA', 'geometry': \
			{'location': {'lat': 37.4215804, 'lng': -122.0851978}, 'location_type': 'ROOFTOP', 'viewport': \
			{'northeast': {'lat': 37.4229293802915, 'lng': -122.0838488197085}, 'southwest': {'lat': 37.4202314197085, \
			'lng': -122.0865467802915}}}, 'place_id': 'ChIJtYuu0V25j4ARwu5e4wwRYgE', 'plus_code': \
			{'compound_code': 'CWC8+W4 Mountain View, California, United States', 'global_code': '849VCWC8+W4'}, \
			'types': ['street_address']}])

		[columns, distance, found_store] = store.search_store("1600 Amphitheatre Parkway, Mountain View, CA")

		self.assertEqual(distance, 2.9372719078313105)
		self.assertEqual(found_store[0], 'Mountain View')


	def test_search_store_failure(self):
		store.gmaps.geocode = MagicMock(return_value=[])
		expected_result = "Please, use valid address or zipcode"

		self.assertTrue(actual_result is None)


	def test_calc_distance(self):
		lat1 = 37.7748363
		lng1 = -122.3872576
		lat2 = 37.7847358
		lng2 = -122.4036914
		distance = store.calc_distance(lat1, lng1, lat2, lng2)

		self.assertEqual(distance, 2.9372719078313105)


if __name__ == '__main__':
	unittest.main()