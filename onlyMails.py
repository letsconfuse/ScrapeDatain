import tkinter as tk
from tkinter import ttk, messagebox
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
collected_emails = set()

def human_like_wait():
    time.sleep(random.uniform(2, 4))

def create_edge_browser():
    options = Options()
    options.use_chromium = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Edge(options=options)
    return driver

def save_to_csv(filename, emails):
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Email"])
        for email in emails:
            writer.writerow([email])

def extract_emails_from_page(driver):
    emails = set()
    try:
        links = driver.find_elements(By.XPATH, '//a[starts-with(@href, "mailto:")]')
        for link in links:
            href = link.get_attribute("href")
            if href and "@" in href:
                email = href.replace("mailto:", "").strip()
                if "." in email and len(email) < 100:
                    emails.add(email)
    except:
        pass
    return emails

def open_selected_website():
    global active_driver, stop_flag
    stop_flag = False
    threading.Thread(target=lambda: open_browser_and_wait("http://www.yellowpages.in"), daemon=True).start()

def open_browser_and_wait(url):
    global active_driver
    try:
        active_driver = create_edge_browser()
        active_driver.get(url)
        #messagebox.showinfo("Action Required", "Search manually, scroll/load more. Then click 'Scrape Emails'.")
    except Exception as e:
        messagebox.showerror("Browser Error", str(e))

def start_scraping_loop():
    global active_driver, stop_flag, collected_emails
    if not active_driver:
        messagebox.showerror("Error", "No active browser session.")
        return

    def scraping_worker():
        while not stop_flag:
            new_emails = extract_emails_from_page(active_driver)
            collected_emails.update(new_emails)
            time.sleep(5)  # Check every 5 seconds

    threading.Thread(target=scraping_worker, daemon=True).start()
    messagebox.showinfo("Scraping Started", "Emails are being collected in the background.\nClick 'Stop' to finish and save.")

def stop_scraping():
    global stop_flag, collected_emails, active_driver
    stop_flag = True
    time.sleep(2)  # Allow last scrape to complete

    if not collected_emails:
        messagebox.showinfo("No Emails", "No emails were collected.")
        return

    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.csv"
    save_to_csv(filename, collected_emails)

    messagebox.showinfo("Scraping Stopped", f"{len(collected_emails)} emails saved to {filename}.")

# GUI Setup
root = tk.Tk()
root.title("YellowPages Email Scraper")
root.geometry("400x250")

ttk.Button(root, text="Open YellowPages.in", command=open_selected_website).pack(pady=20)
ttk.Button(root, text="Scrape", command=start_scraping_loop).pack(pady=10)
ttk.Button(root, text="Stop & Save", command=stop_scraping).pack(pady=10)

root.mainloop()
