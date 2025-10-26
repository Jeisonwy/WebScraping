import undetected_chromedriver as uc

def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    return uc.Chrome(options=options)
