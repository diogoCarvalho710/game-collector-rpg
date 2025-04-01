# Import from libraries.py
from libraries import *

# Import functionality from other modules
from config import setup_driver
from landing_page import get_navigation_bar
from console_games_select_page import parse_grid_elements


def main():
    # Setup
    driver, wait = setup_driver()

    ### Page to Scrap + BS4 Setup
    url = "https://pt.webuy.com/"
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    ######### Home Page:
    ## Home Page: Allows to Wait for Elements to Load

    # Get navigation bar
    dictNavigationBar = get_navigation_bar(driver, wait)

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
    # ex: {3DS:{"title":"3DS","url":"url",elementName:"parecido ao nav-link-2",category:"games"}}

    # Parse grid elements
    href = dictNavigationBar["Jogos"]["url"]
    dictGridOptions = parse_grid_elements(driver, wait, href)

    print(dictGridOptions)

    # #### 2º
    # Os titles que interessam são os que têm "jogos" mas não "acessórios"
    #

    driver.quit()
####

if __name__ == "__main__":
    main()
