# Product Scraper 🤖

A Python-based web scraper that extracts product listings from Myntra.com across multiple pages. Perfect for market research and price tracking.

![Scraper Demo](https://img.icons8.com/color/96/000000/python--v1.png) ![Myntra Logo](https://img.icons8.com/color/96/000000/myntra.png)

## Table of Contents
- [Features](#features-)
- [Requirements](#requirements-)
- [Installation](#installation-)
- [Usage](#usage-)
- [Output Format](#output-format-)
- [Customization](#customization-)
- [Troubleshooting](#troubleshooting-)
- [Disclaimer](#disclaimer-)

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
   cd myntra-scraper

2. **Install Dependencies**
   pip install -r requirements.txt

## Usage 🚀

Run the Scraper:

bash
Copy
python myntra_scraper.py
Enter Product Type:

plaintext
Copy
Search product (e.g., shirts, jeans): running shoes
Monitor Progress:

plaintext
Copy
📃 Processing page 1/7...
✔️ Page 1 completed - Total: 50 products
Find Results:

Navigate to /product_details folder

Open myntra_[your-search-term].json

Output Format 📄
Sample JSON Structure:

json
Copy
[
  {
    "brand": "Nike",
    "name": "Air Zoom Pegasus 38",
    "url": "https://www.myntra.com/nike-air-zoom-pegasus-38"
  }
]