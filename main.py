import tabula

pdf_path = "uploads/Untitled.pdf"

dfs = tabula.read_pdf(pdf_path, pages="all")

# Save each table to a separate CSV file
for i, df in enumerate(dfs):
    df.to_csv(f"all_pages_table{i}.csv", index=False)
