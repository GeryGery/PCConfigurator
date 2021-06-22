import scrapy
import re

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapy import Selector
from selenium import webdriver
import selenium.common.exceptions

import time


#-----------------------------CPU---------------------------------------------

class PcbuilderCPUSpider(scrapy.Spider):
	name = 'pcbuilderCPU'
	allowed_domains = ['cpubenchmark.net']
	start_urls = ['https://www.cpubenchmark.net/CPU_mega_page.html']

	def __init__(self):
		self.table = 'cpu'
		self.driver = self.create_driver()

	def create_driver(self):
		options = webdriver.ChromeOptions()
		options.add_argument("headless")
		desired_capabilities = options.to_capabilities()
		driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
		return driver

	def click_cookies(self):
		try:
			cookies_button = self.driver.find_element_by_xpath('//button[text()="AGREE"]')
		except selenium.common.exceptions.NoSuchElementException:
			print('Cookies already clicked')
		except:
			raise
		else:
			cookies_button.click()
			print('Cookies clicked')

	def parse(self, response):
		self.driver.get(self.start_urls[0])
		self.click_cookies()
		time.sleep(3)
		self.driver.find_element_by_xpath('//select[@id="search_category"]/option[text()="Desktop"]').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[@id="cputable_length"]//select/option[text()="All"]').click()
		time.sleep(2)
		print('---------------------------------------------')
		selenium_response = self.driver.page_source
		new_selector = Selector(text=selenium_response)
		for cpu in new_selector.css('table#cputable tbody tr'):
			if cpu.css('td:nth-child(7)::text').extract_first() != 'Unknown':
				cpulinkfrag = cpu.css('a::attr(href)').extract_first()
				cpulink = 'https://www.cpubenchmark.net/cpu.php?' + cpulinkfrag.split('?')[1]
				yield scrapy.Request(cpulink, callback=self.parse_cpu)
		print('---------------------------------------------')
		self.driver.close()

	def parse_cpu(self, response):
		doc = {}
		specifications = response.css('div.desc-body')
		right = response.css('div.right-desc')
		doc['Name'] = response.css('span.cpuname::text').extract_first()
		doc['Socket'] = re.sub('[ ]', "", str(response.xpath('//div[@class="desc-body"]//div[@class="left-desc-cpu"]//strong[text()="Socket:"]/../text()').extract_first()))
		doc['CoreClock'] = re.sub('[ GHzM]', "", str(response.xpath('//div[@class="desc-body"]//div[@class="left-desc-cpu"]//strong[text()="Clockspeed:"]/../text()').extract_first()))
		if response.xpath('//div[@class="desc-body"]//div[@class="left-desc-cpu"]//strong[text()="Turbo Speed:"]/../text()').extract_first() is not None:
			doc['BoostClock'] = re.sub('[ GHzM]', "", str(response.xpath('//div[@class="desc-body"]//div[@class="left-desc-cpu"]//strong[text()="Turbo Speed:"]/../text()').extract_first()))
		cores = response.xpath('//div[@class="desc-body"]//div[@class="left-desc-cpu"]//strong[text()="Cores:"]/../text()')
		if len(cores) == 2:
			doc['NCore'] = re.sub('[ :]', "", str(cores[0].extract()))
			doc['NThreads'] = re.sub('[ :]', "", str(cores[1].extract()))
		else:
			doc['NCore'] =	re.sub('[ ]', "", str(cores.extract_first().split()[2]))
			doc['NThreads'] = re.sub('[ ]', "", str(cores.extract_first().split()[0]))
		doc['TDP'] = re.sub('[ W]', "", str(response.xpath('//div[@class="desc-body"]//div[@class="left-desc-cpu"]//strong[text()="Typical TDP:"]/../text()').extract_first()))
		doc['Rating'] = re.sub('[ ]', "", str(right.css('span::text').extract()[1]))
		doc['has_integrated_graphics'] = str(response.xpath('//div[@class="desc-body"]//div[@class="left-desc-cpu"]//strong[text()="Description:"]/../text()').extract_first())
		doc['url'] = response.request.url
		yield doc
		
#-----------------------------GPU---------------------------------------------

