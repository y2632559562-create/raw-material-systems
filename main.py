import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import io

st.set_page_config(page_title="原料管理系统", page_icon="🌿", layout="wide")

st.title("🌿 植物提取物原料管理系统")

menu = st.sidebar.selectbox("功能菜单", [
    "📦 产品库",
    "💰 快速报价",
    "📊 库存管理",
    "📁 COA管理",
])

if menu == "📦 产品库":
    st.header("产品库")
    uploaded = st.file_uploader("上传产品Excel表", type=["xlsx"])
    if uploaded:
        df = pd.read_excel(uploaded)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("请上传产品报价Excel文件，表头建议包含：产品名称、规格、单价、库存、产品类型")

elif menu == "💰 快速报价":
    st.header("快速生成报价单")
    uploaded = st.file_uploader("上传产品库Excel", type=["xlsx"])
    if uploaded:
        df = pd.read_excel(uploaded)
        st.subheader("选择报价产品")
        products = st.multiselect("选择产品", df.iloc[:, 0].tolist())
        customer = st.text_input("客户名称")
        margin = st.slider("加价比例 (%)", 0, 100, 20)
        if st.button("生成报价单") and products:
            selected = df[df.iloc[:, 0].isin(products)].copy()
            price_col = [c for c in df.columns if "价" in c or "price" in c.lower()]
            if price_col:
                selected["报价"] = selected[price_col[0]] * (1 + margin / 100)
            selected["客户"] = customer
            selected["日期"] = date.today()
            st.dataframe(selected, use_container_width=True)
            buf = io.BytesIO()
            selected.to_excel(buf, index=False)
            st.download_button("下载报价单", buf.getvalue(),
                               file_name=f"报价单_{customer}_{date.today()}.xlsx")
    else:
        st.info("请上传产品库Excel文件")

elif menu == "📊 库存管理":
    st.header("库存管理")
    uploaded = st.file_uploader("上传库存Excel", type=["xlsx"])
    if uploaded:
        df = pd.read_excel(uploaded)
        st.dataframe(df, use_container_width=True)
        num_cols = df.select_dtypes(include="number").columns.tolist()
        if num_cols:
            col = st.selectbox("选择展示字段", num_cols)
            fig = px.bar(df, x=df.columns[0], y=col, title=f"{col}分布")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("请上传库存Excel文件")

elif menu == "📁 COA管理":
    st.header("COA文件管理")
    st.info("上传产品COA文件（支持PDF/图片），按产品名归档")
    product_name = st.text_input("产品名称")
    coa_file = st.file_uploader("上传COA文件", type=["pdf", "png", "jpg", "jpeg"])
    if coa_file and product_name:
        st.success(f"✅ {product_name} 的COA已上传：{coa_file.name}")
