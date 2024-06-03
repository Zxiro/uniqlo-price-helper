import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Create a new instance of the Chrome driver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(service=service, options=options)
headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
# Navigate to the Uniqlo website
url = "https://www.uniqlo.com/tw/zh_TW/c/SALE1003.html"
print("Start Getting")
driver.get(url)
print("Finished Getting")
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
print("HTML Parsered")
# Find the <a> tag with the class "product-herf"
# print(soup)
product_links = soup.findAll("a", class_="product-herf")
print("Exist: ", len(product_links), "Products")
# Extract the productCode from the href attribute
product_codes = []
# print(product_links)
for prod in product_links:
    print("Code: ", prod["href"].split("productCode=")[1][:14])
    product_codes.append(prod["href"].split("productCode=")[1])

# Construct the JSON URL
for code in product_codes:
    json_url = f"https://www.uniqlo.com/tw/data/products/prodInfo/zh_TW/{code}.json"
    # Send a GET request to the JSON URL
    response = requests.get(json_url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        json_data = response.json()

        # Process the JSON data as needed
        print("Full Data: ", json_data)
        print(f"Product Name: {json_data['fullName']}")
        print(f"Product Original Price: {json_data['originPrice']}")
        print(f"Product Minimum Price: {json_data['minPrice']}")
        # Access other product details as needed
    else:
        print(f"Failed to fetch JSON data. Status code: {response.status_code}")
    time.sleep(5)