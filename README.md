# Indian Passenger Car Market — Sales Analysis & Q1 2025 Forecast

## What this is
An end-to-end analysis of the **Indian passenger car market in 2024**, combining data cleaning, exploratory analysis, SQL-based market analysis, polynomial trend forecasting, and an interactive Power BI dashboard.

The project examines:

- Overall monthly market sales and market movement
- Brand-level market share and annual sales ranking
- Q1-to-Q4 brand growth
- Month-over-month (MoM) brand performance
- Top-selling models within each brand
- Segment-level sales contribution
- Short-term Q1 2025 sales forecasts for the overall market and the top 5 brands
- Forecast-model fit using **R²**

## Business Questions

The project was designed to answer questions such as:

1. Which brands dominated the Indian passenger car market in 2024?
2. How concentrated was the market among the leading brands?
3. Which brands gained or lost momentum between Q1 and Q4?
4. Which models were the leading sales contributors within each brand?
5. Which vehicle segments contributed most to total sales?
6. How did the market evolve month by month?
7. What does a polynomial time-trend model indicate for Q1 2025?
8. How do the forecast trends of the leading brands differ from the overall market?

---

## Data source
"Car Sales in India - 2024" — Kaggle

---

## Scope note

- Period: January–December 2024
- Geography: India
- Coverage: Passenger cars
- Brands: 14
- Observations: model-level monthly sales data
- Excludes: two-wheelers and commercial vehicles

Because the dataset contains only **12 months of observations**, the forecasts should be interpreted as **directional trend estimates rather than precise predictions**.

---

## Tools
Excel (Data inspection & missing-value handling) → Python(Pandas)/scikit-learn (Linear Regression and Polynomial trend forecasting) →
MySQL (CTEs and window functions for market share and growth analysis) → Power BI (Interactive dashboard & business storytelling)

---

## Data Preparation

The original data was provided in a wide format, with separate columns for January–December sales.

### Key preparation steps

- Removed irrelevant/empty columns.
- Standardized column names and categorical text.
- Reshaped monthly sales from wide to long format using `pandas.melt()`.
- Converted month names into proper date values.
- Removed comma separators from sales figures and converted `Units_sold` to numeric.
- Aggregated the cleaned data into brand-month and segment-month tables.
- Loaded the cleaned data into MySQL for SQL analysis.
- Used Excel to document the handling of the missing **Tata Tigor June 2024** value.

The missing Tata Tigor June value was imputed using linear interpolation between May and July:

> June = (May + July) / 2 = (2,098 + 1,495) / 2 = 1,796.5 ≈ **1,797 units**

This avoids treating an unavailable observation as zero and preserves continuity for the time-series analysis.

---

## Key findings
## 1. Maruti dominated the 2024 market

Maruti recorded approximately **1.75 million units**, accounting for **40.90% of total 2024 sales**.

Market concentration was high:

- **Top 2 brands:** 55.04%
- **Top 4 brands:** 80.50%
- **Top 5 brands:** 87.50%

This indicates that a relatively small group of brands accounted for most recorded passenger-car sales in the dataset.

## 2. Brand leadership and model leadership were different

Although **Maruti** was the leading brand, **Tata Punch** was the highest-selling individual model, with approximately **202,031 units**.

Other leading models included:

| Brand | Top Model | 2024 Sales |
|---|---|---:|
| Tata | Punch | 202,031 |
| Maruti | WagonR | 190,855 |
| Hyundai | Creta | 186,919 |
| Mahindra | Scorpio | 166,364 |
| Toyota | Innova Crysta / Innova Hycross | 106,900 |

This demonstrates why both **brand-level and model-level analysis** are useful when evaluating market performance.

## 3. The market peaked in October and weakened by December

Total monthly market sales were:

| Month | Units Sold |
|---|---:|
| January | 393,471 |
| February | 370,279 |
| March | 369,381 |
| April | 337,770 |
| May | 349,057 |
| June | 339,844 |
| July | 343,026 |
| August | 354,273 |
| September | 358,879 |
| October | **397,947** |
| November | 351,592 |
| December | **321,345** |

October was the highest-sales month, while December was the lowest.

January-to-December sales declined by approximately **18.3%**, while Q4 sales were approximately **5.5% lower than Q1**.

