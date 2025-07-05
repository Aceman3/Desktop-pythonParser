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
            progress_label.config(text="Processing...", fg="blue")
            root.update_idletasks()
            convert_to_textypro(file_path, output_path)
            progress_label.config(text="Success! Output saved to: {}".format(output_path), fg="green")
            messagebox.showinfo("Success", f"Output saved to: {output_path}")
        except Exception as e:
            progress_label.config(text="Error: {}".format(str(e)), fg="red")
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
    root.geometry("1080x720")
    root.configure(bg="#f4f6fb")

    title_label = tk.Label(root, text="TextyPro CSV Formatter", font=("Helvetica", 18, "bold"), bg="#f4f6fb", fg="#2d3e50", pady=10)
    title_label.pack()

    desc_label = tk.Label(root, text="Easily format your CSV for TextyPro. Drag and drop or select a file.", font=("Helvetica", 11), bg="#f4f6fb", fg="#4e5d6c")
    desc_label.pack(pady=(0, 10))

    select_btn = tk.Button(root, text="Select CSV File", command=select_file, width=22, height=2, bg="#4e8cff", fg="white", font=("Helvetica", 12, "bold"), activebackground="#357ae8", activeforeground="white", bd=0, relief="ridge", cursor="hand2")
    select_btn.pack(pady=10)
    select_btn.bind("<Enter>", lambda e: select_btn.config(bg="#357ae8"))
    select_btn.bind("<Leave>", lambda e: select_btn.config(bg="#4e8cff"))
    select_btn.tooltip = tk.Label(root, text="Click to browse and select a CSV file.", font=("Helvetica", 9), bg="#f4f6fb", fg="#888", bd=0)

    progress_label = tk.Label(root, text="", font=("Helvetica", 10), bg="#f4f6fb", fg="#2d3e50")
    progress_label.pack(pady=5)

    if dnd_enabled:
        drop_area = tk.Label(root, text="⬇️ Drag and drop your CSV file here ⬇️", font=("Helvetica", 12, "italic"), bg="#eaf0fb", fg="#4e5d6c", width=40, height=4, bd=2, relief="groove")
        drop_area.pack(pady=15)
        drop_area.drop_target_register('DND_Files')
        drop_area.dnd_bind('<<Drop>>', drop)
        drop_area.tooltip = tk.Label(root, text="Drag and drop a CSV file to process.", font=("Helvetica", 9), bg="#f4f6fb", fg="#888", bd=0)
    else:
        drop_area = tk.Label(root, text="Drag and drop (requires tkinterdnd2) or click to select.", font=("Helvetica", 12, "italic"), bg="#eaf0fb", fg="#4e5d6c", width=40, height=4, bd=2, relief="groove")
        drop_area.pack(pady=15)

    # About/info button
    def show_about():
        messagebox.showinfo("About", "TextyPro Formatter\n\n- Drag and drop or select a CSV file.\n- Formats for TextyPro import.\n- Created using Python and Tkinter.")

    about_btn = tk.Button(root, text="About", command=show_about, width=8, bg="#eaf0fb", fg="#2d3e50", font=("Helvetica", 10), bd=0, relief="ridge", cursor="hand2")
    about_btn.pack(side="bottom", pady=8)

    root.mainloop()

if __name__ == "__main__":
    run_gui()