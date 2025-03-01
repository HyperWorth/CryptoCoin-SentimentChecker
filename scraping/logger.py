import logging

def setup_logger():
    # Logger'ı oluştur
    logger = logging.getLogger("CoinDeskScraper")
    
    # Logger seviyesini DEBUG olarak ayarla
    logger.setLevel(logging.DEBUG)
    
    # Konsola log yazmak için bir handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Konsolda sadece INFO seviyesindeki logları göster
    
    # Dosyaya log yazmak için bir handler
    file_handler = logging.FileHandler('log\scraper.log')
    file_handler.setLevel(logging.DEBUG)  # Dosyaya DEBUG seviyesindeki tüm logları yaz

    # Format belirleme
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Handler'ları logger'a ekle
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
