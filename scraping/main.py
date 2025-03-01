import threading
import time
from scraper import get_article_urls, get_news, get_date_from_url#path file
from database import create_connection, create_table, insert_article, fetch_articles, check_if_article_exists#path file
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
from logger import setup_logger  # Logger'ı import ediyoruz


# Logger'ı başlat
logger = setup_logger()


# Tray icon image generator
def create_image():
    # Create an empty image with transparent background
    image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    # Draw a simple icon (just a dot for simplicity)
    draw.ellipse((10, 10, 54, 54), fill='blue', outline='black')
    return image


# Tray icon task to scrape articles
def scrape_articles():
    conn = create_connection("db\\articles.db")
    create_table(conn)
    
    while True:
        try:
            # CoinDesk'ten haber URL'lerini al
            logger.info("Fetching article URLs...")
            urls = get_article_urls()
            logger.info(f"Found {len(urls)} article URLs.")
            
            # Haber metinlerini al
            news_articles = get_news(urls)
            logger.info(f"Fetched {len(news_articles)} news articles.")
            
            # URL ve tarih bilgisiyle her bir makaleyi veritabanına ekle
            for url, article in zip(urls, news_articles):
                # URL'nin daha önce kaydedilip edilmediğini kontrol et
                if check_if_article_exists(conn, url):
                    logger.info(f"Article from {url} already exists. Skipping.")
                else:
                    date = get_date_from_url(url)
                    insert_article(conn, url, date, article)
                    logger.info(f"Article from {url} saved successfully.")
            
            # Veritabanındaki tüm haberleri çek
            all_articles = fetch_articles(conn)
            logger.info(f"Total {len(all_articles)} articles saved.")
        
        except Exception as e:
            logger.error(f"An error occurred while scraping: {e}")
        
        # Her 10 dakikada bir scrape işlemi yap (600 saniye)
        time.sleep(3600)  # 1 saat


# Tray icon'ındaki menü fonksiyonu
def on_quit(icon, item):
    logger.info("Exiting application...")
    icon.stop()  # Tray ikonunu kapat


# Tray icon fonksiyonu
def setup_tray_icon():
    icon = Icon("CoinDesk Scraper", create_image())
    menu = Menu(MenuItem("Quit", on_quit))  # Menüde Quit seçeneği
    icon.menu = menu
    icon.run()


# Ana fonksiyon, tray ikonu ve scraper'ı başlatacak
def main():
    logger.info("Starting the CoinDesk Scraper application...")
    
    # Scraping işlemini ayrı bir thread ile çalıştır
    scraping_thread = threading.Thread(target=scrape_articles)
    scraping_thread.daemon = True  # Ana işlem sonlandığında thread de sonlanır
    scraping_thread.start()

    # Tray icon'u başlat
    setup_tray_icon()


if __name__ == "__main__":
    main()
