import sys,os,re,datetime,cookielib,urllib,urllib2

def replace_vars(str, map):
    out_str = str
    for m in map:
        out_str = out_str.replace(m, map[m])
    return out_str

def get_date(dt_desc, is_iso=False, is_date=False):
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
    
    if not is_date:
        out_dt = out_dt.strftime("%Y%m%d") if not is_iso else out_dt.strftime("%Y-%m-%d")

    return out_dt
    
#-- define color print class (it doesn't work on windows)
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
def print_log(msg):
    # type=1: normal log
    # type=2: warning log
    # type=3: error log
    type_color = {
        1: "OKGREEN",
        2: "WARNING",
        3: "FAIL",
    }
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print "[" + now + "]", msg


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

    
def return_new_name_for_existing_file(file):
    # If file already exists, generate a new name
    while os.path.exists(file):
        r_obj = re.search(r'(?P<file_name>.+)\.(?P<ext>[^\.]+)$', file)
        file = r_obj.group("file_name") + '_1.' + r_obj.group("ext")
    return file
    
if __name__ == "__main__":
    print get_date("theDayAfterTomorrow", is_iso=True, is_date=True)