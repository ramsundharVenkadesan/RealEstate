# Real Estate Data Intelligence & API Pipeline 🏠📊

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scrapy](https://img.shields.io/badge/Scrapy-059922?style=flat&logo=scrapy&logoColor=white)](https://scrapy.org/)

An automated **End-to-End ETL (Extract, Transform, Load) Pipeline** that scrapes live real estate data, performs complex data sanitization, and generates visual market intelligence reports via a RESTful API.

---

## 🏗️ System Architecture

The project is designed with a modular "Service-Oriented" architecture, ensuring each stage of the data lifecycle is handled by a specialized component:



### 1. Extraction (`Spider.py`)
A robust **Scrapy** engine that crawls real estate domains. It handles:
* Dynamic pagination.
* Field extraction for price, address, beds, baths, and square footage.
* Ethical scraping via 5-second download delays and custom User-Agents.

### 2. Transformation (`Analyze.py`)
A data-cleaning layer that handles the "noise" of web data. It features:
* **Regex Sanitization:** Strips currency symbols and formatting.
* **Fraction Handling:** Converts complex strings (e.g., "1/2 bath") into mathematical floats for statistical accuracy.

### 3. Visualization (`Plot.py`)
Generates high-resolution JPEG reports using **Pandas** and **Matplotlib**. It calculates:
* Price distribution histograms.
* Market KPIs (Average Price, SqFt, and Bed/Bath counts).
* Agency Dominance (identifying the top listing agency in a region).

### 4. Orchestration & API (`Pipeline.py` & `App.py`)
* **Pipeline:** Manages the sequential execution of subprocesses.
* **FastAPI:** Exposes the entire system as a REST service, allowing users to trigger a full report generation via a simple HTTP POST request.

---

## 🛠️ Tech Stack
* **Language:** Python
* **Web Scraping:** Scrapy
* **Web Framework:** FastAPI, Uvicorn
* **Data Analysis:** Pandas, NumPy
* **Visualization:** Matplotlib
* **Logic:** Subprocess, Regular Expressions (Regex)

---

## 🚦 Getting Started

### Installation
```bash
# Clone the repository
git clone [https://github.com/yourusername/real-estate-pipeline.git](https://github.com/yourusername/real-estate-pipeline.git)
cd real-estate-pipeline

# Install dependencies
pip install scrapy fastapi uvicorn pandas matplotlib
