from asyncio.log import logger
from logging import warning
import pandas as pd
import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys


class RalphLaurenSpider(scrapy.Spider):
    name = 'ralphlauren'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(RalphLaurenSpider, self).__init__(*args, **kwargs)

        self.category = category
        self.url = url
        self.image_sources = []
        self.num = 0

        self.headers = {
            'authority': self.url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Cafari/537.36'
        }
        self.settings = get_project_settings()
        self.driver_path = self.settings.get('CHROME_DRIVER_PATH')
        
        self.options = ChromeOptions()
        # self.options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        self.options.headless = False
        self.driver = Chrome(executable_path=self.driver_path, options=self.options)
        # self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(40)
        self.driver.implicitly_wait(40)
        self.driver.maximize_window()
        # self.driver.set_window_size(480, 640)
        self.driver.get(self.url)

        time.sleep(2)

        """scrolling till bottom"""
        element = self.driver.find_element_by_tag_name('body')
        timeout = time.time() + 60*2   # 2 minutes from now

        while True:
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            try:
                view_more_btn = self.driver.find_elements_by_xpath('//a[@class="name-link"]')
                for btn in view_more_btn:
                    btn.click()
            except:
                print("Done with more")
            if time.time() > timeout:
                break

    def start_requests(self):
        xpath = '//a[@class="name-link"]'
        link_elements = self.driver.find_elements_by_xpath(xpath)
        links = []

        for link in link_elements:
            links.append(link.get_attribute("href"))
        
        for href in links:
            yield scrapy.Request(url=href, headers=self.headers, callback=self.parse_mango_items, dont_filter=True)
            
    def parse_mango_items(self, response):
        self.driver.get(response.url)
        product_name = self.driver.find_element_by_xpath('//h1[@class="product-name"]').get_attribute('innerHTML')
        imgs = self.driver.find_elements_by_xpath('//img[@class="popup-img pdp-popup-img zoomable"]')
        imgs = [img.get_attribute('data-img') for img in imgs]

        print('+----+' * 10)
        print(f'{product_name} {len(imgs)}')
        print('+----+' * 10)

        for img in range(len(imgs)):
            self.num += 1
            web_scraper_order = f'{int(time.time_ns())}_{img}'
            items = {
                "web-scraper-order": web_scraper_order,
                "web-scraper-start-url": self.url,
                "category": self.category,
                "name": product_name,
                "image-src": imgs[img].split("?")[0]
            }
            self.image_sources.append(items)
        dataframe = pd.DataFrame(self.image_sources)
        dataframe.to_csv(f'{self.category}.csv')
        print('*-*'*10)
        print(f'Number of image: {self.num}')
        print('*-*'*10)
        time.sleep(0.5)
        # self.driver.quit()