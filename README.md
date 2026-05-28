# 📣 Marketing Funnel & Conversion Performance Analysis
### Future Interns — Data Science & Analytics | Task 3

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-4c72b0)
![NumPy](https://img.shields.io/badge/NumPy-Data%20Generation-013243?logo=numpy)
![Status](https://img.shields.io/badge/Status-Completed✅-2dc653)

---

## 📌 Objective

Analyze marketing funnel data to identify:
- Stage-by-stage conversion rates and drop-off points
- Channel performance by revenue, conversion rate, and ROAS
- Cost Per Acquisition (CPA) efficiency across channels
- Monthly trends in leads, revenue, and conversions
- Audience and regional conversion insights
- Actionable recommendations to improve lead-to-customer conversion

---

## 📁 Repository Structure

```
FUTURE_DS_03/
├── FUTURE_DS_03_FullCode.py     # Complete Python analysis script
├── FUTURE_DS_03_Report.pdf      # Client-ready analysis report with charts
├── Marketing_Funnel.csv         # Dataset (auto-generated inside the script)
└── README.md                    # Project documentation
```

---

## 📦 Dataset

| Property | Details |
|----------|---------|
| Name | Marketing Funnel Dataset |
| Rows | 5,000 |
| Columns | 15 |
| Source | Synthetically generated (realistic simulation) |
| Features | Lead ID, Channel, Device, Region, Campaign, Age Group, Visit Date, Time on Site, Pages Viewed, Ad Spend, Funnel Stage, Converted, Revenue, Month |

### Funnel Stages

```
Visitors → Awareness → Product View → Checkout → Converted
```

### Channels Covered
`Organic Search` · `Paid Search` · `Social Media` · `Email` · `Referral` · `Direct`

---

## 🛠️ Tools & Libraries

| Tool | Purpose |
|------|---------|
| Python 3.8+ | Core programming language |
| Pandas | Data manipulation and aggregation |
| NumPy | Dataset generation and numerical operations |
| Matplotlib | Charts, trends, and visualizations |
| Seaborn | Heatmaps and statistical plots |
| ReportLab | PDF report generation |

---

## ⚙️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/FUTURE_DS_03.git
cd FUTURE_DS_03
```

**2. Install dependencies**
```bash
pip install pandas numpy matplotlib seaborn reportlab
```

**3. Run the analysis**
```bash
python FUTURE_DS_03_FullCode.py
```

> 💡 The dataset (`Marketing_Funnel.csv`) is **auto-generated** inside the script.
> No external file download needed.

**4. Outputs generated**
- 7 chart PNG files
- `FUTURE_DS_03_Report.pdf` — complete analysis report
- `Marketing_Funnel.csv` — generated dataset

---

## 📊 Analysis Sections

| # | Section | Description |
|---|---------|-------------|
| 1 | Dataset Generation | Realistic 5,000-lead funnel dataset with 6 channels |
| 2 | KPI Dashboard | Total Leads, Conversions, Conv Rate, Revenue, ROAS, Bounce Rate |
| 3 | Funnel Waterfall | Stage-by-stage volume + drop-off rates + conversion rates |
| 4 | Channel Performance | Revenue, Conversion Rate & ROAS by channel |
| 5 | Drop-off Heatmap | Funnel conversion % heatmap + Device + Campaign performance |
| 6 | Monthly Trends | Leads vs Conversions trend + Revenue + Monthly conversion rate |
| 7 | Audience & Region | Age group conversion + Regional revenue + Order value distribution |
| 8 | CPA & Spend Analysis | CPA by channel + Spend vs Revenue bubble + Stage mix pie |
| 9 | Key Insights | Printed terminal summary |
| 10 | PDF Report | Auto-generated client-ready PDF report |

---

## 📈 Key Findings

| Metric | Value |
|--------|-------|
| Total Leads | 5,000 |
| Total Conversions | 1,037 |
| Overall Conversion Rate | 20.7% |
| Bounce Rate | 29.0% |
| Total Revenue | $144,813 |
| Total Ad Spend | ~$37,500 |
| ROAS | ~3.85x |
| Avg Order Value | $139 |

### Funnel Drop-off Summary

| Stage Transition | Conversion Rate |
|-----------------|----------------|
| Visitor → Awareness | ~71% |
| Awareness → Product View | ~60% |
| Product View → Checkout | ~53% |
| Checkout → Converted | ~42% |

### 🔑 Business Insights

- **Checkout → Converted** is the biggest drop-off — fixing this has the highest revenue impact
- **Email & Referral** channels deliver the best ROAS and lowest CPA
- **Mobile** generates 40%+ of traffic but converts at a lower rate than Desktop
- **25–34 age group** has the highest conversion rate across all segments
- **Seasonal peaks** exist in monthly data — budget timing matters
- **Paid Search** has the highest CPA — ROI should be reviewed

### ✅ Recommendations

1. **Fix Checkout** — Add trust badges, reduce form fields, A/B test layout
2. **Scale Email & Referral** — Best ROAS channels deserve more budget
3. **Mobile UX Audit** — Faster loads, bigger CTAs, simplified checkout
4. **Retargeting** — Target Product View and Checkout abandoners
5. **Seasonal Budget Alignment** — Pre-load spend before peak months
6. **25–34 Lookalike Audiences** — Scale the best-converting segment

---

## 📷 Visualizations Generated

| Chart | Description |
|-------|-------------|
| `t3_kpi.png` | 6-card KPI dashboard |
| `t3_funnel.png` | Funnel waterfall + Stage conversion rates |
| `t3_channel.png` | Revenue, Conversion Rate & ROAS by channel |
| `t3_dropoff.png` | Drop-off heatmap + Device + Campaign revenue |
| `t3_monthly.png` | Monthly Leads, Revenue & Conversion Rate trends |
| `t3_audience.png` | Age Group + Region + Order value distribution |
| `t3_cpa.png` | CPA bars + Spend vs Revenue bubble + Stage pie |

---

## 🏢 About This Internship

This project was completed as part of the **Future Interns Data Science & Analytics** program.

- 🌐 Website: [futureinterns.com](https://futureinterns.com)
- 💼 LinkedIn: [Future Interns](https://www.linkedin.com/company/future-interns/)
- 📧 Contact: contact@futureinterns.com

---

## 👤 Author

**[Your Name]**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [your-linkedin](https://linkedin.com/in/your-linkedin)

---

*Completed as Task 3 of the Future Interns Data Science & Analytics Internship*
*Track Code: **FUTURE_DS_03***
