dict1 = {
    "3DS Acessórios": {
        "id": 101,
        "fatherId": 1,
        "title": "3DS Acessórios",
        "url": "https://pt.webuy.com/search?categoryIds=975&categoryName=3DS%20Acess%C3%B3rios",
        "image": "https://pt.static.webuy.com/images/category/3ds-acess%C3%B3rios.jpg",
        "hub_consola": True,
        "hub_acessorios": True,
        "hub_jogos": False,
    },
    "3DS Consolas": {
        "id": 102,
        "fatherId": 1,
        "title": "3DS Consolas",
        "url": "https://pt.webuy.com/search?categoryIds=976&categoryName=3DS%20Consolas",
        "image": "https://pt.static.webuy.com/images/category/3ds-consolas.jpg",
        "hub_consola": False,
        "hub_acessorios": False,
        "hub_jogos": False,
    },
}


for element in dict1:
    print(element["url"])
