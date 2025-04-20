from libraries import *
from config import setup_driver

driver, wait = setup_driver()
gridElementPerGrid = dict()


def getProducts(driver, wait, gridElementPerGrid):
    dicProducts = dict()

    testDict = {
        "3DS Acessórios": {
            "id": 101,
            "fatherId": 1,
            "title": "3DS Acessórios",
            "url": "https://pt.webuy.com/search?categoryIds=975&categoryName=3DS%20Acess%C3%B3rios",
            "image": "https://pt.static.webuy.com/images/category/3ds-acess%C3%B3rios.jpg",
            "hub_consola": True,
            "hub_acessorios": True,
            "hub_jogos": False,
        }
    }

    # for element in gridElementPerGrid:
    for element in testDict:

        # Enter each Element Page
        time.sleep(3)
        urlElement = testDict[element]["url"]
        driver.get(urlElement)
        time.sleep(10)

        # Find each listing
        mainDiv = driver.find_elements(By.CLASS_NAME, "search-product-card")

        for product in mainDiv:
            # prd = product.find_element(By.TAG_NAME, "a")
            # href = prd.get_attribute("href")
            # print("--->", href)

            productUrl = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            driver.get(productUrl)


getProducts(driver, wait, gridElementPerGrid)