class PcbuilderGPUSpider(scrapy.Spider):
	name = 'pcbuilderGPU'
	allowed_domains = ['videocardbenchmark.net']
	start_urls = ['https://www.videocardbenchmark.net/GPU_mega_page.html']

	def __init__(self):
		self.table = 'gpu'
		self.driver = self.create_driver()

	def create_driver(self):
		options = webdriver.ChromeOptions()
		options.add_argument("headless")
		desired_capabilities = options.to_capabilities()
		driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
		return driver

	def click_cookies(self):
		try:
			cookies_button = self.driver.find_element_by_xpath('//button[text()="AGREE"]')
		except selenium.common.exceptions.NoSuchElementException:
			print('Cookies already clicked')
		except:
			raise
		else:
			cookies_button.click()
			print('Cookies clicked')

	def parse(self, response):
		self.driver.get(self.start_urls[0])
		self.click_cookies()
		time.sleep(3)
		self.driver.find_element_by_xpath('//select[@id="search_category"]/option[text()="Desktop"]').click()
		time.sleep(1)
		self.driver.find_element_by_xpath('//div[@id="cputable_length"]//select/option[text()="All"]').click()
		time.sleep(2)
		print('---------------------------------------------')
		selenium_response = self.driver.page_source
		new_selector = Selector(text=selenium_response)
		for cpu in new_selector.css('table#cputable tbody tr'):
			if cpu.css('td:nth-child(7)::text').extract_first() != 'Unknown':
				cpulinkfrag = cpu.css('a::attr(href)').extract_first()
				cpulink = 'https://www.videocardbenchmark.net/gpu.php?' + cpulinkfrag.split('?')[1]
				yield scrapy.Request(cpulink, callback=self.parse_gpu)
		print('---------------------------------------------')
		self.driver.close()


	def parse_gpu(self, response):
		doc = {}
		specifications = response.css('div.desc-body')
		leftdesc = specifications.css('em.left-desc-cpu')
		doc['Name'] = response.css('span.cpuname::text').extract_first()
		doc['Interface'] = re.sub('[ ]', "", str(response.xpath('//div[@class="desc-body"]//em[@class="left-desc-cpu"]//strong[text()="Bus Interface:"]/../text()').extract_first()))
		doc['CoreClock'] = re.sub('[ GHzM]', "", str(response.xpath('//div[@class="desc-body"]//em[@class="left-desc-cpu"]//strong[text()="Core Clock(s): "]/../text()').extract_first()).split(',')[0])
		doc['VRAMCapacity'] = re.sub('[ GMBK]', "", str(response.xpath('//div[@class="desc-body"]//em[@class="left-desc-cpu"]//strong[text()="Max Memory Size:"]/../text()').extract_first()))
		doc['VRAMClock'] = re.sub('[ GHzM]', "", str(response.xpath('//div[@class="desc-body"]//em[@class="left-desc-cpu"]//strong[text()="Memory Clock(s): "]/../text()').extract_first()))
		doc['TDP'] = re.sub('[ W]', "", str(response.xpath('//div[@class="desc-body"]//em[@class="left-desc-cpu"]//strong[text()="Max TDP:"]/../text()').extract_first()))
		doc['Rating'] = re.sub('[ ]', "", str(response.css('div.right-desc span::text').extract()[1]))
		doc['url'] = response.request.url
		if doc['CoreClock'] == 'None':
			doc.pop('CoreClock', None)
		if doc['VRAMCapacity'] == 'None':
			doc.pop('VRAMCapacity', None)
		if doc['VRAMClock'] == 'None':
			doc.pop('VRAMClock', None)
		if doc['TDP'] == 'None':
			doc.pop('TDP', None)
		if doc['Name'] != 'None' and doc['Interface'] != 'None':
			yield doc


#-----------------------------RAM---------------------------------------------


