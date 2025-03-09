import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px

# 🎯 Tentukan path folder tempat file berada
file_path = 'D:/Analisis Data/DB Camp/submisi/'  # Sesuaikan dengan lokasi folder kamu

# 📂 Daftar nama file
file_names = [
    'PRSA_Data_Aotizhongxin_20130301-20170228.csv',
    'PRSA_Data_Changping_20130301-20170228.csv',
    'PRSA_Data_Dingling_20130301-20170228.csv',
    'PRSA_Data_Guanyuan_20130301-20170228.csv',
    'PRSA_Data_Gucheng_20130301-20170228.csv',
    'PRSA_Data_Huairou_20130301-20170228.csv',
    'PRSA_Data_Nongzhanguan_20130301-20170228.csv',
    'PRSA_Data_Shunyi_20130301-20170228.csv',
    'PRSA_Data_Tiantan_20130301-20170228.csv',
    'PRSA_Data_Wanliu_20130301-20170228.csv',
    'PRSA_Data_Wanshouxigong_20130301-20170228.csv'
]

# 📊 Gabungkan semua dataset menjadi satu DataFrame
combined_df = pd.concat([pd.read_csv(os.path.join(file_path, file)) for file in file_names], ignore_index=True)

# 🗓️ Konversi ke datetime
combined_df['year'] = pd.to_datetime(combined_df['year'], format='%Y')

# 🎈 Sidebar - Pilihan Pertanyaan
st.sidebar.title("🌍 Kualitas Udara di Beijing")
st.sidebar.write("Analisis data kualitas udara berdasarkan berbagai stasiun pemantauan di Beijing.")

# Informasi dataset
num_rows, num_cols = combined_df.shape
start_year = combined_df['year'].dt.year.min()
end_year = combined_df['year'].dt.year.max()
stations = combined_df['station'].unique()

st.sidebar.write(f"📊 **Jumlah Data:** {num_rows} baris, {num_cols} kolom")
st.sidebar.write(f"📅 **Periode Waktu:** {start_year} - {end_year}")
st.sidebar.write(f"📍 **Jumlah Stasiun:** {len(stations)}")

questions = {
    "Pertanyaan 1": "Bagaimana tren tahunan, bulanan, dan harian dari konsentrasi polutan utama (PM2.5, PM10, SO2, NO2, O3)?",
    "Pertanyaan 2": "Bagaimana perbandingan rata-rata kualitas udara antar stasiun pemantauan?",
    "Pertanyaan 3": "Pada jam berapa dalam sehari konsentrasi polutan utama cenderung mencapai puncaknya?"
}

selected_question = st.sidebar.radio("🔍 Pilih Pertanyaan:", list(questions.keys()))

# 🎯 Judul Dashboard
st.title("📊 Dashboard Analisis Kualitas Udara Beijing")
st.write(f"### {selected_question}")
st.write(questions[selected_question])

# ✨ Analisis Berdasarkan Pertanyaan yang Dipilih
if selected_question == "Pertanyaan 1":
    trend_option = st.selectbox("📈 Pilih Tren Waktu", ['Tahunan', 'Bulanan', 'Harian'])
    polutan_list = ['PM2.5', 'PM10', 'SO2', 'NO2', 'O3']
    selected_pollutants = st.multiselect("🧪 Pilih Polutan untuk Ditampilkan", polutan_list, default=['PM2.5', 'PM10'])

    if trend_option == 'Tahunan':
        yearly_trend = combined_df.groupby('year')[selected_pollutants].mean().reset_index()
        fig = px.line(yearly_trend, x='year', y=selected_pollutants, markers=True, title="📅 Tren Tahunan")
        st.plotly_chart(fig)

    elif trend_option == 'Bulanan':
        monthly_trend = combined_df.groupby('month')[selected_pollutants].mean().reset_index()
        fig = px.line(monthly_trend, x='month', y=selected_pollutants, markers=True, title="📆 Tren Bulanan")
        st.plotly_chart(fig)

    elif trend_option == 'Harian':
        daily_trend = combined_df.groupby('day')[selected_pollutants].mean().reset_index()
        fig = px.line(daily_trend, x='day', y=selected_pollutants, markers=True, title="📊 Tren Harian")
        st.plotly_chart(fig)
        
    with st.expander('Penjelasan') :
        st.write(''' 
        1.   Tren Tahunan :
        PM10 dan PM2.5 cenderung mengalami fluktuasi setiap tahun, tetapi tetap berada dalam rentang konsentrasi yang tinggi. PM10 mencapai puncaknya sekitar tahun 2014, mengalami sedikit penurunan, lalu meningkat lagi pada tahun 2017. O3 mengalami sedikit penurunan di tahun 2016 dan menurun lebih tajam pada 2017.
        SO2 relatif stabil dengan sedikit kenaikan di tahun 2017. NO2 mengalami tren penurunan pada 2015–2016, tetapi kembali meningkat pada 2017.
        2. Tren Bulanan :
        PM10 dan PM2.5 cenderung meningkat pada awal dan akhir tahun (Januari–Maret, serta Oktober–Desember), sedangkan menurun pada pertengahan tahun. O3 mengalami pola yang berlawanan dengan PM10 dan PM2.5, dengan konsentrasi tertinggi pada pertengahan tahun (Juni–Agustus). SO2 dan NO2 memiliki fluktuasi yang lebih stabil, dengan tren yang tidak terlalu ekstrem dibanding polutan lainnya.
        3. Tren Harian :
        Konsentrasi PM10 dan PM2.5 menunjukkan pola yang berulang setiap bulan, dengan puncak konsentrasi sekitar pertengahan bulan. SO2 dan NO2 tetap relatif stabil dengan sedikit variasi harian. O3 menunjukkan sedikit peningkatan di pertengahan bulan, namun tidak setajam PM10 dan PM2.5.
        ''')

