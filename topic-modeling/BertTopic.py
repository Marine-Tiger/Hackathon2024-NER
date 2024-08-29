from bertopic import BERTopic
import os
from raw_stopword_list import raw_stopword_list
import spacy
from typing import List
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.vectorizers import ClassTfidfTransformer
import json


#Il faut découper les séances dans une liste pour TF-IDF
#On peut reprendre le texte directement plutôt que les chunks

with open('./topic-modeling/corpus_par_date.json', 'r', encoding='utf-8-sig') as f:
  corpus = json.load(f)

corpus_bert = []
annees = []

for year, seances in corpus.items():
  annees.append(year)
  corpus_bert.append(''.join([seance['texte'] for seance in seances.values()]))
    
with open('./topic-modeling/keywords.json', 'r', encoding='utf-8') as f:
  keywords = json.load(f)
  vocabulary = []
  for key, count in keywords.items():
    if count < 350 and count >= 10:
      vocabulary.append(key)
  print(vocabulary)

vectorizer_model = CountVectorizer(vocabulary=vocabulary) #stop_words=raw_stopword_list)
# ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)
model = BERTopic(vectorizer_model=vectorizer_model, verbose=True, language="french")

clusters, probs = model.fit_transform(corpus_bert)

print(model.get_document_info(corpus_bert))


