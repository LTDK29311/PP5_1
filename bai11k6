import sqlite3
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'weather.db')
def get_connection():
    return sqlite3.connect(DB_PATH)
def create_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS favorite_cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT NOT NULL UNIQUE,
            added_date TEXT,
            notes TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
def add_city(city_name):
    try:
        with get_connection() as conn:
            conn.execute('INSERT INTO favorite_cities (city_name) VALUES (?)', (city_name,))
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print('DB ERROR:', e)
        return False
def view_all_cities():
    with get_connection() as conn:
        return pd.read_sql_query("SELECT * FROM favorite_cities", conn)
def delete_city(city_name):
    with get_connection() as conn:
        conn.execute('DELETE FROM favorite_cities WHERE city_name=?', (city_name,))
def register_user(username, password):
    try:
        with get_connection() as conn:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        return True
    except sqlite3.IntegrityError:
        return False
def login_user(username, password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        return c.fetchone() is not None
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8-sig')
# API_KEY = st.secrets["My_api"]
API_KEY = "5562519f07a31e9b7a94036194028aeb"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast" # map
def get_weather(city_name):
    try:
        url = f"{BASE_URL}?q={city_name}&appid={API_KEY}&units=metric&lang=vi"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "lat": data["coord"]["lat"], #map
                "lon": data["coord"]["lon"] #map
            }
        return None
    except Exception:
        return None
def get_forecast(city_name):
    try:
        url = f"{FORECAST_URL}?q={city_name}&appid={API_KEY}&units=metric&lang=vi"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecast_list = []
            for item in data["list"]:
                if "12:00:00" in item["dt_txt"]:
                    date_obj = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
                    forecast_list.append({
                        "Ngày": date_obj.strftime("%d/%m (%A)"),
                        "Nhiệt độ (°C)": item["main"]["temp"],
                        "Độ ẩm (%)": item["main"]["humidity"],
                        "Thời tiết": item["weather"][0]["description"].capitalize()
                    })
            return forecast_list
        return None
    except Exception:
        return None
