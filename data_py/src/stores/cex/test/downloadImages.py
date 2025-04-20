import requests
import os
from selenium import webdriver


# Method 1: Use requests library (doesn't require Selenium but works alongside it)
def download_image_requests(url, save_directory):
    # Extract filename from URL
    filename = url.split("/")[-1]

    # Create full path including filename
    save_path = os.path.join(save_directory, filename)

    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Image saved to {save_path}")
        return True
    else:
        print(f"Failed to download image: {response.status_code}")
        return False


download_image_requests(
    "https://pt.static.webuy.com/product_images/Jogos/3DS%20Jogos/0045496524326_l.jpg",
    "/home/diogo/projects/game-collector-rpg/data_py/src/stores/cex/test",
)