The large month-to-month variation is one reason a simple time trend has limited explanatory power.

## 4. Growth leaders were not necessarily market-share leaders

The Q1-to-Q4 comparison showed:

| Brand | Q1 Sales | Q4 Sales | Q1→Q4 Growth |
|---|---:|---:|---:|
| MG | 13,005 | 20,580 | **58.25%** |
| Skoda | 7,433 | 11,519 | **54.97%** |
| Volkswagen | 9,815 | 12,278 | **25.09%** |
| Mahindra | 126,100 | 142,150 | **12.73%** |
| Toyota | 71,616 | 78,208 | **9.20%** |
| Jeep | 1,152 | 1,071 | -7.03% |
| Nissan | 8,319 | 7,581 | -8.87% |
| Hyundai | 160,317 | 146,022 | -8.92% |
| Maruti | 477,893 | 431,018 | -9.81% |
| Tata | 155,010 | 139,417 | -10.06% |

MG and Skoda recorded the largest percentage increases, but both started from substantially smaller Q1 sales bases than the market leaders.

**Analytical implication:** growth rate should be evaluated alongside absolute sales volume and market share.

## 5. The leading brands showed different forecast trajectories

The polynomial forecasts for the top five brands are:

| Brand | Linear Component | Curvature | R² | Jan 2025 | Feb 2025 | Mar 2025 |
|---|---:|---:|---:|---:|---:|---:|
| Maruti | -5,479.81 | 346.73 | 0.42 | 145,817 | 149,005 | 152,887 |
| Hyundai | -480.00 | -8.04 | 0.30 | 46,572 | 45,891 | 45,194 |
| Tata | -2,576.95 | 171.90 | **0.77** | 47,663 | 49,383 | 51,448 |
| Mahindra | 505.33 | 6.66 | 0.22 | 48,001 | 48,673 | 49,358 |
| Toyota | 1,094.87 | -67.79 | 0.26 | 25,226 | 24,626 | 23,891 |

The polynomial models produce different trajectories:

- **Maruti:** negative linear component but positive curvature, resulting in a rising Q1 forecast after January.
- **Hyundai:** relatively mild negative trend with negative curvature, producing a gradual decline.
- **Tata:** negative linear component but strong positive curvature; its forecast rises substantially through Q1.
- **Mahindra:** positive linear component and positive curvature, producing a gradual increase.
- **Toyota:** positive linear component but negative curvature, resulting in a declining Q1 forecast after January.

The **R² values should be interpreted as in-sample fit measures**, not as guarantees of forecast accuracy. Tata's model has the highest R² among the five at 0.77, while Mahindra's is 0.22.

## 6. The market was concentrated in a few segments

The largest segments by 2024 sales were:

| Segment | Units Sold | Market Share |
|---|---:|---:|
| C1 | 1,441,776 | **33.63%** |
| C2 | 823,824 | **19.22%** |
| Utility | 659,070 | **15.37%** |
| B2 | 589,952 | **13.76%** |
| B1 | 306,051 | **7.14%** |

C1 and C2 together accounted for more than half of recorded sales.

The Q1-to-Q4 comparison also showed divergent segment movement:

- Premium: +17.54%
- C2: +4.69%
- Utility: +0.43%
- C1: -2.39%
- B2: -16.89%
- B1: -20.98%
- A: -34.03%

This suggests that market movement was not uniform across vehicle segments.

## 7. Extreme MoM growth should be interpreted with the underlying sales base

Citroen recorded the highest monthly growth rate observed in the SQL analysis:

**+280.6% in August 2024.**

However, the increase was from **335 units in July to 1,275 units in August**.

This demonstrates why percentage growth alone can be misleading when the previous-period base is small.

---

# Forecasting Approach

## Overall market polynomial model

A time variable was created:

```text
Period = 0, 1, 2, ..., 11
```

A degree-2 polynomial regression was then fitted:

```text
Ŷ = β₀ + β₁t + β₂t²
```

The fitted model produced:

- **Linear component:** -7,692.18
- **Curvature component:** 496.74
- **R²:** 0.19

The model's time-dependent slope is:

```text
dY/dt = -7692.18 + 2(496.74)t
```

The positive curvature means the negative effect of the linear component becomes less negative as time progresses within the fitted trend.

