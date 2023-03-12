from asyncio.log import logger
from logging import warning
import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from sel_scrapy.items import Item


class FleeceSpider(scrapy.Spider):
    name = 'fleece'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(FleeceSpider, self).__init__(*args, **kwargs)

        self.category = category
        self.url = url
        self.file_ = open(f'{self.category}.csv', 'a+')
        heading = 'web-scraper-order,web-scraper-start-url,category,name,image-src\n'
        if (heading in self.file_.readlines()):
            print('Heading present. skipping...')
        else:
            self.file_.writelines(heading)

        self.headers = {
            'authority': self.url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Cafari/537.36'
        }
        self.settings = get_project_settings()
        self.driver_path = self.settings.get('CHROME_DRIVER_PATH')
        
        self.options = ChromeOptions()
        self.options.headless = False
        self.driver = Chrome(executable_path=self.driver_path, options=self.options)
        # self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(40)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        # self.driver.set_window_size(480, 640)
        self.driver.get(self.url)

        """Handle load more button"""
        # try:
        #     buttons = self.driver.find_elements(By.CSS_SELECTOR, 'a.view-all')
        #     for button in buttons:
        #         button.click()
        #         time.sleep(10)
        # except:
        #     print(logger.warning('No such element found!'))

        try:
            time.sleep(5)
            self.driver.find_element_by_xpath('//button[@data-testid="uc-accept-all-button"]').click()
            time.sleep(2)
        except:
            print(logger.warning('No such element to accept cookies'))

        """Load more button till the ends"""
        while True:
            try:
                load_more_btn = self.driver.find_element_by_xpath('//button[@class="pagination__button button button--primary"]')
                time.sleep(4)
                load_more_btn.click()
                time.sleep(5)
            except:
                print(logger.warning('Ahh! Loading more values finally done!'))
                break            

        """
            Full page loading
        """
        # self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(10)

    def start_requests(self):
        """tom tailor"""
        xpath = '//a[@class="text-link text-link--dark-blue product-tile__h5 text-link--no-underline"]'
        """zara"""
        # xpath = '//a[@class="product-link _item product-grid-product-info__name link"]'
        # xpath = '//a[@class="product-link product-grid-product__link link"]'
        """ralphlauren"""
        # xpath = '//a[@class="name-link"]'
        """massimodutti"""
        # xpath = '//a[@class="pointer"]'
        """public rec"""
        # xpath= '//a[@class="css-5tobas"]'
        """dior"""
        # xpath = '//a[@class="product-wrapper"]'
        """lacoste"""
        # xpath = '//a[@class="js-product-tile-link"]'
        """ioana ciolacu"""
        # xpath = '//div[@class="product_image with_second_image second_image_loaded"]//a'
        """katespade xpath"""
        # xpath = '//a[contains(@data-th,"product-link")]'
        """burberry xpath"""
        # xpath='//div[contains(@class, "product-card")]//a[contains(@class, "product-card__link")]'
        """marcjacobs xpath"""
        # xpath='//div[contains(@class, "product-tile")]//a[contains(@class, "name-link")]'
        
        link_elements = self.driver.find_elements_by_xpath(xpath)

        for link_el in link_elements:
            href = link_el.get_attribute("href")
            yield scrapy.Request(url=href, headers=self.headers, callback=self.parse)
        self.driver.quit()

    def parse(self, response):
        item = Item()
        """tom tailor scraping"""
        product_name = response.css('h1.product-tile__h5::text').get()
        imgs = response.xpath('//div[@class="product-gallery__image"]//img/@src').getall()
        imgs = list(dict.fromkeys(imgs))

        print('+----+' * 10)
        print(product_name)
        print(len(imgs))
        # print(imgs)
        print('+----+' * 10)

        for img in range(len(imgs)):
            web_scraper_order = f'{int(time.time_ns())}_{img}'
            web_scraper_start_url = self.url
            self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{imgs[img].replace('/560_745/', '/1654_2200/')}\n")
        self.file_.close