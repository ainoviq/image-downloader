from selenium.webdriver import Chrome

driver_path = './driver/chromedriver_linux64/chromedriver'

driver = Chrome(executable_path=driver_path)
driver.get('https://www.ralphlauren.com/men-clothing-hoodies-sweatshirts?ab=en_US_MDLP_Slot_2_S1_L1_SHOP')

xpath='//div[contains(@class, "product-tile")]//a[contains(@class, "name-link")]'
link_elements = driver.find_elements_by_xpath(xpath)
links = []

for link_el in link_elements:
    href = link_el.get_attribute("href")
    print(href)
    links.append(href)

driver.quit()