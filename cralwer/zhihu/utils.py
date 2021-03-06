#coding: utf-8
import re
import logging
from datetime import datetime, timedelta

def get_date(date_str):
	"""
	对知乎答案的打不或编辑时间的解析
	params: date_str（时间字符串）
	return: 正则匹配后的时间
	"""
	published_date = None
	m = re.search(u'(\s+([\u4e00-\u9fa5]*)\s*?([0-9:]{5}))|([0-9-]{10})', date_str)
	if m:
		m = m.groups()	
		# logging.error('=======')	
		# logging.error(m)
		if m[0]:
			if m[1] == unicode(u'昨天'):
				hours, minutes = map(lambda x: int(x), m[2].split(':'))
				published_date = datetime.now().replace(hour=0,
														minute=0,
														second=0,
														microsecond=0) \
								+ timedelta(days=-1) \
								+ timedelta(hours=hours) \
								+ timedelta(minutes=minutes)
				published_date = published_date.strftime('%Y-%m-%d %H:%M:%S')        
			elif m[1] == unicode(u'今天'):
				hours, minutes = map(lambda x: int(x), m[2].split(':'))
				published_date = datetime.now().replace(hour=0,
														minute=0,
														second=0,
														microsecond=0) \
								+ timedelta(hours=hours) \
								+ timedelta(minutes=minutes)
				published_date = published_date.strftime('%Y-%m-%d %H:%M:%S')
			else:
				hours, minutes = map(lambda x: int(x), m[2].split(':'))
				published_date = datetime.now().replace(hour=0,
														minute=0,
														second=0,
														microsecond=0) \
								+ timedelta(hours=hours) \
								+ timedelta(minutes=minutes)
				published_date = published_date.strftime('%Y-%m-%d %H:%M:%S')

		elif m[3]:
			published_date = m[3]
	return published_date
