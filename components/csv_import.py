import streamlit as st
import pandas as pd
from datetime import datetime

def render_csv_import(db_manager):
    """Render CSV import interface"""
    st.subheader("📁 Import Transactions from CSV")
    
    st.info("""
    **CSV Format Requirements:**
    - Must have columns for: Date, Amount
    - Optional columns: Description, Category
    - Date format: YYYY-MM-DD (e.g., 2024-10-21)
    - Amount: Positive for income, negative for expenses
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file with your transaction data"
    )
    
    if uploaded_file is not None:
        try:
            # Read CSV
            df = pd.read_csv(uploaded_file)
            
            st.success(f"✅ File loaded successfully! Found {len(df)} rows.")
            
            # Show preview
            with st.expander("📊 Preview Data (first 10 rows)"):
                st.dataframe(df.head(10), use_container_width=True)
            
            st.divider()
            
            # Column mapping section
            st.subheader("Map Your Columns")
            
            col1, col2 = st.columns(2)
            
            with col1:
                date_col = st.selectbox(
                    "Date Column *",
                    options=df.columns.tolist(),
                    help="Select the column containing transaction dates"
                )
                
                amount_col = st.selectbox(
                    "Amount Column *",
                    options=df.columns.tolist(),
                    help="Select the column containing transaction amounts"
                )
            
            with col2:
                description_col = st.selectbox(
                    "Description Column (optional)",
                    options=['None'] + df.columns.tolist(),
                    help="Select the column containing descriptions"
                )
                
                category_col = st.selectbox(
                    "Category Column (optional)",
                    options=['None'] + df.columns.tolist(),
                    help="Select the column containing categories"
                )
            
            # Default category for uncategorized transactions
            default_category = st.text_input(
                "Default Category",
                value="Uncategorized",
                help="Category to use when none is specified"
            )
            
            st.divider()
            
            # Import button
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("🚀 Import Transactions", type="primary"):
                    import_transactions(
                        db_manager=db_manager,
                        df=df,
                        date_col=date_col,
                        amount_col=amount_col,
                        description_col=description_col if description_col != 'None' else None,
                        category_col=category_col if category_col != 'None' else None,
                        default_category=default_category
                    )
            
            with col2:
                if st.button("🔄 Reset"):
                    st.rerun()
        
        except Exception as e:
            st.error(f"❌ Error reading CSV file: {str(e)}")
            st.info("Please make sure your CSV is properly formatted.")


def import_transactions(db_manager, df, date_col, amount_col, 
                       description_col, category_col, default_category):
    """Process and import transactions from DataFrame"""
    
    try:
        # Progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        imported_count = 0
        error_count = 0
        errors = []
        
        total_rows = len(df)
        
        for idx, row in df.iterrows():
            try:
                # Extract date
                date_str = str(row[date_col])
                # Try to parse the date
                try:
                    date_obj = pd.to_datetime(date_str)
                    date_formatted = date_obj.strftime('%Y-%m-%d')
                except:
                    date_formatted = date_str
                
                # Extract amount
                amount = float(row[amount_col])
                
                # Determine transaction type
                if amount < 0:
                    trans_type = 'expense'
                    amount = abs(amount)
                else:
                    trans_type = 'income'
                
                # Extract description
                if description_col and description_col in df.columns:
                    description = str(row[description_col]) if pd.notna(row[description_col]) else ''
                else:
                    description = ''
                
                # Extract category
                if category_col and category_col in df.columns and pd.notna(row[category_col]):
                    category = str(row[category_col])
                else:
                    category = default_category
                
                # Add to database
                db_manager.add_transaction(
                    date=date_formatted,
                    category=category,
                    amount=amount,
                    description=description,
                    trans_type=trans_type
                )
                
                imported_count += 1
                
            except Exception as e:
                error_count += 1
                errors.append(f"Row {idx + 2}: {str(e)}")
            
            # Update progress
            progress = (idx + 1) / total_rows
            progress_bar.progress(progress)
            status_text.text(f"Processing: {idx + 1}/{total_rows} rows")
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        # Show results
        st.success(f"✅ Import Complete!")
        
        col1, col2 = st.columns(2)
        col1.metric("Successfully Imported", imported_count)
        col2.metric("Errors", error_count)
        
        if errors and len(errors) <= 10:
            with st.expander("⚠️ View Errors"):
                for error in errors:
                    st.text(error)
        elif errors:
            with st.expander("⚠️ View Errors (showing first 10)"):
                for error in errors[:10]:
                    st.text(error)
                st.text(f"... and {len(errors) - 10} more errors")
        
        if imported_count > 0:
            st.balloons()
            st.info("💡 Go to the Dashboard or Transactions page to view your imported data!")
    
    except Exception as e:
        st.error(f"❌ Import failed: {str(e)}")


# Example CSV template generator
def generate_example_csv():
    """Generate an example CSV for users to download"""
    example_data = {
        'Date': ['2024-10-01', '2024-10-05', '2024-10-10', '2024-10-15'],
        'Amount': [-50.25, -120.00, 2500.00, -35.99],
        'Category': ['Groceries', 'Utilities', 'Salary', 'Dining Out'],
        'Description': ['Weekly groceries', 'Electric bill', 'Monthly salary', 'Dinner with friends']
    }
    
    df = pd.DataFrame(example_data)
    return df.to_csv(index=False)