class GenericRequest():

	def __init__(self):
		self.request_weight = None
		# self.endpoint_rate_limit = None
		self.pagination_queue = None

		self.url = None
		self.params = None



	def get_pagination_queue(self):
		return self.pagination_queue
	
