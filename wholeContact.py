import tkinter as tk
from tkinter import ttk
import threading
import time
import csv
import os
import random
import datetime
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

# Globals
stop_flag = False
active_driver = None
collected_data = []

def human_like_wait():
    time.sleep(random.uniform(2, 4))

def create_edge_browser():
    options = Options()
    options.use_chromium = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Edge(options=options)
    return driver

def save_to_csv(filename, data):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Email", "Phone"])
        for entry in data:
            writer.writerow(entry)

def extract_data_from_page(driver):
    data = []
    try:
        blocks = driver.find_elements(By.CLASS_NAME, "eachPopular")
        for block in blocks:
            try:
                name = block.find_element(By.CLASS_NAME, "eachPopularTitle").text.strip()
            except:
                name = ""
            try:
                email = block.find_element(By.XPATH, './/a[starts-with(@href, "mailto:")]').get_attribute("href").replace("mailto:", "").strip()
            except:
                email = ""
            try:
                phone = block.find_element(By.CLASS_NAME, "businessContact").text.strip()
            except:
                phone = ""

            if name or email or phone:
                data.append([name, email, phone])

    except Exception as e:
        show_status(f"[ERROR] Extracting data: {e}")
    return data

def open_selected_website():
    global active_driver, stop_flag
    stop_flag = False
    show_status("[INFO] Opening browser... Please wait.")
    threading.Thread(target=lambda: open_browser_and_wait("http://www.yellowpages.in"), daemon=True).start()

def open_browser_and_wait(url):
    global active_driver
    try:
        active_driver = create_edge_browser()
        active_driver.get(url)
        show_status("[INFO] Browser loaded. Select field and location, then click 'Scrape'.")
    except Exception as e:
        show_status(f"[ERROR] Browser failed: {e}")

def start_scraping_loop():
    global active_driver, stop_flag, collected_data
    if not active_driver:
        show_status("[ERROR] No active browser session.")
        return

    def scraping_worker():
        root.title("Scraping in progress...")
        show_status("[INFO] Scraping started. Click 'Quit & Save' to stop.")
        while not stop_flag:
            new_data = extract_data_from_page(active_driver)
            added = 0
            for entry in new_data:
                if entry not in collected_data:
                    collected_data.append(entry)
                    added += 1
            if added > 0:
                show_status(f"[DATA] Added {added} new entries.")
            time.sleep(5)
        root.title("YellowPages Data Scraper")

    threading.Thread(target=scraping_worker, daemon=True).start()

def stop_scraping():
    global stop_flag, collected_data, active_driver
    stop_flag = True
    time.sleep(2)

    if not collected_data:
        show_status("[WARN] No data collected.")
        return

    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_contacts.csv"
    save_to_csv(filename, collected_data)
    show_status(f"[DONE] {len(collected_data)} records saved to '{filename}'.")

    if active_driver:
        active_driver.quit()
        active_driver = None
        show_status("[INFO] Browser closed.")

def clear_data():
    global collected_data
    collected_data = []
    show_status("[INFO] Collected data cleared.")

# GUI Setup
root = tk.Tk()
root.title("YellowPages Data Scraper")
root.geometry("600x400")
root.configure(bg="#212B38")  # Dark background

style = ttk.Style()
style.theme_use("default")

# Base Button Style
style.configure("TButton", font=("Arial", 12), padding=6, relief="flat",
                background="#08C6AB", foreground="#FFFFFF")
style.map("TButton", background=[("active", "#5AFFE7")], foreground=[("active", "#FFFFFF")])

# Open Button → Teal with Aqua hover
style.configure("OpenButton.TButton", background="#08C6AB", foreground="#000000")
style.map("OpenButton.TButton", background=[("active", "#5AFFE7")], foreground=[("active", "#000000")])

# Collect Button 
style.configure("CollectButton.TButton", background="#08C6AB", foreground="#000000")
style.map("CollectButton.TButton", background=[("active", "#5AFFE7")], foreground=[("active", "#000000")])

# Clear Button 
style.configure("ClearButton.TButton", background="#08C6AB", foreground="#000000")
style.map("ClearButton.TButton", background=[("active", "#5AFFE7")], foreground=[("active", "#000000")])

# Save Button 
style.configure("SaveButton.TButton", background="#08C6AB", foreground="#000000")
style.map("SaveButton.TButton", background=[("active", "#5AFFE7")], foreground=[("active", "#000000")])

# Title Label
title_label = tk.Label(root, text="YellowPages.in Scraper",
                       font=("Helvetica", 18, "bold"),
                       bg="#212B38", fg="#FFFF00")  # Bright Yellow title
title_label.pack(pady=(20, 10))


# Button Frame
frame = tk.Frame(root, bg="#212B38")
frame.pack(pady=10)

open_button = ttk.Button(frame, text="Open YellowPages.in", command=open_selected_website, style="OpenButton.TButton")
open_button.grid(row=0, column=0, padx=15, pady=10)

scrape_button = ttk.Button(frame, text="Collect", command=start_scraping_loop, style="CollectButton.TButton")
scrape_button.grid(row=0, column=1, padx=15, pady=10)

clear_button = ttk.Button(frame, text="Clear Data", command=clear_data, style="ClearButton.TButton")
clear_button.grid(row=0, column=2, padx=15, pady=10)

quit_button = ttk.Button(frame, text="Save", command=stop_scraping, style="SaveButton.TButton")
quit_button.grid(row=0, column=3, padx=15, pady=10)

# Status Label
status_label = tk.Label(root, text="Status Log", font=("Arial", 12, "bold"),
                        bg="#212B38", fg="#FFFF00")
status_label.pack()

# Status Text
# status_text = tk.Text(root, height=12, width=72, wrap="word",
#                       state="disabled", bg="#37465B", fg="#FFFFFF",
#                       font=("Courier", 10))

status_text = tk.Text(root, height=12, width=72, wrap="word", state="disabled",
                      bg="#37465B", relief="groove", fg="#FFFFFF", font=("Courier", 11))


status_text.pack(pady=10, padx=10)


def show_status(message):
    status_text.config(state="normal")
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    status_text.insert(tk.END, f"[{timestamp}] {message}\n")
    status_text.see(tk.END)
    status_text.config(state="disabled")

def on_closing():
    global stop_flag
    stop_flag = True
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

show_status("[INFO] Press 'Open YellowPages.in' to start the browser.")

root.mainloop()
