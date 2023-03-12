from asyncio.log import logger
from logging import warning
import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from sel_scrapy.items import Item


class ZalandoLinksSpider(scrapy.Spider):
    name = 'zalando_links'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(ZalandoLinksSpider, self).__init__(*args, **kwargs)
        self.product_lists = []
        self.category = category
        self.url = ['https://en.zalando.de/women-clothing-tunics/']
        [self.url.append(f'https://en.zalando.de/women-clothing-tunics/?p={p}') for p in range(1, 17)]

        print(self.url)
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

        with open('./item_links/zalando.py', 'a+') as f:
            f.write(f"{self.category} = [\n")

    def start_requests(self):
        self.url = list(dict.fromkeys(self.url))

        for url in self.url:
            self.num += 1
            print(f'Page no {self.num}')
            try:
                self.driver.get(url)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                product_links = self.driver.find_elements_by_xpath('//div[@class="DT5BTM w8MdNG cYylcv QylWsg _75qWlu iOzucJ JT3_zV DvypSJ"]/div/article/a[@class="_LM JT3_zV CKDt_l CKDt_l LyRfpJ"]')
                href = [product_link.get_attribute(
                    'href') for product_link in product_links]
                href = list(dict.fromkeys(href))

                with open('./item_links/zalando.py', 'a+') as f:
                    for l in href:
                        url_line = f'"{l}",\n'
                        # print(f'Writing: {url_line}')
                        f.write(url_line)

                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_farfetch, meta={'urls': self.product_lists}, dont_filter=True)
            except:
                print(f'ERROR: Failed to get response from url {url}')
        with open('./item_links/zalando.py', 'a+') as f:
            f.write("]\n")

    def parse_farfetch(self, response):
        item = Item()
        return item
