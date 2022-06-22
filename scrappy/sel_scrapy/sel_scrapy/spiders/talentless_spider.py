from asyncio.log import logger
from logging import warning
import pandas as pd
import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TalentlessSpider(scrapy.Spider):
    name = 'talentless'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(TalentlessSpider, self).__init__(*args, **kwargs)

        self.category = category
        self.url = url
        self.image_sources = []
        self.num = 0
        self.num_link = 0

        self.headers = {
            'authority': self.url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Cafari/537.36'
        }
        self.settings = get_project_settings()
        self.driver_path = self.settings.get('CHROME_DRIVER_PATH')
        
        self.options = ChromeOptions()
        # self.options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        self.options.headless = True
        self.driver = Chrome(executable_path=self.driver_path, options=self.options)
        # self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(40)
        self.driver.implicitly_wait(40)
        self.driver.maximize_window()
        # self.driver.set_window_size(480, 640)
        self.driver.get(self.url)
        time.sleep(2)

        # """scrolling till bottom"""
        element = self.driver.find_element_by_tag_name('body')
        timeout = time.time() + 10   # 1 minutes from now

        while True:
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
            if time.time() > timeout:
                break

    def start_requests(self):
        xpath = '//div[@class="grid-product__content"]/a[@class="grid-product__link"]'
        link_elements = self.driver.find_elements_by_xpath(xpath)
        links = []
        
        for link in link_elements:
            links.append(link.get_attribute("href"))

        for href in links:
            yield scrapy.Request(url=href, headers=self.headers, callback=self.parse_items, dont_filter=True)
            
    def parse_items(self, response):
        self.num_link += 1
        self.driver.get(response.url)
        product_name = self.driver.find_element_by_xpath('//h1[@class="h1 product-single__title"]').get_attribute('innerText')
        imgs = self.driver.find_elements_by_xpath('//div[contains(@class, "product__thumb-item slick-slide")][@style="margin-bottom: 10px; width: 80px;"]//a')
        imgs = [img.get_attribute('href') for img in imgs]
        imgs = list(dict.fromkeys(imgs))

        print('+----+' * 10)
        print(f'Link no: {self.num_link}, product-name: {product_name}, num_imgs: {len(imgs)}, imgs: {imgs}')
        for img in range(len(imgs)):
            self.num += 1
            web_scraper_order = f'{int(time.time_ns())}_{img}'
            items = {
                "web-scraper-order": web_scraper_order,
                "web-scraper-start-url": self.url,
                "category": self.category,
                "product-url": response.url,
                "product-name": product_name,
                "image-src": imgs[img]
            }
            self.image_sources.append(items)
        dataframe = pd.DataFrame(self.image_sources)
        dataframe.to_csv(f'{self.category}.csv')
        print(f'Number of total images: {self.num}')
        print('+----+' * 10)