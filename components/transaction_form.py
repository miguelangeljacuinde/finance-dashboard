import streamlit as st
from datetime import datetime

def render_transaction_form(db_manager, categories):
    '''Render the transaction entry form'''
    st.subheader("Add New Transaction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        trans_type = st.selectbox("Type", ["expense", "income"])
        date = st.date_input("Date", datetime.now())
        category = st.selectbox("Category", categories[trans_type])
    
    with col2:
        amount = st.number_input("Amount", min_value=0.01, step=0.01)
        description = st.text_input("Description")
    
    if st.button("Add Transaction", type="primary"):
        if amount > 0:
            db_manager.add_transaction(
                date=str(date),
                category=category,
                amount=amount,
                description=description,
                trans_type=trans_type
            )
            st.success("Transaction added successfully!")
            st.rerun()
        else:
            st.error("Amount must be greater than 0")