class PcbuilderRAMSpider(scrapy.Spider):
	name = 'pcbuilderRAM'
	allowed_domains = ['userbenchmark.com']
	start_urls = ['https://ram.userbenchmark.com/']

	def __init__(self):
		self.table = 'ram'
		self.driver = self.create_driver()
		
		
	def create_driver(self):
		options = webdriver.ChromeOptions()
		options.add_argument("headless")
		desired_capabilities = options.to_capabilities()
		driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
		return driver


	def click_cookies(self, nextFlag):
		try:
			cookies_button = self.driver.find_element_by_xpath('//div[@class="nb-parent"]/a[text()="Got it"]')
		except selenium.common.exceptions.NoSuchElementException:
			print('Cookies already clicked')
		except:
			nextFlag = False
			raise
		else:
			cookies_button.click()
			print('Cookies clicked')

	def parse(self, response):
		nextFlag = True
		self.driver.get(self.start_urls[0])
		self.click_cookies(nextFlag)
		while nextFlag:
			print('---------------------------------------------')
			selenium_response = self.driver.page_source
			new_selector = Selector(text=selenium_response)
			yield from self.parse_page(new_selector)
			print('---------------------------------------------')
			try:
				next_page = self.driver.find_element_by_xpath('//ul[@class="pagination pagination-lg"]/li/a[text()="Next »"]')
			except selenium.common.exceptions.NoSuchElementException as e:
				nextFlag = False
			except:
				raise
			else:
				try:
					self.driver.execute_script("arguments[0].scrollIntoView();", next_page) 
					self.driver.execute_script("arguments[0].click();", next_page)
				except:
					raise
				else:
					time.sleep(5)
		self.driver.close()

	def parse_page(self, response):
		for ram in response.css('tr.hovertarget div.smallp'):
			page = {}
			ramtitle = str(ram.css('a.nodec::text').extract_first())
			words = ramtitle.split()
			last = len(words) - 1
			page['Name'] = ramtitle
			page['Capacity'] = words[last]
			page['CASLatency'] = re.sub('[ CLAS]', "", str(words[last - 1]))
			page['Speed'] = words[last - 2]
			page['url'] = ram.css('span a::attr(href)').extract_first()
			yield page

#-----------------------------HDD/SSHD---------------------------------------------

class PcbuilderHDDSSHDSpider(scrapy.Spider):
	name = 'pcbuilderHDDSSHD'
	allowed_domains = ['userbenchmark.com']
	start_urls = ['https://hdd.userbenchmark.com/']

	def __init__(self):
		self.table = 'hddsshd'
		self.driver = self.create_driver()
		
		
	def create_driver(self):
		options = webdriver.ChromeOptions()
		options.add_argument("headless")
		desired_capabilities = options.to_capabilities()
		driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
		return driver


	def click_cookies(self, nextFlag):
		try:
			cookies_button = self.driver.find_element_by_xpath('//div[@class="nb-parent"]/a[text()="Got it"]')
		except selenium.common.exceptions.NoSuchElementException:
			print('Cookies already clicked')
		except:
			nextFlag = False
			raise
		else:
			cookies_button.click()
			print('Cookies clicked')

	def parse(self, response):
		nextFlag = True
		self.driver.get(self.start_urls[0])
		self.click_cookies(nextFlag)
		while nextFlag:
			print('---------------------------------------------')
			selenium_response = self.driver.page_source
			new_selector = Selector(text=selenium_response)
			yield from self.parse_page(new_selector)
			print('---------------------------------------------')
			try:
				next_page = self.driver.find_element_by_xpath('//ul[@class="pagination pagination-lg"]/li/a[text()="Next »"]')
			except selenium.common.exceptions.NoSuchElementException as e:
				nextFlag = False
			except:
				raise
			else:
				try:
					self.driver.execute_script("arguments[0].scrollIntoView();", next_page) 
					self.driver.execute_script("arguments[0].click();", next_page)
				except:
					raise
				else:
					time.sleep(5)
		self.driver.close()

	def parse_page(self, response):
		for hdd in response.css('tr.hovertarget div.smallp'):
			doc = {}
			hddtitle = str(hdd.css('a.nodec::text').extract_first())
			words = hddtitle.split()
			if '(' in words[len(words) - 1]:
				last = len(words) - 2
			else:
				last = len(words) - 1
			
			doc['Name'] = hddtitle
			
			try:
				if 'T' in words[last]:
					capacity_raw = re.sub('[ TB]', "", str(words[last]))
					doc['Capacity'] = str(int(capacity_raw) * 1000)
				else:
					capacity_raw = re.sub('[ GB]', "", str(words[last]))
					doc['Capacity'] = capacity_raw
			except Exception as e:
				print(e)
			else:
				if "SSHD" in words:
					doc['isSSHD'] = "1"
				else:
					doc['isSSHD'] = "0"
				doc['url'] = hdd.css('span a::attr(href)').extract_first()
				yield doc


