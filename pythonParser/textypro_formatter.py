import csv
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Define the required output headers
TEXTY_HEADERS = [
    'First_Name', 'Last_Name', 'Buisness_Name', 'Job_Title', 'Phone_Number', 'Email_Address',
    'Street_Address', 'City', 'State', 'Zip_Code', 'Blocked', 'Tags'
]

def format_phone_number(phone):
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    # Only format if 10 or 11 digits (US numbers)
    if len(digits) == 11 and digits.startswith('1'):
        digits = digits[1:]
    if len(digits) == 10:
        return digits  # Return only digits, no formatting
    return ''  # Return empty if not a valid phone number

def convert_to_textypro(input_file, output_file):
    def clean_email(email):
        # Remove all characters except letters, digits, @, ., _, and -
        return re.sub(r'[^a-zA-Z0-9@._-]', '', email)

    with open(input_file, 'r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        formatted_rows = []

        for row in reader:
            raw_phone = row.get('Primary Phone', '').strip() or row.get('Business Phone', '').strip() or row.get('Mobile Phone', '').strip()
            phone = format_phone_number(raw_phone)
            email = clean_email(row.get('E-mail Address', '').strip())
            formatted_rows.append({
                'First_Name': row.get('First Name', '').strip(),
                'Last_Name': row.get('Last Name', '').strip(),
                'Buisness_Name': row.get('Company', '').strip(),
                'Job_Title': row.get('Job Title', '').strip(),
                'Phone_Number': phone,
                'Email_Address': email,
                'Street_Address': row.get('Business Street', '').strip() or row.get('Home Street', '').strip(),
                'City': row.get('Business City', '').strip() or row.get('Home City', '').strip(),
                'State': row.get('Business State', '').strip() or row.get('Home State', '').strip(),
                'Zip_Code': row.get('Business Postal Code', '').strip() or row.get('Home Postal Code', '').strip(),
                'Blocked': 'No',
                'Tags': ''
            })

    # Write to new formatted CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=TEXTY_HEADERS)
        writer.writeheader()
        writer.writerows(formatted_rows)

# GUI for drag-and-drop or file selection

def run_gui():
    def select_file():
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            process_file(file_path)

    def process_file(file_path):
        try:
            output_path = os.path.join(os.path.dirname(file_path), 'formatted_textypro.csv')
            convert_to_textypro(file_path, output_path)
            messagebox.showinfo("Success", f"Output saved to: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def drop(event):
        file_path = event.data if hasattr(event, 'data') else event.widget.tk.splitlist(event.data)[0]
        if file_path.endswith('.csv'):
            process_file(file_path)
        else:
            messagebox.showerror("Error", "Please drop a CSV file.")

    try:
        import tkinterdnd2 as tkdnd
        root = tkdnd.TkinterDnD.Tk()
        dnd_enabled = True
    except ImportError:
        root = tk.Tk()
        dnd_enabled = False

    root.title("TextyPro Formatter")
    root.geometry("400x200")
    label = tk.Label(root, text="Drag and drop your CSV file or click to select.", pady=20)
    label.pack()
    select_btn = tk.Button(root, text="Select CSV File", command=select_file, width=20, height=2)
    select_btn.pack(pady=30)

    if dnd_enabled:
        root.drop_target_register('DND_Files')
        root.dnd_bind('<<Drop>>', drop)
    else:
        label.config(text="Drag and drop (requires tkinterdnd2) or click to select.")

    root.mainloop()

if __name__ == "__main__":
    run_gui()