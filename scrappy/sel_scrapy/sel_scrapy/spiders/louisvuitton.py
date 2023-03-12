import time
import scrapy
from scrapy.utils.project import get_project_settings
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from sel_scrapy.items import Item


class LouisVuittonSpider(scrapy.Spider):
    name = 'louisvuitton'

    def __init__(self, category=None, url=None, *args, **kwargs):
        super(LouisVuittonSpider, self).__init__(*args, **kwargs)

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
        link_polos_tshirts = [
            "https://eu.louisvuitton.com/eng-e1/products/lv-house-printed-t-shirt-nvprod3950026v/1AARP4",
            "https://eu.louisvuitton.com/eng-e1/products/monogram-gradient-t-shirt-nvprod2550079v/1AATQN",
            "https://eu.louisvuitton.com/eng-e1/products/lv-frequency-graphic-t-shirt-nvprod3950027v/1AAU5D",
            "https://eu.louisvuitton.com/eng-e1/products/signature-polo-with-embroidery-nvprod3570124v/1AATRH",
            "https://eu.louisvuitton.com/eng-e1/products/louis-vuitton-vintage-cycling-polo-nvprod3760074v/1AAGMZ",
            "https://eu.louisvuitton.com/eng-e1/products/louis-vuitton-signature-print-t-shirt-nvprod3760125v/1AAGMD",
            "https://eu.louisvuitton.com/eng-e1/products/lv-flower-tapestry-print-t-shirt-nvprod3760136v/1AAGWO",
            "https://eu.louisvuitton.com/eng-e1/products/graphic-sporty-long-sleeved-t-shirt-nvprod3760119v/1AAGMT",
            "https://eu.louisvuitton.com/eng-e1/products/lv-graphic-mesh-long-sleeved-t-shirt-nvprod3760123v/1AAGP1",
            "https://eu.louisvuitton.com/eng-e1/products/signature-lv-knit-t-shirt-nvprod3760077v/1AAGLP",
            "https://eu.louisvuitton.com/eng-e1/products/tie-dye-t-shirt-nvprod3760131v/1AAGQ7",
            "https://eu.louisvuitton.com/eng-e1/products/lv-monogram-t-shirt-nvprod3760124v/1AAGM5",
            "https://eu.louisvuitton.com/eng-e1/products/lv-1854-graphic-knit-t-shirt-nvprod3760082v/1AAGO4",
            "https://eu.louisvuitton.com/eng-e1/products/courbet-painting-printed-t-shirt-nvprod3760118v/1AAGOL",
            "https://eu.louisvuitton.com/eng-e1/products/monogram-bandana-printed-t-shirt-nvprod3570115v/1AA5F4",
            "https://eu.louisvuitton.com/eng-e1/products/3d-lv-graffiti-embroidered-t-shirt-nvprod3570114v/1AA54K",
            "https://eu.louisvuitton.com/eng-e1/products/embossed-lv-t-shirt-nvprod3570121v/1AA5E0",
            "https://eu.louisvuitton.com/eng-e1/products/classic-short-sleeves-pique-polo-009788/1AA4JD",
            "https://eu.louisvuitton.com/eng-e1/products/lvse-signature-3d-pocket-monogram-t-shirt-nvprod1780324v/1AA51T",
            "https://eu.louisvuitton.com/eng-e1/products/lvse-inside-out-t-shirt-nvprod1510035v/1AA51F",
            "https://eu.louisvuitton.com/eng-e1/products/lv-spread-embroidery-t-shirt-nvprod3570112v/1AA808",
            "https://eu.louisvuitton.com/eng-e1/products/lv-spread-embroidery-t-shirt-nvprod3570111v/1AA53Y",
            "https://eu.louisvuitton.com/eng-e1/products/legendary-trunks-t-shirt-nvprod3570103v/1AA4R1",
            "https://eu.louisvuitton.com/eng-e1/products/hand-crocheted-lv-pocket-t-shirt-nvprod3570107v/1AA4TA",
            "https://eu.louisvuitton.com/eng-e1/products/hockey-jersey-t-shirt-nvprod3410181v/1A9V74",
            "https://eu.louisvuitton.com/eng-e1/products/intarsia-football-t-shirt-nvprod3410151v/1A9TAX",
            "https://eu.louisvuitton.com/eng-e1/products/do-a-kickflip-t-shirt-nvprod3410150v/1A9TAP",
            "https://eu.louisvuitton.com/eng-e1/products/oval-printed-vuitton-t-shirt-nvprod3410149v/1A9TAH",
            "https://eu.louisvuitton.com/eng-e1/products/l-vuitton-printed-t-shirt-nvprod3410139v/1A9T6V",
            "https://eu.louisvuitton.com/eng-e1/products/vuitton-graffiti-t-shirt-nvprod3410138v/1A9T6N",
            "https://eu.louisvuitton.com/eng-e1/products/chunky-intarsia-football-t-shirt-nvprod3410111v/1A9SXG",
            "https://eu.louisvuitton.com/eng-e1/products/tiedye-t-shirt-with-lv-signature-nvprod3410109v/1A9SX1",
            "https://eu.louisvuitton.com/eng-e1/products/sporty-t-shirt-with-patch-nvprod3410106v/1A9SWD",
            "https://eu.louisvuitton.com/eng-e1/products/polo-with-lv-signature-nvprod3410104v/1A9SVX",
            "https://eu.louisvuitton.com/eng-e1/products/lv-2054-termo-print-tee-nvprod3210125v/1A9GPA",
            "https://eu.louisvuitton.com/eng-e1/products/printed-flower-drop-shoulders-tee-nvprod3210122v/1A9GP3",
            "https://eu.louisvuitton.com/eng-e1/products/intarsia-jacquard-duck-crewneck-nvprod3210100v/1A9GOM",
            "https://eu.louisvuitton.com/eng-e1/products/lv-2054-intarsia-printed-tee-nvprod3210126v/1A9GN3",
            "https://eu.louisvuitton.com/eng-e1/products/embroidered-louis-vuitton-mockneck-tee-nvprod3010019v/1A9GMO",
            "https://eu.louisvuitton.com/eng-e1/products/intarsia-jacquard-heart-crewneck-nvprod3210030v/1A9GM3",
            "https://eu.louisvuitton.com/eng-e1/products/lvse-inside-out-t-shirt-nvprod3130042v/1A9G7C",
            "https://eu.louisvuitton.com/eng-e1/products/embossed-lv-long-sleeve-t-shirt-nvprod2800030v/1A8ZNU",
            "https://eu.louisvuitton.com/eng-e1/products/embossed-lv-t-shirt-nvprod2800029v/1A8XFQ",
            "https://eu.louisvuitton.com/eng-e1/products/louis-vuitton-2054-technical-printed-half-zip-long-sleeved-top-nvprod2550068v/1A8H7F",
            "https://eu.louisvuitton.com/eng-e1/products/lv-planes-printed-tshirt-nvprod1790043v/1A7PZO",
            "https://eu.louisvuitton.com/eng-e1/products/lv-planes-printed-tshirt-nvprod1790044v/1A5WE4",
            "https://eu.louisvuitton.com/eng-e1/products/3d-pocket-mix-nylon-track-top-nvprod1790048v/1A5WBC",
            "https://eu.louisvuitton.com/eng-e1/products/monogram-3d-effect-print-packable-tshirt-nvprod1790045v/1A5W9W",
            "https://eu.louisvuitton.com/eng-e1/products/iridescent-half-zip-short-sleeve-polo-nvprod1270553v/1A4PW2",
            "https://eu.louisvuitton.com/eng-e1/products/fil-a-fil-polo-015260/1A3M0G",
            "https://eu.louisvuitton.com/eng-e1/products/damier-pocket-polo-013821/999286",
            "https://eu.louisvuitton.com/eng-e1/products/crew-neck-long-sleeve-t-shirt-013419/1A1PK8",
            "https://eu.louisvuitton.com/eng-e1/products/classic-tee-v-neck-013401/1A1PGC",
            "https://eu.louisvuitton.com/eng-e1/products/classic-long-sleeve-pique-polo-013399/1A1PIA",
            "https://eu.louisvuitton.com/eng-e1/products/half-damier-pocket-polo-nvprod2260014v/1A9G85",
            "https://eu.louisvuitton.com/eng-e1/products/half-damier-pocket-t-shirt-nvprod2260013v/1A9G7P",
            "https://eu.louisvuitton.com/eng-e1/products/classic-t-shirt-015262/1A9G67",
            "https://eu.louisvuitton.com/eng-e1/products/classic-damier-pique-polo-015186/1A47JL",
            "https://eu.louisvuitton.com/eng-e1/products/damier-pocket-crew-neck-013475/1A47IH"
        ]

        for url in link_polos_tshirts:
            try:
                self.driver.get(url)
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                name = self.driver.find_elements_by_xpath(
                    '//h1[@class="lv-product__name"]')[0].text
                # imgs = self.driver.find_elements_by_xpath('//img[@class="lv-smart-picture__object" and @sizes="(min-width: 64rem) 50vw,\n(min-width: 0rem) 100vw"]')
                imgs = self.driver.find_elements_by_xpath(
                    '//img')

                imgs_src = [img.get_attribute('srcset') for img in imgs]

                yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_louis_vuitton, meta={'url': url, 'name':name, 'imgs_src': imgs_src}, dont_filter=True)
            except:
                print(f'ERROR: Failed to get response from url {url}')

    def parse_louis_vuitton(self, response):
        item = Item()
        
        item['order'] = int(time.time_ns())
        item['link'] = response.meta['url']
        item['name'] = response.meta['name']
        item['category'] = self.category
        item['imgs_src'] = response.meta['imgs_src']

        return item
