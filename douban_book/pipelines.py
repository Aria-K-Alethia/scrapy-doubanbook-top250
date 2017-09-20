# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# Author:Alethia
import pymysql
from scrapy.exceptions import DropItem


''' This file implement a standard pipeline class '''

class MysqlPipeline(object):
	
	'''	save the data in your mysql database '''

	def __init__(self):
		#init the pipeline
		user_name = "" #your username
		pw = "" # your pw
		self.conn = pymysql.connect(host = '127.0.0.1',user = user_name,passwd = pw,\
									db = 'mysql',charset = 'utf8')
		self.cur = self.conn.cursor()

		#use a database
		self.database_name = "doubanbook_top250"
		try:
			self.cur.execute("create database %s" % self.database_name)
			self.conn.commit()
		except:
			pass
		finally:
			self.cur.execute("use %s" % self.database_name)

		#create a table,NOTE that if the table exists,we will delete it
		self.table_name = "books"
		command = "create table %s(id int primary key auto_increment,\
					name varchar(100) not null,\
					author varchar(50) not null,\
					press varchar(100) null,\
					date varchar(20) null,\
					page varchar(10) null,\
					price varchar(10) null,\
					score varchar(10) null,\
					ISBN varchar(30) null,\
					author_profile varchar(1500) null,\
					content_description varchar(1500) null,\
					link varchar(100) null\
					)default charset = utf8;" % self.table_name
		try:
			self.cur.execute("desc %s" % self.table_name)
			self.cur.execute("drop table %s" % self.table_name)
			self.conn.commit()
		except:
			pass
		finally:
			self.cur.execute(command)
			self.conn.commit()

	def process_item(self, item, spider):
		#save a item in database
		for i in item:
			item[i] = str(item[i])
		try:
			self.cur.execute("insert into %s(name,author,press,date,page,price,score,ISBN,\
						author_profile,content_description,link) values('%s','%s','%s','%s',\
						'%s','%s','%s','%s','%s','%s','%s')" % \
						(self.table_name,item["name"],item["author"],item["press"],item["date"],\
						item["page"],item["price"],item["score"],item["ISBN"],\
						item["author_profile"],item["content_description"],item["link"]))
			self.conn.commit()
			return item
		except e:
			raise DropItem("e:%s" % item)

	def close_spider(self,spider):
		self.cur.close()
		self.conn.close()