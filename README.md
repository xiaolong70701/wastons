# WatsonsScraper 🛍️

A Python-based web scraper for extracting product information from **Watsons Taiwan** using **Selenium-Wire** and **Requests**. The scraper retrieves **Authorization tokens**, fetches product details via the Watsons API, and saves the data in a CSV file.

---

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
```

Alternatively, if you have added `wastons` as a package:

```bash
pip install git+https://github.com/xiaolong70701/wastons.git
```

---

## 🖥 **Install Microsoft Edge WebDriver (`msedgedriver`)**
The scraper uses **Microsoft Edge WebDriver (`msedgedriver`)** to automate browsing.  
You must **download and configure it** before running the script.

### **📌 Step 1: Download Edge WebDriver**
1. Open **[Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)**.
2. Download the **version that matches your Edge browser**.
   - Check your Edge version: Open **Edge** → Click `...` (Menu) → **Settings** → **About Microsoft Edge**.
3. Extract the downloaded file to a location accessible by your system.

### **📌 Step 2: Add `msedgedriver` to System PATH**
You must ensure that `msedgedriver` is accessible from the command line.

#### **Windows (Recommended Path)**
1. Move `msedgedriver.exe` to:
   ```
   C:\Program Files\msedgedriver\msedgedriver.exe
   ```
2. Add it to your **System PATH**:
   - Open **Start Menu** → Search `Environment Variables`.
   - Click `Edit the system environment variables`.
   - Under **System Properties**, go to `Advanced` → Click `Environment Variables`.
   - Find `Path` under **System Variables** → Click `Edit`.
   - Click `New` and add:  
     ```
     C:\Program Files\msedgedriver\
     ```
   - Click `OK` → Restart your computer.

#### **macOS (Default Path)**
Move `msedgedriver` to:
```bash
sudo mv msedgedriver /usr/local/bin/msedgedriver
```
Verify installation:
```bash
msedgedriver --version
```

If the command returns the version, it's correctly installed. After checking the installation of `msedgedriver`, open Terminal and input the following command to give driver permission:

```bash
chmod +x /usr/local/bin/msedgedriver
```

---

## 🚀 **Example Usage**

Run the following script to scrape Watsons for sunscreen stick (防曬棒) products:

```python
from wastons.scraper import WatsonsScraper

scraper = WatsonsScraper(query="防曬棒")
scraper.run()
```

This will:

1. Retrieve the Authorization token and PIM-SESSION-ID.
2. Scrape product data from the Watsons API.
3. Save the results in a CSV file located in `./data/Watsons_防曬棒.csv`.

---

## ⚙ **Customization**

### **Specify Save Folder**
By default, the CSV files are saved in `./data/`. You can specify a different folder:

```python
scraper = WatsonsScraper(query="面膜", save_folder="./my_results")
scraper.run()
```
📌 This will save the output file to `./my_results/Watsons_面膜.csv`.

### **Adjust Number of Products per Page**
To increase the number of products retrieved per API request:

```python
scraper = WatsonsScraper(query="洗面乳", page_size=50)
scraper.run()
```
📌 This increases the page size from **32** (default) to **50**.

---

## 📜 **License**
MIT License - Free to use and modify.

---

### ⭐ **Enjoy Scraping! 🚀**
If this project helps you, consider **starring ⭐ it on GitHub!**
```