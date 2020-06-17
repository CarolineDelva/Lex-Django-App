


## Legal Newsletter Dashboard 


### Background
My intent is to create a tool that helps find the top 5 articles related to a user's entry based on the articles' title and text body.  

### Objective and Design 


A full stack application that is powered by a word embeddings to decide how closely related articles are from text and title;
-	a web-crawler that collects the text data from the email address 
-	a data pipeline to get the data from the email to the model, prepare the data and compute the emails 
  closeness to the text entry
-	a WordEmbedding model to calculate the distance   between the entered text and the emails   
- a django app that renders an user interface powered by the luigi pipeline 
-	a front-end interface that populates the classified summaries  
-	a unit test that ensures that the functions and classes are returning the correct results 


### Python Libraries

-	Pywin32: Data Scraping
-	Luigi: Data pipeline 
-	Word Embedding: Machine learning
-	Django App: User interface
-	W3 School Template: Front-end
-	Pytest: Testing
-	AWS: S3

### Interface 

![Image description](interface.PNG)
