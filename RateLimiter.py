from BinanceEnums import BinanceEnums
from GlobalEnums import GlobalEnums
import time

class RateLimiter():

	def __init__(self, endpoint):
		self.endpoint = endpoint
		self.endpoint_rate_limit_info = GlobalEnums.ENDPOINT_LIMITS.value[self.endpoint]
		self.margin_of_safety_for_request_weight = GlobalEnums.REQUEST_WEIGHT_MARGIN_OF_SAFETY.value
		self.endpoint_weight_limit = self.endpoint_rate_limit_info[0] * self.margin_of_safety_for_request_weight
		# Interval stored in ms but more convenient to work with seconds here
		self.endpoint_weight_limit_interval = self.endpoint_rate_limit_info[1] / 1000

		self.banned_until = None
		self.permanent_stop_flag = False

		print(f"I'm the {self.endpoint} rate limiter and in {self.endpoint_weight_limit_interval} seconds I can accept {self.endpoint_weight_limit}")

	def update_accumulated_weight(self, weight):
		self.accumulated_weight += weight

	def reset_timer(self):
		self.start_time = time.time()
		self.accumulated_weight = 0

	def calculate_wait_time(self, weight):

		if self.permanent_stop_flag:
			return Exception('PermanentStop')
		
		if self.banned_until:
			if time.time() > self.banned_until:
				self.banned_until = None
			else:	
				print(f'Server wants us to wait for another {self.banned_until - time.time()} seconds')
				return self.banned_until - time.time()
			
		if time.time() < self.start_time + self.endpoint_weight_limit_interval:
			if self.accumulated_weight + weight > self.endpoint_weight_limit:
				print(f'Waiting for {self.start_time + self.endpoint_weight_limit_interval - time.time()} seconds')
				return self.start_time + self.endpoint_weight_limit_interval - time.time()
			else:
				return 0
		else:
			self.reset_timer()
			return 0


	def compare_to_server(self, server_accumulated_weight):
		if server_accumulated_weight != self.accumulated_weight:
			print(f'Mismatch between {self.endpoint} rate limiter and server used weight')
			print(f'Rate limiter says {self.accumulated_weight} and server says {server_accumulated_weight}')
			print('Switching to server used weight')
			self.accumulated_weight = server_accumulated_weight

	def retry_after(self, wait_time):
		self.banned_until = time.time() + wait_time

	
	def permanent_stop(self):
		self.permanent_stop_flag = True