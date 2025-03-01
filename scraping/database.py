import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    try:
        sql_create_articles_table = ''' 
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,  -- URL'yi benzersiz yapıyoruz
            date TEXT NOT NULL,
            article_text TEXT
        ); '''
        conn.execute(sql_create_articles_table)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")


def insert_article(conn, url, date, article_text):
    try:
        sql_insert_article = ''' INSERT INTO articles (url, date, article_text)
                                 VALUES (?, ?, ?) '''
        conn.execute(sql_insert_article, (url, date, article_text))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Article with URL {e} already exists. Skipping...")
    except sqlite3.Error as e:
        print(f"Error inserting article: {e}")

def check_if_article_exists(conn, url):
    """
    Veritabanında verilen URL'ye sahip bir makale olup olmadığını kontrol eder.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM articles WHERE url = ?", (url,))
    result = cursor.fetchone()
    return result[0] > 0  # Eğer 0'dan fazla varsa, URL zaten kaydedilmiş demektir
    
def fetch_articles_by_date_range(conn, start_date, end_date):
    """
    Belirtilen tarih aralığında bulunan makaleleri getirir.
    Tarih formatı: YYYY/MM/DD
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT url, date, article_text
        FROM articles 
        WHERE date BETWEEN ? AND ?
        ORDER BY date ASC
    """, (start_date, end_date))
    
    rows = cursor.fetchall()
    if len(rows) == 0:
        return None  # Eğer sonuç yoksa None döneriz
    
    return rows
def fetch_articles(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    return cursor.fetchall()