However, the model explains only **19% of the variation** in the 12 monthly observations, so the forecast should not be interpreted as a highly precise demand prediction.

---

## Q1 2025 Overall Market Forecast

The polynomial model produces:

| Month | Forecast Units |
|---|---:|
| January 2025 | 357,824 |
| February 2025 | 362,550 |
| March 2025 | 368,270 |
| **Q1 2025 Total** | **1,088,644** |

Unlike the linear forecast (check the python script for values), the polynomial forecast shows a **gradual increase from January to March**.

The forecast therefore captures the curvature identified in the fitted model rather than imposing a constant monthly decline.

---

# Recommendations / Business Implications

## 1. Protect core market share while monitoring challengers

Maruti's 40.90% market share means changes in its performance have a substantial effect on the overall market.

At the same time, brands such as MG, Skoda, Volkswagen, Mahindra and Toyota recorded positive Q1-to-Q4 growth.

**Recommendation:** monitor both **absolute sales and growth rate**. A high growth rate from a small base should not be interpreted in the same way as sustained growth from a large base.

## 2. Use model-level analysis for product decisions

Tata Punch was the highest-selling model even though Tata ranked third by total brand sales.

**Recommendation:** evaluate product-level demand alongside brand-level performance when assessing inventory, product positioning and marketing priorities.

## 3. Pay attention to divergent brand trajectories

The polynomial forecasts show that the leading brands do not all follow the same expected direction during Q1 2025.

For example:

- Tata's forecast increases from 47,663 to 51,448.
- Mahindra's forecast increases from 48,001 to 49,358.
- Hyundai's forecast declines from 46,572 to 45,194.
- Toyota's forecast declines from 25,226 to 23,891.
- Maruti's forecast rises from 145,817 to 152,887 after its January level.

**Recommendation:** avoid applying one market-wide growth assumption to every brand. Brand-level trend monitoring can identify where the market is behaving differently.

## 4. Use segment-level trends for planning

C1, C2 and Utility together represent a large proportion of total market sales, while several smaller segments recorded substantial Q1-to-Q4 declines.

**Recommendation:** segment demand should be considered when making inventory, product-positioning and campaign decisions instead of treating the passenger-car market as homogeneous.

## 5. Treat the current forecast as a baseline scenario

The polynomial model's R² of **0.19** indicates that most of the variation in monthly sales is not explained by the time variable alone.

**Recommendation:** use the Q1 2025 forecast as a **directional baseline scenario**, not as a standalone planning number.

A stronger forecasting model could incorporate:

- Multiple years of historical sales
- Seasonality
- Pricing and promotions
- New model launches
- Fuel prices
- Interest rates / financing conditions
- Macroeconomic indicators
- Segment-specific demand drivers

---

## Dashboard
[Dashboard](https://github.com/Samadrita-2002/Indian-Passenger-Car-Market-Sales-Analysis-Q1-2025-Forecast/blob/main/Dashboard.png)

## Files
- [Forecasts](https://github.com/Samadrita-2002/Indian-Passenger-Car-Market-Sales-Analysis-Q1-2025-Forecast/blob/main/forecasts.csv)
- [Brand forecasts](https://github.com/Samadrita-2002/Indian-Passenger-Car-Market-Sales-Analysis-Q1-2025-Forecast/blob/main/brand_forecasts.csv)
- [Python:cleaning and Linear Regression and Polynomial trend forecasting](https://github.com/Samadrita-2002/Indian-Passenger-Car-Market-Sales-Analysis-Q1-2025-Forecast/blob/main/car_sales_trend_analysis.py)
- [SQL: analysis queries](https://github.com/Samadrita-2002/Indian-Passenger-Car-Market-Sales-Analysis-Q1-2025-Forecast/blob/main/auto_market_analysis.sql)
- [Queries outputs and pivot table](https://github.com/Samadrita-2002/Indian-Passenger-Car-Market-Sales-Analysis-Q1-2025-Forecast/blob/main/SQL%20query%20results%20and%20pivot%20table.xlsx)
- [Power BI Dashboard](https://github.com/Samadrita-2002/Indian-Passenger-Car-Market-Sales-Analysis-Q1-2025-Forecast/blob/main/Indian_Auto_Market_Analysis%20Dashboard.pdf)
