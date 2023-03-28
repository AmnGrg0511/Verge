from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import dateparser
import csv
import sqlite3

url = 'https://www.theverge.com'


def get_articles():
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()

    # Navigate to a web page
    driver.get(url)

    # Parse the HTML using Beautiful Soup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the driver
    driver.quit()

    # Find all the links on the page
    links = soup.find_all('a')

    # Filter the links that follow the article link pattern
    articles = [x for (i, x) in enumerate(links)
                if i+1 < len(links)
                and '/author' not in links[i].get('href')
                and '/author' in links[i+1].get('href')]

    return articles


# Extract required fields from article element
def extract_data(article):
    title = str(article.string)
    if title == 'None':
        title = article.get('aria-label')

    link = url + article.get('href')

    # Find all links in parent element
    ele = article.parent
    if len(ele.find_all('a')) == 1:
        ele = article.parent.parent

    # Filter links following author like pattern
    authors = ' and '.join([str(x.string) for x in ele.find_all('a')
                            if '/author' in x.get('href')])

    # Filter <span> elements following date like pattern
    date = [str(x.string) for x in ele.find_all('span')
            if re.search(r'\d\d', str(x.string)) or 'ago' in str(x.string)][0]

    # parse the string like 'two hours ago' to a datetime object
    date = dateparser.parse(date)

    return (title, link, authors, date)


# Insert data in database and write in csv
def insert_data(title, link, authors, date):
    try:
        cursor.execute(
            "INSERT INTO articles ('title', 'link', 'authors', 'date') VALUES (?, ?, ?, ?)",
            (title, link, authors, date))
        # Write the data rows in csv
        writer.writerow({'id': cursor.lastrowid,
                         'link': link,
                         'title': title,
                         'authors': authors,
                         'date': date.strftime('%Y/%m/%d')})
    except sqlite3.IntegrityError:
        print("Row already added to the database.")


filename = datetime.today().strftime('%d%m%Y')+'_verge.csv'

# Open the CSV file in write mode
with open(filename, 'a', newline='') as f:
    # Create a writer object
    writer = csv.DictWriter(
        f, fieldnames=['id', 'link', 'title', 'authors', 'date'])

    # Connect to the database (create a new database if it doesn't exist)
    conn = sqlite3.connect('verge.db')
    # Create a cursor object
    cursor = conn.cursor()
    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                (id INTEGER PRIMARY KEY, title TEXT, link TEXT UNIQUE, authors TEXT, date DATE)''')

    articles = get_articles()

    # Loop through each article
    for article in articles:
        data = extract_data(article)
        insert_data(*data)

    # Commit the changes
    conn.commit()
    # Close the cursor and the connection
    cursor.close()
    conn.close()
