# CS288 Homework 8
# Read the skeleton code carefully and try to follow the structure
# You may modify the code but try to stay within the framework.

import sys
import os
#import commands
import re
import sys

import pymysql

from xml.dom.minidom import parse, parseString

# for converting dict to xml 
#from cStringIO import StringIO
from xml.parsers import expat

def get_elms_for_atr_val(tag,atr,val):
   lst=[]
   elms = dom.getElementsByTagName(tag)
   # print(len(elms))
   for element in elms:
   	lst.append(element)
   return lst

# get all text recursively to the bottom
def get_text(e):
   obj={}

   obj["symbol"] = e.childNodes[0].childNodes[1].firstChild.nodeValue
   obj["name"] = e.childNodes[1].firstChild.nodeValue
   obj["price"] = e.childNodes[2].firstChild.firstChild.nodeValue
   obj["change"] = replace_non_alpha_numeric(e.childNodes[3].firstChild.firstChild.nodeValue)
   obj["p_change"] = replace_non_alpha_numeric(e.childNodes[4].firstChild.firstChild.nodeValue)
   obj["volume"] = replace_non_alpha_numeric(e.childNodes[5].firstChild.firstChild.nodeValue[:-1])
   obj["market_cap"] = replace_non_alpha_numeric(e.childNodes[7].firstChild.firstChild.nodeValue[:-1])

   return obj

# replace whitespace chars
def replace_white_space(str):
   p = re.compile(r'\s+')
   new = p.sub(' ',str)   # a lot of \n\t\t\t\t\t\t
   return new.strip()

# replace but these chars including ':'
def replace_non_alpha_numeric(s):
   p = re.compile(r'[^a-zA-Z0-9.:-]+')
   #   p = re.compile(r'\W+') # replace whitespace chars
   new = p.sub(' ',s)
   return new.strip()

def extract_values(dm):
   lst = []
   thl = []
   l = get_elms_for_atr_val('tr','class','most_actives')
   hdr = l[0]
   first = True
   for e in l:
   	if not first:
   		text = get_text(e)
   		lst.append(text)
   	else:
   		first = False
   #print(lst)
   return lst

# mysql> describe most_active;
def insert_to_db(l,tbl):
   db = pymysql.connect("localhost", "root", "CS288hw8!", "test_stonks")
   cursor = db.cursor()
   s = "CREATE TABLE IF NOT EXISTS " + tbl + " (symbol VARCHAR(10), name VARCHAR(80), price VARCHAR(30), chng VARCHAR(30), p_change VARCHAR(30), volume VARCHAR(30), market_cap VARCHAR(30))"
   cursor.execute(s)
   
   values = []
   for item in l:
   	values.append((item["symbol"], item["name"], item["price"], item["change"], item["p_change"], item["volume"], item["market_cap"]))
   insertS = "INSERT INTO " + tbl + " (symbol, name, price, chng, p_change, volume, market_cap) VALUES (%s, %s, %s, %s, %s, %s, %s)"
   
   cursor.executemany(insertS, values)
   
   db.commit()	   
   #print("OH YEAH")
   return cursor
   
def select_from_db(cursor, tbl):
	selectS = "SELECT * FROM " + tbl
	cursor.execute(selectS)
	info = cursor.fetchall()
	return info
# show databases;
# show tables;
def main():
   xhtml_fn = sys.argv[1]
   fn = xhtml_fn.replace('.xhtml','')
   # xhtml_fn = html_to_xml(html_fn)

   global dom
   dom = parse(xhtml_fn)

   lst = extract_values(dom)

   # make sure your mysql server is up and running
   cursor = insert_to_db(lst,fn) # fn = table name for mysql

   l = select_from_db(cursor,fn) # display the table on the screen

   # make sure the Apache web server is up and running
   # write a PHP script to display the table(s) on your browser
   # print(l)
   exit(fn)
   return 0
# end of main()

if __name__ == "__main__":
    main()
    # os.system("php /home/nicholas/cs288/hw8/table.php")
# end of hw7.py
