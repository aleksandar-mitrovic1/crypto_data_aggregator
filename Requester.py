from requests import get as reqget
from GlobalEnums import GlobalEnums
from RateLimiter import RateLimiter
from time import sleep
import atexit
import json
import time

class Requester():

	def __init__(self, session):
		self.session = session
		self.rate_limiters = {}
		for endpoint in GlobalEnums.ENDPOINTS.value:
			self.rate_limiters.update({endpoint: RateLimiter(endpoint)})
		atexit.register(self.__emergency_save)
		
	
	def execute(self, request):
		self.pagination_queue = request.get_pagination_queue()
		self.endpoint = self.pagination_queue[0]['storage_metadata']['endpoint']
		self.rate_limiters[self.endpoint].reset_timer()

		self.response_queue = []

		for i in range(len(self.pagination_queue)):
			self.url = self.pagination_queue[i]['url']
			self.params = self.pagination_queue[i]['params']
			self.weight = self.pagination_queue[i]['weight']
			self.storage_metadata = self.pagination_queue[i]['storage_metadata']

			self.wait_time_until_execution = self.rate_limiters[self.endpoint].calculate_wait_time(self.weight)
			print(f'Wait time is given as {self.wait_time_until_execution} for {self.endpoint}')
			sleep(self.wait_time_until_execution)
			self.response = reqget(self.url, params=self.params)

			#TODO deal with requests not going through properly because of bad syntax and keep track
			# of which requests did not get fulfilled.

			if self.response.status_code == 200:
				self.response_queue.append(self.response.json())

			self.rate_limiters[self.endpoint].update_accumulated_weight(self.weight)

			match self.storage_metadata['endpoint']:
				case 'binance_spot':
					self.process_binance_spot_response(self.response)
 
		return self.response_queue, self.storage_metadata


	def process_binance_spot_response(self, response):
		self.content = response.json()
		self.headers = response.headers
		if response.status_code != 200:
			match response.status_code:
				case 403:
					print(f'HTTP Error code {response.status_code}')
					print(self.content['msg'])
					# print('403: WAF limit has been violated')
					print(f'Stopping all requests to binance_spot')
					self.rate_limiters[self.endpoint].permanent_stop()
				case 429:
					# print('429: Request rate limit broken')
					print(f'HTTP Error code {response.status_code}')
					print(self.content['msg'])
					self.rate_limiters[self.endpoint].retry_after(int(self.headers['Retry-After']))
				case 418:
					# print('418: Auto ban from too many 429 requests')
					print(f'HTTP Error code {response.status_code}')
					print(self.content['msg'])
					self.rate_limiters[self.endpoint].retry_after(int(self.headers['Retry-After']))
				case _:
					print(f'HTTP Error code {response.status_code}')
					print(f'Binance internal error code {self.content['code']}')
					print(self.content['msg'])
		else:
			self.rate_limiters[self.endpoint].compare_to_server(int(self.headers['x-mbx-used-weight-1m']))

	def __emergency_save(self):
		with open(f'temp/{self.endpoint}_{self.storage_metadata}_raw_request_dump_{str(time.time())}.json', 'w') as f:
			json.dump(self.response_queue, f, indent=4)


