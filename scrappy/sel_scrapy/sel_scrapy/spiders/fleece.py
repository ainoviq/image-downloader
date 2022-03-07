from asyncio.log import logger
from email import header
import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from sel_scrapy.items import FleeceItem


class FleeceSpider(scrapy.Spider):
    name = 'fleece'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(FleeceSpider, self).__init__(*args, **kwargs)

        self.category = category
        self.url = url
        self.file_ = open(f'katespade-{self.category}.csv', 'a')
        self.file_.writelines('web-scraper-order,web-scraper-start-url,category,product-name,image-src\n')

        self.headers = {
            'authority': self.url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Cafari/537.36'
        }
        self.settings = get_project_settings()
        self.driver_path = self.settings.get('CHROME_DRIVER_PATH')
        
        self.options = ChromeOptions()
        self.options.headless = False
        self.driver = Chrome(executable_path=self.driver_path, options=self.options)
        self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(4)
        self.driver.implicitly_wait(4)
        self.driver.maximize_window()
        # self.driver.set_window_size(480, 640)
        print(self.driver.get_window_size())

        self.driver.get(self.url)
        try:
            buttons = self.driver.find_elements(By.XPATH, '//button[@aria-label="View more products"]')
            for button in buttons:
                time.sleep(2)
                button.click()
                self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                time.sleep(2)
        except:
            print(logger.warning('No such element found!'))
        time.sleep(3)

        """
            Full page loading
        """
        self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(3)

    def start_requests(self):
        """
            katespade xpath
        """
        xpath = '//a[contains(@data-th,"product-link")]'
    
        """
            burberry xpath
        """
        # xpath='//div[contains(@class, "product-card")]//a[contains(@class, "product-card__link")]'

        """
            marcjacobs xpath
        """
        # xpath='//div[contains(@class, "product-tile")]//a[contains(@class, "name-link")]'
        
        link_elements = self.driver.find_elements_by_xpath(xpath)

        for link_el in link_elements:
            href = link_el.get_attribute("href")
            print('*' * 20)
            print(href)
            print('*' * 20)
            yield scrapy.Request(url=href, headers=self.headers)
        self.driver.quit()

    def parse(self, response):
        item = FleeceItem()

        """
            katespade scraping
        """
        product_name = response.xpath('//h1[@data-qa="product-name"]/text()').get()
        imgs = response.css('img::attr(src)').getall()
        item['imgs'] = imgs
        print("=====" * 12)
        print(product_name)
        print(len(imgs))
        print("=====" * 12)

        for it in imgs[1:]:
            if "productThumbnail" in it:
                print(it)
                p1 = it.split("$")
                web_scraper_order = p1[0].split('/')[6][:-1]
                web_scraper_start_url = self.url
                img_url = f"{p1[0]}$s7fullsize$"
                self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{img_url}\n")
        self.file_.close


        """
            burberry scraping
        """
        # product_name = response.css('.product-info-panel__title').css('span::text').get()
        # imgs = response.css('img::attr(src)').getall()
        # print("======"*12)
        # print(product_name)
        # print(imgs)
        # print("======"*12)
        
        # item['imgs'] = imgs
        # for it in item['imgs']:
        #     if '.jpg' in it:
        #         print(f'https:{it}')
        #         web_scraper_order = it.split('/')[6].split('?')[0].split('.')[0]
        #         web_scraper_start_url = self.url
        #         self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{it}\n")
        # self.file_.close

        """
            marcjacobs scraping
        """

        # res = response.css('.image').css('img::attr(srcset)').getall()
        # item['imgs'] = res[3:]

        # for it in item['imgs']:
        #     print(f'https:{it}')
        #     it = it.split(', ')
        #     for i in it:
        #         print(f'https:{i}')
        #     web_scraper_order = it.split("/")[5].split("?")[0]
        #     web_scraper_start_url = self.url
        #     self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{it}\n")
        # self.file_.close