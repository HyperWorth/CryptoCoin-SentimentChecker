# Crypto News Sentiment Analyzer

Bu proje, **internet üzerindeki haberleri çekerek belirli bir kripto para birimine etkisini analiz eden** bir Python uygulamasıdır. Yapay zeka destekli **duygu analizi** (sentiment analysis) ile, haberlerin pozitif mi yoksa negatif mi olduğunu belirler ve yatırım kararlarını desteklemek için veri sağlar.

## 🚀 Özellikler

- **Haber Toplama:** CoinDesk gibi haber kaynaklarından veri çeker.
- **Veri Tabanı Kaydı:** Çekilen haberleri SQLite veritabanına kaydeder.
- **Tarih Bazlı Filtreleme:** Belirtilen tarihler arasında haberleri çekme özelliği.
- **Yapay Zeka ile Duygu Analizi:** Haberlerin ilgili kripto para birimi üzerindeki etkisini puanlar (-100 ile +100 arasında).
- **Tray Icon Desteği:** Arka planda çalışan bir sistem tepsisi uygulaması olarak çalıştırılabilir.
- **Logging:** Uygulama süreçlerini takip edebilmek için loglama mekanizması.

---

## 🛠 Gereksinimler

Aşağıdaki bağımlılıkların yüklenmiş olması gerekmektedir. Eğer eksik bir bağımlılık varsa `requirements.txt` dosyasını kullanarak yükleyebilirsiniz.

### Kullanılan Kütüphaneler

```bash
requests
beautifulsoup4
datetime
sqlite3
pystray
PIL
logging
json
re
ollama
```

### Bağımlılıkları Yükleme

```bash
pip install -r requirements.txt
```

---

## 📌 Kurulum ve Kullanım

1. **Projeyi klonlayın:**

   ```bash
   git clone https://github.com/hyperworth/crypto-news-analyzer.git
   cd crypto-news-analyzer
   ```

2. **Bağımlılıkları yükleyin:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Veritabanını oluşturun:** (İlk çalıştırmadan önce)

   ```bash
   python database.py
   ```

4. **Ana uygulamayı başlatın:**

   ```bash
   python main.py
   ```

5. **Belirli bir tarih aralığındaki haberlerin analizini yapmak için:**

   ```bash
   python sentiment.py
   ```

   Tarih formatı `YYYY-MM-DD` şeklinde olmalıdır.

---

## 🧐 Çalışma Mantığı

1. `main.py` başlatıldığında, CoinDesk gibi haber sitelerinden makaleler çeker ve veritabanına kaydeder.
2. Kullanıcı, `sentiment.py` dosyasını çalıştırarak belirli bir tarih aralığındaki haberleri analiz eder.
3. **Yapay zeka (Ollama modeli)**, haberlerin belirtilen kripto para birimi üzerindeki etkisini değerlendirir ve sonuçları JSON formatında saklar.
4. Sonuçlar bir dosyaya kaydedilir (`sentiment_analysis_results.json`).

---

## 📊 Örnek Kullanım

### 🔍 Örnek Haber ve Analiz Sonucu

Haber Başlığı: *"Bitcoin fiyatları yükselişte!"*

**Model Çıktısı:**

```json
{
    "Adress": "https://www.coindesk.com/bitcoin-price-news",
    "Date": "2025-02-17",
    "Article": "Bitcoin fiyatları son 24 saatte %5 arttı...",
    "score": 85
}
```

Bu, haberin **Bitcoin için oldukça olumlu** olduğunu gösterir.

---

## 📝 Geliştirme ve Katkı

Projeye katkıda bulunmak isterseniz, lütfen aşağıdaki adımları takip edin:

1. **Fork** edin ve yeni bir özellik eklemek için bir **branch** oluşturun.
2. Yaptığınız değişiklikleri **commit** edin ve **push** yapın.
3. Pull request açarak değişikliklerinizi paylaşın.

---

## ⚠️ Lisans

Bu proje **MIT Lisansı** altında dağıtılmaktadır.

**Hazırlayan:** [Muhammed Ali Uğur]

