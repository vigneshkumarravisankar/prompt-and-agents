import sqlite3
import json
import sys

def list_invoices(db_path="invoices.db"):
    """Lists all invoices and their summary data from the database."""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM invoices ORDER BY created_at DESC")
        rows = cursor.fetchall()
        
        if not rows:
            print("No invoices found in the database.")
            return

        print(f"{'ID':<4} | {'Invoice ID':<15} | {'Bill To':<20} | {'Total':<10} | {'Date':<15}")
        print("-" * 75)
        
        for row in rows:
            print(f"{row['id']:<4} | {str(row['invoice_id']):<15} | {str(row['bill_to']):<20} | {row['invoice_total']:<10} | {str(row['invoice_date']):<15}")
            
    except Exception as e:
        print(f"Error querying database: {e}")
    finally:
        conn.close()

def show_invoice_details(invoice_db_id, db_path="invoices.db"):
    """Shows full details for a specific invoice, including line items."""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get invoice
        cursor.execute("SELECT * FROM invoices WHERE id = ?", (invoice_db_id,))
        invoice = cursor.fetchone()
        
        if not invoice:
            print(f"Invoice with ID {invoice_db_id} not found.")
            return
        
        print("\n=== Invoice Details ===")
        for key in invoice.keys():
            if key != 'raw_json':
                print(f"{key.replace('_', ' ').title()}: {invoice[key]}")
        
        # Get line items
        cursor.execute("SELECT * FROM line_items WHERE invoice_db_id = ?", (invoice_db_id,))
        items = cursor.fetchall()
        
        if items:
            print("\n--- Line Items ---")
            print(f"{'Name':<30} | {'Qty':<5} | {'Rate':<8} | {'Amount':<8}")
            print("-" * 60)
            for item in items:
                print(f"{str(item['line_item_name'])[:30]:<30} | {item['line_item_quantity']:<5} | {item['line_item_rate']:<8} | {item['line_item_amount']:<8}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If an ID is provided, show details
        show_invoice_details(sys.argv[1])
    else:
        # Otherwise list all
        list_invoices()
