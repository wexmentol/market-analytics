import streamlit as st
import pandas as pd
import sqlite3
import requests
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Market Analytics Pro", layout="wide")

DB_NAME = "market_data.db"

# --- INTERNETDAN REAL MA'LUMOT OLISH FUNKSIYASI ---
def get_and_save_data():
    url = "https://fakestoreapi.com/products"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            products = response.json()
            
            # Bazani ochamiz va jadvalni yaratamiz
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nomi TEXT,
                    narxi REAL,
                    sotilgan INTEGER,
                    sana TEXT
                )
            ''')
            
            bugun = datetime.now().strftime("%Y-%m-%d")
            
            # Ma'lumotlarni bazaga yozamiz
            for prod in products:
                title = prod.get('title')
                price = prod.get('price', 0) * 12500  # so'mga simulyatsiya
                orders = prod.get('rating', {}).get('count', 0)
                
                cursor.execute('''
                    INSERT INTO products (nomi, narxi, sotilgan, sana)
                    VALUES (?, ?, ?, ?)
                ''', (title, price, orders, bugun))
                
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        st.sidebar.error(f"Xatolik: {e}")
        return False
    return False

# Sarlavha qismi

st.title("📊 BOZOR TAHLILCHISI VA NARXLARNI KUZATUVCHI SAYT")
st.caption("Startap loyihaning ega ilg'or modeli")

st.markdown("### 👨‍💻 Loyiha muallifi: **GOFUROV FAYOZBEK**")
st.markdown(" DASTURCHI va STARTUP LOYIHALAR ASOSCHISI")
# --- MAJBURIY YANGILASH TUGMASI ---
st.sidebar.header("🔄 Ma'lumotlar yangilash")
if st.sidebar.button("Bazani yangilash"):
    with st.sidebar.spinner("Internetdan ma'lumot yuklanmoqda..."):
        success = get_and_save_data()
        if success:
            st.sidebar.success("Ma'lumotlar bazaga yuklandi!")
            st.rerun()
        else:
            st.sidebar.error("Yuklashda xatolik bo'ldi.")

st.sidebar.markdown("---")

# Boshqaruv paneli (Sidebar)
st.sidebar.header("⚙️ Boshqaruv Paneli")
platforma = st.sidebar.selectbox("Platformani tanlang:", ["Uzum Market", "OLX", "AliExpress"])

st.markdown(f"### 📍 Hozirgi tanlangan platforma: **{platforma}**")

def load_data_from_db():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT nomi, narxi, sotilgan, sana FROM products", conn)
    conn.close()
    return df

# Asosiy qism: ma'lumotlarni tekshirish va chiqarish
try:
    df = load_data_from_db()
    
    if not df.empty:
        st.markdown("---")
        st.subheader("🔍 Aqlli Qidiruv va Filtrlash")
        
        col_search, col_sort = st.columns([2, 1])
        with col_search:
            qidiruv_sozi = st.text_input("Mahsulot nomini kiriting:", "", placeholder="Masalan: Backpack, Jacket...")
        with col_sort:
            saralash = st.selectbox("Saralash turi:", ["Sotilganlar soni bo'yicha (Kamayish)", "Narxi bo'yicha (O'sish)", "Narxi bo'yicha (Kamayish)"])

        if qidiruv_sozi:
            df = df[df['nomi'].str.contains(qidiruv_sozi, case=False, na=False)]

        if saralash == "Sotilganlar soni bo'yicha (Kamayish)":
            df = df.sort_values(by="sotilgan", ascending=False)
        elif saralash == "Narxi bo'yicha (O'sish)":
            df = df.sort_values(by="narxi", ascending=True)
        elif saralash == "Narxi bo'yicha (Kamayish)":
            df = df.sort_values(by="narxi", ascending=False)

        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        if not df.empty:
            col1.metric("Topilgan mahsulotlar", f"{len(df)} ta")
            col2.metric("Eng yuqori narx", f"{int(df['narxi'].max()):,} so'm")
            col3.metric("Eng ko'p sotilgan", f"{int(df['sotilgan'].max())} ta")

            st.subheader("📋 Filtrlangan mahsulotlar ro'yxati")
            st.dataframe(df, use_container_width=True)

        st.subheader("📊 Mahsulotlarning narxlari solishtirmasi (Top 10)")

# Rang-barang (qizil-ko'k-sariq jiloli) 
fig = px.bar(
    x="nomi", 
    y="narxi", 
    color="narxi", # Narxiga qarab avtomatik rang beriladi
    labels={"nomi": "Mahsulot nomi", "narxi": "Narxi (so'm)"},
    color_continuous_scale=px.colors.sequential.Plasma # ranglar gammasi (ko'k, binafsha, qizil, sariq)
)

# Grafik dizaynini saytning qora foni bilan moslashtirish
fig.update_layout(
    template="plotly_dark",
    xaxis_tickangle=-45,
    margin=dict(l=20, r=20, t=20, b=100)
)

# Grafikni saytda ko'rsatish
st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Bunday nomdagi mahsulot bazadan topilmadi!")
            
    else:
        st.warning("⚠️ Bazada ma'lumot yo'q! Iltimos, chap tarafdagi 'Bazani yangilash' tugmasini bosing.")

except Exception as e:
    st.warning("⚠️ Baza hali yaratilmagan! Iltimos, chap tarafdagi 'Bazani yangilash' tugmasini bosing.")
# app.py ichidagi hamma grafiklar kodidan keyin joylashtiring:
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>© 2026 GOFUROV FAYOZBEK | Dasturchi va Startup loyihalar asoschisi</p>", unsafe_allow_html=True)