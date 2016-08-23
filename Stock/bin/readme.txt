# Set python env
-> install_env.py

# Install psyconpg2
-> update /etc/apt/source.list
-> apt-get update
-> apt-get install python-psycopg2

# Install PyYAML
-> http://pyyaml.org/wiki/PyYAML
-> wget http://pyyaml.org/download/pyyaml/PyYAML-3.11.tar.gz
-> python setup.py install

# Install xlrd
-> https://pypi.python.org/pypi/xlrd
-> wget https://pypi.python.org/packages/source/x/xlrd/xlrd-0.9.4.tar.gz
-> python setup.py install

# Install taskflow
-> pip install taskflow

# Install Flask
-> pip install flask
-> pip install flask-login
-> pip install flask-openid
-> pip install flask-mail # for windows, install via -> pip install --no-deps lamson chardet flask-mail
-> pip install flask-sqlalchemy
-> pip install sqlalchemy-migrate
-> pip install flask-whooshalchemy
-> pip install flask-wtf
-> pip install flask-babel
-> pip install flup