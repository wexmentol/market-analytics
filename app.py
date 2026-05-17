import streamlit as px
import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Sahifa sozlamalari
st.set_page_config(page_title="Market Analytics Pro", page_icon="📊", layout="wide")


st.title("📊 BOZOR TAHLILCHISI VA NARXLARNI KUZATUVCHI SAYT")
st.caption("Startup loyihaylarning eng ilg'or modeli")

st.markdown("---")

st.markdown("### 👨‍💻 Loyiha muallifi: **GOFUROV FAYOZBEK**")
st.caption("DASTURCHI va STARTUP LOYIHALAR ASOSCHISI")

st.markdown("---")

# Ma'lumotlar bazasi fayli
DB_FILE = "market_data.csv"

if not os.path.exists(DB_FILE):
    dummy_data = {
        "nomi": [
            "Rain Jacket Women Windbreaker Striped Climbing Raincoats",
            "Professional Sports Backpack 40L",
            "Men's Casual Slim Fit Jacket",
            "Wireless Bluetooth Earbuds Pro",
            "Smart Watch Series 8 Sport",
            "Ergonomic Gaming Mouse Wireless",
            "Mechanical Gaming Keyboard RGB",
            "Portable Power Bank 20000mAh",
            "4K Ultra HD Action Camera",
            "Samsung A25 + 5G",
        ],
        "narxi": [499875, 350000, 420000, 250000, 1200000, 180000, 450000, 300000, 850000, 150000],
        "sotilgan": [679, 450, 320, 1200, 850, 1500, 600, 950, 210, 430],
        "sana": ["2026-05-16"] * 10
    }
    df = pd.DataFrame(dummy_data)
    df.to_csv(DB_FILE, index=False)

# Bazani o'qish
df = pd.read_csv(DB_FILE)

# Yon panel (Sidebar)
st.sidebar.title("🔄 Ma'lumotlar yangilash")
if st.sidebar.button("Bazani yangilash"):
    st.sidebar.success("Ma'lumotlar muvaffaqiyatli yangilandi!")

st.sidebar.markdown("---")
st.sidebar.title("⚙️ Boshqaruv Paneli")
platforma = st.sidebar.selectbox("Platformani tanlang:", ["Uzum Market"])
st.markdown(f"### 📍 Hozirgi tanlangan platforma: {platforma} 🔗")

# Aqlli qidiruv va filtrlash
st.markdown("### 🔍 Aqlli Qidiruv va Filtrlash")

col1, col2 = st.columns(2)
with col1:
    qidiruv = st.text_input("Mahsulot nomini kiriting:", placeholder="Masalan: Backpack, Jacket...")
with col2:
    saralash = st.selectbox("Saralash turi:", ["Sotilganlar soni bo'yicha (Kamayish)", "Narxi bo'yicha (O'sish)", "Narxi bo'yicha (Kamayish)"])

# Filtrlash jarayoni
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
    m2.metric("Eng yuqori narx", f"{df['narxi'].max():,} so'm".replace(",", " "))
    m3.metric("Eng ko'p sotilgan", f"{df['sotilgan'].max()} ta")
else:
    m2.metric("Eng yuqori narx", "0 so'm")
    m3.metric("Eng ko'p sotilgan", "0 ta")

st.markdown("---")

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
st.markdown("<p style='text-align: center; color: gray; font-size: 14px;'>© 2026 Fayozbek Napalionov | Dasturchi va G'oya muallifi</p>", unsafe_allow_html=True)