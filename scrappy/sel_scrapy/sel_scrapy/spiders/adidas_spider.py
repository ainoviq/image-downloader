from asyncio.log import logger
from logging import warning
import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains


class FleeceSpider(scrapy.Spider):
    name = 'adidas'

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
        # self.options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        self.options.headless = False
        self.driver = Chrome(executable_path=self.driver_path, options=self.options)
        # self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(40)
        self.driver.implicitly_wait(40)
        self.driver.maximize_window()
        # self.driver.set_window_size(480, 640)
        self.driver.get(self.url)
        
        """
            Full page loading
        """
        # self.driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
        time.sleep(20)

        """Goto next page"""
        # while True:
        #     try:
        #         """Scroll to next button"""
        #         actions = ActionChains(self.driver)
        #         self.driver.execute_script("arguments[0].scrollIntoView();", next_page)
        #         next_page = self.driver.find_element_by_xpath('//a[@data-auto-id="plp-pagination-next"]')
        #         actions.move_to_element(next_page).perform()
        #         next_page.click()
        #         time.sleep(2)
        #     except:
        #         print(logger.warning('Ahh! Done with the next pages!'))
        #         break

    def start_requests(self):
        """adidas"""
        xpath = '//div[@class="glass-product-card color-variations__fixed-size plp-product-card___1sck4 product-card-content___2O10f"]/a'
        link_elements = self.driver.find_elements_by_xpath(xpath)

        for link_el in link_elements:
            href = link_el.get_attribute("href")
            yield scrapy.Request(url=href, headers=self.headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """adidas scraping"""
        self.driver.get(response.url)
        product_name = self.driver.find_elements_by_xpath('//h1[@data-auto-id="product-title"]/span')[0].get_attribute('innerHTML')
        imgs = self.driver.find_elements_by_xpath('//div[@data-auto-id="pdp__image-viewer__desktop-zoom__content"]//img')

        print('+----+' * 10)
        print(product_name)
        print(len(imgs))
        print('+----+' * 10)

        for img in range(len(imgs)):
            web_scraper_order = f'{int(time.time_ns())}_{img}'
            web_scraper_start_url = self.url
            self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{imgs[img].get_attribute('src').replace('/h_600,', '/')}\n")
        self.file_.close
        # self.driver.quit()
        # time.sleep(2)