from urllib.parse import urlparse, parse_qs, unquote, urljoin
import requests
from bs4 import BeautifulSoup

baseUrl = "https://shop.kimelo.com"
url = "https://shop.kimelo.com/department/cheese/3365"
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")
# first find all job listing boxes:
results = soup.select("a.chakra-card.group.css-5pmr4x")
# then extract listing from each box:
for item in results:
    href = item["href"]
    sku = href.split("/")[-1]

    showImage = item.select_one("img")["srcset"]
    showImage = parse_qs(urlparse(showImage.split(" ")[0]).query)
    showImage = unquote(showImage['url'][0])

    res = requests.get(urljoin(baseUrl, href))
    with open("html/{}.html".format(sku), "wb") as f:
        f.write(res.content)
        f.close()
    childSoup = BeautifulSoup(res.text, "lxml")
    name = childSoup.select("h1.chakra-heading.css-18j379d")

    print(sku, showImage, len(name))
