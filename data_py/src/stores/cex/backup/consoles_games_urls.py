from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


####### Setup:
print("Process has started!")

### Firefox Cookies CeX Profile:
firefox_profile_path = os.path.expanduser(
    "/home/diogo/projects/game-collector-rpg/data_py/src/stores/cex/config/1ai0mpgq.default"
)
firefox_profile = FirefoxProfile(firefox_profile_path)

### Selenium Firefox
service = Service(executable_path="/snap/bin/geckodriver")
options = Options()
options.add_argument("-headless")
options.profile = firefox_profile
driver = webdriver.Firefox(service=service, options=options)

### Page to Scrap + BS4 Setup
url = "https://pt.webuy.com/"
driver.get(url)
soup = BeautifulSoup(driver.page_source, "html.parser")


######### Home Page:

## Home Page: Allows to Wait for Elements to Load
wait = WebDriverWait(driver, 10)

## Home Page: Navigation Bar Options -- Exemplo: {"Jogos":"url"}
elementNavBarHP = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "nav-menu"))
)

navmenuFatherUL = driver.find_element(By.CLASS_NAME, "nav-menu")
navmenuChildrenLI = navmenuFatherUL.find_elements(By.TAG_NAME, "li")

## Home Page: Navigation Bar - Dictionary
dictNavigationBar = dict()

for li in navmenuChildrenLI:
    aTag = li.find_element(By.TAG_NAME, "A")
    href = aTag.get_attribute("href")
    spanText = aTag.find_element(By.TAG_NAME, "span").text
    elementName = li.get_attribute("class")

    dictNavigationBar[spanText] = {
        "title": spanText,
        "url": href,
        "elementName": elementName,
    }

## Home Page End: Move to "Jogos Tab"
driver.get(dictNavigationBar["Jogos"]["url"])


##### "Jogos Tab"
# Jogos Software -> por cada elemento X jogos fazer -> ... ||jogos
# Jogos Retro -> por cada elemento X jogos fazer -> ... ||jogos
# PC Jogos -> por cada elemento X jogos fazer -> ... ||jogos
# Jogos Consolas por cada elemento X jogos fazer -> ... ||consolas
#
# #### 1º
# Fazer parecido ao dictNavigationBar:
#  ex: {3DS:{"title":"3DS","url":"url",elementName:"parecido ao nav-link-2",category:"games"}}

## Find Options Grid


elementGridJogos = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a[href*='search?productLineId=']")
    )
)
gridElements = driver.find_elements(By.CSS_SELECTOR, "a[href*='search?productLineId=']")

listHrefsGrid = []
dictGridOptions = dict()

for element in gridElements:
    hrefGrid = element.get_attribute("href")

    productLine = hrefGrid.replace("%20", "")[
        (href.find("productLineName=") + len("productLineName=")) :
    ]

    if productLine not in listHrefsGrid:
        imageGrid = element.find_element(By.TAG_NAME, "img")
        imgGrid = imageGrid.get_attribute("src")
        titleGrid = imageGrid.get_attribute("alt")
        listHrefsGrid.append(productLine)

        dictGridOptions[titleGrid] = {
            "title": titleGrid,
            "url": hrefGrid,
            "image": imgGrid,
            "hub_consola": (
                True
                if "Jogos" not in titleGrid and "Consolas" not in titleGrid
                else False
            ),
            "hub_acessorios": True if "Acessórios" in titleGrid else False,
            "hub_jogos": (
                True
                if "Jogos" in titleGrid
                and "Consolas" not in titleGrid
                and "Acessórios" not in titleGrid
                else False
            ),
        }

    else:
        continue

print(dictGridOptions)
driver.quit()

# #### 2º
# Os titles que interessam são os que têm "jogos" mas não "acessórios"
#
