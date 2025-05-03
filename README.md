# YellowPages.in Data Scraper

<p align="center">
  <img src="image.png" alt="YellowPages Scraper GUI">
</p>

A simple Python application with a **Tkinter GUI** that uses **Selenium WebDriver (Microsoft Edge Chromium)** to scrape **business names, emails, and phone numbers** from [YellowPages.in](http://www.yellowpages.in).

✅ Opens a browser for manual search input
✅ Collects data every few seconds from visible page blocks
✅ Exports collected data into a CSV file
✅ Logs scraping status inside the app

---

## 🚀 Features

* **Human-like scraping delay** (2–4 seconds randomized) to avoid rapid bot detection
* **GUI interface** for non-technical users
* **Real-time status log** in the application
* **Data deduplication** (avoids saving duplicate entries)
* **Threaded scraping** (keeps UI responsive)
* **Colorful themed interface**

## 🖼️ GUI Preview (Working Example)

<p align="center">
  <img src="image02.png" alt="Working GUI Screenshot">
</p>

*Above: A live screenshot of the scraper in action.*


---


## 💻 Installation & Usage

1. Install dependencies:

   ```bash
   pip install selenium
   ```
2. Ensure you have **Microsoft Edge** installed with a compatible `msedgedriver` in PATH
3. Run the script:

   ```bash
   python yellowpages_scraper.py
   ```
4. In the app:

   * Click **Open YellowPages.in** → manually enter your desired **search and location**
   * Click **Collect** to start scraping
   * Click **Save** to stop scraping and export CSV
   * Click **Clear Data** to reset collected results

The scraper collects from **visible search results on the current page**—pagination is manual.

---

## ⚠️ Disclaimer

🛑 **IMPORTANT: This tool is for educational purposes only.**

* Scraping [YellowPages.in](http://www.yellowpages.in) **violates their Terms of Service**.
* This code **does not bypass bot detection or anti-scraping mechanisms**—instead, it loads the site normally in a browser and lets you manually input fields.
* Any scraping of the site should comply with legal, ethical, and robots.txt rules.
* I do not encourage scraping sites that prohibit automated data collection.

**This project is intended as a learning example of Selenium, Tkinter, and data extraction techniques, not as a production tool.**

---

## 📝 Notes

* This scraper **does not spoof headless browsing** or aggressively avoid detection.
* Since it waits for manual input and runs in a full browser session, it **mimics a human user** more closely than headless bots.
* It only scrapes content **currently visible on the page**—no automated navigation or pagination.

---

Feel free to update the image path and let me know if you'd like to add installation instructions for other environments or drivers!