def setup_page():
    st.set_page_config(
        page_title="Dự Báo Thời Tiết",
        page_icon="⛅",
        layout="wide"
    )
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(to right, #e0f7fa, #80deea); }
        .login-box { background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
        </style>
    """, unsafe_allow_html=True)
create_table()
setup_page()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
if not st.session_state.logged_in:
    st.title("🔒 Hệ Thống Thời Tiết Thông Minh")
    st.markdown("Vui lòng đăng nhập hoặc đăng ký tài khoản để tiếp tục sử dụng ứng dụng.")
    st.markdown("---")
    left_co, cent_co, right_co = st.columns([1, 2, 1])
    with cent_co:
        auth_mode = st.radio("Lựa chọn", ["Đăng nhập", "Đăng ký đầy đủ"], horizontal=True)

        user_input = st.text_input("Tên đăng nhập", placeholder="Nhập username...")
        pass_input = st.text_input("Mật khẩu", type="password", placeholder="Nhập password...")

        if auth_mode == "Đăng nhập":
            if st.button("🔑 Tiến hành Đăng nhập", use_container_width=True):
                if login_user(user_input, pass_input):
                    st.session_state.logged_in = True
                    st.session_state.username = user_input
                    st.success(f"🎉 Đăng nhập thành công! Chào mừng {user_input}.")
                    st.rerun()
                else:
                    st.error("❌ Sai tài khoản hoặc mật khẩu, vui lòng thử lại!")
        else:
            if st.button("📝 Tạo tài khoản mới", use_container_width=True):
                if user_input and pass_input:
                    if register_user(user_input, pass_input):
                        st.success("✅ Đăng ký thành công! Hãy chuyển sang tab Đăng nhập.")
                    else:
                        st.error("❌ Tên đăng nhập này đã tồn tại trên hệ thống!")
                else:
                    st.warning("⚠️ Vui lòng không để trống Tên đăng nhập hoặc Mật khẩu.")

else:
    # 1. TIÊU ĐỀ CHÍNH
    st.title("⛅ App Thời Tiết Thông Minh")
    st.markdown(f"Xin chào thành viên: **{st.session_state.username}** 👋")
    st.markdown("---")

    # 2. SIDEBAR (Quản lý tài khoản & Thành phố yêu thích)
    st.sidebar.header("👤 Tài khoản")
    st.sidebar.write(f"🟢 Tài khoản: **{st.session_state.username}**")
    if st.sidebar.button("Đăng xuất"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
    st.sidebar.markdown("---")
    st.sidebar.header("❤️ Thành phố yêu thích")
    df_cities = view_all_cities()
    if not df_cities.empty:
        list_city_names = df_cities['city_name'].tolist()
        st.sidebar.write("Danh sách đã lưu:")
        for city in list_city_names:
            st.sidebar.text(f"- {city}")
        st.sidebar.markdown("---")
        city_to_delete = st.sidebar.selectbox("Chọn thành phố để xóa", list_city_names, key="delete_box")
        if st.sidebar.button("Xóa khỏi danh sách"):
            delete_city(city_to_delete)
            st.success(f"Đã xóa {city_to_delete}")
            st.rerun()
    else:
        st.sidebar.info("Chưa có thành phố nào được lưu.")

    # 3. GIAO DIỆN CHÍNH (TABS CHỨC NĂNG)
    tab1, tab2 = st.tabs(["🔍 Tra cứu & Lưu trữ", "📊 Thống kê & So sánh"])
    with tab1:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            city_input = st.text_input(
                "Nhập tên thành phố",
                placeholder="Hanoi, Hong Kong, New York...",
                key="city_search_input"
            )
        with col2:
            st.write("")
            st.write("")
            search_btn = st.button("Xem", use_container_width=True)
        with col3:
            st.write("")
            st.write("")
            forecast_btn = st.button("Xem 5 ngày", use_container_width=True)
        with col4:
            st.write("")
            st.write("")
            p_btn = st.button("Xem 7=>15 ngày", use_container_width=True)
            # có thể tính trung bình cộng các ngày trước rồi quy ra
        if "display_mode" not in st.session_state:
            st.session_state.display_mode = "current"
        if search_btn and city_input:
            with st.spinner('Đang tải thời tiết hiện tại...'):
                data = get_weather(city_input)
                if data:
                    st.session_state.weather_data = data
                    st.session_state.display_mode = "current"
                else:
                    st.session_state.weather_data = None
                    st.error("❌ Không tìm thấy thành phố này!")
        if forecast_btn and city_input:
            with st.spinner('Đang tải dữ liệu dự báo...'):
                data = get_weather(city_input)
                forecast_data = get_forecast(city_input)
                if data and forecast_data:
                    st.session_state.weather_data = data
                    st.session_state.forecast_data = forecast_data
                    st.session_state.display_mode = "forecast"
                else:
                    st.error("❌ Không thể lấy dữ liệu dự báo cho thành phố này!")
        if p_btn and city_input:
            st.warning("Dữ liệu Premium - Vui lòng nâng cấp tài khoản")
        if "weather_data" in st.session_state and st.session_state.weather_data:
            data = st.session_state.weather_data
            st.success(f"📍 Khu vực: {data['city']}")
            if st.session_state.display_mode == "current":
                col_a, col_b = st.columns(2)
                with col_a:
                    icon_url = f"http://openweathermap.org/img/wn/{data['icon']}@4x.png"
                    st.image(icon_url, width=120)
                    st.caption(data['description'].capitalize())
                with col_b:
                    st.metric("Nhiệt độ", f"{data['temp']} °C")
                    st.metric("Độ ẩm", f"{data['humidity']} %")
            elif st.session_state.display_mode == "forecast":
                st.subheader("🗓️ Dự báo thời tiết các ngày tới (Mốc 12h00)")
                df_forecast = pd.DataFrame(st.session_state.forecast_data)
                fig_forecast = px.line(df_forecast, x="Ngày", y="Nhiệt độ (°C)", text="Nhiệt độ (°C)",
                                       title="Xu hướng nhiệt độ")
                st.plotly_chart(fig_forecast, use_container_width=True)
                st.dataframe(df_forecast, use_container_width=True)
            st.markdown("### 🗺️ Bản đồ khu vực")
            map_data = pd.DataFrame({'lat': [data['lat']], 'lon': [data['lon']]})
            st.map(map_data, zoom=11)
            st.markdown("---")
            if st.button(f"❤️ Lưu {data['city']} vào danh sách"):
                saved = add_city(data['city'])
                if saved:
                    st.success("Đã lưu thành công!")
                    st.rerun()
                else:
                    st.warning("Thành phố đã tồn tại hoặc lỗi khi lưu.")
        st.markdown("---")
        st.caption("Tip: dùng 'Ho Chi Minh' hoặc 'Saigon'")
    with tab2:
        st.subheader("So sánh thời tiết các thành phố đã lưu")
        if df_cities.empty:
            st.info("Hãy lưu ít nhất 1 thành phố ở Tab Tra cứu để xem biểu đồ.")
        else:
            if st.button("Cập nhật dữ liệu mới nhất"):
                list_names = df_cities['city_name'].tolist()
                report_data = []
                my_bar = st.progress(0)
                for i, name in enumerate(list_names):
                    info = get_weather(name)
                    if info:
                        report_data.append(info)
                    my_bar.progress((i + 1) / len(list_names))
                df_report = pd.DataFrame(report_data)
                st.write("### 🌡️ So sánh Nhiệt độ (°C)")
                fig = px.bar(df_report, x='city', y='temp', color='temp',
                             color_continuous_scale='RdYlBu_r')
                st.plotly_chart(fig, use_container_width=True)
                st.write("### 📋 Bảng dữ liệu chi tiết")
                st.dataframe(df_report)
                csv = convert_df_to_csv(df_report)
                st.download_button(
                    label="📥 Tải báo cáo về máy (CSV)",
                    data=csv,
                    file_name='thoi_tiet_yeu_thich.csv',
                    mime='text/csv',
                )
