from django.shortcuts import render
import pandas as pd

import os
import glob
from approject.run import run_luigi


def index(request):
    errors = []
    article_titles_out = []
    text_out = []
    template = 'index.html'
    if request.method == 'GET':
        return render(request, template, dict(errors=errors, article_titles_out=article_titles_out, text_out=text_out))
    elif request.method == 'POST':
        text = request.POST.get('CheckIn', "")
        n_similar = request.POST.get("CheckOut", "")

        try:
            n_similar = int(n_similar)
        except (ValueError, TypeError):
            errors.append("The number must be a valid integer")

        if errors:
            return render(request, template, dict(errors=errors, article_titles_out=article_titles_out, text_out=text_out))

        #print(text, n_similar)
        run_luigi(text=text, n_similar=n_similar)

        results_dir = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "approject"), "data"), "results")

        article_title_dir = os.path.join(results_dir, "article_title")
        text_dir = os.path.join(results_dir, "text")

        article_title_pkl = glob.glob(f"{article_title_dir}/**/*.pkl", recursive=True)[0]
        text_pkl = glob.glob(f"{text_dir}/**/*.pkl", recursive=True)[0]

        
        
        article_titles_out = []
        article_title = pd.read_pickle(article_title_pkl)
        for row in article_title.iterrows():
            #import pdb; pdb.set_trace()
            _row = row[1]
            _text = _row.text
            _article_title = _row.article_title
            _article_date = _row.article_date
            _article_dict = {
                "text": _text,
                "title": _article_title,
                "date": _article_date,
            }
            article_titles_out.append(_article_dict)


        text_out = []
        text = pd.read_pickle(text_pkl)
      
        for row in text.iterrows():
            
            #import pdb; pdb.set_trace()
            _row = row[1]
            _text = _row.text
            _article_title = _row.article_title
            _article_date = _row.article_date
            _article_dict = {
                "text": _text,
                "title": _article_title,
                "date": _article_date,
                }
            text_out.append(_article_dict)

        #import pdb; pdb.set_trace()
        return render(request, template, dict(errors=errors, article_titles_out=article_titles_out, text_out=text_out))

