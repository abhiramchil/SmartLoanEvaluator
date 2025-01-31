import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from data_extraction import extract_transactions_from_pdf

def upload_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        try:
            df = extract_transactions_from_pdf(file_path)
            messagebox.showinfo("Success", "File processed successfully!")
            print(df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")

# Create GUI window
root = tk.Tk()
root.title("Bank Statement Analyzer")
root.geometry("300x150")

tk.Label(root, text="Upload a PDF Bank Statement").pack(pady=10)
btn_upload = tk.Button(root, text="Upload PDF", command=upload_pdf)
btn_upload.pack(pady=20)

root.mainloop()