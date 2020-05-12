import luigi 
from luigi import LocalTarget, Task 
from approject.approject.emailretriever import DownloadArticle
from approject.approject.embeddding import WordEmbedding
import pandas as pd 



class EmbeddingsGlove(luigi.ExternalTask):

    emb_path = luigi.Parameter()
    
    def output(self):
        return luigi.LocalTarget(self.emb_path)

class InitEmbedings(luigi.Task):

    emb_path = luigi.Parameter()

    def requires(self):
        return  EmbeddingsGlove(emb_path=self.emb_path)
        
    def run(self):

        embedding = WordEmbedding.from_files(self.input().path)
        pd.to_pickle(embedding, self.output().open('w').path)
    
    def output(self):
        return luigi.LocalTarget(f'data/emb/embedding_class.pkl')

class PrepareData(luigi.Task):

    lexology_urls = luigi.ListParameter()
    emb_path = luigi.Parameter()
    col_to_use = luigi.Parameter()

    def requires(self):
        return [DownloadArticle(lexology_urls=self.lexology_urls), 
                InitEmbedings(emb_path=self.emb_path)]
        
    def run(self):

        df = pd.read_pickle(self.input()[0].path)
        embedding = pd.read_pickle(self.input()[1].path)
        embeddings = df[self.col_to_use].apply(embedding.embed_document)

        #Save final result.
        pd.to_pickle(embeddings, self.output().open('w').path)
    
    def output(self):
        return luigi.LocalTarget(f'data/clean/{self.col_to_use}-embeddings.pkl')