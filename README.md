# EZScrape

# **EZScrap: Automated eBay Price Tracking**

EZScrap is a Python-based web scraping tool designed to automatically gather price data from eBay for items of interest. The project aims to help users easily search for product listings, track current prices, and store the data in a MySQL database for further analysis. This is especially useful for tracking market trends for collectibles, electronics, or any other items of value.

## Key Features
- **Automated Data Collection**: Scrapes eBay search results for item titles, prices, and links.
- **Price Transformation and Storage**: Cleans up and transforms the price data before storing it in a MySQL database.
- **Batch Processing**: Includes a timestamp with each batch of listings to track changes over time.
- **SQL Analysis**: Uses SQL queries to analyze the scraped data, providing insights like minimum, maximum, and average item prices.

## Technologies Used
- **Python**: The primary language for scripting and automation.
- **BeautifulSoup**: To parse HTML pages from eBay and extract relevant data.
- **SQLAlchemy**: For database interactions with MySQL, providing a seamless way to store and retrieve data.
- **Pandas**: For data transformation and organization before pushing to the database.
- **dotenv**: To securely manage and load environment variables, like database credentials.

## How It Works
1. **Search Query**: Users provide a search term (e.g., "Tatsuro Yamashita Vinyls"), and EZScrap fetches the search results from eBay.
2. **Data Extraction**: The script extracts item titles, prices, and URLs from the eBay results page.
3. **Data Transformation**: The prices are cleaned and converted to a numerical format, and irrelevant items are filtered out.
4. **Data Storage**: The cleaned data is then uploaded to a MySQL database table, allowing for long-term tracking and historical analysis.
5. **SQL Analysis**: A set of SQL queries are run to provide aggregated insights about the collected data, including statistics on prices.

This project is useful for anyone looking to track eBay pricing trends for specific products or categories, particularly resellers, collectors, or data analysts interested in market analysis.

