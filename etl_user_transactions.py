import pandas as pd
import logging
import sqlite3
from datetime import datetime


def process_transactions():
    # Configure logging
    logging.basicConfig(filename='etl.log', level=logging.INFO, format='%(asctime)s %(message)s')

    try:
        ## Loading data
        user_df = pd.read_csv('/workspaces/fc_engineer-codetest/data_sources/users-1.csv', delimiter=',', encoding='utf-8')
        pricing_df = pd.read_csv('/workspaces/fc_engineer-codetest/data_sources/pricing-1.csv', delimiter=',', encoding='utf-8')
        transactions_df = pd.read_csv('/workspaces/fc_engineer-codetest/data_sources/transactions-1.csv', delimiter=',', encoding='utf-8')


        ## Implementing processing methods to ensure data quality and correct formatting
        transactions_df['amount'] = pd.to_numeric(transactions_df['amount'], errors='coerce') ## converting amount into numeric and adding 'coerce' to set invalids as NA
        transactions_df['trans_date'] = pd.to_datetime(transactions_df['trans_date'], format = 'ISO8601') ## converting date string to datetime format
        transactions_df2 = transactions_df.dropna(subset=['trans_date', 'amount']) ## this is to remove records where transaction date or amount is NA
        removed_rows = len(transactions_df) - len(transactions_df2)

        user_df['date_joined'] = pd.to_datetime(user_df['date_joined'], format = 'ISO8601') ## converting date string to datetime format

        ## Applying transformation instructions
        user_df['email'] = user_df['email'].str.lower()
        transactions_df['product'] = transactions_df2['product'].str.upper()

        ## To calculate each user's spending
        user_spends = transactions_df2.groupby('user_id')['amount'].sum().reset_index()
        user_spends.columns = ['user_id', 'total_spent']

        user_df2 = user_df.merge(user_spends, on='user_id', how='left')

        ## Loading resulting dataframe to an SQLite database
        conn = sqlite3.connect('/workspaces/fc_engineer-codetest/users.db')
        user_df2.to_sql('Users', conn, if_exists='replace', index=False)

        # Logging   
        logging.info(f'Processed {len(user_df)} records from users.csv')
        logging.info(f'Processed {len(transactions_df)} records from transactions.csv')
        logging.info(f'Removed {removed_rows} invalid rows in transactions.csv')
        logging.info(f'Loaded {len(user_df2)} records into the Users table')

    except Exception as e:
        logging.error(f'Error processing transactions: {e}')

process_transactions()

