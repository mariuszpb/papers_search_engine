# -*- coding: utf-8 -*-
import sqlite3
import sys
import spacy
from collections import Counter

nlp = spacy.load("pl_core_news_sm")

query = sys.argv[1]

def tokenize(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return tokens

conn = sqlite3.connect('DataBaseInz.db')
cursor = conn.cursor()

cursor.execute("SELECT article_id, word FROM words;")
rows = cursor.fetchall()

article_words = {}
for article_id, word in rows:
    article_words.setdefault(article_id, []).append(word.lower())

query_tokens = tokenize(query)
query_counter = Counter(query_tokens)

scores = []
for article_id, words in article_words.items():
    word_counter = Counter(words)
    common = set(query_tokens) & set(words)
    score = sum(min(query_counter[word], word_counter[word]) for word in common)
    if score > 0:
        scores.append((article_id, score))

scores.sort(key=lambda x: x[1], reverse=True)

if not scores:
    print("Brak dopasowan.")
    sys.exit(0)

top_article_ids = [str(article_id) for article_id, _ in scores[:3]]
placeholders = ','.join(['?'] * len(top_article_ids))
cursor.execute(f"SELECT id, title, link FROM articles WHERE id IN ({placeholders});", top_article_ids)
results = cursor.fetchall()

for article in results:
    print(f"{article[0]}|{article[1]}|{article[2]}")

conn.close()