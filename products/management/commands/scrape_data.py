import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Scrapes product data from an e-commerce website'

    def handle(self, *args, **kwargs):
        base_url = "https://books.toscrape.com/catalogue/page-"
        for i in range(1, 13):  # Scrape 12 pages (200 products)
            url = f"{base_url}{i}.html"
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, 'lxml')

            products = soup.find_all("article", class_="product_pod")

            for product in products:
                img_tag = product.find("img", class_="thumbnail")
                if img_tag and img_tag.get("src"):
                    img_url = img_tag["src"]
                    img_url = f"https://books.toscrape.com/{img_url}"

                name = product.find("h3").find("a")["title"]
                price = product.find("p", class_="price_color").text
                rating = product.find("p", class_="star-rating")["class"][1]
                description = product.find("p", class_="instock availability").text.strip()

                product_instance = Product(
                    name=name,
                    price=price,
                    rating=rating,
                    description=description,
                    image_url=img_url
                )
                product_instance.save()
                self.stdout.write(f"Scraped and saved product: {name}")

        self.stdout.write(self.style.SUCCESS("Data scraped and saved successfully!"))
