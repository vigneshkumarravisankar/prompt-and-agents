import pdfplumber
import json
import os
import sys
import re
from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions
from storage import InvoiceStorage

load_dotenv()

if(os.getenv("GOOGLE_API_KEY")==None):
    print("Error: GOOGLE_API_KEY environment variable is not set.")
    sys.exit(1)

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)
    return text

def clean_json_response(response_text):
    """Cleans the response text from Gemini to extract just the JSON part."""
    # Remove markdown code blocks if present
    json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    
    # If no code blocks, try to find the first '{' and last '}'
    start = response_text.find('{')
    end = response_text.rfind('}')
    if start != -1 and end != -1:
        return response_text[start:end+1]
    
    return response_text

def parse_invoice_with_gemini(text):
    """Sends extracted text to Gemini for structured extraction using a formal prompt framework."""
    try:
        client = genai.Client(http_options=HttpOptions(api_version="v1"))
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        print("Make sure GOOGLE_API_KEY environment variable is set.")
        sys.exit(1)
    
    prompt = f"""
    # 1. ROLE / PERSONA
    # Acting as a Senior Financial Data Analyst and Expert OCR Verification Specialist.
    You are a highly detailed AI agent specialized in parsing complex financial documents with 100% accuracy.

    # 2. TASK
    # The primary objective is to transform raw, unstructured text into a clean, machine-readable format.
    Your task is to analyze the provided OCR-extracted text from an invoice and map it to a specific JSON schema.

    # 3. CONTEXT
    # This task is part of an automated accounts payable pipeline where accuracy is critical for tax and auditing purposes.
    The text is extracted from various invoice layouts, potentially containing noise, line breaks, or misaligned columns.

    # 4. INPUT DATA
    # The raw text extracted from the PDF using pdfplumber.
    --- INVOICE TEXT START ---
    {text}
    --- INVOICE TEXT END ---

    # 5. OUTPUT FORMAT
    # Define the exact JSON structure required for the downstream database.
    Return ONLY a valid JSON object following this schema:
    {{
        "invoice_id": "string",
        "order_id": "string",
        "bill_to": "string",
        "ship_to": "string",
        "ship_to_address": "string",
        "invoice_date": "string",
        "invoice_ship_mode": "string",
        "invoice_balance_due": number,
        "line_items": [
            {{
                "line_item_name": "string",
                "line_item_quantity": number,
                "line_item_rate": number,
                "line_item_amount": number
            }}
        ],
        "invoice_subtotal": number,
        "invoice_discount": number,
        "invoice_shipping": number,
        "invoice_total": number
    }}

    # 6. CONSTRAINTS
    # Rules that must be strictly followed during generation.
    - Output must be strict, valid JSON.
    - No preamble, no postamble, no conversational text.
    - If a field is missing, use null or an empty string.
    - Ensure numeric values are extracted as numbers (float/int), not strings.
    - Maintain the highest fidelity to the original text.

    # 7. EXAMPLES
    # Few-shot example to guide the model on formatting and edge cases.
    Example Logic:
    Input: "INV-999 | PO-456 | Bill to: John Doe | Ship to: Jane Smith | Date: 2024-05-10 | Item: Widget | Qty: 2 | Rate: 10 | Total: 20"
    Output: {{
        "invoice_id": "INV-999", 
        "order_id": "PO-456", 
        "bill_to": "John Doe", 
        "ship_to": "Jane Smith", 
        "invoice_date": "2024-05-10", 
        "line_items": [
            {{"line_item_name": "Widget", "line_item_quantity": 2, "line_item_rate": 10.0, "line_item_amount": 20.0}}
        ],
        "invoice_total": 20.0
    }}

    JSON Result:
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        cleaned_json = clean_json_response(response.text)
        return json.loads(cleaned_json)
    except Exception as e:
        print(f"Error during Gemini generation or JSON parsing: {e}")
        return {"error": str(e), "raw_response": response.text if 'response' in locals() else None}

def setup_result_folders(pdf_path):
    """Creates a folder structure for the results based on steps."""
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = f"results_{base_name}"
    
    step_folders = {
        "step1": os.path.join(output_dir, "step_1_ocr"),
        "step2": os.path.join(output_dir, "step_2_llm"),
        "step3": os.path.join(output_dir, "step_3_storage")
    }
    
    for folder in step_folders.values():
        os.makedirs(folder, exist_ok=True)
        
    return step_folders

def process_single_invoice(pdf_path):
    """Full pipeline for a single invoice."""
    # Initialize folders
    folders = setup_result_folders(pdf_path)
        
    print(f"--- Step 1: Extracting text from {pdf_path} ---")
    extracted_text = extract_text_from_pdf(pdf_path)
    
    if not extracted_text.strip():
        print("Warning: No text could be extracted from the PDF.")
        return
    
    print(f"Extracted {len(extracted_text)} characters.")
    # Save raw text to Step 1 folder
    raw_text_path = os.path.join(folders["step1"], "raw_extracted_text.txt")
    with open(raw_text_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)
    print(f"-> Raw text saved to: {raw_text_path}")
    
    print("--- Step 2: Parsing with Gemini ---")
    extracted_data = parse_invoice_with_gemini(extracted_text)
    
    # Save parsed JSON to Step 2 folder
    parsed_json_path = os.path.join(folders["step2"], "parsed_invoice.json")
    with open(parsed_json_path, "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)
    print(f"-> Parsed JSON saved to: {parsed_json_path}")
    
    # --- Step 3: Storage ---
    if "error" not in extracted_data:
        print("--- Step 3: Saving Results ---")
        storage = InvoiceStorage()
        storage.save_to_json(extracted_data)
        storage.save_to_sqlite(extracted_data)
        
        # Save a summary of the storage action to Step 3 folder
        storage_log_path = os.path.join(folders["step3"], "storage_log.txt")
        with open(storage_log_path, "w", encoding="utf-8") as f:
            f.write(f"Status: Success\n")
            f.write(f"Invoice Number: {extracted_data.get('invoice_number')}\n")
            f.write(f"Stored in: invoices.json and invoices.db\n")
        print(f"-> Storage log saved to: {storage_log_path}")
    else:
        print("Skipping storage due to parsing error.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python invoice_parser.py <path_to_pdf_or_directory>")
        print("Example 1 (File): python invoice_parser.py invoice.pdf")
        print("Example 2 (Dir):  python invoice_parser.py ./invoices/")
        sys.exit(1)
        
    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"Error: Path {input_path} not found.")
        sys.exit(1)
        
    if os.path.isfile(input_path):
        if input_path.lower().endswith(".pdf"):
            process_single_invoice(input_path)
        else:
            print("Error: The file provided is not a PDF.")
    elif os.path.isdir(input_path):
        print(f"--- Batch Processing Mode: {input_path} ---")
        pdf_files = [f for f in os.listdir(input_path) if f.lower().endswith(".pdf")]
        
        if not pdf_files:
            print("No PDF files found in the directory.")
        else:
            print(f"Found {len(pdf_files)} PDF(s). Starting pipeline...")
            for pdf_file in pdf_files:
                full_path = os.path.join(input_path, pdf_file)
                process_single_invoice(full_path)
            print("\n--- Batch Processing Completed ---")
