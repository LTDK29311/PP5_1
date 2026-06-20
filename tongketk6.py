import sqlite3
import streamlit as st
import pandas as pd
import os
st.set_page_config(page_title="Tiến Độ Công Việc", layout="wide")
st.title('📝 Quản Lý Tiến Độ Công Việc')
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks.db')
def S_query(sql, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(sql, params)
        conn.commit()
        return c.fetchall()
S_query('''CREATE TABLE IF NOT EXISTS cv (
    id INTEGER PRIMARY KEY AUTOINCREMENT, tên TEXT, trạng_thái TEXT, ghi_chú TEXT)''')
col_luu, col_sua = st.columns(2)
with col_luu:
    st.subheader("➕ Thêm công việc mới")
    with st.form("add_form", clear_on_submit=True):
        ten = st.text_input("Tên công việc:")
        trang_thai = st.selectbox("Trạng thái:", ["Chưa bắt đầu", "Đang làm", "Hoàn thành"])
        ghi_chu = st.text_area("Ghi chú:")
        if st.form_submit_button("Lưu công việc") and ten:
            S_query("INSERT INTO cv (tên, trạng_thái, ghi_chú) VALUES (?, ?, ?)", (ten, trang_thai, ghi_chu))
            st.success("Đã lưu!")
            st.rerun()
data = S_query("SELECT * FROM cv")
df = pd.DataFrame(data, columns=["ID", "Tên", "Trạng thái", "Ghi chú"]) if data else pd.DataFrame()
with col_sua:
    st.subheader("✏️ Sửa đổi / Cập nhật")
    if not df.empty:
        id_sua = st.selectbox("Chọn ID công việc cần sửa:", df["ID"].tolist())
        row = df[df["ID"] == id_sua].iloc[0]
        ten_new = st.text_input("Sửa tên:", value=row["Tên"])
        tt_new = st.selectbox("Sửa trạng thái:", ["Chưa bắt đầu", "Đang làm", "Hoàn thành"],
                              index=["Chưa bắt đầu", "Đang làm", "Hoàn thành"].index(row["Trạng thái"]))
        gc_new = st.text_area("Sửa ghi chú:", value=row["Ghi chú"])
        c1, c2 = st.columns(2)
        if c1.button("🔥 Cập nhật"):
            S_query("UPDATE cv SET tên=?, trạng_thái=?, ghi_chú=? WHERE id=?", (ten_new, tt_new, gc_new, id_sua))
            st.success("Đã cập nhật!")
            st.rerun()
        if c2.button("🗑️ Xóa việc này"):
            S_query("DELETE FROM cv WHERE id=?", (id_sua,))
            st.warning("Đã xóa!")
            st.rerun()
    else:
        st.info("Chưa có công việc nào để sửa.")
st.markdown("---")
st.subheader("📋 Danh sách công việc hiện tại")
if not df.empty:
    st.dataframe(df, hide_index=True, use_container_width=True)
else:
    st.write("Trống.")
