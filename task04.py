import requests
import csv
from bs4 import BeautifulSoup

# Website URLs
HEADLINES_URL = "https://news.ycombinator.com/"
QUOTES_URL = "https://quotes.toscrape.com/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Function to scrape headlines
def scrape_headlines():

    print("\n========== NEWS HEADLINES ==========")

    try:
        response = requests.get(
            HEADLINES_URL,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        headlines = []

        for item in soup.select("tr.athing")[:10]:

            title_tag = item.select_one(".titleline > a")

            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.get("href", "")

                headlines.append({
                    "Title": title,
                    "Link": link
                })

        for i, news in enumerate(headlines, start=1):
            print(f"\n{i}. {news['Title']}")
            print("Link:", news["Link"])

        return headlines

    except requests.RequestException as error:
        print("Error fetching headlines:", error)
        return []


# Function to scrape quotes
def scrape_quotes():

    print("\n========== FAMOUS QUOTES ==========")

    try:
        response = requests.get(
            QUOTES_URL,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        quotes = []

        for item in soup.select(".quote")[:10]:

            quote_text = item.select_one(".text")
            author = item.select_one(".author")

            if quote_text and author:

                quotes.append({
                    "Quote": quote_text.get_text(strip=True),
                    "Author": author.get_text(strip=True)
                })

        for i, quote in enumerate(quotes, start=1):
            print(f"\n{i}. {quote['Quote']}")
            print("Author:", quote["Author"])

        return quotes

    except requests.RequestException as error:
        print("Error fetching quotes:", error)
        return []


# Function to save headlines in CSV
def save_headlines(data):

    with open("headlines.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["Title", "Link"]
        )

        writer.writeheader()
        writer.writerows(data)

    print("\nHeadlines saved in headlines.csv")


# Function to save quotes in CSV
def save_quotes(data):

    with open("quotes.csv", "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["Quote", "Author"]
        )

        writer.writeheader()
        writer.writerows(data)

    print("\nQuotes saved in quotes.csv")


# Main menu
while True:

    print("\n================================")
    print("       WEB SCRAPER PROJECT")
    print("================================")
    print("1. Scrape News Headlines")
    print("2. Scrape Famous Quotes")
    print("3. Scrape Both")
    print("4. Exit")

    choice = input("\nEnter your choice (1-4): ")

    if choice == "1":

        headlines = scrape_headlines()

        if headlines:
            save_headlines(headlines)

    elif choice == "2":

        quotes = scrape_quotes()

        if quotes:
            save_quotes(quotes)

    elif choice == "3":

        headlines = scrape_headlines()
        quotes = scrape_quotes()

        if headlines:
            save_headlines(headlines)

        if quotes:
            save_quotes(quotes)

    elif choice == "4":

        print("\nThank you for using Web Scraper!")
        break

    else:

        print("\nInvalid choice! Please select 1-4.")