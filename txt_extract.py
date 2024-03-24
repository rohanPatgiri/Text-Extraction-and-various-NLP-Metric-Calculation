from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import os


# Create a new directory named 'extracted_text'. This is the folder where the extracted text files will be stored
if not os.path.exists('extracted_text'):
    os.makedirs('extracted_text')

# Read the Input Excel file, which contains the links of the web pages
df = pd.read_excel('Input.xlsx')

# Set up the Selenium driver. This will be used to load the webpages
driver = webdriver.Chrome()

# For each row in the DataFrame
for index, row in df.iterrows():
    # Get the URL ID and URL
    url_id = row['URL_ID']
    url = row['URL']

    # Use Selenium to load the webpage
    driver.get(url)

    # Get the HTML content of the webpage
    webpage = driver.page_source

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(webpage, 'html.parser')

    # Find the title of the article
    title = soup.find('h1').get_text() if soup.find('h1') else ''

    # Find the division containing the article text
    article_div = soup.find('div', {'class': 'td-post-content tagdiv-type'}) or soup.find('div', {'class': 'tdb_single_content'})

    # Extract all text within the specified <div> tag
    if article_div:
        text = ' '.join(article_div.stripped_strings)
    else:
        text = ''
     

    # Write the title and text to a txt file named after the URL ID in the 'extracted_text' directory
    with open(os.path.join('extracted_text', f'{url_id}.txt'), 'w', encoding='utf-8') as f:
        f.write(title + '\n' + text)

# Close the Selenium driver
driver.quit()
