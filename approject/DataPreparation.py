import luigi 
from luigi import LocalTarget, Task 
from approject.emailretriever import DownloadArticle
import pandas as pd 

class PrepareData(luigi.Task):

    lexology_url = luigi.ListParameter()

    def requires(self):
        return DownloadArticle(lexology_urls=lexology_ursl)
        
    def run(self):
        df = pd.read_pickle(self.input().path)
        
        #Save final result.
        #df.to_pickle(self.output().open('w').path)
    
    def output(self):
        return luigi.LocalTarget(f'data/clean/clean_articles.pkl')