from asyncio.log import logger
from logging import warning
import pandas as pd
import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys


class GuessSpider(scrapy.Spider):
    name = 'guess'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(GuessSpider, self).__init__(*args, **kwargs)

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

        time.sleep(5)

        """scrolling till bottom for 40 seconds"""
        element = self.driver.find_element_by_tag_name('body')
        timeout = time.time() + 15 # 2 minutes from now

        while True:
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)
            if time.time() > timeout:
                break

        # try:
        #     button_next = self.driver.find_element_by_xpath('//div[@class="pagination pagination__bottom"]//button[@aria-label="Next"]')
        #     button_next.click()
        #     time.sleep(4)
        # except:
        #     print('Done with next next!!')

    def start_requests(self):
        xpath = '//a[@class="link product-tile__link"]'
        link_elements = self.driver.find_elements_by_xpath(xpath)
        links = []

        for link in link_elements:
            links.append(link.get_attribute("href"))
        print('------'*10)
        print(links)
        print('------'*10)
        for href in links:
            yield scrapy.Request(url=href, headers=self.headers, callback=self.parse_guess_items, dont_filter=True)
            
    def parse_guess_items(self, response):
        self.driver.get(response.url)
        product_name = self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[2]/div/div[1]/div/h1').get_attribute('innerHTML')
        imgs = self.driver.find_elements_by_xpath('//div[@data-test="image-wrap"]//div[@class="css-b7jmoi"]//img[@width="76"]')
        imgs = [img.get_attribute('currentSrc') for img in imgs]

        print('+----+' * 10)
        print(f'{product_name} {len(imgs)}')
        print(imgs)
        print('+----+' * 10)

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
        # print('*-*'*10)
        # print(f'Number of image: {self.num}')
        # print('*-*'*10)
        # time.sleep(0.5)
        # self.driver.quit()