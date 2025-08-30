# Cryptocurrency Data Aggregator

## Description

This project is a data aggregator for historical crypto spot and derivative data from multiple exchanges. It has been written to minimise overhead on adding new request types and all logic has been writen to be as generic and universal as possible.
<br><br>
It is still a work in progress at this point but is being actively worked on. Currently only binance spot API calls are implemented but there is more to come.

## Features

* Standardisation of data and storage in Parquet files.
* Custom API request handling and universal rate limiting implementation.
* Crash protection that saves working memory.

### TODO List

* Add other exchanges.
* Add other request types.
* Recovery system for crash dumps.
* Automatic HTTP error handling.
* Data validation and cleaning (spike filters, etc.)
