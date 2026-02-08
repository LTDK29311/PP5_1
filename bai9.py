import streamlit as st
import pandas as pd
df=pd.read_csv('data.csv')
st.title('Phân tích giá nhà HN')
st.subheader('DL gốc')
st.dataframe(df)
st.subheader('Nhà có giá trên 100tr/m2')
gia_100=df[df['Giá bán/m2']>100]
st.dataframe(gia_100)
st.subheader('Quận có giá cao nhất,thấp nhất')
q_cao=df.groupby('Quận/Huyện')['Giá bán (tổng)'].max().idxmax()
q_thap=df.groupby('Quận/Huyện')['Giá bán (tổng)'].min().idxmin()
st.write('Quận có giá nhà cao nhất: ',q_cao)
st.write('Quận có giá nhà thấp nhất: ',q_thap)
st.subheader('Loại hình có giá nhà cao nhất')
l_cao=df.groupby('Loại hình nhà ở')['Giá bán (tổng)'].mean().idxmax()
st.write('Loại hình có giá nhà cao nhất: ',l_cao)
