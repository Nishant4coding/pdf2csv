import pdfplumber
import pandas as pd

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to parse the extracted text into a structured format
def parse_bill_text(text):
    bills = []
    sections = text.split('WARMHLEE (A unit of Taneja Enterprises)')[1:]  # Split by the recurring section header
    for section in sections:
        lines = section.split('\n')
        buyer_info = {
            "name": None,
            "order_date": None,
            "invoice": None,
            "order_no": None,
            "address": None,
            "state": None,
            "postal_code": None,
            "item": None,
            "quantity": None,
            "hsn_code": None,
            "unit_price": None,
            "subtotal": None,
            "igst": None,
            "total": None
        }
        for i, line in enumerate(lines):
            if "ORDER DATE :" in line:
                buyer_info['order_date'] = line.split(': ')[1].strip()
                buyer_info['name'] = lines[i-1].strip()
            elif "Invoice-" in line:
                buyer_info['invoice'] = line.split(' ')[-1].strip()
            elif "ORDER NO :" in line:
                buyer_info['order_no'] = line.split(': ')[1].strip()
            elif line.strip().endswith('India'):
                address_lines = []
                for j in range(i+1, len(lines)):
                    if "ORDER DATE :" in lines[j] or "Invoice-" in lines[j] or "ORDER NO :" in lines[j]:
                        break
                    address_lines.append(lines[j].strip())
                buyer_info['address'] = ' '.join(address_lines)
            elif "WARMHLEE Weighted Plushie" in line:
                buyer_info['item'] = line.strip()
                buyer_info['quantity'] = lines[i + 1].strip()
                buyer_info['hsn_code'] = lines[i + 2].strip()
                buyer_info['unit_price'] = lines[i + 3].strip()
                buyer_info['subtotal'] = lines[i + 4].strip().split()[-1]
                buyer_info['igst'] = lines[i + 5].strip().split()[-1]
                buyer_info['total'] = lines[i + 6].strip().split()[-1]
        
        # Check if we captured all the necessary fields
        if all(buyer_info.values()):
            bills.append(buyer_info)
    return bills

# Extract text from the PDF
pdf_path = "BILL.pdf"  # Path to your PDF file
text = extract_text_from_pdf(pdf_path)

# Parse the text to get structured bill data
bills = parse_bill_text(text)

# Print each bill's data with a gap or enter between them
for bill in bills:
    print(bill)
    print("\n")  # Add a newline between each bill
    print("\n")  # Add a newline between each bill

# Convert to DataFrame
df = pd.DataFrame(bills)

# Write to CSV
output_csv_path = "bills.csv"
df.to_csv(output_csv_path, index=False)

print("Bills have been successfully written to bills.csv")
print("Extracted text:", text)  # Print extracted text
print("Parsed bills:", bills)  # Print parsed bills
