import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests
import validators

def is_valid_url(url):
    return validators.url(url)

def block_website():
    ip = ip_entry.get()
    blocked_site = website_entry.get()
    if not ip or not blocked_site:
        messagebox.showerror("Error", "Both IP Address and Website URL are required.")
        return
    if not is_valid_url(blocked_site):
        messagebox.showerror("Error", "Invalid URL")
        return
    host_path = "C:/Windows/System32/drivers/etc/hosts"
    try:
        with open(host_path, "r+") as host_file:
            content = host_file.read()
            if blocked_site not in content:
                host_file.write(ip + " " + blocked_site.replace("https://","") + "\n")
            else:
                messagebox.showinfo("Info", f"{blocked_site} is already blocked.")
    except IOError as e:
        messagebox.showerror("Error", f"Failed to open or write to hosts file: {e}")
        return
    try:
        conn = sqlite3.connect('xyz1.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS blocked_websites
                       (ip TEXT,
                       url TEXT,
                       CONSTRAINT unique_ip_url UNIQUE(ip, url))''')
        cursor.execute('INSERT INTO blocked_websites(ip, url) VALUES (?, ?)', (ip, blocked_site))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showinfo("Info", f"{blocked_site} is already blocked.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to insert into database: {e}")
    finally:
        conn.close()
    messagebox.showinfo("Blocked", f"{blocked_site} has been blocked.")

def unblock_website():
    ip = ip_entry.get()
    blocked_site = website_entry.get()
    if not ip or not blocked_site:
        messagebox.showerror("Error", "Both IP Address and Website URL are required.")
        return
    if not is_valid_url(blocked_site):
        messagebox.showerror("Error", "Invalid URL")
        return
    host_path = "C:/Windows/System32/drivers/etc/hosts"
    try:
        with open(host_path, "r") as host_file:
            lines = host_file.readlines()
        blocked_site = blocked_site.replace("https://","")
        with open(host_path, "w") as host_file:
            for line in lines:
                if not (blocked_site in line and ip in line):
                    host_file.write(line)
    except IOError as e:
        messagebox.showerror("Error", f"Failed to open or write to hosts file: {e}")
        return
    try:
        conn = sqlite3.connect('xyz1.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM blocked_websites WHERE ip=? AND url=?', (ip, blocked_site))
        conn.commit()
        messagebox.showinfo("Unblocked", f"{blocked_site} has been unblocked.")
    except sqlite3.Error as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to delete from database: {e}")
    finally:
        conn.close()

root = tk.Tk()
root.title("Website Blocker")
root.configure(bg="aqua")

label1 = tk.Label(root, text="Enter Ip Address:", fg='black', bg='aqua')
label1.pack(pady=5)
label1.config(font=('Comic Sans', 12))
ip_entry = tk.Entry(root, width=50)
ip_entry.pack(ipady=5)

label = tk.Label(root, text="Enter Website url:", fg='black', bg='aqua')
label.pack(pady=5)
label.config(font=('Comic Sans', 12))
website_entry = tk.Entry(root, width=50)
website_entry.pack(ipady=5)

block_button = tk.Button(root, text="Block", command=block_website, width=15, fg='white', bg='black')
block_button.config(font=('Comic Sans', 12))
block_button.pack(ipady=5, pady=20)

unblock_button = tk.Button(root, text="Unblock", command=unblock_website, width=15, fg='white', bg='black')
unblock_button.config(font=('Comic Sans', 12))
unblock_button.pack(ipady=5, pady=20)

root.mainloop()