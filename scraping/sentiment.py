import ollama  # Ollama API'sini import ettik
import json  # JSON dosyası oluşturmak için import ettik
import re  # Kripto para isimlerini tanımak için regex kullanacağız
from datetime import datetime
from database import create_connection, fetch_articles_by_date_range#path file
import logging

# Logging yapılandırması
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,  # INFO ve üzeri seviyeleri kaydedeceğiz
    handlers=[
        logging.FileHandler("log\sentiment_analysis.log"),  # Logları dosyaya kaydeder
        logging.StreamHandler()  # Aynı logları ekrana da yazdırır
    ]
)

def fetch_data_in_date_range(start_date, end_date=datetime.today().strftime('%Y/%m/%d')):
    conn = create_connection("db\\articles.db")
    
    # Belirtilen tarih aralığındaki makaleleri çek
    logging.info(f"Fetching articles from {start_date} to {end_date}")
    articles = fetch_articles_by_date_range(conn, start_date, end_date)
    
    if articles is None:
        logging.warning(f"No articles found between {start_date} and {end_date}.")
        return
    logging.info(f"Found {len(articles)} articles.")
    return articles

# Deepseek-r1b1.5 modeli ile duygu analizi yap ve kripto etkisini belirle
def analyze_sentiment_with_ollama(news_articles, coin):
    results = []
    logging.info(f"Analyzing sentiment for coin: {coin}")

    for url, date, article in news_articles:
        prompt = f"""
        Important Rules:
        1. Focus only on the specified cryptocurrency: `{coin}`   
        2. Assign a score between -100 and +100 based on the impact of the news on `{coin}`  
            A positive score indicates a positive impact of the news on `{coin}` (potential increase in value).
            A negative score indicates a negative impact of the news on `{coin}` (potential decrease in value).
            A score of 0 means no significant impact of the news on `{coin}`.
        3. Return the output strictly in JSON format without any extra text
        4. Do NOT include reasoning or explanation—only provide the JSON output.
        5. The output format must be strictly: "score" : score_value 
            score is the key, and score_value is a numerical value between -100 and +100.
        News Article:       
        {article} 
        """
        
        try:
            response = ollama.chat(
                model="deepseek-r1:1.5b",  # deepseek-r1:1.5b modelini kullanıyoruz
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": 0,   # Aynı yanıtı almak için
                    "max_tokens": 4,    # Tek bir token (sayı) için
                    "top_p": 1,         # Tüm olasılıklar dikkate alınır
                    "frequency_penalty": 0,
                    "presence_penalty": 0
                }
            )

            sentiment_raw = response["message"]["content"]
            sentiment_cleaned = re.sub(r"<think>.*?</think>", "", sentiment_raw, flags=re.DOTALL).strip()
            sentiment_cleaned = sentiment_cleaned.split(":")
            
            results.append({
                "Adress": url,  
                "Date": date,
                "Article": article[:100],  # İlk 100 karakter
                sentiment_cleaned[0]: sentiment_cleaned[1]
            })
            logging.info(f"Sentiment analysis completed for article: {url}")

        except Exception as e:
            logging.error(f"Error analyzing article {url}: {str(e)}")
    
    return results

# JSON dosyasına kaydetme fonksiyonu
def save_results_to_json(results, filename="Json\sentiment_analysis_results.json"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
        logging.info(f"Results have been saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving results to JSON: {str(e)}")

# Ana fonksiyon
if __name__ == "__main__":
    today = datetime.today()
    coin = input("Enter the cryptocurrency: ")
    date_string = input("Enter a Date (in format YYYY-MM-DD): ")
    
    try:
        start_date = datetime.strptime(date_string, "%Y-%m-%d")
        
        # Tarihin bugünün tarihini geçmediğini kontrol et
        if start_date <= today:
            logging.info(f"The entered date is: {start_date}")
            news_articles = fetch_data_in_date_range(start_date)  # URL'lere göre haber metinlerini al
            if news_articles:  # Eğer haberler varsa, analiz yap
                logging.info("Performing sentiment analysis with deepseek-r1:1.5b...")
                sentiment_results = analyze_sentiment_with_ollama(news_articles, coin)  # Duygu analizini yap
                # Sonuçları JSON dosyasına kaydet
                save_results_to_json(sentiment_results)  # Sonuçları kaydet
        else:
            logging.error("Error: The date cannot be in the future.")
        
    except ValueError:
        logging.error("Error: Incorrect date format. Please use YYYY-MM-DD format.")
