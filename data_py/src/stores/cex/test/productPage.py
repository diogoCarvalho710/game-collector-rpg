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
from urllib.parse import quote, unquote
import re


def setup_driver():
    ### Firefox Cookies CeX Profile:
    firefox_profile_path = os.path.expanduser(
        "/home/diogo/projects/game-collector-rpg/data_py/src/stores/cex/config/1ai0mpgq.default"
    )
    firefox_profile = FirefoxProfile(firefox_profile_path)

    ### Selenium Firefox
    service = Service(executable_path="/snap/bin/geckodriver")
    options = Options()
    # options.add_argument("-headless")
    options.profile = firefox_profile

    # Block location access requests
    firefox_profile.set_preference("geo.enabled", False)
    firefox_profile.set_preference("geo.provider.use_corelocation", False)
    firefox_profile.set_preference("geo.prompt.testing", False)
    firefox_profile.set_preference("geo.prompt.testing.allow", False)

    driver = webdriver.Firefox(service=service, options=options)
    print("Config Setup!")
    print("returned", "setup_driver")
    return driver, WebDriverWait(driver, 25)


driver, wait = setup_driver()

url = "https://pt.webuy.com/product-detail?id=0045496524326&categoryName=3DS-JOGOS&superCatName=JOGOS&title=&queryID=1B446FB1B8EB30672827C1D54262BF61&position=1"
noStockUrl = "https://pt.webuy.com/product-detail?id=045496472344&categoryName=3DS-JOGOS&superCatName=JOGOS&title=&queryID=43CC2BD5BE491E095D5606083D26D02B&position=1"

driver.get(url)
time.sleep(5)


def cssSelectorReplacer(string):
    return "." + string.strip().replace(" ", ".")


def getProductImage():
    time.sleep(10)
    tag = driver.find_element(
        By.CSS_SELECTOR,
        ".product-gallery-image",
    )
    imgTag = tag.find_element(By.TAG_NAME, "img")
    imgUrl = imgTag.get_attribute("src")
    print(imgUrl)
    return imgUrl


def getProductPrices():
    # tag = driver.find_element(By.CSS_SELECTOR, ".d-flex.flex-wrap.w-100")

    tag = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".d-flex.flex-wrap.w-100"))
    )

    buyPrice = 0
    sellVoucherPrice = 0
    sellCashPrice = 0

    # Get Buy Price
    buySpan = tag.find_element(By.TAG_NAME, "span")
    if re.search(r"\d", buySpan.text):
        buyPrice = buySpan.text
    else:
        buyPrice = "error"

    # Get Sell Prices
    pTags = tag.find_elements(By.TAG_NAME, "p")
    for p in pTags:
        spans = p.find_elements(By.TAG_NAME, "span")
        for span in spans:
            if re.search(r"\d", span.text):
                if sellVoucherPrice == 0:
                    sellVoucherPrice = span.text
                elif sellVoucherPrice != 0 and sellCashPrice == 0:
                    sellCashPrice = span.text
                else:
                    continue
    print(buyPrice, sellVoucherPrice, sellCashPrice)
    return buyPrice, sellVoucherPrice, sellCashPrice


def getProductNameAndProductCategory():
    tag = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                cssSelectorReplacer("heading-block order-2 md-order-1 mb-l md-mb-m"),
            )
        )
    )

    # Product Category
    span = tag.find_element(By.TAG_NAME, "span")
    productCategory = span.text
    # Product Name
    h1 = tag.find_element(By.TAG_NAME, "h1")
    productName = h1.text

    return productCategory, productName


def getProductStock():
    tag = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                cssSelectorReplacer("row mb-m"),
            )
        )
    )
    time.sleep(5)

    outOfStock = tag.find_elements(
        By.CSS_SELECTOR,
        cssSelectorReplacer(
            "col-12 md-col-6 d-flex align-items-center pr-xs mb-m md-mb-0 feedback-error-500-color"
        ),
    )

    inStock = tag.find_elements(
        By.CSS_SELECTOR,
        cssSelectorReplacer(
            "col-12 md-col-6 d-flex align-items-center pr-xs mb-m md-mb-0"
        ),
    )

    if len(outOfStock) > 0 and len(inStock) == 0:
        # Return variable Out of Stock = True
        return False
    elif len(inStock) > 0 and len(outOfStock) == 0:
        return True
    else:
        # Gerar Erro
        x = 1


def getStoresStock():
    time.sleep(3)
    tag = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                cssSelectorReplacer(
                    "text-sm md-text-base font-semibold grey-1000-color cx-link cursor-pointer"
                ),
            )
        )
    )
    tag.click()
    see_all_stores_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(.,'Ver em todas as lojas')]")
        )
    )
    see_all_stores_button.click()
    time.sleep(3)
    storesList = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "store-list"))
    )
    stores = storesList.find_elements(By.CLASS_NAME, "store-card")

    # Create the main dictionary to store all store information
    dictionary = {}

    for store in stores:
        # Nome
        storeName = (store.find_element(By.TAG_NAME, "span")).text
        print(storeName)

        # Stock
        stock_div = store.find_element(
            By.CSS_SELECTOR, cssSelectorReplacer("text-sm mb-xs")
        )
        # Get the complete text
        full_text = stock_div.text  # This will be something like "1 Em stock"
        # Use regex to extract only the number
        stockNumber = re.search(r"(\d+)", full_text)
        if stockNumber:
            stockNumber = full_text.split(" ", 1)[0]
            stockNumber = int(stockNumber)
        else:
            stockNumber = "0"
        print(stockNumber)

        # Click and Collect || True or False
        collect_in_store = "False"
        if (
            len(
                store.find_elements(
                    By.CSS_SELECTOR,
                    cssSelectorReplacer(
                        "store-click-collect d-flex align-items-center mb-xs"
                    ),
                )
            )
            > 0
        ):
            # Need to check if it's available or unavailable
            if (
                len(
                    store.find_elements(
                        By.CSS_SELECTOR,
                        cssSelectorReplacer(
                            "store-click-collect d-flex align-items-center mb-xs feedback-error-500-color"
                        ),
                    )
                )
                > 0
            ):
                print("No Click")
            else:
                print("Click")
                collect_in_store = "True"
        else:
            print("No Click & Collect information found")

        # Add this store's info to the main dictionary
        dictionary[storeName] = {
            "store name": storeName,
            "stock": str(stockNumber),
            "collect in store": collect_in_store,
        }

    return dictionary


def productData():
    imagePath = getProductImage()
    buyPrice, sellVoucherPrice, sellCashPrice = getProductPrices()
    productCategory, productName = getProductNameAndProductCategory()
    inStock = getProductStock()
    dictStoresStock = getStoresStock()
    print("Image Path: ", imagePath)
    print("Image Prices: ", buyPrice, sellVoucherPrice, sellCashPrice)
    print("Product: ", productCategory, productName)
    print("In Stock: ", inStock)
    print("Stores Dict: ", dictStoresStock)


productData()
