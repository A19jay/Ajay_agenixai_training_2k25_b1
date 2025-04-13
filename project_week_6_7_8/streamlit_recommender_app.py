import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from ucimlrepo import fetch_ucirepo

# Load cleaned data and similarity matrix
data = pd.read_csv(r"C:\Users\ajayr\OneDrive\Desktop\agenix\project_week_6_7_8\cleaned_online_retail.csv")
similarity_matrix = pd.read_csv(r"C:\Users\ajayr\OneDrive\Desktop\agenix\project_week_6_7_8\item_similarity_matrix.csv", index_col=0)

# Sidebar inputs
st.sidebar.header("🔍 Product Recommendation")
product_list = similarity_matrix.columns.tolist()
selected_product = st.sidebar.selectbox("Select a product:", product_list)
top_n = st.sidebar.slider("Number of recommendations:", 1, 10, 5)

# Header
st.title("🛍️ Product Recommendation System")
st.markdown("This app recommends similar products based on purchase behavior using item-based collaborative filtering.")

# Recommendations
if selected_product:
    st.subheader(f"📦 Top {top_n} Recommendations for: {selected_product}")
    try:
        recommendations = similarity_matrix[selected_product].sort_values(ascending=False)[1:top_n+1]
        st.write(recommendations.to_frame("Similarity Score"))
    except:
        st.error("Product not found in similarity matrix.")

# EDA
st.markdown("---")
st.subheader("📊 EDA Snapshots")

# Top products
top_products = data['Description'].value_counts().head(10)
st.bar_chart(top_products)

# Monthly trend
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
data['Month'] = data['InvoiceDate'].dt.to_period('M')
monthly_sales = data.groupby('Month')['TotalPrice'].sum()
st.line_chart(monthly_sales)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")