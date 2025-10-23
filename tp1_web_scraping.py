import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

def scrape_goodreads_books():
    
    list_url = "https://www.goodreads.com/list/show/1.Best_Books_Ever"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    books_data = []
    page_num = 1
    
    while len(books_data) < 1000:
        if page_num == 1:
            current_url = list_url
        else:
            current_url = f"{list_url}?page={page_num}"
        
        response = requests.get(current_url, headers=headers)
        if response.status_code != 200:
            break
            
        soup = BeautifulSoup(response.content, 'html.parser')
        book_elements = soup.find_all('tr', itemtype='http://schema.org/Book')
        
        if not book_elements:
            break
        
        for book in book_elements:
            if len(books_data) >= 1000:
                break
            
            try:
                title_element = book.find('a', class_='bookTitle')
                title = title_element.find('span').text.strip() if title_element else "N/A"
                
                author_element = book.find('a', class_='authorName')
                author = author_element.find('span').text.strip() if author_element else "N/A"
                
                rating_element = book.find('span', class_='minirating')
                rating_text = rating_element.text.strip() if rating_element else ""
                
                rating_match = re.search(r'(\d+\.\d+)', rating_text)
                avg_rating = rating_match.group(1) if rating_match else "N/A"
                
                books_data.append({
                    'Title': title,
                    'Author': author,
                    'Average_Rating': avg_rating
                })
                
            except:
                continue
        
        page_num += 1
        time.sleep(2)
    
    return books_data[:1000]

books = scrape_goodreads_books()

# Save to CSV
df = pd.DataFrame(books)

df.to_csv('goodreads_books.csv', index=False, encoding='utf-8')
