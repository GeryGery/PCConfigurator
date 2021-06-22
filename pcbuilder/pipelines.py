# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from scrapy.utils.project import get_project_settings
import mariadb

class PcbuilderPipeline(object):

	def __init__(self):
		self.create_connection()

	def create_connection(self):
		DB_CREDS = get_project_settings().get('DB_CREDS')
		self.conn = mariadb.connect(user=DB_CREDS['user'], password=DB_CREDS['pass'], host=DB_CREDS['host'], database=DB_CREDS['db'])
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		self.values = "', '".join(item.values())
		self.columns = ', '.join(item.keys())
		self.query = "INSERT INTO %s (%s) VALUES ('%s')" % (spider.table, self.columns, self.values)

		try:
			self.cursor.execute(self.query)
			self.conn.commit()

		except Exception as e:
			if 'server has gone away' in str(e):
				self.create_connection()
				self.cursor.execute(self.query)
				self.conn.commit()
			else:
				raise e
		except (mariadb.Error, mariadb.Warning) as e:
			print(e)
			raise e

		return item

	def close_spider(self, spider):
		self.conn.close()
