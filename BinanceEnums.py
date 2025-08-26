from enum import Enum

class BinanceEnums(Enum):
	# Endpoints
	BINANCE_SPOT_BASE_URL = 'https://data-api.binance.vision'
	BINANCE_SPOT_KLINE_MODIFIER = '/api/v3/klines'

	# Headers
	KLINE_HEADER = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore']
	KLINE_NUMERIC_HEADER_FLAG = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume']

	# Limits and intervals in ms

	