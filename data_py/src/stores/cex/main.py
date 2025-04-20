# Import from libraries.py
from libraries import *

# Import functionality from other modules
from config import setup_driver
from landing_page import get_navigation_bar
from console_games_select_page import parse_grid_elements
from grid_per_gridJogos import gridPerGridElement
from get_products import getProducts


def main():
    ######### Setup:
    ## Driver + Wait on Elements
    driver, wait = setup_driver()

    ### Page to Scrap + BS4 Setup
    url = "https://pt.webuy.com/"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    ######### Home Page:
    ## Get navigation bar
    dictNavigationBar = get_navigation_bar(driver, wait)

    ## Home Page End: Move to "Jogos Tab"
    driver.get(dictNavigationBar["Jogos"]["url"])

    ######### Jogos Navigation Menu:
    ## Get Grid Elements
    jogosUrl = dictNavigationBar["Jogos"]["url"]
    dictGridOptions = parse_grid_elements(driver, wait, jogosUrl)

    ## Get Grid per Grid Element
    dictGridPerGridEleement = gridPerGridElement(driver, wait, dictGridOptions)
    # print(dictGridPerGridEleement)

    dictProductPerGridElement = getProducts(driver, wait, dictGridPerGridEleement)
    driver.quit()


####
if __name__ == "__main__":
    main()
