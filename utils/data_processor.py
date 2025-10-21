import pandas as pd
from datetime import datetime

class DataProcessor:
    @staticmethod
    def calculate_monthly_summary(df):
        '''Calculate monthly income, expenses, and savings'''
        if df.empty:
            return pd.DataFrame()
        
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        summary = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
        
        if 'income' in summary.columns and 'expense' in summary.columns:
            summary['savings'] = summary['income'] - summary['expense']
        
        return summary
    
    @staticmethod
    def calculate_category_totals(df, trans_type='expense'):
        '''Calculate totals by category'''
        if df.empty:
            return pd.DataFrame()
        
        filtered = df[df['type'] == trans_type]
        return filtered.groupby('category')['amount'].sum().sort_values(ascending=False)
    
    @staticmethod
    def filter_by_month(df, year, month):
        '''Filter transactions by specific month'''
        if df.empty:
            return df
        
        df['date'] = pd.to_datetime(df['date'])
        return df[(df['date'].dt.year == year) & (df['date'].dt.month == month)]