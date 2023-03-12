from asyncio.log import logger
from logging import warning
import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from sel_scrapy.items import Item


class FarfetchLinksSpider(scrapy.Spider):
    name = 'farfetch_links'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(FarfetchLinksSpider, self).__init__(*args, **kwargs)
        self.product_lists = []
        self.category = category
        self.url = [
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=0&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=1&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=2&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=3&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=4&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=5&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=6&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=7&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=8&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=9&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=10&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=11&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=12&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=13&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=14&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=15&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=16&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=17&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=18&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=19&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=20&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=21&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=22&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=23&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=24&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=25&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=26&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=27&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=28&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=29&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=30&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=31&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=32&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=33&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=34&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=35&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=36&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=37&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=38&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=39&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=40&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=41&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=42&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=43&view=90&sort=3&category=136101',
            'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=44&view=90&sort=3&category=136101', 'https://www.farfetch.com/bd/shopping/women/clothing-1/items.aspx?page=45&view=90&sort=3&category=136101',
        ]
        self.num = 0
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Cafari/537.36'

        self.headers = {
            'authority': self.url,
            'user-agent': self.user_agent,
            "accept-language": "en-US,en;q=0.9"
        }
        self.settings = get_project_settings()
        self.driver_path = self.settings.get('CHROME_DRIVER_PATH')

        self.options = ChromeOptions()
        # self.options.add_experimental_option(
        #     "prefs", {"profile.managed_default_content_settings.images": 2})

        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.headless = False

        self.driver = Chrome(
            executable_path=self.driver_path, options=self.options)
        # self.driver.set_window_size(1366, 768)
        # self.wait = WebDriverWait(self.driver, 5)
        self.action = ActionChains(self.driver)

        with open('./item_links/farfetch.py', 'a+') as f:
            f.write(f"{self.category} = [\n")

    def start_requests(self):
        self.url = list(dict.fromkeys(self.url))

        for url in self.url:
            self.num += 1
            print(f'Page no {self.num}')
            try:
                self.driver.get(url)
                product_links = self.driver.find_elements_by_xpath(
                    '//div[@class="ltr-x69rqn e19e7out0"]/a[@data-component="ProductCardLink"]')
                href = [product_link.get_attribute(
                    'href') for product_link in product_links]
                href = list(dict.fromkeys(href))

                with open('./item_links/farfetch.py', 'a+') as f:
                    for l in href:
                        url_line = f'"{l}",\n'
                        # print(f'Writing: {url_line}')
                        f.write(url_line)

                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_farfetch, meta={'urls': self.product_lists}, dont_filter=True)
            except:
                print(f'ERROR: Failed to get response from url {url}')
        with open('./item_links/farfetch.py', 'a+') as f:
            f.write("]\n")

    def parse_farfetch(self, response):
        item = Item()

        # item['link'] = response.meta['urls']

        return item