elif selected_question == "Pertanyaan 2":
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'O3']
    selected_pollutants = st.multiselect("🌡️ Pilih Polutan:", pollutants, default=pollutants)
    all_stations = combined_df['station'].unique().tolist()
    selected_stations = st.multiselect("🏢 Pilih Stasiun:", all_stations, default=all_stations[:5])

    station_avg = combined_df.groupby('station')[selected_pollutants].mean()

    filtered_data = station_avg.loc[selected_stations, selected_pollutants]

    st.write("### 📊 Rata-rata Polutan per Stasiun")
    fig, ax = plt.subplots(figsize=(12, 6))
    filtered_data.plot(kind='bar', ax=ax)
    plt.xlabel('Stasiun')
    plt.ylabel('Konsentrasi (µg/m³)')
    plt.xticks(rotation=45)
    plt.legend(title="Polutan")
    st.pyplot(fig)

    with st.expander('Penjelasan') :
        st.write(''' 
        1. Stasiun dengan Polusi Udara Terparah yaitu Nongzhanguan, Dongsi, dan Tiantan. Stasiun ini memiliki tingkat polusi yang lebih tinggi dibandingkan yang lain, terutama dari PM10 dan NO2.
        2. Stasiun dengan Kualitas Udara Lebih Baik yaitu Dingling dan Huairou cenderung memiliki konsentrasi polutan lebih rendah dibandingkan stasiun lainnya.
        3. PM10 memiliki konsentrasi tertinggi dibandingkan polutan lain di hampir semua stasiun. Stasiun Nongzhanguan memiliki konsentrasi PM10 tertinggi (~119.4 µg/m³), diikuti oleh Dongsi dan Tiantan.
        4. Stasiun dengan konsentrasi PM2.5 yang relatif tinggi adalah Dongsi dan Gucheng. Polutan NO2 memiliki variasi besar antar stasiun, dengan Tiantan memiliki tingkat tertinggi (~64.7 µg/m³).
        5. SO2 memiliki konsentrasi rendah di semua stasiun, dengan Dingling sebagai yang terendah (~ 11.7 µg/m³). Polutan O3 cenderung lebih merata, tetapi Dingling memiliki konsentrasi tertinggi (~ 68.9 µg/m³).
        ''')

elif selected_question == "Pertanyaan 3":
    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'O3']
    selected_pollutant = st.selectbox("⚡ Pilih Polutan:", pollutants)
    hour_range = st.slider("⏳ Pilih Rentang Jam:", 0, 23, (0, 23))

    hourly_avg = combined_df.groupby('hour')[pollutants].mean().reset_index()
    filtered_data = hourly_avg[(hourly_avg['hour'] >= hour_range[0]) & (hourly_avg['hour'] <= hour_range[1])]

    st.write("### ⏰ Tren Harian Berdasarkan Jam")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=filtered_data, x='hour', y=selected_pollutant, marker='o', linewidth=2, ax=ax)
    plt.xlabel('Jam dalam Sehari')
    plt.ylabel('Konsentrasi (µg/m³)')
    plt.xticks(range(hour_range[0], hour_range[1] + 1, 1))
    plt.grid()
    st.pyplot(fig)

    with st.expander('Penjelasan') :
        st.write(''' 
        1. Polutan PM2.5 : Cenderung mengalami kenaikan di malam hari dan mencapai puncaknya sekitar pukul 22.00 - 23.00.
        2. Polutan PM10 : Memiliki tren yang mirip dengan PM2.5, dengan puncak konsentrasi terjadi sekitar 21.00 - 23.00.
        3. Polutan SO2 : Konsentrasi relatif stabil dengan sedikit peningkatan di sore hari, tetapi tidak ada lonjakan signifikan.
        4. Polutan NO2 : Mengalami peningkatan tajam mulai pukul 10.00 dan mencapai puncaknya sekitar 16.00 - 17.00, kemudian menurun setelahnya.
        5. Polutan O3 : Konsentrasi meningkat secara signifikan mulai pagi hingga siang hari, mencapai puncaknya sekitar 15.00 - 16.00, lalu menurun setelahnya.
        ''')

st.write("### 🎉 Dashboard Selesai 🚀")
