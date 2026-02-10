# YellowPages.in Data Extraction Suite

A technical utility designed for structured data extraction from YellowPages.in. This suite provides a graphical interface for real-time monitoring of scraping tasks, incorporating human-like interaction delays and data deduplication logic to ensure high data integrity.

## Core Features

- **Human-Centric Interaction**: Implements randomized delays (2–4 seconds) to mimic human browsing patterns and mitigate rapid-bot detection.
- **Asynchronous GUI**: A threaded Tkinter-based interface that maintains responsiveness during intensive data collection tasks.
- **Real-Time Instrumentation**: Integrated status logs within the application for monitoring extraction progress.
- **Data Integrity Layer**: Automated deduplication logic to prevent redundant record entry during a single session.
- **Flexible Export**: Concurrent data saving to timestamped CSV files.

## Visual Documentation

### Graphical User Interface Execution
<p align="center">
  <img src="image02.png" alt="Working GUI Screenshot">
</p>

<p align="center">
  <img src="image03.png" alt="Working GUI Screenshot">
</p>

## Technical Implementation

| Component | Technology | Role |
| :--- | :--- | :--- |
| Core Engine | Selenium WebDriver | Browser automation and data extraction |
| Frontend | Tkinter | Graphical user interface and logging |
| Driver | msedgedriver | Microsoft Edge integration |
| Multi-threading | Python `threading` | Decoupling extraction logic from the UI thread |

## Installation and Deployment

### 1. Environment Preparation
Ensure a Python 3.x environment is active and the Microsoft Edge browser is installed.

### 2. Dependency Installation
Execute the following command to install the required automation library:
```bash
pip install selenium
```

### 3. Execution
Launch the primary extraction utility:
```bash
python wholeContact.py
```

### 4. Operational Protocol
1. **Initialize Browser**: Click **Open YellowPages.in** within the GUI.
2. **Configure Search**: Manually perform the desired search/location query in the opened browser instance.
3. **Extraction**: Click **Collect** to begin processing the current results page.
4. **Finalization**: Click **Save** to finalize data extraction and export the collected dataset to CSV.

## Data Output Structure

The utility exports data in a standardized CSV format: `YYYYMMDD_HHMMSS_contacts.csv`.

| Attribute | Description |
| :--- | :--- |
| **Name** | The registered business or entity name |
| **Email** | Publicly listed contact email address |
| **Phone Number** | Primary contact number |

## Streamlined Alternative: `onlyMails.py`

For use cases requiring only email addresses without the overhead of a graphical interface, the `onlyMails.py` utility is provided.

- **Objective**: High-speed, focused email extraction.
- **Design**: Lightweight script without GUI dependencies.
- **Output**: Single-column CSV containing validated email strings.

## Legal and Ethical Disclaimer

> [!IMPORTANT]
> This tool is developed strictly for educational and research purposes. Automated extraction of data from YellowPages.in may conflict with their Terms of Service. Users are responsible for ensuring compliance with local laws and the robots.txt directives of the target domain. This system is intended to demonstrate Selenium and Tkinter integration patterns, not for high-volume production scraping.

## Architectural Notes

- **Manual Navigation**: This tool prioritizes manual pagination and search input to maintain a low-detection profile.
- **Customization**: Wait intervals and post-execution browser behavior can be modified within the `human_like_wait()` and `stop_scraping()` functions respectively.

---
**Author**: letsconfuse  
**License**: Standard Open Source conventions apply.
