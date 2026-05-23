import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="原料管理系统", layout="wide", page_icon="🌿")

# 数据文件
DATA_FILE = "data/products.json"
os.makedirs("data", exist_ok=True)

def load_products():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return pd.DataFrame(json.load(f))
    return pd.DataFrame(columns=["产品名称", "规格", "来源", "成本价", "建议售价", "MOQ", "COA参数", "库存"])

def save_products(df):
    df.to_json(DATA_FILE, force_ascii=False, orient="records")

if "products" not in st.session_state:
    st.session_state.products = load_products()

# 侧边栏
st.sidebar.title("🌿 原料管理系统")
page = st.sidebar.selectbox("请选择功能", ["仪表盘", "产品管理", "智能报价助手"])

# 仪表盘
if page == "仪表盘":
    st.title("📊 业务仪表盘")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("产品数量", len(st.session_state.products))
    with col2: st.metric("待报价", "2")
    with col3: st.metric("活跃客户", "8")
    
    st.subheader("产品概览")
    if not st.session_state.products.empty:
        st.dataframe(st.session_state.products[["产品名称", "来源", "建议售价", "库存"]], use_container_width=True)

# 产品管理
elif page == "产品管理":
    st.title("📦 产品管理")
    
    with st.form("add_product"):
        name = st.text_input("产品名称 *")
        spec = st.text_input("规格")
        source = st.selectbox("来源", ["自产", "外采"])
        cost = st.number_input("成本价 (元/kg)", value=50.0)
        price = st.number_input("建议售价 (元/kg)", value=88.0)
        stock = st.number_input("库存 (kg)", value=100)
        coa = st.text_area("COA关键参数", "多酚≥40% 等")
        
        if st.form_submit_button("保存产品"):
            if name:
                new_row = pd.DataFrame([{
                    "产品名称": name, "规格": spec, "来源": source,
                    "成本价": cost, "建议售价": price, "MOQ": 25,
                    "COA参数": coa, "库存": stock,
                    "更新时间": datetime.now().strftime("%Y-%m-%d")
                }])
                st.session_state.products = pd.concat([st.session_state.products, new_row], ignore_index=True)
                save_products(st.session_state.products)
                st.success(f"✅ {name} 已保存！")

    if not st.session_state.products.empty:
        st.dataframe(st.session_state.products, use_container_width=True)

# 智能报价助手
elif page == "智能报价助手":
    st.title("🤖 智能报价助手")
    st.write("描述客户需求，系统将自动推荐产品")
    
    client = st.text_input("客户名称")
    demand = st.text_area("客户需求", 
        "例如：需要水溶性绿茶提取物，用于饮料，预算80元/kg，用量500kg", 
        height=120)
    
    if st.button("生成报价方案", type="primary"):
        if demand:
            st.success("✅ 已为您生成方案！")
            st.subheader("推荐产品")
            if not st.session_state.products.empty:
                st.dataframe(st.session_state.products.head(3))
            else:
                st.info("请先添加产品")
            
            st.write("**个性化话术示例：**")
            st.write(f"您好{client}，根据您的需求，我为您推荐了以下高性价比原料方案...")
        else:
            st.warning("请输入需求描述")

st.sidebar.caption("植物提取物原料管理系统 v1.0")
