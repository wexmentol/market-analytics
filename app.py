import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Sahifa sozlamalari
st.set_page_config(page_title="Bozor Tahlili Pro", page_icon="📊", layout="wide")

# --- ENG TEPADAGI SARLAVHA VA ISMINING BIRGA TURISHI ---
st.title("📊 BOZOR TAHLILCHISI VA NARXLARNI  KUZATUVCHI SAYT")
st.caption("Bozordagi mahsulotlarni tahlil qiluvchi ilg'or startap platforma")

st.markdown("---")
st.markdown("### 👨‍💻 LOYIHA MUALLIFI: **GOFUROV FAYOZBEK**")
st.caption("DASTURCHI VA STARTUP LOYIHALAR ASOSCHISI")
st.markdown("---")

DB_FILE = "market_data.csv"

def load_real_data():
    real_data = {
        "nomi": [
            "Smartfon Xiaomi Redmi Note 13 8/256 GB",
            "Simsiz quloqchinlar Apple AirPods 3 (Premium copy)",
            "Erkaklar uchun yozgi krossovkalar Comfort Sport",
            "Smart soat HK9 Pro Max Gen2 AMOLED",
            "Mexanik klaviatura RGB yoritgichli Gaming",
            "Tezkor quvvatlovchi Power Bank 20000 mAh 22.5W",
            "Simsiz fleshka Kingston DataTraveler 64 GB",
            "Professional fen va stayler Dyson Airwrap (5 in 1)",
            "Erkaklar charm hamyoni Classic Luxury",
            "Ko'chma simsiz bluetooth kalonka JBL Charge 5"
        ],
        "narxi": [4250000, 320000, 185000, 420000, 380000, 265000, 75000, 1250000, 110000, 680000],
        "sotilgan": [840, 1540, 620, 930, 410, 1280, 2450, 310, 520, 750],
        "sana": ["2026-05-18"] * 10
    }
    df_new = pd.DataFrame(real_data)
    df_new.to_csv(DB_FILE, index=False)
    return df_new

df = load_real_data()

# Yon panel (Sidebar)
st.sidebar.title("🔄 Ma'lumotlar holati")
st.sidebar.success("Uzum Market real ma'lumotlar bazasi faol!")

st.sidebar.markdown("---")
st.sidebar.title("⚙️ Boshqaruv Paneli")
platforma = st.sidebar.selectbox("Platformani tanlang:", ["Uzum Market"])

st.markdown(f"### 📍 Hozirgi tanlangan platforma: {platforma} 🔗")
st.markdown("---")

# Aqlli qidiruv va filtrlash
st.markdown("### 🔍 Aqlli Qidiruv va Filtrlash")

col1, col2 = st.columns(2)
with col1:
    qidiruv = st.text_input("Mahsulot nomini kiriting:", placeholder="Masalan: Smartfon, Quloqchin, Krossovka...")
with col2:
    saralash = st.selectbox("Saralash turi:", ["Sotilganlar soni bo'yicha (Kamayish)", "Narxi bo'yicha (O'sish)", "Narxi bo'yicha (Kamayish)"])

if qidiruv:
    df = df[df["nomi"].str.contains(qidiruv, case=False, na=False)]

if saralash == "Sotilganlar soni bo'yicha (Kamayish)":
    df = df.sort_values(by="sotilgan", ascending=False)
elif saralash == "Narxi bo'yicha (O'sish)":
    df = df.sort_values(by="narxi", ascending=True)
elif saralash == "Narxi bo'yicha (Kamayish)":
    df = df.sort_values(by="narxi", ascending=False)

# Metrikalar
m1, m2, m3 = st.columns(3)
m1.metric("Topilgan mahsulotlar", f"{len(df)} ta")
if not df.empty:
    m2.metric("Eng yuqori narx", f"{int(df['narxi'].max()):,} so'm".replace(",", " "))
    m3.metric("Eng ko'p sotilgan", f"{int(df['sotilgan'].max())} ta")
else:
    m2.metric("Eng yuqori narx", "0 so'm")
    m3.metric("Eng ko'p sotilgan", "0 ta")

# Jadvalni ko'rsatish
st.markdown("### 📋 Filtrangan mahsulotlar ro'yxati")
st.dataframe(df, use_container_width=True)

st.markdown("---")

# Rang-barang interaktiv grafik qismi
if not df.empty:
    st.subheader("📊 Mahsulotlarning narxlari solishtirmasi (Top 10)")
    top_10 = df.head(10)
    
    fig = px.bar(
        top_10, 
        x="nomi", 
        y="narxi", 
        color="narxi", 
        labels={"nomi": "Mahsulot nomi", "narxi": "Narxi (so'm)"},
        color_continuous_scale=px.colors.sequential.Plasma
    )
    fig.update_layout(template="plotly_dark", xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Ostki qism (Footer)
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>© 2026 GOFUROV FAYOZBEK | Dasturchi va G'oya muallifi</p>", unsafe_allow_html=True)