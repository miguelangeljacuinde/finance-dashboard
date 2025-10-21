import pandas as pd

class CSVImporter:
    @staticmethod
    def import_transactions(file, date_col='Date', amount_col='Amount', 
                          description_col='Description', category_col='Category'):
        '''Import transactions from CSV file'''
        try:
            df = pd.read_csv(file)
            
            # Basic validation
            required_cols = [date_col, amount_col]
            if not all(col in df.columns for col in required_cols):
                raise ValueError(f"CSV must contain columns: {required_cols}")
            
            # Standardize column names
            df = df.rename(columns={
                date_col: 'date',
                amount_col: 'amount',
                description_col: 'description' if description_col in df.columns else None,
                category_col: 'category' if category_col in df.columns else None
            })
            
            # Add default values if columns don't exist
            if 'description' not in df.columns:
                df['description'] = ''
            if 'category' not in df.columns:
                df['category'] = 'Uncategorized'
            
            # Determine type based on amount (negative = expense, positive = income)
            df['type'] = df['amount'].apply(lambda x: 'expense' if x < 0 else 'income')
            df['amount'] = df['amount'].abs()
            
            return df[['date', 'category', 'amount', 'description', 'type']]
        
        except Exception as e:
            raise Exception(f"Error importing CSV: {str(e)}")