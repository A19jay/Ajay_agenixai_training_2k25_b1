import pandas as pd # type: ignore
import psycopg2
import re
from user_agents import parse # type: ignore
from datetime import datetime

class ApacheLogParser:
    def __init__(self, log_file):
        self.log_file = log_file
        self.data = []

    def parse_logs(self):
        log_pattern = r'(?P<ip>\S+) - - \[(?P<timestamp>.*?)\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status_code>\d+) \S+ "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
        with open(self.log_file, 'r') as file:
            for line in file:
                match = re.match(log_pattern, line)
                if match:
                    user_agent = parse(match.group('user_agent'))
                    
                    # Convert timestamp to proper format
                    timestamp_str = match.group('timestamp')
                    timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")

                    self.data.append({
                        'ip': match.group('ip'),
                        'timestamp': timestamp,
                        'method': match.group('method'),
                        'url': match.group('url'),
                        'status_code': int(match.group('status_code')),
                        'referrer': match.group('referrer'),
                        'user_agent': match.group('user_agent'),
                        'os': user_agent.os.family,
                        'browser': user_agent.browser.family
                    })
        return self.data

class PostgreSQLDatabase:
    def __init__(self, db_name, user, password, host, port):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            print("Connected to PostgreSQL successfully!")
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS apache_logs (
            id SERIAL PRIMARY KEY,
            ip VARCHAR(50),
            timestamp TIMESTAMP,
            method VARCHAR(10),
            url TEXT,
            status_code INT,
            referrer TEXT,
            user_agent TEXT,
            os VARCHAR(50),
            browser VARCHAR(50)
        );
        '''
        with self.conn.cursor() as cursor:
            cursor.execute(create_table_query)
            self.conn.commit()
            print("Table 'apache_logs' created successfully.")

    def insert_data(self, data):
        insert_query = '''
        INSERT INTO apache_logs (ip, timestamp, method, url, status_code, referrer, user_agent, os, browser) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        try:
            with self.conn.cursor() as cursor:
                for row in data:
                    cursor.execute(insert_query, (
                        row['ip'], row['timestamp'], row['method'], row['url'], 
                        row['status_code'], row['referrer'], row['user_agent'], row['os'], row['browser']
                    ))
                self.conn.commit()
                print(f"Inserted {len(data)} log entries successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    # Parse Apache logs
    log_parser = ApacheLogParser('apache_logs.txt')
    parsed_data = log_parser.parse_logs()
    
    # Store in PostgreSQL
    db = PostgreSQLDatabase(db_name='log_db', user='postgres', password='root', host='127.0.0.1', port='5432')
    db.connect()
    db.create_table()
    
    db.insert_data(parsed_data)
    db.close()
