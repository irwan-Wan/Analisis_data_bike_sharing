import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_count_by_hour_df(hour_df):
  hour_count_df =  hour_df.groupby(by="hours").agg({"count_cr": ["sum"]})
  return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (hour_df):
    sum_order_items_df = hour_df.groupby("weather_situation").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def macem_season (day_df): 
    one_of_week_df = day_df.groupby(by="one_of_week").count_cr.sum().reset_index() 
    return one_of_week_df

days_df = pd.read_csv("day_data.csv")
hours_df = pd.read_csv("hour_data.csv")

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

max_season_df = days_df.loc[days_df.groupby("season")["count_cr"].idxmax()].sort_values(by="season")

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")

    st.subheader('By : Irwandika M.F ')
    st.subheader('Submission for Dicoding')
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])
    
    st.markdown('<p style="font-size:15px;">Data disamping merupakan rangkuman data dari penyewaan sepeda yang dilakukan dari 2011 hingga 2012</p>', unsafe_allow_html=True)

  
main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & 
                       (days_df["dteday"] <= str(end_date))]

main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & 
                        (hours_df["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
sum_order_items_df = sum_order(main_df_hour)
one_of_week_df = macem_season(main_df_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Sharing :sparkles:')



st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.count_cr.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("performa penyewaan berdasarkan tiap season di tahun 2012?")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    max_season_df["season"],
    max_season_df["count_cr"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.markdown('<p style="font-size:20px;">Berdasarkan data yang kita lihat, performa penjualan tertinggi berada pada season Fall dengan winter di urutan kedua</p>', unsafe_allow_html=True)

st.subheader("Hari apa penyewaan sepeda terbanyak??")

colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3",  "#90CAF9",  "#90CAF9",  "#D3D3D3"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
        y="count_cr", 
        x="one_of_week",
        data=one_of_week_df.sort_values(by="one_of_week", ascending=False),
        palette=colors,
        ax=ax
    )
ax.set_title("Grafik Antar Hari", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.markdown('<p style="font-size:20px;">Hasil yang di dapat pada grafik di atas terlihat hari jumat merupakan hari dimana terjadi paling banyak penyewaan sepeda. dan paling sedikit di hari minggu.</p>', unsafe_allow_html=True)




st.subheader("Pada cuaca apa penyewa sepeda paling banyak dan paling sedikit?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="weather_situation", y="count_cr", data=sum_order_items_df.head(4), palette=["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Cuaca dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=25)


sns.barplot(x="weather_situation", y="count_cr", data=sum_order_items_df.sort_values(by="weather_situation", ascending=True).head(4), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Cuaca dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=25)

 
st.pyplot(fig)


st.markdown('<p style="font-size:20px;">Penyewaan sepeda paling banyak terjadi pada cuaca clear dan sebaliknya pada cuaca heavy rainsnow tidak ada yang melakukan penyewaan sepeda</p>', unsafe_allow_html=True)






st.subheader("Perbandingan Customer yang Registered dengan casual")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')  

st.pyplot(fig1)


st.markdown('<p style="font-size:20px;">Dari grafik yang dapat kita lihat, Registered = 81.2% dengan casual sebesar 18.8%</p>', unsafe_allow_html=True)
