import streamlit as st
import pandas as pd
import matplotlib.pyplot  as plt

st.set_page_config(
    page_title="Dashboard E-commerce Brazil",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

st.title('Dashboard E-Commerce Brazil')

col = st.columns((1.5, 4.5, 2), gap='medium')

def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

with col[0]:
    st.markdown('### Stats')
    customer_df = pd.read_csv('./dataset/olist_customers_dataset.csv')
    seller_df = pd.read_csv('./dataset/olist_sellers_dataset.csv')
    st.metric(label='Customers', value=format_number(customer_df.shape[0]))
    st.metric(label='Sellers', value=format_number(seller_df.shape[0]))

with col[1]:
    order_df = pd.read_csv('./dashboard/monthly_order.csv')
    order_df.rename(columns={'purchase_count':'Purchase Count','month_name':'Months','year_month':'Year Month'},inplace=True)
    st.markdown('### Trend Order')
    st.bar_chart(order_df,y='Purchase Count',x='Year Month')

    st.markdown('### Customer Distribution')
    customer_location = pd.read_csv('./dashboard/customer_location.csv')
    customer_location.rename(columns={'geolocation_lat':'lat','geolocation_lng':'lon'},inplace=True)
    center_map = [customer_location['lat'].mean(),customer_location['lon'].mean()]
    st.map(customer_location,zoom=2)

    st.markdown('### Payment Type Usage')
    payment = pd.read_csv('./dashboard/payment_type_count.csv')
    payment.rename(columns={'payment_type':'Payment Type','count':'Count'},inplace=True)
    # fig, ax = plt.subplots()
    # ax.pie(sizes=payment['Count'],labels=payment['Payment Type'])
    st.bar_chart(payment,y='Count',x='Payment Type')
    # st.pyplot(fig)

with col[2]:
    st.markdown('### Customer Cities')
    customer_city = pd.read_csv('./dashboard/customer_by_city.csv')
    st.dataframe(customer_city,
                 column_order=('customer_city','customer_count'),
                 hide_index=True,
                 width=None,
                  column_config={
                    "customer_city": st.column_config.TextColumn(
                        "Cities",
                    ),
                    "customer_count": st.column_config.ProgressColumn(
                        "Customers",
                        format="%f",
                        min_value=0,
                        max_value=max(customer_city['customer_count']),
                     )}
                 )
    st.markdown('### Top Product by Reviews')
    top_product = pd.read_csv('./dashboard/top_scores_product_category.csv')
    st.dataframe(top_product,
                 column_order=('product_category_name_english','average_review_score'),
                 hide_index=True,
                 width=None,
                  column_config={
                    "product_category_name_english": st.column_config.TextColumn(
                        "Products",
                    ),
                    "average_review_score": st.column_config.ProgressColumn(
                        "Avg Scores",
                        format="%.2f",
                        min_value=0,
                        max_value=5,
                     )}
                 )