1. Install mysql
----- Prerequisite 1 (install latest gcc: http://blog.sina.com.cn/s/blog_493667730100zt6n.html)
1.1. Install gmp
-> mkdir /usr/local/gmp-5.0.1
-> configure --prefix=/usr/local/gmp-5.0.1

1.2. Install mpfr
-> mkdir /usr/local/mpfr-3.1.3
-> configure --prefix=/usr/local/mpfr-3.1.3 --with-gmp=/usr/local/gmp-5.0.1

1.3. Install mpc
-> mkdir /usr/local/mpc-1.0.2
-> configure --prefix=/usr/local/mpc-1.0.2 --with-gmp=/usr/local/gmp-5.0.1 --with-mpfr=/usr/local/mpfr-3.1.3

1.4. Install gcc
-> export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/mpc-1.0.2/lib:/usr/local/gmp-5.0.1/lib:/usr/local/mpfr-3.1.3/lib
-> configure --prefix=/usr/local/gcc-5.3.0 --enable-threads=posix --disable-checking --disable-multilib --enable-languages=c,c++ --with-gmp=/usr/local/gmp-5.0.1 --with-mpfr=/usr/local/mpfr-3.1.3 --with-mpc=/usr/local/mpc-1.0.2


export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/mpc-1.0.2/lib:/usr/local/gmp-5.0d1/lib:/usr/local/mpfr-3.1.3/lib

cmake . \
-DCMAKE_INSTALL_PREFIX=/app/database/mysql/installation/mysql-5.7.10 \
-DMYSQL_UNIX_ADDR=/app/database/mysql.sock \
-DDEFAULT_CHARSET=gbk \
-DDEFAULT_COLLATION=gbk_general_ci \
-DWITH_MYISAM_STORAGE_ENGINE=1 \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_ARCHIVE_STORAGE_ENGINE=1 \
-DWITH_BLACKHOLE_STORAGE_ENGINE=1 \
-DWITH_MEMORY_STORAGE_ENGINE=1 \
-DWITH_READLINE=1 \
-DENABLED_LOCAL_INFILE=1 \
-DMYSQL_DATADIR=/app/database/mysql/data \
-DMYSQL_USER=mysql \
-DMYSQL_TCP_PORT=3306 \
-DDOWNLOAD_BOOST=1 \
-DWITH_BOOST=/app/database/mysql
