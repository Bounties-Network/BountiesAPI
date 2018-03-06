import datetime
import time
import logging

logger = logging.getLogger('django')
max_datetime = datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)
max_time_stamp = time.mktime(max_datetime.timetuple())

def getDateTimeFromTimestamp(timestamp):
	try:
		integer_stamp = int(timestamp)
	except ValueError:
		logger.error('Incorrect timestamp')
		return max_datetime

	if integer_stamp > max_time_stamp:
		logger.error('Timestamp greater than max')
		return max_datetime
	return datetime.datetime.fromtimestamp(integer_stamp)