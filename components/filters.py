import streamlit as st
from datetime import datetime, timedelta

def render_date_filter():
    '''Render date range filter'''
    st.subheader("Filter by Date Range")
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=30)
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now()
        )
    
    return start_date, end_date

def render_category_filter(categories):
    '''Render category filter'''
    all_categories = categories['expense'] + categories['income']
    selected = st.multiselect(
        "Filter by Categories",
        all_categories,
        default=[]
    )
    return selected