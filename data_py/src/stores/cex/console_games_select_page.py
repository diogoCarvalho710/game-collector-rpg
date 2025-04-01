# Import from libraries.py
from libraries import *


def parse_grid_elements(driver, wait, href):
    ## Find Options Grid
    elementGridJogos = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a[href*='search?productLineId=']")
        )
    )
    gridElements = driver.find_elements(
        By.CSS_SELECTOR, "a[href*='search?productLineId=']"
    )

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
    print("returned", "parse_grid_elements")
    return dictGridOptions
