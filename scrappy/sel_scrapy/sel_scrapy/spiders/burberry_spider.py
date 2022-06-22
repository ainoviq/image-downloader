import time
from unicodedata import category
import scrapy
import pandas as pd
from scrapy.utils.project import get_project_settings

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys


class BurberrySpider(scrapy.Spider):
    name = "burberry"

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(BurberrySpider, self).__init__(*args, **kwargs)

        self.category = category
        self.url = url
        self.image_links = []
        self.num = 0

        self.settings = get_project_settings()
        self.driver_path = self.settings.get('CHROME_DRIVER_PATH')
        self.headers = {
            'authority': self.url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Cafari/537.36'
        }
        self.options = ChromeOptions()
        self.options.headless = False
        # self.options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
        self.driver = Chrome(executable_path=self.driver_path, options=self.options)
        # self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(40)
        self.driver.implicitly_wait(40)
        self.driver.maximize_window()
        self.driver.get(self.url)
        time.sleep(3)

        """Scroll till bottom"""
        element = self.driver.find_element_by_tag_name('body')
        timeout = time.time() + 60

        while True:
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)
            if time.time() > timeout:
                break

    def start_requests(self):
        xpath = xpath='//div[contains(@class, "product-card")]//a[contains(@class, "product-card__link")]'
        links = self.driver.find_elements_by_xpath(xpath=xpath)
        links_list = []
        for link in links:
            links_list.append(link.get_attribute('href'))

        for link in links_list:
            yield scrapy.Request(url=link, callback=self.parse_images, headers=self.headers, dont_filter=True)

    def parse_images(self, response):
        self.driver.get(response.url)
        product_name = response.css('.product-info-panel__title').css('span::text').get()
        imgs = response.css('img::attr(src)').getall()

        print('+-----+'*10)
        print(f'product_name: {product_name}')
        # print(f'product_name: {product_name}, imgs: {imgs}')
        print('+-----+'*10)

        for img in range(len(imgs)):
            self.num += 1
            if '.jpg' in imgs[img]:
                web_scraper_order = f'{int(time.time_ns())}_{img}'
                items = {
                    "web-scraper-order": web_scraper_order,
                    "web-scraper-start-url": self.url,
                    "category": self.category,
                    "product-name": product_name,
                    "image-src": imgs[img]
                }
                self.image_links.append(items)
        print(f'Number of image: {self.num}')
        data = pd.DataFrame(self.image_links)
        data.to_csv(f'{self.category}.csv')