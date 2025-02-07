from selenium import webdriver
from selenium.webdriver.edge.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-renderer-backgrounding")
options.add_argument("--disable-background-timer-throttling")
options.add_argument("--disable-backgrounding-occluded-windows")

driver = webdriver.Edge(options=options)

# Truy cập một trang web
driver.get("https://example.com")
print(driver.title)

# Đóng trình duyệt
driver.quit()

