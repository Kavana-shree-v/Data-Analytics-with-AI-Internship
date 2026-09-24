# 🍽️ Customer Food Product & Preference Analysis Dashboard

> **Author:** Kavana Shree V
> **Dataset:** Swiggy Food Delivery — 50,000 Orders [[www.kaggle.com/datasets/vanithacheerla/swiggy-food-delivery-dataset](https://www.kaggle.com/datasets/vanithacheerla/swiggy-food-delivery-dataset)]
> **Tool:** Python · Streamlit · Plotly
> **File:** `Kavana Shree V.py`

---

## 📌 Project Overview

This project builds a **multi-page, fully interactive analytics dashboard** that analyses customer food preferences, ordering behaviour, restaurant performance, delivery metrics, and satisfaction patterns from a Swiggy food delivery dataset containing **50,000 orders** across **8 Indian cities**.

The objective is to answer key business questions:

- What do customers usually prefer to order?
- Which food categories and cuisines are the most popular?
- How does purchasing behaviour change by time, city, restaurant, and customer segment?
- Do discounts drive more orders or repeat purchases?
- What factors are associated with higher customer ratings?

---

## 🗂️ Project Files

| File                   | Description                                                 |
| ---------------------- | ----------------------------------------------------------- |
| `Kavana Shree V.py`  | Main Streamlit dashboard application (all code in one file) |
| `requirements.txt`   | Python package dependencies                                 |
| `README.md`          | This project documentation                                  |
| `archive (2).zip`    | Raw dataset ZIP (place in same folder as the`.py` file)   |
| `archive_extracted/` | Auto-extracted folder (created on first run)                |

---

## 📊 Dataset Description

| Column                | Type   | Description                                 |
| --------------------- | ------ | ------------------------------------------- |
| `Order_ID`          | string | Unique order identifier                     |
| `Order_Date`        | date   | Date of order placement                     |
| `Order_Time`        | time   | Time of order placement                     |
| `Delivery_Date`     | date   | Date of delivery                            |
| `Customer_ID`       | string | Unique customer identifier                  |
| `Restaurant_ID`     | string | Unique restaurant identifier                |
| `Restaurant_Name`   | string | Name of the restaurant                      |
| `City`              | string | City of the order (8 cities)                |
| `Cuisines`          | string | Cuisine type (15 types)                     |
| `Food_Category`     | string | Food category (20 types)                    |
| `Quantity`          | int    | Number of items ordered                     |
| `Order_Value`       | int    | Gross order amount (₹)                     |
| `Discount`          | float  | Discount applied (₹)                       |
| `Delivery_Charges`  | int    | Delivery fee (₹)                           |
| `Tax`               | float  | Tax amount (₹)                             |
| `Net_Revenue`       | float  | Net revenue after discount + tax + delivery |
| `Payment_Method`    | string | UPI / Card / Wallet / Cash                  |
| `Order_Status`      | string | Delivered / Cancelled / Delayed             |
| `Delivery_Time`     | int    | Delivery duration (minutes)                 |
| `Delivery_Distance` | float  | Delivery distance (km)                      |
| `Customer_Rating`   | float  | Rating 1–5 (missing for cancelled orders)  |

---

## 🔢 Total Steps Involved in This Project

### Step 1 — Environment Setup

- Install Python 3.9+
- Install required libraries via `requirements.txt`
- Place the dataset ZIP in the project folder

### Step 2 — Data Loading

- Detect and read the CSV from the ZIP archive
- Cache data with `@st.cache_data` for performance

### Step 3 — Data Cleaning & EDA

- Parse `Order_Date`, `Delivery_Date` as datetime
- Parse `Order_Time` as time
- Check for missing values → **3,487 missing Customer_Rating** (cancelled orders)
- Check for duplicates → **0 duplicates**
- Verify data types for each column
- Identify cancelled/delayed orders
- Check outliers in Order_Value, Delivery_Time

### Step 4 — Feature Engineering

- Extract `Hour`, `Day`, `Weekday`, `Month`, `Year`, `Quarter` from dates/times
- Derive `IsWeekend` flag
- Create `Season` (Winter/Spring/Summer/Autumn)
- Create `TimeOfDay` (Morning/Afternoon/Evening/Night)
- Create `HasDiscount` flag
- Create `ValueSegment` bins (5 price buckets)
- Create `CustomerSegment` (Bronze/Silver/Gold) by net revenue quartiles

### Step 5 — KPI Computation

- Total orders, total customers, total revenue, net revenue
- Avg order value, avg quantity per order
- Avg customer rating
- Repeat customers count and percentage

### Step 6 — Food Preference Analysis

- Orders and revenue by food category
- Orders and revenue by cuisine type
- Treemap of cuisine revenue
- Avg quantity per food category and cuisine

### Step 7 — Time-Based Analysis

- Hourly order and revenue chart
- Orders by time of day (Morning/Afternoon/Evening/Night)
- Orders by weekday (weekends highlighted)
- Monthly order trend line chart
- Seasonal order distribution
- Weekday × Hour heatmap
- Favourite foods stacked by time of day

### Step 8 — Customer Behaviour Analysis

- Customer-level aggregation (total orders, spend, avg rating)
- Favourite food category and cuisine per customer
- Distribution of orders per customer
- Distribution of avg spend per customer
- Customer value segments (Bronze / Silver / Gold)
- Avg spend comparison by segment
- RFM-style scatter: Total Orders vs Total Spend

### Step 9 — Restaurant & Location Analysis

- City-wise order and revenue analysis
- City bubble chart (orders vs revenue, size = customers)
- Stacked bar: cuisine by city
- Top N restaurants by orders (slider control)
- Restaurant performance scatter (orders vs revenue)
- Avg customer rating by city

### Step 10 — Discount Behaviour Analysis

- Discounted vs non-discounted order comparison
- Discount amount vs order value scatter
- Repeat customers vs one-time: discount rate comparison
- Discount rate vs avg spend scatter
- Avg discount by food category and cuisine

### Step 11 — Delivery Performance Analysis

- Delivery time and distance distributions
- Distance vs delivery time scatter with trendline
- Delivery performance by city (avg time + delay %)
- Delivery time by food category

### Step 12 — Rating Analysis

- Rating distribution bar and histogram
- Avg rating by food category and cuisine
- Avg rating by delivery time bucket
- Delivery time vs rating scatter
- Avg rating by order value segment
- Avg rating by payment method
- Top 15 rated restaurants (min 50 orders)

### Step 13 — Dashboard Styling & UX

- Custom dark purple CSS theme
- Consistent VIBRANT / PURPLE_SEQ colour palettes
- Sidebar with global filters (city, status, category, date range)
- Multi-page navigation (8 pages via sidebar radio)
- KPI cards with metric deltas

### Step 14 — Validation & Launch

- Run the Streamlit app locally
- Verify all charts load correctly
- Test filter interactions
- Confirm performance with cached data loader

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Place dataset

Ensure `archive (2).zip` is in the same directory as `Kavana Shree V.py`.

### 3. Launch the dashboard

```bash
streamlit run "Kavana Shree V.py"
```

### 4. Open in browser

Streamlit will automatically open `http://localhost:8502` in your default browser.

---

## 🖥️ Dashboard Pages

| # | Page                    | Description                                           |
| - | ----------------------- | ----------------------------------------------------- |
| 1 | 🏠 Overview & KPIs      | Summary KPIs, data quality, monthly trend             |
| 2 | 🍽️ Food Preferences   | Top categories, cuisine rankings, order values        |
| 3 | ⏰ Time Analysis        | Hourly, daily, weekly, monthly, seasonal patterns     |
| 4 | 👥 Customer Behaviour   | Repeat analysis, segments, RFM scatter                |
| 5 | 🏪 Restaurant & City    | City demand, restaurant rankings, cuisine by location |
| 6 | 💰 Discount Behaviour   | Discount impact on orders, spend & repeat buys        |
| 7 | 🚴 Delivery Performance | Time/distance analysis, delays by city                |
| 8 | ⭐ Rating Analysis      | What drives satisfaction? Ratings deep-dive           |

---

## 📦 Libraries Used

| Library         | Purpose                                                                |
| --------------- | ---------------------------------------------------------------------- |
| `streamlit`   | Web application framework                                              |
| `pandas`      | Data manipulation and analysis                                         |
| `numpy`       | Numerical computations                                                 |
| `plotly`      | Interactive visualisations (bar, line, scatter, heatmap, treemap, pie) |
| `statsmodels` | OLS trendline in scatter plots                                         |

---

## 📈 Key Insights Summary

- **Beverages & Pizza** top the order count charts across most cities
- **Evening (17:00–21:00) & Night** are peak ordering windows
- **Friday & Saturday** drive the highest weekend demand
- **87.8%** of customers are repeat buyers (ordered more than once)
- **Discounted orders** have marginally higher average quantities
- **Longer delivery times** correlate slightly with lower ratings
- **Pune & Delhi** lead in order volumes; **Bengaluru** shows highest net revenue
- **Gold-tier customers** spend 3× more than Bronze on average

---

## 📝 Author

**Kavana Shree V**
IBM Internship — Data Analytics With AI
Food Delivery Customer Preference Analysis Project
