import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from sel_scrapy.items import Item

from item_links.zara import zara_tees, crop_tops, body_suits, \
    corset, tulle, shirts, blouses, satin, cropped, tshirts_basics, tshirts_long_sleeve, tshirts_half_sleeve, tshirts_sleeveless, tshirts_seamless


class ZaraSpider(scrapy.Spider):
    name = 'zara'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(ZaraSpider, self).__init__(*args, **kwargs)

        self.category = category
        self.url = url
        self.image_sources = []
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
        self.options.add_experimental_option(
            "prefs", {"profile.managed_default_content_settings.images": 2})
        self.options.add_argument('user-agent={0}'.format(self.user_agent))
        self.options.add_argument("accept-language='en-US,en;q=0.9'")
        self.options.headless = True
        self.options.add_argument("start-maximized")
        self.options.add_argument(
            '--disable-blink-features=AutomationControlled')
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)

        self.driver = Chrome(
            executable_path=self.driver_path, options=self.options)
        self.driver.set_window_size(1366, 768)
        self.wait = WebDriverWait(self.driver, 5)
        self.action = ActionChains(self.driver)

    def start_requests(self):
        links = list(dict.fromkeys(tshirts_seamless))
        print(len(links))

        for url in links:
            self.num += 1
            print(f'URL no {self.num}')
            try:
                self.driver.get(url)
                time.sleep(0.5)

                name = self.driver.find_elements_by_xpath(
                    '//h1[@class="product-detail-info__header-name"]')[0].text
                imgs = self.driver.find_elements_by_xpath('//ul[@class="product-detail-images-thumbnails product-detail-images__thumbnails"]/li/button/div/div[@class="media__wrapper media__wrapper--fill"]/img[@class="media-image__image media__wrapper--media"]')
                imgs_src = [img.get_attribute('src').replace('w/26/', 'w/1920/') for img in imgs]

                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_zara, meta={'url': url, 'name': name, 'imgs_src': imgs_src}, dont_filter=True)
            except:
                print(f'ERROR: Failed to get response from url {url}')

    def parse_zara(self, response):
        item = Item()
        item['order'] = int(time.time_ns())
        item['link'] = response.meta['url']
        item['name'] = response.meta['name']
        item['category'] = self.category
        item['imgs_src'] = response.meta['imgs_src']
        return item
