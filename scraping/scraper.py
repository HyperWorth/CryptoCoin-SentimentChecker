import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_date_from_url(url):
    """
    URL'deki tarihi ayıklamak için bir fonksiyon.
    URL formatı şu şekilde olacak: https://www.coindesk.com/markets/YYYY/MM/DD/{article-name}
    """
    parts = url.split('/')
    # Tarih kısımlarını almak (YYYY/MM/DD)
    article_date_str = '/'.join(parts[4:7])  # 4. 5. ve 6. elemanlar tarih kısmıdır
    return article_date_str


def check_if_today_article(url):
    """
    URL'deki tarih kısmını alıp bugünün tarihiyle karşılaştırır.
    Eğer tarih uyuyorsa, o tarihi döndürür.
    """
    # URL'den tarihi al
    article_date_str = get_date_from_url(url)

    # Bugünün tarihini alıyoruz
    today_date_str = datetime.today().strftime('%Y/%m/%d')

    # Eğer tarih uyuyorsa, o tarihi döndür
    if article_date_str == today_date_str:
        return True
    else:
        return False  # Eğer tarih uyuşmuyorsa False döner


def get_article_urls():
    """
    CoinDesk 'Markets' ve 'Business' kategorilerindeki makalelerin URL'lerini alır.
    Fakat sadece bugünün tarihine uygun olanları alır.
    """
    # İlk olarak markets kategorisini alıyoruz
    market_url = "https://www.coindesk.com/markets"
    response = requests.get(market_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # markets sayfasındaki tüm linkleri al
    article_links = soup.find_all('a', class_='flex shrink-0 flex-col', href=True)
    urls = []
    base_url = "https://www.coindesk.com"
    
    # markets sayfasındaki linkleri kontrol et
    for link in article_links:
        href = link['href']
        full_url = base_url + href if not href.startswith('http') else href
        
        # Tarihi kontrol et ve sadece bugünün tarihine uygun olanları ekle
        if check_if_today_article(full_url):
            urls.append(full_url)
    
    # Şimdi business kategorisini alıyoruz
    business_url = "https://www.coindesk.com/business"
    response = requests.get(business_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # business sayfasındaki tüm linkleri al
    article_links = soup.find_all('a', class_='flex shrink-0 flex-col', href=True)
    
    # business sayfasındaki linkleri kontrol et ve sadece bugünün tarihine uygun olanları ekle
    for link in article_links:
        href = link['href']
        full_url = base_url + href if not href.startswith('http') else href
        
        # Tarihi kontrol et ve sadece bugünün tarihine uygun olanları ekle
        if check_if_today_article(full_url):
            urls.append(full_url)
    
    return urls


def get_news(urls):
    all_articles = []  # To store all news articles

    # Loop through each URL to scrape
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text from 'p' tags, which are typically used for paragraphs
        news_list = soup.find_all('p')
        
        # Clean and combine all paragraphs into one
        news_articles = [news.get_text() for news in news_list]
        
        # Filter out irrelevant text (e.g., "about", "contact", "policies")
        clean_articles = [article for article in news_articles if article.strip() and article.lower() not in ["about", "contact", "policies"]]
        
        # Combine all article parts into one string
        full_article = " ".join(clean_articles)
        
        all_articles.append(full_article)  # Add the article to the list
    
    return all_articles


       