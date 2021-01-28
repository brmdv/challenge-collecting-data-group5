# selenium
  
# import webdriver 
from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import requests

# import local modules
from property_structure import Property
from scrapers.immo_scraping import ImmoScraper, ImmoPropScraper, ImmoListScraper

url="https://www.immoweb.be/en"

# create webdriver object
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)

# When opening the url on Firefox, a pop-up window appears.
# Click on accept browsing
python_button = driver.find_elements_by_xpath("//button[@id='uc-btn-accept-banner']")[0]
python_button.click()


# The following line is a statement confirming that the title contains the word "Python"
# assert "Python" in driver.title
# WebDriver offers several methods to search for items using one of the methods 
# find_element_by_by_ * . For example, the input text element can be located by its name attribute by 
# using the find_element_by_name method 
# elem = driver.find_element_by_name("q")

# to search all houses and appartment, we have to
# 1. Make sure the "House and apartment label is selected"
python_label_button = driver.find_elements_by_xpath("//button[@id='propertyTypesDesktop']")[0]
python_label_button.click()
python_house_apartment_button = driver.find_elements_by_xpath("//li[@data-value='HOUSE,APARTMENT']")[0]
python_house_apartment_button.click()

# 2. click on search
python_search_button = driver.find_elements_by_xpath("//button[@id='searchBoxSubmitButton']")[0]
python_search_button.click()

# Now we have a page with a list of all houses and apartment (currently the search returns a 333 pages or more list)
links = driver.find_elements_by_xpath("//a[@class='card__title-link']")
links_list = [link.get_attribute('href') for link in links]
print(links_list)

# Now that we have the list of links to houses and apartment in a page, let's try to get all info of a property
# 1. instantiate an ImmoPropScraper object
first_property = ImmoPropScraper(links_list[0])
print(first_property)
# 2. wait a bit before browsing to the property url
driver.implicitly_wait(30)
driver.get(first_property.page_url)

# 3. Get property information in the url and fill the property with the information found
soup=BeautifulSoup(driver.page_source)
# soup=BeautifulSoup(driver.page_source, 'features="lxml"')

# Fill Locality information
# driver.find_elements_by_xpath("//th[contains(text(), 'locality')]")
# label = soup.find_all("th", text="Neighbourhood or locality")
label = soup.select_one('th:-soup-contains("locality")')
first_property._property.locality = label.next_sibling.next_sibling.text.strip()

# Fill property_type information
if 'house' in driver.title.lower():
    first_property._property.property_type = 'house'
elif 'apartment' in driver.title.lower():
    first_property._property.property_type = 'apartment'


print(first_property.format_to_csv())

# for elem in soup.find_all('tr',attrs={"data-qa-id" :"adview_number_phone_contact" }):
#     print(elem.text)




# driver.close()




# soup=BeautifulSoup(driver.page_source)
# 

# # And then it's like Beautiful soup
# for elem in soup.find_all('a',attrs={"data-qa-id" :"adview_number_phone_contact" }):
#     print(elem.text)

# # clear search bar, search for "selenium" and press Return
# elem.clear()
# elem.send_keys("selenium")
# elem.send_keys(Keys.RETURN)

# # And then it's like Beautiful soup
# soup=BeautifulSoup(driver.page_source)

# driver.close()

# # get elements 
# elem = driver.find_elements_by_xpath("//input[@id ='autocomplete-input-fb0f26dc-eb25-412b-a665-0d40f6b9bb08']")
# print(elem)

# # And then it's like Beautiful soup
# for elem in soup.find_all('input',attrs={"name" :"search" }):
#     print(elem)



csv_header = [attr for attr in Property.__dict__.keys() if not attr.startswith('_') and not callable(getattr(Property, attr))]