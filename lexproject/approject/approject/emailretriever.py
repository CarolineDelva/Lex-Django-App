import win32com.client
import re
import time
import requests 
import luigi
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd


def get_article(article_link):
    r = requests.get(article_link) 
    html = r.text
   
    #article title
    article_title_soup = BeautifulSoup(html, 'html.parser')
    article_title = article_title_soup.select('h1')[0]
    title = article_title.text.strip()

    # article date 
    Soup_date = article_title_soup.find('div', class_='article-attributes')
    article_date = Soup_date.find('span', class_='publication')
    article_date = article_date.text.strip()

    # article body 
    article_div = article_title_soup.find('div', class_='article-body')
    article = article_div.text.strip()
    return [title, article_date, article]
    

class DownloadArticle(luigi.Task):

    lexology_urls = luigi.ListParameter() # luigi parameter
    def run(self):

        for lexology_url in self.lexology_urls:
            r = requests.get(lexology_url)
            html = r.text
            soup = BeautifulSoup(html, 'html.parser')
            article_header = soup.select('h4')
            article_link_list = []
            for links in article_header:
                article_links = links.find_all('a', href=True)
                for link in article_links: 
                    article_link = link.get('href')
                    article_link_list.append(article_link)
                    #print(article_link_list)
            all_text = []
            for article_link in article_link_list:
                try: 
                    text = get_article(article_link)
                    all_text.append(text)
                except Exception as e:
                    print(f'error in {article_link}, {e}')

                
        df = pd.DataFrame(all_text, columns=['article_title','article_date','text'])
        df.to_pickle(self.output().open('w').path)
    
    def output(self):
        return luigi.LocalTarget(f'data/raw/raw_articles.pkl')




