from asyncio.log import logger
from logging import warning
import pandas as pd
import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys


class MonclerSpider(scrapy.Spider):
    name = 'moncler'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(MonclerSpider, self).__init__(*args, **kwargs)

        self.category = category
        self.url = url
        self.image_sources = []
        self.num = 0
        self.custom_settings = {
            'DOWNLOAD_DELAY': 1,
        }

        self.headers = {
            'authority': self.url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Cafari/537.36'
        }
        self.settings = get_project_settings()
        self.driver_path = self.settings.get('CHROME_DRIVER_PATH')

        self.options = ChromeOptions()
        self.options.headless = False
        self.driver = Chrome(
            executable_path=self.driver_path, options=self.options)
        # self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(10)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.driver.get(self.url)

        """scrolling till bottom"""
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def start_requests(self):
        xpath = '//li/div/div[@class="product-tile__card"]/a[@class="product-tile__link"]'
        link_elements = self.driver.find_elements_by_xpath(xpath)
        links = []

        for link in link_elements:
            links.append(link.get_attribute("href"))

        for href in links:
            yield scrapy.Request(url=href, headers=self.headers, dont_filter=True, priority=1)

    def parse(self, response):
        # product_name = response.xpath('//h1[@class="product-selection__name-price__name"]/text()').getall()
        product_name = response.css('h1::text').get()
        imgs = response.xpath(
            '//button/div[@class="product-image"]/img/@src').getall()

        print(f'Number of image: {product_name}\n{imgs}')
        print()

        # for img in range(len(imgs)):
        #     self.num += 1
        #     web_scraper_order = f'{int(time.time_ns())}_{img}'
        #     items = {
        #         "web-scraper-order": web_scraper_order,
        #         "web-scraper-start-url": self.url,
        #         "category": self.category,
        #         "name": product_name,
        #         "image-src": imgs[img].split("?")[0]
        #     }
        #     self.image_sources.append(items)
        # dataframe = pd.DataFrame(self.image_sources)
        # dataframe.to_csv(f'{self.category}.csv')
