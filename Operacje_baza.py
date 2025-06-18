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

conn = sqlite3.connect("DataBaseInz.db")
c = conn.cursor()
c.execute("SELECT id FROM articles")
rows = c.fetchall()
article_ids_in_articles = [row[0] for row in rows]

c.execute("SELECT article_id FROM articles_text")
rows = c.fetchall()
article_ids_in_articles_text = [row[0] for row in rows]

c.execute("SELECT distinct(article_id) FROM words")
rows = c.fetchall()
article_ids_in_words = [row[0] for row in rows]

conn.commit()
conn.close()

#UPDATE

#aktualizuje tytuł artykułu
def update_article_title(article_id, new_title):
    if article_id not in article_ids_in_articles:
        print(f"Nie ma takiego artykułu w bazie: dla update_article_title {article_id}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("UPDATE articles SET title = ? WHERE id = ?", (new_title, article_id))
        print(f"Udało się zaaktualizować tytuł artykułu {article_id} w tabeli articles_text")
        conn.commit()
        conn.close()

#aktualizuje link artykulu
def update_article_link(article_id, new_link):
    if article_id not in article_ids_in_articles:
        print(f"Nie ma takiego artykułu w bazie: dla update_article_link {article_id}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("UPDATE articles SET link = ? WHERE id = ?", (new_link, article_id))
        print(f"Udało się zaaktualizować link artykułu {article_id} w tabeli articles_text")
        conn.commit()
        conn.close()

#aktualizuje tytuł i link artykułu
def update_article(article_id, new_title, new_link):
    if article_id not in article_ids_in_articles:
        print(f"Nie ma takiego artykułu w bazie: dla update_article {article_id}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("UPDATE articles SET title = ?, link = ? WHERE id = ?", (new_title, new_link, article_id))
        print(f"Udało się zaaktualizować artykuł {article_id} w tabeli articles")
        conn.commit()
        conn.close()

#aktualizuje wyraz danego typu z danego artykułu
def update_word(article_id, old_word_type, new_word):
    if article_id not in article_ids_in_words:
        print(f"Nie ma takiego artykułu w tabeli words: dla update_word {article_id}")
    elif old_word_type not in ["Rzeczownik_1","Rzeczownik_2","Czasownik","Przymiotnik"]:
        print(f"Nie ma takiego typu wyrazu w bazie: dla update_word {old_word_type}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("UPDATE words SET word = ? WHERE article_id = ? AND word_type = ?",(new_word, article_id, old_word_type))
        print(f"Udało się zaaktualizować wyraz artykułu {article_id} o typie {old_word_type} do wyrazu {new_word} w tabeli words")
        conn.commit()
        conn.close()

#aktualizuje tekst artykułu
def update_article_text(article_id, new_text):
    if article_id not in article_ids_in_articles_text:
        print(f"Nie ma takiego artykułu w tabeli words: dla update_article_content {article_id}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("UPDATE articles_text SET article_text = ? WHERE article_id = ?", (new_text, article_id))
        print(f"Udało się zaaktualizować tekst artykułu {article_id} w tabeli articles_text")
        conn.commit()
        conn.close()

#INSERT

#dodaje artykuł z przypisanym konkretnym id
def force_insert_article(id, title, link):
    if not isinstance(id, int):
        print(f"article_id powinien być typem int")
    elif id not in article_ids_in_articles:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("INSERT INTO articles (id, title, link) VALUES (?, ?, ?)",(id, title, link))
        print(f"Udało się dodać artykułu {id} do tabeli articles")
        conn.commit()
        conn.close()
    else:
        print(f"Artykuł o danym id już jest w bazie: dla force_insert_article {id}")

#dodaje artykuł o automatycznej inkrementacji id (do pierwszego wolnego id)
def insert_article(title, link):
    conn = sqlite3.connect("DataBaseInz.db")
    c = conn.cursor()
    c.execute("INSERT INTO articles (title, link) VALUES (?, ?)",(title, link))
    print(f"Udało się dodać artykuł do tabeli articles")
    conn.commit()
    conn.close()

#dodaje jeden wyraz danego typu do danego artykułu do tabeli words
def insert_words(article_id, word_type, word):
    if not isinstance(article_id, int):
        print(f"article_id powinien być typem int")
    elif word_type not in ["Rzeczownik_1","Rzeczownik_2","Czasownik","Przymiotnik"]:
        print(f"Nie ma takiego typu wyrazu w bazie: dla insert_words {word_type}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        if article_id in article_ids_in_words:
            c.execute("SELECT * FROM words WHERE article_id = (?)", (article_id,))
            rows = c.fetchall()
            types_in_article_words = [row[1] for row in rows]
            if word_type in types_in_article_words:
                print(f"Istnieje już ten typ słowa dla danego artykułu (insert_words {article_id} {word_type}), jeśli chcesz zamienić użyj update_word")
                conn.commit()
                conn.close()
            else:
                c.execute("INSERT INTO words (article_id, word_type, word) VALUES (?, ?, ?)", (article_id, word_type, word))
                print(f"Udało się dodać wyraz {word} do artykułu {article_id} o typie {word_type} do tabeli words")
                conn.commit()
                conn.close()
        else:
            c.execute("INSERT INTO words (article_id, word_type, word) VALUES (?, ?, ?)",(article_id, word_type, word))
            print(f"Udało się dodać wyraz {word} do artykułu {article_id} o typie {word_type} do tabeli words")
            conn.commit()
            conn.close()

#dodaje tekst do tabeli articles_text do danego artykułu
def insert_article_text(article_id, article_text):
    if not isinstance(article_id, int):
        print(f"article_id powinien być typem int")
    elif article_id not in article_ids_in_articles_text:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("INSERT INTO articles_text (article_id, article_text) VALUES (?, ?)",(article_id, article_text))
        print(f"Udało się dodać tekst artykułu {article_id} do tabeli articles_text")
        conn.commit()
        conn.close()
    else:
        print(f"Artykuł o id={article_id} już jest w bazie, jeśli chcesz zamienić tekst użyj funkcji update_article_content")

#DELETE

#usuwa artykuł o podanym id z tabeli articles
def delete_from_article(id):
    if id not in article_ids_in_articles:
        print(f"Nie ma takiego artykułu w bazie: dla delete_from_article {id}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")
        c.execute("DELETE FROM articles WHERE id=(?)",(id,))
        print(f"Udało się usunąć artykuł {id}")
        conn.commit()
        conn.close()

#usuwa jeden wyraz i typ (1 rekord) z podanego id artykułu w tabeli words
def delete_from_words_word(article_id, word_type):
    if word_type not in ["Rzeczownik_1","Rzeczownik_2","Czasownik","Przymiotnik"]:
        print(f"Nie ma takiego typu wyrazu w bazie: dla delete_from_words_word {word_type}")
    elif article_id not in article_ids_in_words:
        print(f"Nie ma takiego artykułu w tabeli words: dla delete_from_words_word {article_id}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("DELETE FROM words WHERE article_id=(?) AND word_type = (?)", (article_id,word_type))
        print(f"Udało się usunąć wyraz artykułu {article_id} o typie {word_type} z tabeli words")
        conn.commit()
        conn.close()

#usuwa wszystkie typy i wyrazy (do 4 rekordów) danego id artykułu w tabeli words
def delete_from_words_article(article_id):
    if article_id not in article_ids_in_words:
        print(f"Nie ma takiego artykułu w tabeli words: dla delete_from_words_article {article_id}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("DELETE FROM words WHERE article_id=(?)", (article_id,))
        print(f"Udało się usunąć cały artykuł {article_id} z tabeli words")
        conn.commit()
        conn.close()

#usuwa artykuł o danym id z articles_text
def delete_from_article_text(article_id):
    if article_id not in article_ids_in_articles_text:
        print(f"Nie ma takiego artykułu w tabeli articles_text: dla delete_from_article_text {article_id}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("DELETE FROM articles_text WHERE article_id=(?)", (article_id,))
        print(f"Udało się usunąć artykuł {article_id} z tabeli articles_text")
        conn.commit()
        conn.close()

#ODCZYT

def select_article(id):
    if id not in article_ids_in_articles:
        print(f"Nie ma takiego artykułu w bazie: dla select_article {id}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("SELECT * FROM articles WHERE id = (?)", (id,))
        print(c.fetchall())
        conn.close()

def select_word(article_id, word_type):
    if word_type not in ["Rzeczownik_1","Rzeczownik_2","Czasownik","Przymiotnik"]:
        print(f"Nie ma takiego typu wyrazu w bazie: dla select_word {word_type}")
    elif article_id not in article_ids_in_words:
        print(f"Nie ma takiego artykułu w tabeli words: dla select_word {article_id}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("SELECT * FROM words WHERE article_id = (?) AND word_type = (?)",(article_id, word_type))
        print(c.fetchall())
        conn.close()

def select_words_from_article(article_id):
    if article_id not in article_ids_in_words:
        print(f"Nie ma takiego artykułu w tabeli words: dla select_words_from_article {article_id}")
    else:
        conn = sqlite3.connect("DataBaseInz.db")
        c = conn.cursor()
        c.execute("SELECT * FROM words WHERE article_id = (?)",(article_id,))
        rows = c.fetchall()
        for row in rows:
            print(row)
        conn.close()

def select_article_text(article_id):
    if article_id not in article_ids_in_articles_text:
        print(f"Nie ma takiego artykułu w tabeli articles_text: dla select_article_text {article_id}")
    else:
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

