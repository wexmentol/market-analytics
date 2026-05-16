import sqlite3
from datetime import datetime

DB_NAME = "market_data.db"

def init_db():
    """Bazani va undagi jadvalni yaratish"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Mahsulotlarni saqlash uchun jadval
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nomi TEXT,
            narxi REAL,
            sotilgan INTEGER,
            sana TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_products_to_db(products_list):
    """Skraperdan kelgan hamma tovarlarni bazaga saqlash"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    bugun = datetime.now().strftime("%Y-%m-%d")
    
    for prod in products_list:
        cursor.execute('''
            INSERT INTO products (nomi, narxi, sotilgan, sana)
            VALUES (?, ?, ?, ?)
        ''', (prod['Nomi'], prod['Narxi'], prod['Sotilgan'], bugun))
        
    conn.commit()
    conn.close()
    print(f"✅ {len(products_list)} ta tovar muvaffaqiyatli bazaga saqlandi!")

def get_all_products_from_db():
    """Bazadagi hamma ma'lumotni o'qib olish (Dashboard uchun)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT nomi, narxi, sotilgan, sana FROM products")
    rows = cursor.fetchall()
    
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()
    print("Baza tayyorlandi!")