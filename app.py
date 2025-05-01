
import streamlit as st
import pandas as pd
import os

# Oy verecek isimler
players = [
    "İlker", "Feyyaz", "Yusuf", "Furkan", "Bedirhan",
    "Muhammed", "Alperen", "Cemil", "Ufuk", "Serdar Öztürk",
    "Serdar Çakal", "Alihan", "Haris", "Buğra", "Nisan"
]

data_file = "oylar.csv"
voted_file = "oy_kullananlar.txt"

st.set_page_config(page_title="Halı Saha Oylama", page_icon="⚽")

st.title("⚽ Halı Saha Oyuncu Oylama")
st.write("Her oyuncuya 1–10 arası puan ver. Oylar gizli, sonuçlar herkes için açık!")

# Oy kullanan kişiyi sor
name = st.text_input("Adınızı girin (oy kullanan kişi):")

if name:
    if name not in players:
        st.warning("Bu isim listede yok.")
    else:
        # daha önce oy kullanmış mı kontrol et
        if os.path.exists(voted_file):
            with open(voted_file, "r") as f:
                voted_names = f.read().splitlines()
        else:
            voted_names = []

        if name in voted_names:
            st.error("Zaten oy kullandınız!")
        else:
            st.success("Oy verebilirsiniz.")

            vote_dict = {}
            for player in players:
                if player != name:
                    vote = st.slider(f"{player} için puanınız:", 1, 10, 5)
                    vote_dict[player] = vote

            if st.button("Oylamayı Gönder"):
                # oyları CSV'ye ekle
                df = pd.DataFrame([vote_dict])
                if os.path.exists(data_file):
                    df.to_csv(data_file, mode='a', header=False, index=False)
                else:
                    df.to_csv(data_file, index=False)

                with open(voted_file, "a") as f:
                    f.write(name + "\n")

                st.success("Oyunuz kaydedildi! Teşekkürler.")

# Herkese açık sonuç bölümü
st.markdown("---")
st.subheader("📊 Anlık Ortalama Sonuçlar")

if os.path.exists(data_file):
    df_all = pd.read_csv(data_file)
  for p in players:
    if p not in df_all.columns:
        df_all[p] = pd.NA

avg_scores = df_all[players].mean().sort_values(ascending=False)
    st.table(avg_scores.round(2).reset_index().rename(columns={"index": "Oyuncu", 0: "Ortalama Puan"}))
else:
    st.info("Henüz hiç oy verilmedi.")
