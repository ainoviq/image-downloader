import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from sel_scrapy.items import FleeceItem


class FleeceSpider(scrapy.Spider):
    name = 'fleece'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(FleeceSpider, self).__init__(*args, **kwargs)

        # category = 'TOPS & BLOUSES'
        # category = 'Dresses'
        # url = 'https://www.marcjacobs.com/default/the-marc-jacobs/the-clothing/tops-blouses/?sz=22'
        # url = 'https://www.marcjacobs.com/default/the-marc-jacobs/the-clothing/dresses/?sz=29'

        self.category = category
        self.url = url

        print("======" * 10)
        print(category)
        print(url)
        print("======" * 10)

        self.file_ = open(f'burberry-{self.category}.csv', 'a')
        self.file_.writelines('web-scraper-order,web-scraper-start-url,category,image-src\n')

    def start_requests(self):
        settings = get_project_settings()
        driver_path = settings.get('CHROME_DRIVER_PATH')
        
        options = ChromeOptions()
        options.headless = True
        driver = Chrome(executable_path=driver_path, options=options)

        # xpath='//div[contains(@class, "product-tile")]//a[contains(@class, "name-link")]'
        # xpath='//a[contains(@class, "lockup-card")]'
        xpath='//div[contains(@class, "product-card")]//a[contains(@class, "product-card__link")]'
        driver.get(self.url)
        
        link_elements = driver.find_elements_by_xpath(xpath)

        headers = {
            'authority': self.url,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Cafari/537.36'
        }
        for link_el in link_elements:
            href = link_el.get_attribute("href")
            yield scrapy.Request(url=href, headers=headers)
        driver.quit()
        time.sleep(5.5)

    def parse(self, response):
        item = FleeceItem()
        # res = response.css('.image').css('img::attr(srcset)').getall()
        # item['imgs'] = res[3:]

        # res = response.css('.desktop-product-gallery__image__picture').css('picture').css('source::attr(srcset)').getall()
        res = response.css('.product-gallery__item__source').get()
        print("======"*12)
        print(res)
        print("======"*12)
        item['imgs'] = res

        # for it in item['imgs']:
        #     print(f'https:{it}')
            # it = it.split(', ')
            # for i in it:
                # print(f'https:{i}')
            # web_scraper_order = it.split("/")[5].split("?")[0]
            # web_scraper_start_url = self.url
            # self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{it}\n")
        # self.file_.close