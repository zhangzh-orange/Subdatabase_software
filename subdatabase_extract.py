import tkinter as tk
from tkinter import filedialog
import pandas as pd
from Bio import SeqIO

def process_files():
    protein_groups_path = entry_protein_groups.get()
    fasta_file_path = entry_fasta_file.get()

    if not protein_groups_path or not fasta_file_path:
        label_status.config(text="Please give both Protein Groups and Fasta Database files.")
        return

    df = pd.read_table(protein_groups_path, sep="\t")

    uniprot_id_list = [prot.strip() for proteins in df['Majority protein IDs'].to_list() for prot in proteins.split(";")]

    fasta_file = SeqIO.parse(fasta_file_path, "fasta")
    my_records = []
    record_id = []

    for seq_record in fasta_file:
        if seq_record.id.split("|")[1].strip() in uniprot_id_list:
            my_records.append(seq_record)
            record_id.append(seq_record.id.split("|")[1].strip())

    output_file_path = filedialog.asksaveasfilename(defaultextension=".fasta", filetypes=[("Fasta files", "*.fasta")])
    prot_num = SeqIO.write(my_records, output_file_path, "fasta")

    label_status.config(text="Processing completed. Output file saved. \nSubdatabase contain {} protein sequences".format(prot_num))

def restart():
    entry_protein_groups.delete(0, tk.END)
    entry_fasta_file.delete(0, tk.END)
    label_status.config(text="")

# Create the main window
root = tk.Tk()
root.title("Subdatabase Extraction")

# Create and place widgets
label_protein_groups = tk.Label(root, text="Protein Groups File:",width=20)
label_protein_groups.grid(row=0, column=0, pady=(10, 0))

entry_protein_groups = tk.Entry(root, width=50)
entry_protein_groups.grid(row=0, column=1, pady=(10, 0))

button_browse_protein_groups = tk.Button(root, text="Browse", command=lambda: entry_protein_groups.insert(0, filedialog.askopenfilename()),width=10)
button_browse_protein_groups.grid(row=0, column=2, pady=(10, 0), padx=(15, 20))

label_fasta_file = tk.Label(root, text="Original Database File:",width=20)
label_fasta_file.grid(row=1, column=0, pady=(10, 0))

entry_fasta_file = tk.Entry(root, width=50)
entry_fasta_file.grid(row=1, column=1, pady=(10, 0))

button_browse_fasta_file = tk.Button(root, text="Browse", command=lambda: entry_fasta_file.insert(0, filedialog.askopenfilename()),width=10)
button_browse_fasta_file.grid(row=1, column=2, pady=(10, 0), padx=(15, 20))

button_run = tk.Button(root, text="Run", command=process_files, height=1, width=10)  # Adjust height and width
button_run.grid(row=2, column=2, pady=(20, 20), padx=(15, 20))

label_status_file = tk.Label(root, text="Running result:",width=20)
label_status_file.grid(row=2, column=0, pady=(20, 20))

# frame = tk.Frame(root, width=50)
# frame.grid(row=2, column=1, pady=(10, 15))

# label_status = tk.Label(root, text="",bg="#cfccc9",width=50,cursor="circle")
# label_status.grid(row=2, column=1, pady=(10, 15))
label_status = tk.Label(root, text="",bg="#cfccc9",height=2, width=50,cursor="circle")
label_status.grid(row=2, column=1, pady=(10, 10))

button_restart = tk.Button(root, text="Restart", command=restart, height=1, width=20)
button_restart.grid(row=3, column=1, pady=(5, 15), padx=(15, 20))

root.mainloop()