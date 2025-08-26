from enum import Enum

class GlobalEnums(Enum):
	TIME_IN_MS = {'1m': 60000,
				   '3m': 180000,
				   '5m': 300000,
				   '15m': 900000,
				   '30m': 1800000,
				   '1h': 3600000,
				   '2h': 7200000,
				   '4h': 14400000,
				   '6h': 21600000,
				   '8h': 28800000,
				   '12h': 43200000,
				   '1d': 86400000,
				   '3d': 259200000,
				   '1w': 604800000,
				   '1M': 2629746000}
	

	HEADERS = {'binance_spot_kline_data': ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']}

	ENDPOINTS = ['binance_spot']
	# Endpoint limits: request weight and interval in ms
	ENDPOINT_LIMITS = {'binance_spot': [6000, 60000]}

	REQUEST_WEIGHT_MARGIN_OF_SAFETY = 0.9