# WatsonsScraper 🛍️

A Python-based web scraper for extracting product information from **Watsons Taiwan** using **Selenium-Wire** and **Requests**. The scraper retrieves **Authorization tokens**, fetches product details via the Watsons API, and saves the data in a CSV file.

## 📌 Features
✔ **Automated Authorization Retrieval** - Uses `Selenium-Wire` to extract `Authorization` and `PIM-SESSION-ID`.  
✔ **Watsons API Data Scraping** - Fetches product details including **name, price, image URL, and product link**.  
✔ **Progress Bar with `tqdm`** - Displays real-time progress while scraping.  
✔ **CSV Data Storage** - Saves extracted data in a structured CSV format.  
✔ **Customizable Folder Path** - Allows users to specify the save location (defaults to `./data`).  

---

## 📦 **Installation**
Before running the scraper, install the required dependencies:

```bash
pip install selenium-wire requests tqdm
