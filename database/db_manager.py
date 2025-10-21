import sqlite3
from datetime import datetime
import pandas as pd
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path='data/finance.db'):
        self.db_path = db_path
        # Create data directory if it doesn't exist
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        '''Initialize database with transactions table'''
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                type TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_transaction(self, date, category, amount, description, trans_type):
        '''Add a new transaction'''
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (date, category, amount, description, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, category, amount, description, trans_type))
        
        conn.commit()
        conn.close()
    
    def get_all_transactions(self):
        '''Get all transactions as a DataFrame'''
        conn = self.get_connection()
        df = pd.read_sql_query('SELECT * FROM transactions ORDER BY date DESC', conn)
        conn.close()
        return df
    
    def get_transactions_by_date_range(self, start_date, end_date):
        '''Get transactions within a date range'''
        conn = self.get_connection()
        query = '''
            SELECT * FROM transactions 
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC
        '''
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        return df
    
    def delete_transaction(self, transaction_id):
        '''Delete a transaction by ID'''
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        conn.commit()
        conn.close()