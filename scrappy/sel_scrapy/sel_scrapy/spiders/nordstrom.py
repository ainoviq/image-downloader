import time
from asyncio.log import logger
from logging import warning
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from sel_scrapy.items import Item

from item_links.nordstrom import nordstrom_tees


class NordstromSpider(scrapy.Spider):
    name = 'nordstrom'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(NordstromSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.count = 0
        self.url = url
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
        self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(5)
        self.driver.implicitly_wait(5)

    def start_requests(self):
        print('No Filter = ', len(nordstrom_tees))
        links = list(dict.fromkeys(nordstrom_tees))
        print('After Filter = ', len(links))

        for url in links:
            self.count += 1
            print(f'URL no {self.count}')
            try:
                self.driver.get(url)
                time.sleep(5)

                name = self.driver.find_elements_by_xpath('//h1[@class=" _39r2W gFaKF _3jNIn _36liS"]')[0].text
                
                show_all_btn = self.driver.find_elements_by_xpath('//button[@class="_1jf6R"]')
                try:
                    show_all_btn[0].click()
                    print('Expanded show all button...')
                except:
                    print('No show all button...')

                imgs = self.driver.find_elements_by_xpath('//div[@class="_39fQ4"]/div/div/img[@class="_1xX4Z _1VwWY"]')
                imgs_src = [img.get_attribute('src').replace(
                    '&w=780&h=1196', '') for img in imgs]
                imgs_src = list(dict.fromkeys(imgs_src))

                print(name)
                print(imgs_src)

                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_Nordstrom, meta={'url': url, 'name': name, 'imgs_src': imgs_src}, dont_filter=True)
            except:
                print(f'ERROR: Failed to get response from url {url}')

    def parse_Nordstrom(self, response):
        item = Item()

        item['order'] = int(time.time_ns())
        item['link'] = response.meta['url']
        item['name'] = response.meta['name']
        item['category'] = self.category
        item['imgs_src'] = response.meta['imgs_src']

        return item
