import os
import sqlite3
from cryptography.fernet import Fernet, InvalidToken

class Database:
    def __init__(self, db_name='database.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
        # Load or generate the encryption key
        self.key = self.load_or_generate_key()
        self.cipher_suite = Fernet(self.key)

        # Ensure the table exists and has the correct schema
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS history
                               (id INTEGER PRIMARY KEY, filename TEXT, query TEXT)''')

        # Add the 'answer' column if it doesn't exist
        try:
            self.cursor.execute("ALTER TABLE history ADD COLUMN answer TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists

        self.conn.commit()


    def load_or_generate_key(self):
        key_file_path = 'secret.key'
        if not os.path.exists(key_file_path):
            # Generate a new key and save it
            key = Fernet.generate_key()
            with open(key_file_path, 'wb') as key_file:
                key_file.write(key)
        else:
            # Load the existing key
            with open(key_file_path, 'rb') as key_file:
                key = key_file.read()
        return key

    def save_query(self, filename, query, answer):
        encrypted_query = self.cipher_suite.encrypt(query.encode())
        encrypted_answer = self.cipher_suite.encrypt(answer.encode())
        self.cursor.execute("INSERT INTO history (filename, query, answer) VALUES (?, ?, ?)", 
                            (filename, encrypted_query, encrypted_answer))
        self.conn.commit()
        
    def get_history(self, filename):
        try:
            self.cursor.execute("SELECT query, answer FROM history WHERE filename=?", (filename,))
            rows = self.cursor.fetchall()
            history = []
            for row in rows:
                try:
                    decrypted_query = self.cipher_suite.decrypt(row[0]).decode()
                    decrypted_answer = self.cipher_suite.decrypt(row[1]).decode()
                    history.append({
                        "query": decrypted_query,
                        "answer": decrypted_answer
                    })
                except InvalidToken:
                    history.append({
                        "query": "Decryption failed for this query.",
                        "answer": "Decryption failed for this answer."
                    })
            return history
        except Exception as e:
            print(f"An error occurred while retrieving history: {e}")
            return []
