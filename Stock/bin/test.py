#!/usr/bin/python

import psycopg2

print "hello world"


conn = psycopg2.connect(database="StockDb", user="hong", password="hong", host="192.168.122.131", port="5432")

print "Opened database successfully"

