import streamlit as st
import pandas as pd
import sqlite3
import subprocess

st.set_page_config(page_title="Market Analytics Pro", layout="wide")

# Sarlavha qismi
st.title("📊 Market Analytics & Price Tracker Platforma")
st.caption("Startap loyihangizning qidiruv va filtrlarga ega ilg'or MVP modeli")

# --- INTERNETDA MAJBURIY ISHGA TUSHIRISH TUGMASI ---
st.sidebar.header("🔄 Ma'lumotlar yangilash")
if st.sidebar.button("Bazani yangilash"):
    st.sidebar.info("Skraper ishga tushdi, biroz kuting...")
    subprocess.run(["python", "scraper.py"])
    st.sidebar.success("Ma'lumotlar bazaga muvaffaqiyatli yuklandi!")
    st.rerun()

st.sidebar.markdown("---")

# Boshqaruv paneli (Sidebar)
st.sidebar.header("⚙️ Boshqaruv Paneli")
platforma = st.sidebar.selectbox("Platformani tanlang:", ["Uzum Market", "OLX", "AliExpress"])

st.markdown(f"### 📍 Hozirgi tanlangan platforma: **{platforma}**")

def load_data_from_db():
    conn = sqlite3.connect("market_data.db")
    df = pd.read_sql_query("SELECT nomi, narxi, sotilgan, sana FROM products", conn)
    conn.close()
    return df

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

            st.markdown("---")
            st.subheader("📊 Mahsulotlarning narxlari solishtirmasi (Top 10)")
            top_10 = df.head(10)
            st.bar_chart(data=top_10, x="nomi", y="narxi")
        else:
            st.error("Bunday nomdagi mahsulot bazadan topilmadi!")
            
    else:
        st.warning("⚠️ Bazada ma'lumot yo'q! Iltimos, chap tarafdagi 'Bazani yangilash' tugmasini bosing.")

except Exception as e:
    st.warning("⚠️ Baza hali yaratilmagan! Iltimos, chap tarafdagi 'Bazani yangilash' tugmasini bosing.")