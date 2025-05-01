import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# 设置网页标题
st.set_page_config(page_title="Sydney Projects Map", layout="wide")

# 加载数据
df = pd.read_excel("/Users/fukang/Downloads/my project/sydney_map_app/sydney_projects.xlsx")

st.sidebar.header("筛选条件")

# 筛选项目类型
project_types = ["All"] + sorted(df["project_type"].dropna().unique().tolist())
selected_type = st.sidebar.selectbox("选择项目类型", project_types)

# 筛选区域
suburbs = ["All"] + sorted(df["suburb"].dropna().unique().tolist())
selected_suburb = st.sidebar.selectbox("选择区域", suburbs)

# 筛选状态
statuses = ["All"] + sorted(df["status"].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("选择状态", statuses)

# 过滤数据
filtered_df = df.copy()
if selected_type != "All":
    filtered_df = filtered_df[filtered_df["project_type"] == selected_type]
if selected_suburb != "All":
    filtered_df = filtered_df[filtered_df["suburb"] == selected_suburb]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df["status"] == selected_status]

# 类型颜色映射
color_map = {
    "shop": "blue",
    "house": "green",
    "clinic": "red",
    "office": "purple",
    "commercial": "orange",
    "education": "darkred"
}

# 创建地图
m = folium.Map(location=[-33.87, 151.2], zoom_start=10)

for _, row in filtered_df.iterrows():
    popup_text = f"""
    <b>{row['name']}</b><br>
    类型: {row['project_type']}<br>
    状态: {row['status']}<br>
    起止时间: {row['start_date']} → {row['end_date']}<br>
    描述: {row['description']}
    """
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=popup_text,
        icon=folium.Icon(color=color_map.get(row["project_type"], "gray"), icon="info-sign")
    ).add_to(m)

# 显示地图
st.title("🏗️ 悉尼装修项目地图")
st.markdown("根据项目类型、区域和状态进行筛选，查看对应装修项目的位置。")
st_folium(m, width=900, height=600)

# 加入统计图
st.subheader("📊 项目数量分布（按类型）")
count_by_type = df["project_type"].value_counts().sort_index()

fig, ax = plt.subplots()
count_by_type.plot(kind="bar", color=[color_map.get(t, "gray") for t in count_by_type.index], ax=ax)
ax.set_xlabel("项目类型")
ax.set_ylabel("数量")
ax.set_title("项目类型数量统计")
st.pyplot(fig)
