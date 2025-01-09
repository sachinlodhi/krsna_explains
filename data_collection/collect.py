import requests
from bs4 import BeautifulSoup
import json


# Getting all the response from the main page
response = requests.get('https://vedabase.io/en/library/bg/')
if response.status_code == 200:
    print("yes")

# creating bs4 object
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify())

