from asyncio.log import logger
from logging import warning
import pandas as pd
import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys


class DiorSpider(scrapy.Spider):
    name = 'dior'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(DiorSpider, self).__init__(*args, **kwargs)

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

        # time.sleep(1)
        # try:
        #     self.driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
        #     time.sleep(1)
        #     self.driver.find_element_by_css_selector('#navColumns4').click()
        # except:
        #     print('Cookie accepted!')
        time.sleep(2)

        """scrolling till bottom"""
        element = self.driver.find_element_by_tag_name('body')
        timeout = time.time() + 25   # 1 minutes from now

        while True:
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            if time.time() > timeout:
                break

    def start_requests(self):
        xpath = '//a[@class="product-wrapper"]'
        link_elements = self.driver.find_elements_by_xpath(xpath)
        links = []

        for link in link_elements:
            links.append(link.get_attribute("href"))
        
        for href in links:
            yield scrapy.Request(url=href, headers=self.headers, callback=self.parse_mango_items, dont_filter=True)
            
    def parse_mango_items(self, response):
        self.driver.get(response.url)
        product_name = self.driver.find_element_by_xpath('//h1//span[@class="multiline-text Titles_title__PAVsd"]').get_attribute('innerHTML')
        buttons = self.driver.find_elements_by_xpath('//li[@class="product-medias-grid-image"]//button[@class="Media_product-media__nZ4TD product-media"]')
        imgs = []
        
        for button in buttons:
            button.click()
            img = self.driver.find_element_by_xpath('//*[@id="imgZoomerViewer"]/div/img').get_attribute('src')
            print(img)
            self.driver.find_element_by_xpath('//button[@class="popin__wrapper__close"]').click()
            imgs.append(img)

        print('+----+' * 10)
        print(f'{product_name}')
        print(len(imgs))
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
        # time.sleep(0.5)
        # self.driver.quit()