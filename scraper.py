import requests

def get_uzum_products():
    # Bu ochiq test do'kon API'si (Hamma uchun ochiq)
    url = "https://fakestoreapi.com/products"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            products = response.json()
            
            cleaned_products = []
            for prod in products:
                title = prod.get('title')
                price = prod.get('price', 0) * 12500 # Dollarni so'mga simulyatsiya qilamiz
                orders = prod.get('rating', {}).get('count', 0) # Sotilganlar soni
                
                cleaned_products.append({
                    "Nomi": title,
                    "Narxi": price,
                    "Sotilgan": orders
                })
            return cleaned_products
    except Exception as e:
        print(f"Ulanishda xatolik: {e}")
        return []
    return []

# scraper.py faylining eng tagiga qo'shasiz:
if __name__ == "__main__":
    from database import init_db, save_products_to_db
    
    print("🚀 Skraper va Baza ulanishi boshlandi...")
    init_db() # Birinchi marta bo'lsa bazani ochadi
    
    tovarlar = get_uzum_products()
    if tovarlar:
        save_products_to_db(tovarlar) # Ma'lumotni bazaga tiqadi
    else:
        print("Xatolik: Ma'lumot yig'ilmadi.")