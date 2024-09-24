import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

def init_db():
    with sqlite3.connect('residential_society.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS flats (
                flat_no TEXT PRIMARY KEY,
                owner TEXT,
                family_members INTEGER
            )
        ''')

def clear_fields():
    for entry in (entry_flat_no, entry_owner, entry_family_members):
        entry.delete(0, END)

def execute_db(func, *args):
    with sqlite3.connect('residential_society.db') as conn:
        return func(conn, *args)

def show_message(title, message, is_success):
    if is_success:
        messagebox.showinfo(title, message)
    else:
        messagebox.showerror(title, message)

def add_record():
    flat_no = entry_flat_no.get().strip()
    owner = entry_owner.get().strip()
    family_members = entry_family_members.get().strip()

    if flat_no and owner and family_members.isdigit() and int(family_members) >= 0:
        try:
            execute_db(lambda conn: conn.execute(
                "INSERT INTO flats (flat_no, owner, family_members) VALUES (?, ?, ?)", 
                (flat_no, owner, int(family_members))
            ))
            show_message("Success", "Record added successfully!", True)
            clear_fields()
        except sqlite3.IntegrityError:
            show_message("Error", "Flat number already exists.", False)
    else:
        show_message("Error", "Please fill all fields correctly!", False)

def search_record():
    flat_no = entry_flat_no.get().strip()
    record = execute_db(lambda conn: conn.execute("SELECT * FROM flats WHERE flat_no = ?", (flat_no,)).fetchone())
    if record:
        entry_owner.delete(0, END)
        entry_family_members.delete(0, END)
        entry_owner.insert(0, record[1])
        entry_family_members.insert(0, record[2])
    else:
        show_message("Error", "Flat not found!", False)

def modify_record():
    flat_no = entry_flat_no.get().strip()
    owner = entry_owner.get().strip()
    family_members = entry_family_members.get().strip()

    if flat_no and owner and family_members.isdigit() and int(family_members) >= 0:
        execute_db(lambda conn: conn.execute(
            "UPDATE flats SET owner = ?, family_members = ? WHERE flat_no = ?", 
            (owner, int(family_members), flat_no)
        ))
        show_message("Success", "Record updated successfully!", True)
        clear_fields()
    else:
        show_message("Error", "Please fill all fields correctly!", False)

def delete_record():
    flat_no = entry_flat_no.get().strip()
    if flat_no:
        execute_db(lambda conn: conn.execute("DELETE FROM flats WHERE flat_no = ?", (flat_no,)))
        show_message("Success", "Record deleted successfully!", True)
        clear_fields()
    else:
        show_message("Error", "Please enter a flat number to delete.", False)

def display_records():
    for row in tree.get_children():
        tree.delete(row)
    records = execute_db(lambda conn: conn.execute("SELECT * FROM flats").fetchall())
    for record in records:
        tree.insert("", "end", values=record)

# Initialize the main window
root = Tk()
root.title("Residential Society Record Modifier")
root.configure(bg="#ADD8E6")  # Light blue background

# GUI layout
labels = ["Flat No", "Owner of Flat", "No. of Family Members"]
entries = [Entry(root) for _ in labels]
for i, label in enumerate(labels):
    Label(root, text=label, bg="#ADD8E6",font=('Arial Bold',17)).grid(row=i, column=0, padx=10, pady=10)
    entries[i].grid(row=i, column=1, padx=10, pady=10)

entry_flat_no, entry_owner, entry_family_members = entries

# Buttons with white background and colored text
Button(root, text="Add", command=add_record, bg="white", fg="black",font=('Arial',15)).grid(row=4, column=0, padx=10, pady=10)
Button(root, text="Search", command=search_record, bg="white", fg="black",font=('Arial',15)).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Modify", command=modify_record, bg="white", fg="black",font=('Arial',15)).grid(row=5, column=0, padx=10, pady=10)
Button(root, text="Delete", command=delete_record, bg="white", fg="black",font=('Arial',15)).grid(row=5, column=1, padx=10, pady=10)
Button(root, text=" Display ", command=display_records, bg="white", fg="black",font=('Arial',15)).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Treeview for displaying records
tree = ttk.Treeview(root, columns=("Flat No", "Owner", "Family Members"), show='headings')
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Initialize the database and run the application
init_db()
root.mainloop()
