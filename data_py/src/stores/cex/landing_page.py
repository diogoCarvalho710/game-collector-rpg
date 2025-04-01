from libraries import *


def get_navigation_bar(driver, wait):

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
    print("returned", "dictNavigationBar")
    return dictNavigationBar
