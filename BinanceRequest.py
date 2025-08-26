from GenericRequest import GenericRequest
from BinanceEnums import BinanceEnums
from GlobalEnums import GlobalEnums
from math import ceil


class BinanceSpotDataRequest(GenericRequest):

	def __init__(self):
		super().__init__()
		self.base_url = BinanceEnums.BINANCE_SPOT_BASE_URL.value
		self.exchange = 'binance'
		self.endpoint = 'binance_spot'

	# Start and end time passed in ms and at UTC+0.
	# Necessary requests must be passed as int to be iterable.
	def __calculate_necessary_requests(self, start_time, end_time, interval, limit):
		self.time_in_ms = GlobalEnums.TIME_IN_MS.value[interval]
		self.period = end_time - start_time
		self.candles_in_period = self.period/self.time_in_ms
		self.necessary_requests = int(ceil(self.candles_in_period/limit))
		return self.necessary_requests
	
	def calculate_requests_and_breakpoints(self, start_time, end_time, interval, limit):
		self.necessary_requests = self.__calculate_necessary_requests(start_time, end_time, interval, limit)
		self.break_points = [start_time]
		for i in range(1, self.necessary_requests):
			self.break_points.append(start_time + limit*i*self.time_in_ms)
		self.break_points.append(end_time)
		return self.necessary_requests, self.break_points 



class BinanceHistoricalKlineData(BinanceSpotDataRequest):
	
	def __init__(self, symbol=None, interval=None, start_time=None, end_time=None):
		super().__init__()
		self.request_name = 'kline_data'
		self.request_weight = 2
		self.limit = 1000
		self.url = self.base_url + BinanceEnums.BINANCE_SPOT_KLINE_MODIFIER.value

		self.symbol=symbol
		self.interval = interval
		self.start_time = start_time
		self.end_time = end_time

		if symbol != None and interval != None and start_time != None and end_time != None:
			self.create_pagination_queue()

	def set_metadata(self, symbol, interval, start_time, end_time):
		self.symbol = symbol
		self.interval = interval
		self.start_time = start_time
		self.end_time = end_time

		self.create_pagination_queue()

	def create_pagination_queue(self):
		self.necessary_requests, self.break_points = self.calculate_requests_and_breakpoints(self.start_time, self.end_time, self.interval, self.limit)
		self.pagination_queue = []
		for i in range(self.necessary_requests):
			self.params = {'symbol': self.symbol,
			 'interval': self.interval,
			 'startTime': self.break_points[i],
			 'endTime': self.break_points[i+1],
			 'limit': self.limit}
			self.storage_metadata = {'exchange': self.exchange, 'endpoint': self.endpoint, 'request_type': self.request_name, 'interval': self.interval, 'symbol': self.symbol}
			self.pagination_queue.append({'url': self.url, 'params': self.params, 'weight': self.request_weight, 'storage_metadata': self.storage_metadata})


	
		