#-----------------------------SSD/M2---------------------------------------------

class PcbuilderSSDM2Spider(scrapy.Spider):
	name = 'pcbuilderSSDM2'
	allowed_domains = ['userbenchmark.com']
	start_urls = ['https://ssd.userbenchmark.com/']

	def __init__(self):
		self.table = 'ssdm2'
		self.driver = self.create_driver()
		
		
	def create_driver(self):
		options = webdriver.ChromeOptions()
		options.add_argument("headless")
		desired_capabilities = options.to_capabilities()
		driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
		return driver


	def click_cookies(self, nextFlag):
		try:
			cookies_button = self.driver.find_element_by_xpath('//div[@class="nb-parent"]/a[text()="Got it"]')
		except selenium.common.exceptions.NoSuchElementException:
			print('Cookies already clicked')
		except:
			nextFlag = False
			raise
		else:
			cookies_button.click()
			print('Cookies clicked')

	def parse(self, response):
		nextFlag = True
		self.driver.get(self.start_urls[0])
		self.click_cookies(nextFlag)
		while nextFlag:
			print('---------------------------------------------')
			selenium_response = self.driver.page_source
			new_selector = Selector(text=selenium_response)
			yield from self.parse_page(new_selector)
			print('---------------------------------------------')
			try:
				next_page = self.driver.find_element_by_xpath('//ul[@class="pagination pagination-lg"]/li/a[text()="Next »"]')
			except selenium.common.exceptions.NoSuchElementException as e:
				nextFlag = False
			except:
				raise
			else:
				try:
					self.driver.execute_script("arguments[0].scrollIntoView();", next_page) 
					self.driver.execute_script("arguments[0].click();", next_page)
				except:
					raise
				else:
					time.sleep(5)
		self.driver.close()

	def parse_page(self, response):
		for ssd in response.css('tr.hovertarget div.smallp'):
			doc = {}
			ssdtitle = str(ssd.css('a.nodec::text').extract_first())
			words = ssdtitle.split()
			last = len(words) - 1
			
			doc['Name'] = ssdtitle
			
			try:
				if 'T' in words[last]:
					capacity_raw = re.sub('[ TB]', "", str(words[last]))
					doc['Capacity'] = str(int(capacity_raw) * 1000)
				else:
					capacity_raw = re.sub('[ GB]', "", str(words[last]))
					doc['Capacity'] = capacity_raw
			except Exception as e:
				print(e)
			else:
				if "NVMe" in words or "M.2" in words:
					doc['ism2'] = "1"
				else:
					doc['ism2'] = "0"
				doc['url'] = ssd.css('span a::attr(href)').extract_first()
				yield doc

#-----------------------------MOTHERBOARD---------------------------------------------

