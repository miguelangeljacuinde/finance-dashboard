import streamlit as st
from datetime import datetime
from components.csv_import import render_csv_import, generate_example_csv
from database.db_manager import DatabaseManager
from components.transaction_form import render_transaction_form
from components.charts import (
    create_category_pie_chart,
    create_monthly_trend_chart,
    create_category_bar_chart
)
from components.filters import render_date_filter
from utils.data_processor import DataProcessor
import time

# Page configuration
st.set_page_config(
    page_title="Personal Finance Dashboard",
    page_icon="💰",
    layout="wide"
)

# Initialize database
db = DatabaseManager()

# Define categories
CATEGORIES = {
    'expense': [
        'Groceries', 'Rent/Mortgage', 'Utilities', 'Transportation',
        'Entertainment', 'Healthcare', 'Shopping', 'Dining Out',
        'Insurance', 'Education', 'Maintenance', 'Other'
    ],
    'income': [
        'Salary', 'Freelance', 'Investment', 'Gift', 'Other'
    ]
}

st.divider()

# Download example CSV template
st.subheader("📥 Download Template")
csv_template = generate_example_csv()
st.download_button(
    label="Download Example CSV",
    data=csv_template,
    file_name="transaction_template.csv",
    mime="text/csv",
    help="Download a CSV template to see the expected format"
)

# Main app
st.title("💰 Personal Finance Dashboard")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio(["Dashboard", "Add Transaction", "Transactions", "Analytics", "Import CSV"])

# Dashboard Page
if page == "Dashboard":
    st.header("Overview")
    
    # Get all transactions
    df = db.get_all_transactions()
    
    if not df.empty:
        # Calculate key metrics
        total_income = df[df['type'] == 'income']['amount'].sum()
        total_expenses = df[df['type'] == 'expense']['amount'].sum()
        net_savings = total_income - total_expenses
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"${total_income:,.2f}")
        col2.metric("Total Expenses", f"${total_expenses:,.2f}")
        col3.metric("Net Savings", f"${net_savings:,.2f}", 
                   delta=f"{(net_savings/total_income*100):.1f}%" if total_income > 0 else "0%")
        
        st.divider()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_category_pie_chart(df, 'expense')
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_category_bar_chart(df, 'expense', top_n=5)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # Monthly trend
        fig = create_monthly_trend_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No transactions yet. Add your first transaction to see your dashboard!")

# Add Transaction Page
elif page == "Add Transaction":
    render_transaction_form(db, CATEGORIES)

# Transactions Page
elif page == "Transactions":
    st.header("All Transactions")
    
    df = db.get_all_transactions()
    
    if not df.empty:
        # Display transactions
        st.dataframe(
            df[['id', 'date', 'type', 'category', 'amount', 'description']],
            use_container_width=True,
            hide_index=True
        )
        
        # Option to edit transaction details
        with st.expander("Edit Transaction"):
            transaction_id = st.number_input("Transaction ID", min_value=1, step=1, key="edit_transaction_id")

            trans_type = st.selectbox("Type", ["expense", "income"])
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                date = st.date_input("Date", datetime.now())
            with col2:
                category = st.selectbox("Category", CATEGORIES[trans_type])
            with col3:
                amount = st.number_input("Amount", min_value=0.00, step=1.00)
            with col4:
                description = st.text_input("Description")

            if st.button("Update Transaction Details", type="secondary", key="update_button"):
                ## check to see if transaction exists
                if transaction_id not in df['id'].values:
                    st.error("Transaction ID not found.")
                    time.sleep(1.5)  # Brief pause to show the toast before rerun
                else:
                    db.update_transaction_details(transaction_id, {
                        "date": date,
                        "category": category,
                        "amount": amount,
                        "description": description
                    })
                    st.success("✅ Transaction updated!")
                    time.sleep(1.5)  # Brief pause to show the toast before rerun
                    st.rerun()
            
        # Option to delete transactions
        with st.expander("Delete Transaction"):
            transaction_id = st.number_input("Transaction ID", min_value=1, step=1, key="delete_transaction_id")

            if st.button("Delete", type="primary", key="delete_button"):
                ## check to see if transaction exists
                if transaction_id not in df['id'].values:
                    st.error("Transaction ID not found.")
                    time.sleep(1.5)  # Brief pause to show the toast before rerun
                else:
                    db.delete_transaction(transaction_id)
                    st.success("✅ Transaction deleted!")
                    time.sleep(1.5)  # Brief pause to show the toast before rerun
                    st.rerun()
    else:
        st.info("No transactions to display.")

# Analytics Page
elif page == "Analytics":
    st.header("Analytics")
    
    df = db.get_all_transactions()
    
    if not df.empty:
        processor = DataProcessor()
        
        # Monthly summary
        st.subheader("Monthly Summary")
        monthly_summary = processor.calculate_monthly_summary(df)
        if not monthly_summary.empty:
            st.dataframe(monthly_summary, use_container_width=True)
        
        st.divider()
        
        # Category analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Expense Categories")
            expense_cats = processor.calculate_category_totals(df, 'expense')
            st.dataframe(expense_cats, use_container_width=True)
        
        with col2:
            st.subheader("Income Categories")
            income_cats = processor.calculate_category_totals(df, 'income')
            st.dataframe(income_cats, use_container_width=True)
    else:
        st.info("No data available for analytics.")

# Import CSV Page (NEW)
elif page == "Import CSV":
    render_csv_import(db)