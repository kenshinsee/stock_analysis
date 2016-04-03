import sys,os,re,datetime,cookielib,urllib,urllib2,yaml
from tooling.psql import get_conn, get_cur

def replace_vars(str, map):
    out_str = str
    for m in map:
        out_str = out_str.replace(m, map[m])
    return out_str

def get_date(dt_desc, to_iso=False, to_date=False):
    # dt_desc could be 
    # # today|yesterday|theDayBeforeYesterday|tomorrow|theDayAfterTomorrow
    # # T is today
    # # T-n|...|T|...|T+n
    today = datetime.date.today()
    out_dt = ""
    dates = {
        "today": today,
        "yesterday": today + datetime.timedelta(-1),
        "theDayBeforeYesterday": today + datetime.timedelta(-2),
        "tomorrow": today + datetime.timedelta(+1),
        "theDayAfterTomorrow": today + datetime.timedelta(+2),
    }
    if re.match("^T[-+]?\d*$", dt_desc):
        delta = int(dt_desc.replace("T","")) if len(dt_desc.replace("T",""))>0 else 0
        out_dt = today + datetime.timedelta(delta)
    elif dt_desc in dates:
        out_dt = dates[dt_desc]
    else:
        raise RuntimeError("Unknow date description. [" + dt_desc + "]") 
    
    if not to_date:
        out_dt = out_dt.strftime("%Y%m%d") if not to_iso else out_dt.strftime("%Y-%m-%d")

    return out_dt
    
#-- define color print class
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
#-- print log  func
def print_log(msg, tee_to_handler=None):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if not tee_to_handler is None:
		tee_to_handler.write(msg + '\n')
	print bcolors.OKGREEN + "[" + now + "] " + msg + bcolors.ENDC

def warn_log(msg, tee_to_handler=None):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if not tee_to_handler is None:
		tee_to_handler.write(msg + '\n')
	print bcolors.WARNING + "[" + now + "] " + msg + bcolors.ENDC

def error_log(msg, tee_to_handler=None):
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if not tee_to_handler is None:
		tee_to_handler.write(msg + '\n')
	print bcolors.FAIL + "[" + now + "] " + msg + bcolors.ENDC

	
def url_opener(head = {
    'Connection': 'keep-alive',    
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
}):
    cj=cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
    
def read_url(url,timeout=100):
    opener = url_opener()
    return opener.open(url, timeout = timeout).read().strip()

def get_file_from_url(url):
    try:
        opener=url_opener()
        urllib2.install_opener(opener)
        
        req=urllib2.Request(url)
        operate=opener.open(req)
        data=operate.read()
        return data
    except BaseException, e:
        print e
        return None

def save_file_from_url(file_name, url):
    if url == None:
        return
    file=open(file_name, "wb")
    file.write(get_file_from_url(url))
    file.flush()
    file.close()
 
    
def return_new_name_for_existing_file(file):
    # If file already exists, generate a new name
    while os.path.exists(file):
        r_obj = re.search(r'(?P<file_name>.+)\.(?P<ext>[^\.]+)$', file)
        file = r_obj.group("file_name") + '_1.' + r_obj.group("ext")
    return file

def get_yaml(yml_file):
	f = open(yml_file)
	y = yaml.load(f)
	f.close()
	return y

def recent_working_day(in_date='today', is_skip_holiday=False, conn=None): # date=yyyymmdd
	# if is_skip_holiday=False, return the most recent non-weekend day
	# if is_skip_holiday=True, return the most recent non-weekend day AND holiday will be skipped as well
	holidays = []
	if re.match("^\d{8}$", in_date):
		date_date = datetime.datetime.strptime(in_date, '%Y%m%d')
	else:
		date_date = get_date(in_date, to_date=True)
		
	if is_skip_holiday:
		if conn is None: 
			raise RuntimeError('connection is None which must be available when skip_holiday mode is on.')
		else:
			cur = get_cur(conn)
			cur.execute('select date from dw.holiday') # yyyymmdd
			rows = list(cur)
			for row in rows:
				holidays.append(row['date'])
			cur.close()

	while date_date.isoweekday() >= 6 or date_date.strftime('%Y%m%d') in holidays:
		date_date = date_date + datetime.timedelta(-1)
	
	return date_date.strftime('%Y%m%d')


if __name__ == "__main__":
	conn = get_conn("StockDb", "hong", "hong", "192.168.122.131", "5432")
	print recent_working_day(is_skip_holiday=True, conn=conn)
	
	