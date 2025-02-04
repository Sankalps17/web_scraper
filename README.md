# Product Scraper 🤖

A Python-based web scraper that extracts product listings from Myntra.com across multiple pages.

## Table of Contents
- [Features](#features-)
- [Requirements](#requirements-)
- [Installation](#Installation-)
- [Usage](#usage-)
- [Output Format](#output-format-)

## Features ✨
- Multi-page scraping
- Automatic Chrome driver setup
- JSON output with brand, product name, and URLs
- Dedicated output folder organization
- Real-time progress tracking

## Requirements 📦
- Python 3.7+
- Google Chrome browser
- Stable internet connection

## Installation 🛠️

1. **Clone Repository**:
   ```bash
   git clone https://github.com/Sankalps17/web_scraper

2. **Install Dependencies**
   pip install -r requirements.txt

## Usage 🚀

1. Run the Scraper: Both scrapers perform the same function, but product_details_scraper.py uses Selenium, while using_bs4.py utilizes both Selenium and bs4.

```bash
  python product_details_scraper.py
```
```bash
  python using_bs4.py
```

2. Enter Product Type:
```plaintext
Search product (e.g., shirts, jeans): running shoes
```
3. Monitor Progress:

```plaintext
📃 Processing page 1/7...
✔️ Page 1 completed - Total: 50 products
```

4. Find Results:

Navigate to /product_details folder

Open myntra_[your-search-term].json

## Output Format 📄
Sample JSON Structure:

```json
[
  {
    "brand": "Nike",
    "name": "Air Zoom Pegasus 38",
    "url": "https://www.myntra.com/nike-air-zoom-pegasus-38"
  }
]
```
