from asyncio.log import logger
from logging import warning
import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from sel_scrapy.items import Item


class FleeceSpider(scrapy.Spider):
    name = 'nord'

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
        self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(40)
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.driver.set_window_size(480, 640)
        self.driver.get(self.url)

        """
            Captcha hold the door
        """
        
        # element = self.driver.find_element_by_css_selector('#px-captcha')
        # action = ActionChains(self.driver)
        # click = ActionChains(self.driver)
        # action.click_and_hold(element)
        # action.perform()
        # time.sleep(10)
        # action.release(element)
        # action.perform()
        # time.sleep(0.2)
        # action.release(element)

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
        xpath = '//article/div/h3/a'
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
        """gucci"""
        # xpath = '//a[@class="product-tiles-grid-item-link js-ga-track"]'
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
        product_name = response.css('h1._39r2W gFaKF _3jNIn _36liS::text').get()
        imgs = response.xpath('//div[contains(@class, "_39fQ4")]/div/div')
        # imgs = list(dict.fromkeys(imgs))

        print('+----+' * 10)
        print(product_name)
        print(imgs)
        # print(imgs)
        print('+----+' * 10)

        for img in range(len(imgs)):
            web_scraper_order = f'{int(time.time_ns())}_{img}'
            web_scraper_start_url = self.url
            self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{imgs[img].replace('/560_745/', '/1654_2200/')}\n")
        self.file_.close

        """zara scraping"""
        # product_name = response.css('h1.product-detail-info__header-name::text').get()
        # imgs = response.xpath('//picture[@class="media-image"]/source[@sizes="100vw"]/@srcset').getall()

        # print('+----+' * 10)
        # print(product_name)
        # print(len(imgs))
        # print('+----+' * 10)

        # for img in range(len(imgs)):
        #     web_scraper_order = f'{int(time.time_ns())}_{img}'
        #     web_scraper_start_url = self.url
        #     self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{imgs[img].split(' ')[2].replace('w/750/', 'w/2048/')}\n")
        # self.file_.close

        """massimo dutti scraping"""
        # product_name = response.xpath('//h1[contains(@class, "text-20-b pb-16 ttu")]/text()').get()
        # imgs = response.xpath('//div[@class="p-view placeholder"]/img/@src').getall()

        # print(product_name)
        # print(imgs)

        """public rec scraping"""
        # product_name = response.css("h1.css-17yz6ma::text").get()
        # imgs = response.xpath('//div[contains(@class, "css-1gphjnj")]//div//div//div//img/@src').getall()
         
        # for img in imgs:
        #     print(f'https:{img}\n')

        """dior scraping"""

        # product_name = response.css("h1").css("span.multiline-text.Titles_title__PAVsd::text").get()
        # buttons = response.xpath('//li[@class="product-medias-grid-image"]//button[@class="Media_product-media__nZ4TD product-media"]').getall()

        # for img in range(len(imgs[1:])):
        #     web_scraper_order = f'{int(time.time_ns())}_{img}'
        #     web_scraper_start_url = self.url
        #     self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{imgs[img]}\n")
        # self.file_.close

        """lacoste scraping"""

        # product_name = response.css('h1.title--medium.l-vmargin--medium.padding-m-1::text').get()
        # imgs = response.xpath('//li//button[contains(@class, "js-slideshow-bullet slideshow-nav-item is-image")]//img/@data-src').getall()

        # for img in range(len(imgs)):
        #     web_scraper_order = f'{int(time.time_ns())}_{img}'
        #     web_scraper_start_url = self.url
        #     self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{imgs[img].split('?')[0]}\n")
        # self.file_.close

        """ioana ciolacu scraping"""

        # product_name = response.css('h1.product_title.entry-title::text').get()
        # imgs = response.css('div.jet-woo-product-gallery__image.jet-woo-product-gallery__image--with-zoom').css('img::attr(src)').getall()

        # for img in range(len(imgs)):
        #     web_scraper_order = f'{int(time.time_ns())}_{img}'
        #     web_scraper_start_url = self.url
        #     self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{imgs[img]}\n")
        # self.file_.close

        """gucci scraping"""
        # product_name = response.css('h1.product-name.product-detail-product-name::text').get()
        # # imgs = response.xpath('//img[@class="item-content product-detail-carousel-image zoom-item"]/@currentSrc').getall()
        # imgs = response.css('img.item-content::attr(srcset)').getall()
        
        # for it in imgs:
        #     print(it)
        #     web_scraper_order = it.split("/")[5]
        #     web_scraper_start_url = self.url
        #     img_url = it.replace('490x490', '2400x2400')
        #     self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{img_url}\n")
        # self.file_.close

        """guess scraping"""
        # product_name = response.xpath('//h1[@class="product-name"]/text()').get()
        # # imgs = response.xpath('//div[@class="css-b7jmoi"]//img[@width="509"]/@src').getall()

        """katespade scraping"""
        # product_name = response.xpath('//h1[@data-qa="product-name"]/text()').get()
        # imgs = response.css('img::attr(src)').getall()
        # item['imgs'] = imgs

        # for it in imgs[1:]:
        #     if "productThumbnail" in it:
        #         print(it)
        #         p1 = it.split("$")
        #         web_scraper_order = p1[0].split('/')[6][:-1]
        #         web_scraper_start_url = self.url
        #         img_url = f"{p1[0]}$s7fullsize$"
        #         self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{img_url}\n")
        # self.file_.close

        """burberry scraping"""
        # product_name = response.css('.product-info-panel__title').css('span::text').get()
        # imgs = response.css('img::attr(src)').getall()
        
        # item['imgs'] = imgs
        # for it in item['imgs']:
        #     if '.jpg' in it:
        #         print(f'https:{it}')
        #         web_scraper_order = it.split('/')[6].split('?')[0].split('.')[0]
        #         web_scraper_start_url = self.url
        #         self.file_.writelines(f"{web_scraper_order},{web_scraper_start_url},{self.category},{product_name},{it}\n")
        # self.file_.close

        """marcjacobs scraping"""

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