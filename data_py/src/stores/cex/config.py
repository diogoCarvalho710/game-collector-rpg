from libraries import *


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
    driver = webdriver.Firefox(service=service, options=options)
    print("Config Setup!")
    print("returned", "setup_driver")
    return driver, WebDriverWait(driver, 25)
