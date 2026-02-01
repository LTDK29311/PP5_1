import streamlit as st
import pandas as pd
# B1: Ghi dữ liệu vào file CSV 
csv_data = """ID KH,Tuổi,Giới tính,Thu nhập,Nghề nghiệp,Điểm tín dụng,SP đã mua,Giá,Số lượng,Ngày mua hàng
1,30,Nam,50000,Kỹ sư phần mềm,750,Điện thoại,500,1,2026-1-15
2,25,Nữ,30000,Giáo viên,680,Máy tính,700,1,2025-12-10
3,40,Nam,75000,Bác sĩ,820,Tivi,1000,1,2026-1-02
4,50,Nữ,40000,Chủ doanh nghiệp,700,Tủ lạnh,1200,2,2025-12-28
5,60,Nam,60000,Nghỉ hưu,800,Máy Giặt,1500,1,2025-12-30
"""

with open("pro5.8.csv", "w", encoding="utf-8") as f:
    f.write(csv_data)

# B2: Đọc dữ liệu
df = pd.read_csv("pro5.8.csv")

st.title("Phân tích DL KH (pro5.8.csv)")
st.subheader("Dữ liệu gốc:")
st.dataframe(df)

# B3: Phân tích cơ bản
roi_bo = df[df["Điểm tín dụng"] <= 700]["ID KH"].tolist()
mua_hang = df[(df["Thu nhập"] >= 50000) & (df["Điểm tín dụng"] >= 750)]["ID KH"].tolist()
# chi_tieu = df[df["Nghề nghiệp"].isin(["Bác sĩ", "Chủ doanh nghiệp"])]["ID KH"].tolist()
chi_tieu = df[df["Thu nhập"] >= 60000]["ID KH"].tolist()

# Khách hàng đã mua hàng tháng trước và có điểm tín dụng >= 700
import datetime
thang_hien_tai = datetime.datetime.now().month
thang_truoc = thang_hien_tai - 1 if thang_hien_tai > 1 else 12
phan_hoi = df[
    (pd.to_datetime(df["Ngày mua hàng"]).dt.month == thang_truoc)
    & (df["Điểm tín dụng"] > 700)
]["ID KH"].tolist()

# B4: Hiển thị kết quả
st.subheader("Kết quả phân tích:")
st.write("**KH có khả năng rời bỏ:**", roi_bo)
st.write("**KH có khả năng mua hàng tháng tới:**", mua_hang)
st.write("**KH có khả năng chi tiêu nhiều hơn:**", chi_tieu)
st.write("**KH đã mua hàng tháng trước và có điểm tín dụng >700:**", phan_hoi)
