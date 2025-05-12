import sqlite3
import os

conn=sqlite3.connect('DataBaseInz.db')
c = conn.cursor()

conn.execute("PRAGMA foreign_keys = ON")
c.execute("DELETE FROM sqlite_sequence WHERE name='articles'")

'''
c.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    link TEXT
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS words (
    article_id INTEGER,
    word_type TEXT,
    word TEXT,
    FOREIGN KEY(article_id) REFERENCES articles(id) ON DELETE CASCADE
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS articles_text (
    article_id INTEGER INTEGER PRIMARY KEY,
    article_text TEXT,
    FOREIGN KEY(article_id) REFERENCES articles(id) ON DELETE CASCADE
)
""")
'''
conn.commit()
conn.close()

#UPDATE

def update_article(article_id, new_title, new_link):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("UPDATE articles SET title = ?, link = ? WHERE id = ?", (new_title, new_link, article_id))
    conn.commit()
    conn.close()

def update_word(article_id, old_word_type, new_word):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("UPDATE words SET word = ? WHERE article_id = ? AND word_type = ?",
                (new_word, article_id, old_word_type))
    conn.commit()
    conn.close()

def update_article_content(article_id, new_text):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("UPDATE articles_text SET article_text = ? WHERE article_id = ?", (new_text, article_id))
    conn.commit()
    conn.close()

#INSERT

def insert_article(title, link):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("INSERT INTO articles (title, link) VALUES (?, ?)",(title, link))
    conn.commit()
    conn.close()

def insert_words(article_id, word_type, word):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("INSERT INTO words (article_id, word_type, word) VALUES (?, ?, ?)",(article_id, word_type, word))
    conn.commit()
    conn.close()

def insert_article_text(article_id, article_text):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("INSERT INTO articles_text (article_id, article_text) VALUES (?, ?)",(article_id, article_text))
    conn.commit()
    conn.close()

#DELETE

def delete_from_article(id):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("DELETE FROM articles WHERE id=(?)",(id,))
    conn.commit()
    conn.close()

def delete_from_words(article_id, word_type):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("DELETE FROM words WHERE article_id=(?) AND word_type = (?)", (article_id,word_type))
    conn.commit()
    conn.close()

def delete_from_article_text(article_id):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("DELETE FROM articles_text WHERE article_id=(?)", (article_id,))
    conn.commit()
    conn.close()

#ODCZYT

def select_article(id):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("SELECT * FROM articles WHERE id = (?)",(id,))
    print(c.fetchall())
    conn.close()

def select_words(article_id, word_type):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("SELECT * FROM words WHERE article_id = (?) AND word_type = (?)",(article_id, word_type))
    print(c.fetchall())
    conn.close()

def select_article_text(article_id):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("SELECT * FROM articles_text WHERE article_id = (?)",(article_id,))
    print(c.fetchall())
    conn.close()



#ODCZYT CAŁOŚCI
def calosc():
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()

    c.execute("SELECT * FROM articles")
    rows = c.fetchall()
    for row in rows:
        print(row)

    c.execute("SELECT * FROM words")
    rows = c.fetchall()
    for row in rows:
        print(rows)

    c.execute("SELECT * FROM articles_text")
    rows = c.fetchall()
    for row in rows:
        print(row)


    conn.commit()
    conn.close()

#Testy - próbne wywołania np.
#calosc()
#insert_words(1,"Czasownik", "Być")
#select_words(1,"Czasownik")
#update_word(1,"Czasownik","nie Być")
#delete_from_words(1,"Czasownik")
