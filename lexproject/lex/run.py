from approject.DataPreparation import PrepareData
from approject.computesimilarity import ComputeSimilarities
import luigi
import win32com.client
import re
import requests 
import luigi
from bs4 import BeautifulSoup

my_outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

folder = my_outlook.GetDefaultFolder(6).Folders.Item("Lexology")
lex_urls = []
for item in folder.Items:    
    emailbody = item.body
    lexology_date = item.SentOn.strftime("%Y-%m-%d")
    lexology_url = re.findall(r'[<]\S*', emailbody)[0].strip('<').strip('>')
    print(lexology_url, lexology_date)
    lex_urls.append(lexology_url)


lexology_urls = lex_urls
emb_path = 'data/glove.6B.50d.txt'
text = 'my name is'
n_similar = 10

task_list = [ComputeSimilarities(lexology_urls=lexology_urls, emb_path=emb_path,
                        col_to_use='article_title', text=text, n_similar=n_similar ),
            ComputeSimilarities(lexology_urls=lexology_urls, emb_path=emb_path,
                        col_to_use='text', text=text, n_similar=n_similar )
                        ]

luigi.build(task_list, local_scheduler=True)