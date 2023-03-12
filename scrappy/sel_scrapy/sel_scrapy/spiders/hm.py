import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from sel_scrapy.items import Item

from item_links.hm import blouses

class HMSpider(scrapy.Spider):
    name = 'hm'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(HMSpider, self).__init__(*args, **kwargs)

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
        # self.options.add_experimental_option(
        #     "prefs", {"profile.managed_default_content_settings.images": 2})
        self.options.add_argument('user-agent={0}'.format(self.user_agent))
        self.options.add_argument("accept-language='en-US,en;q=0.9'")
        self.options.headless = False
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
        links = list(dict.fromkeys(blouses))
        print('After Filter = ', len(links))

        for url in links:
            self.num += 1
            print(f'URL no {self.num}')
            try:
                self.driver.get(url)
                time.sleep(4)
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")

                name = self.driver.find_elements_by_xpath(
                    '//h1[@class="Heading-module--general__3HQET ProductName-module--productTitle__1T9f0 Heading-module--small__SFfSh"]')[0].text
                primary_img = self.driver.find_elements_by_xpath(
                    '//figure[@class="pdp-image product-detail-images product-detail-main-image"]//div/img')

                imgs = self.driver.find_elements_by_xpath(
                    '//figure[@class="pdp-secondary-image pdp-image"]/img')
                imgs_src = [primary_img[0].get_attribute('src')]
                for im in imgs:
                    imgs_src.append(im.get_attribute('src'))

                # imgs_src = [img.get_attribute('srcset') for img in imgs]

                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_HM, meta={'url': url, 'name': name, 'imgs_src': imgs_src}, dont_filter=True)
            except:
                print(f'ERROR: Failed to get response from url {url}')

    def parse_HM(self, response):
        item = Item()
        item['order'] = int(time.time_ns())
        item['link'] = response.meta['url']
        item['name'] = response.meta['name']
        item['category'] = self.category
        item['imgs_src'] = response.meta['imgs_src']

        print(item)
        return item
