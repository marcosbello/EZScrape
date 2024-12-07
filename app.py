#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

Di = __name__
load_dotenv()

def search_ebay(query):
    query = query.replace(' ', '+')
    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize lists to store scraped data
    prices = []
    titles = []
    links = []

    # Extract prices
    for price in soup.find_all('span', class_='s-item__price'):
        prices.append(price.get_text())

    #Extract Titles
    for title in soup.find_all('div',class_='s-item__title'):
        titles.append(title.get_text())

    #extract link to posts
    for link in soup.find_all('a', class_='s-item__link'):
        links.append(link.get_text())
    #clean links list
   
    


    #check list lengths
    if len(titles)!= len(links):
       logging.warning("Number of prices and titles do not match. Truncating to the minimum length.")
    min_length = min(len(prices), len(titles), len(links))
    print(min_length)
    prices = prices[:(min_length)]
    titles = titles[:(min_length)]
    links = links[:min_length]


    # Create a DataFrame with the scraped lists
    df = pd.DataFrame({'Title': titles,'Price': prices,'Urls': links})
    #transformation to add the runtime of the program
    df['batchTime'] = (datetime.now())
    #transformation to keep the first price
    df['Price'] = df['Price'].str.extract(r'(\d+\.\d+)').astype(float)
    #df = df['links'].replace('Open in a new window','')
 
   # print(links)
    return df


# # MySQL database connection details
# host = os.getenv('DB_HOST')
# port = os.getenv('DB_PORT')
# dbname = os.getenv('DB_NAME')
# user = os.getenv('DB_USER')
# password = os.getenv('DB_PASSWORD')

# # Create a MySQL connection URL using SQLAlchemy
# connection_url = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}'

# # Create a SQLAlchemy engine for MySQL
# engine = create_engine(connection_url,echo=True)

# # Specify the table name where you want to upload the DataFrame
# table_name = 'guitar_test'

# # Upload the DataFrame to MySQL
# df.to_sql(table_name, engine, if_exists='append', index=False)

# print(f"DataFrame has been uploaded to the '{table_name}' table in MySQL.")

def upload_dataframe_to_mysql(df, table_name):
    """
    Uploads a DataFrame to a MySQL table.

    Args:
        df (pd.DataFrame): The DataFrame to upload.
        table_name (str): The name of the table.
    """
    # MySQL database connection details
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    # Create a MySQL connection URL using SQLAlchemy
    connection_url = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbname}'

    # Create a SQLAlchemy engine for MySQL
    engine = create_engine(connection_url, echo=True)
    Session = sessionmaker(bind=engine)

    # Open a session, upload the DataFrame, and close the session
    with Session() as session:
        try:
            df.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"DataFrame has been uploaded to the '{table_name}' table in MySQL.")
        except Exception as e:
            print(f"An error occurred while uploading the DataFrame: {e}")
            raise


def query_data(sql_string):
    Session = sessionmaker(bind=engine)
    session = Session()
    result = session.execute(text(sql_string))
    for i in result:
        print(i)
    session.close()

sql_string = """
    with data as (
SELECT tatsuro_album.Album as album_name,guitar_test.Title as album_title, price
FROM guitar_test
JOIN tatsuro_album
ON guitar_test.Title LIKE CONCAT('%', tatsuro_album.Album, '%')
WHERE LENGTH(guitar_test.Title) > LENGTH(tatsuro_album.Album)
)

select album_name
,count(album_title)
,min(price) min
,avg(price) avg
,max(price) max
,std(price) sd
from data 
group by 1
limit 10
    """
#query_data(sql_string)

if __name__ == '__main__':
    Di



# Example usage
search_query = "Tatsuro Yamashita Vinyls"
df = search_ebay(search_query)
print(df)
drop_string = 'Shop on eBay'
df = df[df['Title'] != drop_string]
table_name = 'guitar_test'
upload_dataframe_to_mysql(df, table_name)