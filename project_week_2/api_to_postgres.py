import requests
import psycopg2
from psycopg2 import sql
import json

class WeatherAPIClient:
    def __init__(self, api_key):
        self.api_url = "https://api.weatherstack.com/current"
        self.api_key = api_key

    def fetch_weather_data(self, location):
        response = requests.get(self.api_url, params={'access_key': self.api_key, 'query': location})
        return response.json() if response.status_code == 200 else None

class WeatherPostgresDB:
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
            print("Connected to the database successfully.")
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")

    def create_table(self, table_name):
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            type TEXT,
            query TEXT,
            language TEXT,
            unit TEXT,
            name TEXT,
            country TEXT,
            region TEXT,
            lat DOUBLE PRECISION,
            lon DOUBLE PRECISION,
            timezone_id TEXT,
            wind_degree INT,
            wind_dir TEXT,
            pressure INT,
            precip DOUBLE PRECISION,
            humidity INT,
            cloudcover INT,
            feelslike INT,
            uv_index INT,
            visibility INT,
            is_day TEXT
        );
        """
        with self.conn.cursor() as cursor:
            cursor.execute(create_table_query)
            self.conn.commit()
            print(f"Table {table_name} created successfully.")

    def insert_weather_data(self, table_name, weather_data):
        insert_query = sql.SQL("""
            INSERT INTO {table} (type, query, language, unit, name, country, region, lat, lon, timezone_id, wind_degree, wind_dir, pressure, precip, humidity, cloudcover, feelslike, uv_index, visibility, is_day)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """).format(table=sql.Identifier(table_name))
        
        with self.conn.cursor() as cursor:
            cursor.execute(insert_query, (
                weather_data.get('request', {}).get('type', ''),
                weather_data.get('request', {}).get('query', ''),
                weather_data.get('request', {}).get('language', ''),
                weather_data.get('request', {}).get('unit', ''),
                weather_data.get('location', {}).get('name', ''),
                weather_data.get('location', {}).get('country', ''),
                weather_data.get('location', {}).get('region', ''),
                weather_data.get('location', {}).get('lat', 0),
                weather_data.get('location', {}).get('lon', 0),
                weather_data.get('location', {}).get('timezone_id', ''),
                weather_data.get('current', {}).get('wind_degree', 0),
                weather_data.get('current', {}).get('wind_dir', ''),
                weather_data.get('current', {}).get('pressure', 0),
                weather_data.get('current', {}).get('precip', 0.0),
                weather_data.get('current', {}).get('humidity', 0),
                weather_data.get('current', {}).get('cloudcover', 0),
                weather_data.get('current', {}).get('feelslike', 0),
                weather_data.get('current', {}).get('uv_index', 0),
                weather_data.get('current', {}).get('visibility', 0),
                weather_data.get('current', {}).get('is_day', '')
            ))
            self.conn.commit()
            print("Weather data inserted successfully.")
    
    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    API_KEY = '56760d673c94fbe78501aa7077454386'
    LOCATIONS = ["New Delhi, India", "Chennai, India", "Maisuru, India", "Bhilwara, India", "Kolkata, India", "Mumbai, India", "Hyderabad, India", "Bangalore, India", "Pune, India", "Ahmedabad, India"]
    DB_CONFIG = {
        "db_name": "api_db",
        "user": "postgres",
        "password": "root",
        "host": "127.0.0.1",
        "port": "5432"
    }
    TABLE_NAME = "weather_data"

    # Fetch data from API
    api_client = WeatherAPIClient(API_KEY)
    db = WeatherPostgresDB(**DB_CONFIG)
    db.connect()
    db.create_table(TABLE_NAME)
    
    for location in LOCATIONS:
        result = api_client.fetch_weather_data(location)
        if result and 'request' in result:
            db.insert_weather_data(TABLE_NAME, result)
    
    db.close_connection()


