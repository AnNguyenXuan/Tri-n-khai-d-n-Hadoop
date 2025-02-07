import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

def initialize_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

def close_driver(driver):
    driver.quit()

def save_image(image_url, folder_name, image_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        image_path = os.path.join(folder_name, image_name)
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Saved image: {image_path}")
    else:
        print(f"Failed to download image: {image_url}")

def get_category_links(driver, url):
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    categories = soup.find_all('li', class_='navi1 has-sub nav-level0')
    category_links = []
    
    for category in categories:
        link_tag = category.find('a')
        if link_tag and 'href' in link_tag.attrs:
            link = link_tag['href']
            category_links.append(link)
    
    return category_links

def crawl_product_links(driver, category_url):
    driver.get(category_url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    products = soup.find_all('div', class_='product-block product-resize fixheight')
    product_links = []
    
    for product in products:
        link_tag = product.find('a', href=True)
        if link_tag:
            link = link_tag['href']
            product_links.append(link)
    
    return product_links

def crawl_product_details(driver, product_url, category_name, output_folder):
    driver.get(product_url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    image_tag = soup.find('li', class_='product-gallery-item')
    image_url = image_tag.find('img')['src'] if image_tag else None
    if image_url:
        full_image_url = f"https:{image_url}"
        save_image(full_image_url, os.path.join(output_folder, category_name), "main_image.jpg")

    title_tag = soup.find('h1')
    price_tag = soup.find('span', class_='pro-price')
    description_tag = soup.find('div', class_='description-productdetail')

    title = title_tag.text.strip() if title_tag else "N/A"
    price = price_tag.text.strip() if price_tag else "N/A"
    description = description_tag.text.strip() if description_tag else "N/A"

    # Lưu thông tin vào file JSON
    product_data = {
        "title": title,
        "price": price,
        "description": description,
        "image_url": full_image_url if image_url else "N/A",
        "product_url": product_url
    }
    json_data = json.dumps(product_data, ensure_ascii=False, indent=4)
    output_file = os.path.join(output_folder, f"{category_name}.txt")
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(json_data + "\n")
    print(f"Saved product details for: {title}")

# Hàm chính để crawl toàn bộ dữ liệu
def main():
    base_url = "https://kenta.vn"
    output_folder = "products"  # Thư mục lưu trữ dữ liệu
    driver = initialize_driver()
    
    try:
        category_links = get_category_links(driver, base_url)

        for category_link in category_links:
            category_name = category_link.split("/")[-1]  # Lấy tên danh mục từ URL
            full_category_url = f"{base_url}{category_link}"
            print(f"Crawling category: {full_category_url}")
            
            # Lấy danh sách sản phẩm từ danh mục
            product_links = crawl_product_links(driver, full_category_url)
            
            # Duyệt qua từng sản phẩm và crawl thông tin chi tiết
            for product_link in product_links:
                full_product_url = f"{base_url}{product_link}"
                crawl_product_details(driver, full_product_url, category_name, output_folder)
    finally:
        close_driver(driver)

if __name__ == "__main__":
    main()
