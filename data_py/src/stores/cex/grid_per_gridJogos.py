from libraries import *


def gridPerGridElement(driver, wait, gridDict):
    dictGridPerGridElement = dict()
    listUniqueHrefs = []

    for key in gridDict:
        time.sleep(5)
        listIds = []
        url = gridDict[key]["url"]
        driver.get(url)

        elementGridJogos = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[href*='search?categoryIds=']")
            )
        )

        gridElements = driver.find_elements(
            By.CSS_SELECTOR, "a[href*='search?categoryIds=']"
        )

        def idGenerator(fatherId):
            separator = 0

            if len(listIds) == 0:
                id = 1
            else:
                id = max(listIds) + 1

            result = int(f"{fatherId}{separator}{id}")
            listIds.append(id)
            return result

        for element in gridElements:
            time.sleep(2)
            href = element.get_attribute("href")

            if href not in listUniqueHrefs:
                imageGrid = element.find_element(By.TAG_NAME, "img")
                imgGrid = imageGrid.get_attribute("src")
                titleGrid = imageGrid.get_attribute("alt")
                listUniqueHrefs.append(href)

                dictGridPerGridElement[titleGrid] = {
                    "id": idGenerator(gridDict[key]["id"]),
                    "fatherId": gridDict[key]["id"],
                    "title": titleGrid,
                    "url": href,
                    "image": imgGrid,
                    "hub_consola": (
                        True
                        if "Jogos" not in titleGrid and "Consolas" not in titleGrid
                        else False
                    ),
                    "hub_acessorios": True if "Acessórios" in titleGrid else False,
                    "hub_jogos": (
                        True
                        if "Jogos" in titleGrid and "Acessórios" not in titleGrid
                        else False
                    ),
                }

    return dictGridPerGridElement
