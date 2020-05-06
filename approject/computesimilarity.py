import luigi 
from luigi import LocalTarget, Task 
from approject.emailretriever import DownloadArticle
from approject.embeddding import WordEmbedding
from approject.DataPreparation import PrepareData, InitEmbedings
from approject.cosinesimilarity import cosine_similarity
import pandas as pd 
import hashlib

class ComputeSimilarities(luigi.Task):

    lexology_urls = luigi.ListParameter()
    emb_path = luigi.Parameter()
    col_to_use = luigi.Parameter()
    n_similar = luigi.IntParameter(default=5)
    text = luigi.Parameter()

    def requires(self):
        return [PrepareData(lexology_urls=self.lexology_urls,
                            emb_path=self.emb_path,col_to_use=self.col_to_use), 
                DownloadArticle(lexology_urls=self.lexology_urls),
                InitEmbedings(emb_path=self.emb_path)]
        
    def run(self):

        emb = pd.read_pickle(self.input()[2].path)
        text = emb.embed_document(self.text)
        embeddings = pd.read_pickle(self.input()[0].path)
        cos_similarity = embeddings.apply(lambda x: cosine_similarity(text, x))
        distances = 1 - cos_similarity 

        raw = pd.read_pickle(self.input()[1].path)
        response = raw.iloc[distances.nsmallest(self.n_similar).index]   
        #Save final result.
        pd.to_pickle(response, self.output().open('w').path)
    
    def output(self):
        h = hashlib.md5(self.text.encode()).hexdigest()[:10]
        return luigi.LocalTarget(f'data/results/{self.col_to_use}/top_{self.n_similar}/embeddings-{h}.pkl')