class PcbuilderMOBOSpider(scrapy.Spider):
	name = 'pcbuilderSSDM2'
	allowed_domains = ['motherboarddb.com']
	start_urls = ['https://motherboarddb.com/motherboards/?dt=table&market=c&ram_type=4&form_factor=2']

	def __init__(self):
		self.table = 'mobo'
		self.driver = self.create_driver()
		
		
	def create_driver(self):
		options = webdriver.ChromeOptions()
		options.add_argument("headless")
		desired_capabilities = options.to_capabilities()
		driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
		return driver

	def parse(self, response):
		nextFlag = True
		self.driver.get(self.start_urls[0])
		time.sleep(2)
		while nextFlag:
			print('---------------------------------------------')
			selenium_response = self.driver.page_source
			new_selector = Selector(text=selenium_response)
			for mobolinkfrag in new_selector.css('table tbody a::attr(href)').extract():
				mobolink = 'https://motherboarddb.com' + mobolinkfrag
				yield scrapy.Request(mobolink, callback=self.parse_page)
			print('---------------------------------------------')
			try:
				next_page = self.driver.find_element_by_xpath('//ul[@class="pagination pagination-sm"]/li/a[text()="Next"]')
			except selenium.common.exceptions.NoSuchElementException as e:
				nextFlag = False
			except:
				raise
			else:
				try:
					self.driver.execute_script("arguments[0].scrollIntoView();", next_page) 
					self.driver.execute_script("arguments[0].click();", next_page)
				except:
					raise
				else:
					time.sleep(2)
		self.driver.close()

	def parse_page(self, response):
		doc = {}
		doc['Name'] = response.css('div.container div.row h1::text').extract_first()
		
		main = response.css('div.main-content')
		doc['Chipset'] = main.css('div.card-body tr:nth-child(5) a::text').extract_first()
		doc['formFactor'] = main.css('div.card-body tr:nth-child(4) a::text').extract_first()
		doc['Socket'] = re.sub('[ ]', "", str(main.css('div.card-body tr:nth-child(3) a::text').extract_first()))
		doc['PCIex16Slots'] = 0
		doc['PCIex16x16Slots'] = 0
		for expansion in main.css('div.row:nth-child(5) li::text').extract():
			words = expansion.split()
			if words[3] == 'x16':
				doc['PCIex16Slots'] = doc['PCIex16Slots'] + int(re.sub('[x]', '', words[0]))
				if words[len(words)-1] == 'x16':
					doc['PCIex16x16Slots'] = int(re.sub('[x]', '', words[0]))
			elif words[3] == 'x8':
				doc['PCIex8Slots'] = re.sub('[x]', '', words[0])
			elif words[3] == 'x4':
				doc['PCIex4Slots'] = re.sub('[x]', '', words[0])
			elif words[3] == 'x1':
				doc['PCIex1Slots'] = re.sub('[x]', '', words[0])
		doc['PCIex16Slots'] = str(doc['PCIex16Slots'])
		doc['PCIex16x16Slots'] = str(doc['PCIex16x16Slots'])
		
		MultipleGPUCompatibilities = main.css('div.row:nth-child(5) div.col:nth-child(1) div.card:nth-child(3) tr td:nth-child(2)::text').extract()
		print(MultipleGPUCompatibilities)
		doc['CrossfireCompatible'] = str(int(MultipleGPUCompatibilities[0] == 'Yes'))
		doc['SLICompatible'] =  str(int(MultipleGPUCompatibilities[1] == 'Yes'))
		sataslots = response.xpath('//div[@class="row"][2]/div[2]/div[@class="card"][1]//h6[text()="Storage"]/following-sibling::ul[1]/li/text()').extract()
		n = 0
		for satas in sataslots:
			n += int(re.sub('[x]', '', satas.split()[0]))
		doc['SATASlots'] = str(n)
		if len(response.css('div.row:nth-child(5) div.col:nth-child(2) div.card-header::text').extract()) == 3:
			doc['M2Slots'] = re.sub('[x]', '', response.css('div.row:nth-child(5) div.col:nth-child(2) div.card:nth-child(6) td:nth-child(1)::text').extract_first())
			doc['M2Sizes'] = re.sub('[,\n]', ' ', response.css('div.row:nth-child(5) div.col:nth-child(2) div.card:nth-child(6) td:nth-child(3)::text').extract_first())
		else:
			doc['M2Slots'] = '0'
		doc['RAMSlots'] = response.css('div.row b::text').extract_first()
		doc['MaxMemorySpeed'] = response.css('div.row:nth-child(5) div.col:nth-child(2) div.card:nth-child(4) tr:nth-child(3) td::text').extract_first()
		doc['url'] = response.request.url
		yield doc

process = CrawlerProcess(get_project_settings())
#process.crawl(PcbuilderCPUSpider)
#process.crawl(PcbuilderGPUSpider)
#process.crawl(PcbuilderRAMSpider)
#process.crawl(PcbuilderHDDSSHDSpider)
#process.crawl(PcbuilderSSDM2Spider)
process.crawl(PcbuilderMOBOSpider)
process.start()
