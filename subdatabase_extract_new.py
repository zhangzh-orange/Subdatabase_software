import tkinter as tk
from tkinter import filedialog
import pandas as pd
from Bio import SeqIO
import logging

logging.basicConfig(filename="app.log",level=logging.DEBUG)

# Constants
ANALYZER_MAXQUANT = "MaxQuant"
ANALYZER_THERMO_PROTEOME_DISCOVERER = "Thermo Proteome Discoverer"

def error_back():
    error_back_window = tk.Toplevel(root)
    error_back_window.title("Error")

    def restart_and_close():
        restart()
        error_back_window.destroy()

    error_label = tk.Label(error_back_window, text="Error in data identification, please restart with\nother data or contact the author.", width=50)
    error_label.pack()

    button_restart = tk.Button(error_back_window, text="Restart", command=restart_and_close, height=1, width=10)
    button_restart.pack(pady=(10,10), padx=(15, 20))

def show_error_message(error_message):
    """Show error message"""
    error_window = tk.Toplevel(root)
    error_window.title("Error")

    error_label = tk.Label(error_window, text=error_message, wraplength=300)
    error_label.pack(padx=(20,20), pady=(5, 15))

    button_ok = tk.Button(error_window, text="OK", command=error_window.destroy, height=1, width=10)
    button_ok.pack(pady=(5, 15), padx=(15, 20))

def show_asking_window():
    try:
        protein_groups_path = entry_protein_groups.get()
        df = pd.read_table(protein_groups_path, sep="\t")

        analyzer_software = determine_analyzer_software(df)

        asking_window = tk.Toplevel(root)
        asking_window.title("Confirm")

        def yes_action():
            asking_window.destroy()
            process_files(analyzer_software)

        def no_action():
            asking_window.destroy()
            error_back()

        def not_sure_action():
            asking_window.destroy()
            process_files(analyzer_software)

        asking_label = tk.Label(asking_window, text=f"Do this result file from {analyzer_software}")
        asking_label.grid(row=0, column=1, columnspan=3) # Span across 3 columns

        button1 = tk.Button(asking_window, text="Yes", command=yes_action, width=15)
        button1.grid(row=1, column=1, pady=(5, 15), padx=(15, 20))

        button2 = tk.Button(asking_window, text="No", command=no_action, width=15)
        button2.grid(row=1, column=2, pady=(5, 15), padx=(15, 20))

        button3 = tk.Button(asking_window, text="Not Sure", command=not_sure_action, width=15)
        button3.grid(row=1, column=3, pady=(5, 15), padx=(15, 20))

    # If errors occur, display it
    except FileNotFoundError as e:
        show_error_message(f"File not found: {str(e)}")
    except pd.errors.EmptyDataError:
        show_error_message("The data file is empty.")
    except Exception as e:
        show_error_message(f"An error occurred: {str(e)}")

def determine_analyzer_software(df):
    if "Majority protein IDs" in df.columns and "Accession" not in df.columns:
        return ANALYZER_MAXQUANT
    elif "Majority protein IDs" not in df.columns and "Accession" in df.columns:
        return ANALYZER_THERMO_PROTEOME_DISCOVERER
    else:
        return None

def process_files(analyzer_software):
    """Input is the protein id's column name"""
    protein_groups_path = entry_protein_groups.get()
    fasta_file_path = entry_fasta_file.get()

    if not protein_groups_path or not fasta_file_path:
        label_status.config(text="Please give both Protein Groups and Fasta Database files.")
        return

    df = pd.read_table(protein_groups_path, sep="\t")

    column_name = "Majority protein IDs" if analyzer_software == ANALYZER_MAXQUANT else "Accession"

    uniprot_id_list = [prot.strip() for proteins in df[column_name].to_list() for prot in proteins.split(";")]

    fasta_file = SeqIO.parse(fasta_file_path, "fasta")
    my_records = []

    for seq_record in fasta_file:
        if seq_record.id.split("|")[1].strip() in uniprot_id_list:
            my_records.append(seq_record)

    output_file_path = filedialog.asksaveasfilename(defaultextension=".fasta", filetypes=[("Fasta files", "*.fasta")])
    prot_num = SeqIO.write(my_records, output_file_path, "fasta")

    label_status.config(text=f"Processing completed. Output file saved. \nSubdatabase contains {prot_num} protein sequences.")

def restart():
    entry_protein_groups.delete(0, tk.END)
    entry_fasta_file.delete(0, tk.END)
    label_status.config(text="")

# Create the main window
root = tk.Tk()
root.title("Subdatabase Extraction")

# Create and place widgets
label_protein_groups = tk.Label(root, text="Searching Result File:", width=20)
label_protein_groups.grid(row=0, column=0, pady=(10, 0))

entry_protein_groups = tk.Entry(root, width=50)
entry_protein_groups.grid(row=0, column=1, pady=(10, 0))

button_browse_protein_groups = tk.Button(root, text="Browse", command=lambda: entry_protein_groups.insert(0, filedialog.askopenfilename()), width=10)
button_browse_protein_groups.grid(row=0, column=2, pady=(10, 0), padx=(15, 20))

label_fasta_file = tk.Label(root, text="Original Database File:", width=20)
label_fasta_file.grid(row=1, column=0, pady=(10, 0))

entry_fasta_file = tk.Entry(root, width=50)
entry_fasta_file.grid(row=1, column=1, pady=(10, 0))

button_browse_fasta_file = tk.Button(root, text="Browse", command=lambda: entry_fasta_file.insert(0, filedialog.askopenfilename()), width=10)
button_browse_fasta_file.grid(row=1, column=2, pady=(10, 0), padx=(15, 20))

button_run = tk.Button(root, text="Run", command=show_asking_window, height=1, width=10) # Adjust height and width
button_run.grid(row=2, column=2, pady=(20, 20), padx=(15, 20))

label_status_file = tk.Label(root, text="Running result:", width=20)
label_status_file.grid(row=2, column=0, pady=(20, 20))

label_status = tk.Label(root, text="", bg="#cfccc9", height=2, width=50, cursor="circle")
label_status.grid(row=2, column=1, pady=(10, 10))

button_restart = tk.Button(root, text="Restart", command=restart, height=1, width=20)
button_restart.grid(row=3, column=1, pady=(5, 15), padx=(15, 20))

root.mainloop()
