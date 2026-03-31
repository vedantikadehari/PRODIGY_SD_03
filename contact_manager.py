import tkinter as tk
from tkinter import messagebox, Scrollbar
import json
import os

# ------------------- STORAGE -------------------
FILE_NAME = "contacts.json"

def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_contacts():
    with open(FILE_NAME, "w") as f:
        json.dump(contacts, f, indent=4)

contacts = load_contacts()

# ------------------- LOGIC -------------------
def update_listbox(data=None):
    listbox.delete(0, tk.END)
    display = data if data else contacts
    for c in display:
        listbox.insert(tk.END, f"{c['name']} | {c['phone']} | {c['email']} | {c['category']}")

def create_popup(title):
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("300x320")
    popup.configure(bg="white")
    return popup

def validate_phone(p):
    return (p.isdigit() and len(p) <= 10) or p == ""

# ------------------- ADD CONTACT -------------------
def add_contact():
    popup = create_popup("Add Contact")

    tk.Label(popup, text="Name", bg="white").pack(pady=5)
    name = tk.Entry(popup)
    name.pack()

    tk.Label(popup, text="Phone", bg="white").pack(pady=5)
    phone = tk.Entry(popup)
    phone.pack()

    tk.Label(popup, text="Email", bg="white").pack(pady=5)
    email = tk.Entry(popup)
    email.pack()

    tk.Label(popup, text="Category", bg="white").pack(pady=5)
    category = tk.Entry(popup)
    category.pack()

    # Enter key navigation
    name.bind("<Return>", lambda e: phone.focus())
    phone.bind("<Return>", lambda e: email.focus())
    email.bind("<Return>", lambda e: category.focus())
    category.bind("<Return>", lambda e: save())

    # Phone validation
    vcmd = popup.register(validate_phone)
    phone.config(validate="key", validatecommand=(vcmd, "%P"))

    def save():
        if not name.get() or not phone.get() or not email.get():
            messagebox.showwarning("Warning", "All fields required!")
            return

        if len(phone.get()) != 10:
            messagebox.showwarning("Warning", "Phone must be 10 digits!")
            return

        contacts.append({
            "name": name.get(),
            "phone": phone.get(),
            "email": email.get(),
            "category": category.get() or "Other"
        })

        save_contacts()
        update_listbox()
        popup.destroy()

    tk.Button(popup, text="Save", bg="black", fg="white",
              width=12, command=save).pack(pady=10)

# ------------------- UPDATE CONTACT -------------------
def update_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a contact")
        return

    idx = selected[0]
    c = contacts[idx]

    popup = create_popup("Update Contact")

    tk.Label(popup, text="Name", bg="white").pack(pady=5)
    name = tk.Entry(popup)
    name.insert(0, c['name'])
    name.pack()

    tk.Label(popup, text="Phone", bg="white").pack(pady=5)
    phone = tk.Entry(popup)
    phone.insert(0, c['phone'])
    phone.pack()

    tk.Label(popup, text="Email", bg="white").pack(pady=5)
    email = tk.Entry(popup)
    email.insert(0, c['email'])
    email.pack()

    tk.Label(popup, text="Category", bg="white").pack(pady=5)
    category = tk.Entry(popup)
    category.insert(0, c['category'])
    category.pack()

    # Enter navigation
    name.bind("<Return>", lambda e: phone.focus())
    phone.bind("<Return>", lambda e: email.focus())
    email.bind("<Return>", lambda e: category.focus())
    category.bind("<Return>", lambda e: save())

    # Phone validation
    vcmd = popup.register(validate_phone)
    phone.config(validate="key", validatecommand=(vcmd, "%P"))

    def save():
        if len(phone.get()) != 10:
            messagebox.showwarning("Warning", "Phone must be 10 digits!")
            return

        c['name'] = name.get()
        c['phone'] = phone.get()
        c['email'] = email.get()
        c['category'] = category.get()

        save_contacts()
        update_listbox()
        popup.destroy()

    tk.Button(popup, text="Update", bg="black", fg="white",
              width=12, command=save).pack(pady=10)

# ------------------- DELETE -------------------
def delete_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a contact")
        return

    contacts.pop(selected[0])
    save_contacts()
    update_listbox()

# ------------------- SEARCH -------------------
def search_contact():
    popup = create_popup("Search Contact")

    tk.Label(popup, text="Enter Name or Category", bg="white").pack(pady=5)
    entry = tk.Entry(popup)
    entry.pack()

    entry.bind("<Return>", lambda e: search())

    def search():
        keyword = entry.get().lower()
        result = [c for c in contacts if keyword in c['name'].lower() or keyword in c['category'].lower()]
        update_listbox(result)
        popup.destroy()

    tk.Button(popup, text="Search", bg="black", fg="white",
              width=12, command=search).pack(pady=10)

# ------------------- SHOW ALL -------------------
def show_all():
    update_listbox()

# ------------------- GUI -------------------
root = tk.Tk()
root.title("Contact Manager")
root.geometry("700x500")
root.configure(bg="#f0f4f8")

tk.Label(root, text="Contact Manager",
         font=("Helvetica", 20, "bold"),
         bg="#f0f4f8").pack(pady=10)

frame = tk.Frame(root)
frame.pack()

listbox = tk.Listbox(frame, width=80, height=15,
                     font=("Arial", 12),
                     bg="white",
                     selectbackground="#4a90e2")
listbox.pack(side=tk.LEFT)

scrollbar = Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

btn_frame = tk.Frame(root, bg="#f0f4f8")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", bg="#4CAF50", fg="white",
          width=12, command=add_contact).grid(row=0, column=0, padx=5, pady=5)

tk.Button(btn_frame, text="Update", bg="#ff9800", fg="white",
          width=12, command=update_contact).grid(row=0, column=1, padx=5, pady=5)

tk.Button(btn_frame, text="Delete", bg="#f44336", fg="white",
          width=12, command=delete_contact).grid(row=0, column=2, padx=5, pady=5)

tk.Button(btn_frame, text="Search", bg="#2196f3", fg="white",
          width=12, command=search_contact).grid(row=1, column=0, padx=5, pady=5)

tk.Button(btn_frame, text="Show All", bg="#9c27b0", fg="white",
          width=12, command=show_all).grid(row=1, column=1, padx=5, pady=5)

update_listbox()

root.mainloop()