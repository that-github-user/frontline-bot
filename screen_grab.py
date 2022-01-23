from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from PIL import Image
from io import BytesIO

# To work:
# conda install -c conda-forge selenium firefox geckodriver pillow

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0")
options.add_argument("--headless")  # open Browser in maximized mode
options.add_argument("window-size=1400,600")
options.add_argument("--hide-scrollbars")
options.add_argument("--disable-extensions")  # disabling extensions
options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
options.add_argument("--no-sandbox")  # Bypass OS security model
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.set_page_load_timeout(10)
driver.get('<your url>')
driver.execute_script("window.scrollTo(0, 530)")

png = driver.get_screenshot_as_png()  # saves screenshot of entire page
driver.quit()

im = Image.open(BytesIO(png))  # uses PIL library to open image in memory

im = im.crop((204, 0, 1194, 280)) # defines crop points
im.save('screenshot.png')  # saves new cropped image

