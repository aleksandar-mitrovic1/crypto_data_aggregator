import os
from pathlib import Path
from GlobalEnums import GlobalEnums
import pandas as pd
import atexit
import json
import time

class DataStorage():

	def __init__(self):
		# self.current_directory = os.path.dirname(os.path.abspath(__file__))
		self.current_directory = Path(__file__).resolve().parent
		os.chdir(self.current_directory)

		# Dump data to json in case of failure saving
		atexit.register(self.__emergency_save)
		

	def __folder_check(self, path):
		self.folder = Path(path)
		self.folder.mkdir(parents=True, exist_ok=True)

	def __file_check(self, path):
		self.file_path = Path(path)
		if self.file_path.is_file():
			return True
		else:
			return False


	def save(self, response_queue, storage_metadata):

		self.response_queue = response_queue

		for response in self.response_queue:
			self.exchange = storage_metadata['exchange']
			self.endpoint = storage_metadata['endpoint']
			self.request_type = storage_metadata['request_type']
			self.interval = storage_metadata['interval']
			self.symbol = storage_metadata['symbol']
			self.response = response
		
			self.headers_key = self.endpoint + '_' + self.request_type
			self.headers = GlobalEnums.HEADERS.value[self.headers_key]

			self.response_df = pd.DataFrame(self.response, columns=self.headers)

			try:
				self.response_df_full = pd.concat([self.response_df_full, self.response_df])
			except AttributeError:
				self.response_df_full = self.response_df

				
		self.folder_location = 'data/' + self.exchange + '/' + self.endpoint + '/' + self.request_type + '/' + self.interval + '/'
		self.__folder_check(self.folder_location)
		self.full_path = self.folder_location + str(self.symbol) + '.parquet'

		# Check if file exists already and merge if applicable.
		if self.__file_check(self.full_path):
			self.stored_file = pd.read_parquet(self.full_path)
			self.stored_file = pd.concat([self.stored_file, self.response_df_full])
			self.stored_file.to_parquet(self.full_path)
		else:
			self.response_df_full.to_parquet(self.full_path)



	def __emergency_save(self):
		with open(f'temp/{self.endpoint}_{self.request_type}_{self.interval}_{self.symbol}_storage_dump_{str(time.time())}.json', 'w') as f:
			json.dump(self.response_queue, f, indent=4)