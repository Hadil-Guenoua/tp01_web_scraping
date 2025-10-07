import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fetch the content of the web page
url = "https://quotes.toscrape.com" 
response = requests.get(url)
print(response.text)  

# Use BeautifulSoup to extract all quotes from the page
soup = BeautifulSoup(response.text, "html.parser")
quotes = soup.find_all("span", class_="text")
authors = soup.find_all("small", class_="author")

quotes_list = [q.text for q in quotes]
authors_list = [a.text for a in authors]

# Save results to a CSV file using pandas
data = {"Quote": quotes_list, "Author": authors_list}
df = pd.DataFrame(data)
df.to_csv("quotes.csv", index=False)
