import json
import sqlite3
import os
from datetime import datetime

class InvoiceStorage:
    def __init__(self, db_path="invoices.db", json_path="invoices.json"):
        self.db_path = db_path
        self.json_path = json_path
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database schema with the new structure."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # We'll drop existing tables for this update to ensure correct schema
        # In a production app, we would use migrations.
        cursor.execute('DROP TABLE IF EXISTS line_items')
        cursor.execute('DROP TABLE IF EXISTS invoices')
        
        # Create Invoices table with new fields
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id TEXT,
                order_id TEXT,
                bill_to TEXT,
                ship_to TEXT,
                ship_to_address TEXT,
                invoice_date TEXT,
                invoice_ship_mode TEXT,
                invoice_balance_due REAL,
                invoice_subtotal REAL,
                invoice_discount REAL,
                invoice_shipping REAL,
                invoice_total REAL,
                raw_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Line Items table with new fields
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS line_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_db_id INTEGER,
                line_item_name TEXT,
                line_item_quantity REAL,
                line_item_rate REAL,
                line_item_amount REAL,
                FOREIGN KEY (invoice_db_id) REFERENCES invoices (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def save_to_json(self, data):
        """Append the invoice data to a local JSON file."""
        existing_data = []
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                existing_data = []

        # Add timestamp to the record
        data_to_store = data.copy()
        data_to_store['processed_at'] = datetime.now().isoformat()
        existing_data.append(data_to_store)

        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4)
        print(f"-> Saved to JSON: {self.json_path}")

    def save_to_sqlite(self, data):
        """Save the invoice and its line items to the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Insert main invoice data
            cursor.execute('''
                INSERT INTO invoices (
                    invoice_id, order_id, bill_to, ship_to, 
                    ship_to_address, invoice_date, invoice_ship_mode, 
                    invoice_balance_due, invoice_subtotal, invoice_discount, 
                    invoice_shipping, invoice_total, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get("invoice_id"),
                data.get("order_id"),
                data.get("bill_to"),
                data.get("ship_to"),
                data.get("ship_to_address"),
                data.get("invoice_date"),
                data.get("invoice_ship_mode"),
                data.get("invoice_balance_due"),
                data.get("invoice_subtotal"),
                data.get("invoice_discount"),
                data.get("invoice_shipping"),
                data.get("invoice_total"),
                json.dumps(data)
            ))
            
            invoice_db_id = cursor.lastrowid
            
            # Insert line items
            line_items = data.get("line_items", [])
            for item in line_items:
                cursor.execute('''
                    INSERT INTO line_items (
                        invoice_db_id, line_item_name, line_item_quantity, 
                        line_item_rate, line_item_amount
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    invoice_db_id,
                    item.get("line_item_name"),
                    item.get("line_item_quantity"),
                    item.get("line_item_rate"),
                    item.get("line_item_amount")
                ))
            
            conn.commit()
            print(f"-> Saved to SQLite: {self.db_path} (DB ID: {invoice_db_id})")
        except Exception as e:
            conn.rollback()
            print(f"Error saving to SQLite: {e}")
        finally:
            conn.close()
