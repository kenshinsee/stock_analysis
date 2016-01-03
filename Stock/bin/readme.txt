1. Install PyQt or PySide (the bit should be consistent with the bit for operation system and python)
  - Tried PyQt firstly, but there was some issue when running commands, so replace it with PySide
  - pip install pyside -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

2. Install Ghost.py
  - Indicate a source in pip command: %PYTHON_HOME%/Scripts/pip install ghost.py -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
  - Use global mode, refer to http://segmentfault.com/q/1010000000496093, official doc: https://pip.pypa.io/en/latest/user_guide.html#configuration
  - Document of ghost.py: http://ghost-py.readthedocs.org/en/latest/
  
------------- I haven't found a way to click the "Go" button using Ghost.py, trying Scrapy

3. Install Scrapy [http://cuiqingcai.com/912.html]
  - Follow http://cuiqingcai.com/912.html to install the required pluggings and additionally 
    - pip install wheel -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
	- pip install setuptools -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
	- Download libxml2 from http://www.lfd.uci.edu/~gohlke/pythonlibs/
	- wheel install C:\Users\Hong\Desktop\libxml2_python-2.9.3-cp27-none-win_amd64.whl
	- easy_install -i http://pypi.douban.com/simple lxml ################ next time we could just run easy_install?
  - pip install scrapy -i http://pypi.douban.com/simple --trusted-host pypi.douban.com