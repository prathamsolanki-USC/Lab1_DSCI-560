import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv

source_file_path = "/home/prathamuser/Desktop/prathamsolanki_3242692358/data/raw_data/web_data.html"
market_data_csv_path = "/home/prathamuser/Desktop/prathamsolanki_3242692358/data/processed_data/market_data.csv"
news_data_csv_path = "/home/prathamuser/Desktop/prathamsolanki_3242692358/data/processed_data/news_data.csv"

def read_html_page(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        html_list = file.readlines()

    html_str = "\n".join(html_list)

    html_parsed = BeautifulSoup(html_str, 'html.parser')

    return html_parsed

def get_market_data(html_parsed):
    market_banner_main = html_parsed.find('div',class_="MarketsBanner-main")
    market_banner = market_banner_main.find("div",class_="MarketsBanner-marketData")
    a_tags = market_banner.find_all('a')

    marketcard_smybol_list,marketcard_stockposition_list,MarketCard_changesPcs_list = [],[],[]

    for a in a_tags:
        marketcard_smybol_list.append(a.find('span',class_= "MarketCard-symbol").get_text(strip=True))
        marketcard_stockposition_list.append(a.find('span', class_="MarketCard-stockPosition").get_text(strip=True))
        MarketCard_changesPcs_list.append(a.find('span', class_="MarketCard-changesPct").get_text(strip=True))

    market_card_dict = {"marketcard_symbol": marketcard_smybol_list,
                        "marketcard_stockposition": marketcard_stockposition_list,
                        "MarketCard_changesPct":MarketCard_changesPcs_list
                        }
    if len(marketcard_smybol_list)!=0 or len(marketcard_stockposition_list)!=0 or len(MarketCard_changesPcs_list)!=0:
        print("Market Data Fetching was Unsuccessfully")
    return market_card_dict

def get_news_data(html_parsed):
    lates_news_list = html_parsed.find('ul',class_="LatestNews-list")
    latest_news_items_list = lates_news_list.find_all('li',class_='LatestNews-item')

    timestamp_list,title_list,link_list = [],[],[]
    for latest_news in latest_news_items_list:
        timestamp_list.append(latest_news.find('time',class_="LatestNews-timestamp").get_text(strip=True))
        title_list.append(latest_news.find('a',class_="LatestNews-headline").get('title'))
        link_list.append(latest_news.find('a', class_="LatestNews-headline").get('href'))

    latest_news_data_dict = {"LatestNews-timestamp":timestamp_list,
                             "LatestNews-title":title_list,
                             "LatestNews-link":link_list}
 
    #print(latest_news_data_dict)
    if len(timestamp_list)!=0 or len(title_list!=0 or len(link_list)!=0:
        print("News Data Fetching was Unsuccessfully")
    return latest_news_data_dict

def write_to_csv(market_data_dict,news_data_dict,market_data_csv_path,news_data_csv_path):
    # Writing to CSV
    with open(market_data_csv_path, mode='w', newline='', encoding='utf-8') as market_file:
        market_writer = csv.writer(market_file)
        # Write header
        market_writer.writerow(['marketCard_symbol', 'marketCard_stockPosition', 'marketCard-changePct'])
        # Write data rows
        for symbol, position, changes in zip(
            market_data_dict["marketcard_symbol"],
            market_data_dict["marketcard_stockposition"],
            market_data_dict["MarketCard_changesPct"]
        ):
            market_writer.writerow([str(symbol), str(position), str(changes)])


    # Writing to CSV
    with open(news_data_csv_path, mode='w', newline='', encoding='utf-8') as news_file:
        news_writer = csv.writer(news_file)
        # Write header
        news_writer.writerow(['LatestNews-timestamp', 'LatestNews-title', 'LatestNews-link'])
        # Write data rows
        for timestamp, title, link in zip(
            news_data_dict["LatestNews-timestamp"],
            news_data_dict["LatestNews-title"],
            news_data_dict["LatestNews-link"]
        ):
            if len([str(timestamp), str(title), str(link)])!=3:
                print([str(timestamp), str(title), str(link)])
            news_writer.writerow([str(timestamp), str(title), str(link)])

    return None

## Main

#reading the HTML file
html_parsed = read_html_page(source_file_path)
print("successfully Read HTML code from web_data.html")

# fetching Market Data
market_data_dict = get_market_data(html_parsed)
print("successfully Fetched Market data")

# fetching
news_data_dict =get_news_data(html_parsed)
print("successfully Fetched news data")

#writing to CSV
write_to_csv(market_data_dict,news_data_dict,market_data_csv_path,news_data_csv_path)
print("Data successfully written to market_data.csv and news_data.csv")





