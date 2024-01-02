from bs4 import BeautifulSoup
import requests


class BookScraper:
    # Initialize the class with the URL
    def __init__(self, base_url):
        self.base_url = base_url

    def get_soup(self, url):
        response = requests.get(url)  # HTTP request to the given URL
        soup = BeautifulSoup(response.content, 'html.parser') # Parse the HTML content of the page
        return soup
    
    # Method to find the link of a specific category based on input
    def get_category_link(self, category_name):
        soup = self.get_soup(self.base_url)
        categories_ul = soup.find('ul', class_='nav-list').find_all('li')[1:]  # Skip the first 'Books' category)
        for category in categories_ul: 
            if category_name.lower() == category.get_text(strip=True).lower():  # Matching user input
                return category.find('a')['href']
            return None
        
    # Get the book from specific category
    def get_books_from_category(self, category_link):
        full_url = f'{self.base_url}{category_link}'
        soup = self.get_soup(full_url)
        books_data = []  # List to hold book data 

        products = soup.find_all('article', class_='product_pod') # Find all book entries on the page

        for product in products: 
            title = product.find('h3').find('a')['title'] # book title
            price = product.find('p', class_='price_color').text # book price
            availability = product.find('p', class_='instock availability').get_text(strip=True) # Availability
            books_data.append({'title': title, 'price': price, 'availability': availability}) # Append the book data to the list
        return books_data 
    
    # Method to run the entire scraper
    def run_scraper(self):
        user_search = input("Enter Category: ").strip()  # Prompt the user for a category
        category_link = self.get_category_link(user_search)  # Get the link to the user-specified category

        if category_link:  # Check if a valid category link was found
            books = self.get_books_from_category(category_link)  # Get books from the category
            print(f"Books in the '{user_search}' category:")  # Print the category name
            for book in books:  # Iterate through each book
                print(f"{book['title']} - {book['price']} - {book['availability']}")  # Print book details
        else:
            print("Category not found.")  # Notify the user if the category was not found

# Main script
scraper = BookScraper('https://books.toscrape.com/')  # Create an instance of the BookScraper with the base URL
scraper.run_scraper()  # Run the scraper


    







