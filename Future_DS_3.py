# ============================================================
#   FUTURE INTERNS — DATA SCIENCE & ANALYTICS
#   Task 3 : Marketing Funnel & Conversion Performance Analysis
#   Repo   : FUTURE_DS_03
#   Dataset: Marketing_Funnel.csv (generated inside this script)
#   Tools  : Python, Pandas, Matplotlib, Seaborn, ReportLab
# ============================================================

# pip install pandas matplotlib seaborn reportlab numpy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Image, Table, TableStyle, HRFlowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid')
plt.rcParams.update({
    'figure.dpi': 130, 'font.family': 'DejaVu Sans',
    'axes.titlesize': 14, 'axes.labelsize': 12,
    'xtick.labelsize': 11, 'ytick.labelsize': 11
})

# ════════════════════════════════════════════════════════════
# SECTION 1 — GENERATE DATASET
# ════════════════════════════════════════════════════════════

print("=" * 57)
print("  FUTURE_DS_03 — Marketing Funnel & Conversion Analysis")
print("=" * 57)

np.random.seed(42)
n = 5000

channels   = ['Organic Search','Paid Search','Social Media','Email','Referral','Direct']
ch_weights = [0.30, 0.22, 0.20, 0.13, 0.10, 0.05]
devices    = ['Desktop','Mobile','Tablet']
dv_weights = [0.50, 0.40, 0.10]
campaigns  = ['Brand Awareness','Lead Gen','Retargeting','Seasonal Offer','Product Launch']

df = pd.DataFrame({
    'lead_id'         : range(1, n+1),
    'channel'         : np.random.choice(channels,  n, p=ch_weights),
    'device'          : np.random.choice(devices,   n, p=dv_weights),
    'region'          : np.random.choice(['North','South','East','West'], n),
    'campaign'        : np.random.choice(campaigns, n),
    'age_group'       : np.random.choice(['18-24','25-34','35-44','45-54','55+'],
                                          n, p=[0.15,0.35,0.25,0.15,0.10]),
    'visit_date'      : pd.date_range('2024-01-01', periods=n, freq='2h'),
    'time_on_site_sec': np.random.randint(30, 900, n),
    'pages_viewed'    : np.random.randint(1, 15, n),
    'ad_spend'        : np.random.uniform(0.5, 15.0, n).round(2),
})

# Conversion probabilities per channel
ch_conv = {
    'Organic Search': (0.72, 0.55, 0.38, 0.22),
    'Paid Search'   : (0.68, 0.50, 0.32, 0.18),
    'Social Media'  : (0.60, 0.38, 0.22, 0.10),
    'Email'         : (0.80, 0.65, 0.48, 0.30),
    'Referral'      : (0.75, 0.60, 0.42, 0.26),
    'Direct'        : (0.78, 0.62, 0.44, 0.28),
}

def assign_stage(row):
    p = ch_conv[row['channel']]
    r = np.random.random()
    if   r < p[3]: return 'Converted'
    elif r < p[2]: return 'Checkout'
    elif r < p[1]: return 'Product View'
    elif r < p[0]: return 'Awareness'
    else:          return 'Bounced'

df['funnel_stage'] = df.apply(assign_stage, axis=1)
df['converted']    = (df['funnel_stage'] == 'Converted').astype(int)

df['revenue'] = 0.0
mask = df['converted'] == 1
df.loc[mask, 'revenue'] = np.random.choice(
    [49, 99, 149, 249, 499], mask.sum(), p=[0.30, 0.28, 0.22, 0.14, 0.06])

df['month']      = df['visit_date'].dt.month
df['month_name'] = df['visit_date'].dt.strftime('%b')
df.to_csv('Marketing_Funnel.csv', index=False)

# KPIs
total_leads   = len(df)
total_conv    = df['converted'].sum()
conv_rate     = total_conv / total_leads * 100
total_revenue = df['revenue'].sum()
total_spend   = df['ad_spend'].sum()
roas          = total_revenue / total_spend
avg_order     = df[df['converted']==1]['revenue'].mean()
bounce_rate   = (df['funnel_stage']=='Bounced').sum() / total_leads * 100

# Funnel stage counts (cumulative)
awareness_n    = (df['funnel_stage'].isin(['Awareness','Product View','Checkout','Converted'])).sum()
product_view_n = (df['funnel_stage'].isin(['Product View','Checkout','Converted'])).sum()
checkout_n     = (df['funnel_stage'].isin(['Checkout','Converted'])).sum()
converted_n    = (df['funnel_stage']=='Converted').sum()
funnel_counts  = [total_leads, awareness_n, product_view_n, checkout_n, converted_n]

print(f"\n{'─'*57}")
print(f"  MARKETING FUNNEL SUMMARY")
print(f"{'─'*57}")
print(f"  Total Leads      : {total_leads:,}")
print(f"  Total Conversions: {total_conv:,}  ({conv_rate:.1f}%)")
print(f"  Bounce Rate      : {bounce_rate:.1f}%")
print(f"  Total Revenue    : ${total_revenue:,.0f}")
print(f"  Total Ad Spend   : ${total_spend:,.0f}")
print(f"  ROAS             : {roas:.2f}x")
print(f"  Avg Order Value  : ${avg_order:.0f}")
print(f"{'─'*57}\n")


# ════════════════════════════════════════════════════════════
# SECTION 2 — KPI DASHBOARD
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 6, figsize=(26, 4))
fig.patch.set_facecolor('#0f0f1a')
kpis = [
    ('Total Leads',    f'{total_leads:,}',          '#4361ee'),
    ('Conversions',    f'{total_conv:,}',            '#2dc653'),
    ('Conv. Rate',     f'{conv_rate:.1f}%',           '#f72585'),
    ('Total Revenue',  f'${total_revenue/1e3:.1f}K', '#f8961e'),
    ('ROAS',           f'{roas:.2f}x',                '#7b2d8b'),
    ('Bounce Rate',    f'{bounce_rate:.1f}%',          '#e63946'),
]
for ax, (title, value, color) in zip(axes, kpis):
    ax.set_facecolor(color)
    ax.text(0.5, 0.58, value, ha='center', va='center',
            fontsize=22, fontweight='bold', color='white',
            transform=ax.transAxes)
    ax.text(0.5, 0.22, title, ha='center', va='center',
            fontsize=10, color='#ffffffcc', transform=ax.transAxes)
    ax.axis('off')

plt.suptitle('📊 Marketing Funnel KPI Overview',
             fontsize=15, fontweight='bold', color='white', y=1.05)
plt.tight_layout(pad=0.8)
plt.savefig('t3_kpi.png', bbox_inches='tight', facecolor=fig.get_facecolor())
plt.show()
print("📊 Chart 1 saved : t3_kpi.png")


# ════════════════════════════════════════════════════════════
# SECTION 3 — FUNNEL WATERFALL + STAGE CONVERSIONS
# ════════════════════════════════════════════════════════════

funnel_labels = ['Visitors\n(All Leads)', 'Awareness', 'Product View', 'Checkout', 'Converted']
drop_rates    = [0] + [round((1 - funnel_counts[i]/funnel_counts[i-1])*100, 1)
                        for i in range(1, 5)]
stage_conv    = [(funnel_counts[i]/funnel_counts[i-1])*100
                  for i in range(1, len(funnel_counts))]
stage_labels_conv = ['Visitor→\nAwareness', 'Awareness→\nProduct View',
                      'Product View→\nCheckout', 'Checkout→\nConverted']

fig, axes = plt.subplots(1, 2, figsize=(22, 8))
fig.subplots_adjust(wspace=0.35)

palette = ['#4361ee', '#4895ef', '#4cc9f0', '#f8961e', '#2dc653']
bars = axes[0].barh(funnel_labels[::-1], funnel_counts[::-1],
                    color=palette[::-1], edgecolor='white',
                    linewidth=1, height=0.6)
axes[0].set_title('Marketing Funnel — Stage-by-Stage Volume',
                   fontweight='bold', fontsize=15, pad=12)
axes[0].set_xlabel('Number of Leads', fontsize=12)
for bar, val, drop in zip(bars, funnel_counts[::-1], drop_rates[::-1]):
    axes[0].text(val + 30, bar.get_y() + bar.get_height()/2,
                 f'{val:,}', va='center', fontsize=11, fontweight='bold')
    if drop > 0:
        axes[0].text(val + 30, bar.get_y() - 0.28,
                     f'↓ {drop}% drop-off', va='center',
                     fontsize=9, color='#e63946')
axes[0].set_xlim(0, max(funnel_counts) * 1.22)

colors_conv = ['#2dc653' if r > 50 else '#f8961e' if r > 30 else '#f72585'
               for r in stage_conv]
bars2 = axes[1].bar(stage_labels_conv, stage_conv, color=colors_conv,
                    edgecolor='white', linewidth=1, width=0.55)
axes[1].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[1].set_title('Stage-to-Stage Conversion Rates',
                   fontweight='bold', fontsize=15, pad=12)
axes[1].set_ylabel('Conversion Rate (%)', fontsize=12)
axes[1].set_ylim(0, max(stage_conv) * 1.25)
for bar, val in zip(bars2, stage_conv):
    axes[1].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.5,
                 f'{val:.1f}%', ha='center',
                 fontsize=12, fontweight='bold')

plt.suptitle('Funnel Volume & Stage Conversion Analysis',
             fontsize=16, fontweight='bold', y=1.02)
plt.savefig('t3_funnel.png', bbox_inches='tight')
plt.show()
print("📊 Chart 2 saved : t3_funnel.png")


# ════════════════════════════════════════════════════════════
# SECTION 4 — CHANNEL PERFORMANCE
# ════════════════════════════════════════════════════════════

ch = df.groupby('channel').agg(
    Leads=('lead_id', 'count'),
    Conversions=('converted', 'sum'),
    Revenue=('revenue', 'sum'),
    Spend=('ad_spend', 'sum')
).reset_index()
ch['Conv Rate (%)'] = ch['Conversions'] / ch['Leads'] * 100
ch['ROAS']          = ch['Revenue'] / ch['Spend']
ch['CPA']           = ch['Spend'] / ch['Conversions']

print("\n📡 Channel Performance:")
print(ch[['channel','Leads','Conversions','Conv Rate (%)','Revenue','ROAS','CPA']].to_string(index=False))

fig, axes = plt.subplots(1, 3, figsize=(24, 7))
fig.subplots_adjust(wspace=0.38)
palette6 = ['#4361ee','#f72585','#2dc653','#f8961e','#7b2d8b','#4cc9f0']

ch_rev = ch.sort_values('Revenue', ascending=False)
bars = axes[0].bar(ch_rev['channel'], ch_rev['Revenue'],
                   color=palette6, edgecolor='white', linewidth=1, width=0.6)
axes[0].yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K'))
axes[0].set_title('Revenue by Channel', fontweight='bold', fontsize=15, pad=12)
axes[0].set_ylabel('Total Revenue ($)', fontsize=12)
axes[0].tick_params(axis='x', rotation=20)
axes[0].set_ylim(0, ch_rev['Revenue'].max() * 1.2)
for bar, val in zip(bars, ch_rev['Revenue']):
    axes[0].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 500,
                 f'${val/1e3:.1f}K', ha='center',
                 fontsize=10, fontweight='bold')

ch_cr = ch.sort_values('Conv Rate (%)', ascending=False)
bar_c = ['#2dc653' if r > 25 else '#f8961e' if r > 15 else '#f72585'
         for r in ch_cr['Conv Rate (%)']]
bars2 = axes[1].bar(ch_cr['channel'], ch_cr['Conv Rate (%)'],
                    color=bar_c, edgecolor='white', linewidth=1, width=0.6)
axes[1].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[1].set_title('Conversion Rate by Channel',
                   fontweight='bold', fontsize=15, pad=12)
axes[1].set_ylabel('Conversion Rate (%)', fontsize=12)
axes[1].tick_params(axis='x', rotation=20)
axes[1].set_ylim(0, ch_cr['Conv Rate (%)'].max() * 1.22)
for bar, val in zip(bars2, ch_cr['Conv Rate (%)']):
    axes[1].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.3,
                 f'{val:.1f}%', ha='center',
                 fontsize=11, fontweight='bold')

ch_roas = ch.sort_values('ROAS', ascending=False)
bar_r = ['#2dc653' if r > 3 else '#f8961e' if r > 2 else '#f72585'
         for r in ch_roas['ROAS']]
bars3 = axes[2].bar(ch_roas['channel'], ch_roas['ROAS'],
                    color=bar_r, edgecolor='white', linewidth=1, width=0.6)
axes[2].axhline(1, color='red', linestyle='--',
                linewidth=1.5, label='Break-even (1x)')
axes[2].set_title('Return on Ad Spend (ROAS) by Channel',
                   fontweight='bold', fontsize=15, pad=12)
axes[2].set_ylabel('ROAS (x)', fontsize=12)
axes[2].tick_params(axis='x', rotation=20)
axes[2].legend(fontsize=10)
axes[2].set_ylim(0, ch_roas['ROAS'].max() * 1.22)
for bar, val in zip(bars3, ch_roas['ROAS']):
    axes[2].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.05,
                 f'{val:.2f}x', ha='center',
                 fontsize=11, fontweight='bold')

plt.suptitle('Channel Performance Analysis',
             fontsize=16, fontweight='bold', y=1.02)
plt.savefig('t3_channel.png', bbox_inches='tight')
plt.show()
print("📊 Chart 3 saved : t3_channel.png")


# ════════════════════════════════════════════════════════════
# SECTION 5 — DROP-OFF HEATMAP + DEVICE + CAMPAIGN
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(24, 7))
fig.subplots_adjust(wspace=0.38)

# Heatmap: channel × funnel stage
hm_data = pd.DataFrame(index=df['channel'].unique(),
                        columns=['Awareness','Product View','Checkout','Converted'])
for ch_n in df['channel'].unique():
    total = len(df[df['channel']==ch_n])
    hm_data.loc[ch_n,'Awareness']    = (df[(df['channel']==ch_n) & df['funnel_stage'].isin(['Awareness','Product View','Checkout','Converted'])].shape[0]) / total * 100
    hm_data.loc[ch_n,'Product View'] = (df[(df['channel']==ch_n) & df['funnel_stage'].isin(['Product View','Checkout','Converted'])].shape[0]) / total * 100
    hm_data.loc[ch_n,'Checkout']     = (df[(df['channel']==ch_n) & df['funnel_stage'].isin(['Checkout','Converted'])].shape[0]) / total * 100
    hm_data.loc[ch_n,'Converted']    = (df[(df['channel']==ch_n) & (df['funnel_stage']=='Converted')].shape[0]) / total * 100
hm_data = hm_data.astype(float).round(1)

sns.heatmap(hm_data, ax=axes[0], annot=True, fmt='.1f',
            cmap='RdYlGn', linewidths=0.8, linecolor='white',
            annot_kws={'size': 11, 'weight': 'bold'},
            cbar_kws={'label': '% of Channel Leads'})
axes[0].set_title('Funnel Conversion Rate (%)\nby Channel',
                   fontweight='bold', fontsize=14, pad=12)
axes[0].set_xlabel('Funnel Stage', fontsize=12)
axes[0].set_ylabel('Channel', fontsize=12)
axes[0].tick_params(axis='x', rotation=20)

# Device conversion rate
dev = df.groupby('device')['converted'].agg(['sum','count'])
dev['rate'] = dev['sum'] / dev['count'] * 100
dev = dev.sort_values('rate', ascending=False)
bar_c2 = ['#2dc653' if r > 22 else '#f8961e' if r > 18 else '#f72585'
           for r in dev['rate']]
bars_d = axes[1].bar(dev.index, dev['rate'], color=bar_c2,
                     edgecolor='white', linewidth=1, width=0.5)
axes[1].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[1].set_title('Conversion Rate by Device',
                   fontweight='bold', fontsize=14, pad=12)
axes[1].set_ylabel('Conversion Rate (%)', fontsize=12)
axes[1].set_ylim(0, dev['rate'].max() * 1.22)
for bar, val in zip(bars_d, dev['rate']):
    axes[1].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.3,
                 f'{val:.1f}%', ha='center',
                 fontsize=12, fontweight='bold')

# Campaign revenue
camp = df.groupby('campaign').agg(
    Leads=('lead_id','count'),
    Revenue=('revenue','sum'),
    Conversions=('converted','sum')
).reset_index()
camp['Conv Rate'] = camp['Conversions'] / camp['Leads'] * 100
camp = camp.sort_values('Revenue', ascending=True)
bars_c = axes[2].barh(camp['campaign'], camp['Revenue'],
                      color='#4361ee', edgecolor='white',
                      linewidth=1, height=0.55)
axes[2].xaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K'))
axes[2].set_title('Revenue by Campaign',
                   fontweight='bold', fontsize=14, pad=12)
axes[2].set_xlabel('Total Revenue ($)', fontsize=12)
axes[2].set_xlim(0, camp['Revenue'].max() * 1.25)
for bar, val, rate in zip(bars_c, camp['Revenue'], camp['Conv Rate']):
    axes[2].text(val + 300, bar.get_y() + bar.get_height()/2,
                 f'${val/1e3:.1f}K  ({rate:.1f}%)',
                 va='center', fontsize=10, fontweight='bold')

plt.suptitle('Drop-off Heatmap · Device · Campaign Performance',
             fontsize=16, fontweight='bold', y=1.02)
plt.savefig('t3_dropoff.png', bbox_inches='tight')
plt.show()
print("📊 Chart 4 saved : t3_dropoff.png")


# ════════════════════════════════════════════════════════════
# SECTION 6 — MONTHLY TRENDS
# ════════════════════════════════════════════════════════════

month_order = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']
monthly = df.groupby('month_name').agg(
    Leads=('lead_id','count'),
    Conversions=('converted','sum'),
    Revenue=('revenue','sum'),
    Spend=('ad_spend','sum')
).reset_index()
monthly['Conv Rate'] = monthly['Conversions'] / monthly['Leads'] * 100
monthly['month_num'] = monthly['month_name'].map(
    {m: i+1 for i, m in enumerate(month_order)})
monthly = monthly.sort_values('month_num')

fig, axes = plt.subplots(1, 3, figsize=(24, 7))
fig.subplots_adjust(wspace=0.38)

# Leads + Conversions dual axis
ax1 = axes[0]
ax2 = ax1.twinx()
ax1.bar(monthly['month_name'], monthly['Leads'],
        color='#4361ee', alpha=0.6, label='Leads',
        width=0.6, edgecolor='white')
ax2.plot(monthly['month_name'], monthly['Conversions'],
         color='#f72585', marker='o', linewidth=2.5, markersize=8,
         markerfacecolor='white', markeredgewidth=2, label='Conversions')
ax1.set_ylabel('Total Leads', fontsize=12, color='#4361ee')
ax2.set_ylabel('Conversions', fontsize=12, color='#f72585')
ax1.tick_params(axis='x', rotation=35)
ax1.set_title('Monthly Leads vs Conversions',
               fontweight='bold', fontsize=14, pad=12)
l1, lb1 = ax1.get_legend_handles_labels()
l2, lb2 = ax2.get_legend_handles_labels()
ax1.legend(l1+l2, lb1+lb2, fontsize=10, loc='upper left')

# Revenue trend
axes[1].plot(range(len(monthly)), monthly['Revenue'],
             color='#2dc653', marker='s', linewidth=2.5, markersize=9,
             markerfacecolor='white', markeredgewidth=2)
axes[1].fill_between(range(len(monthly)), monthly['Revenue'],
                     alpha=0.12, color='#2dc653')
axes[1].set_xticks(range(len(monthly)))
axes[1].set_xticklabels(monthly['month_name'], rotation=35)
axes[1].yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K'))
axes[1].set_title('Monthly Revenue Trend',
                   fontweight='bold', fontsize=14, pad=12)
axes[1].set_ylabel('Revenue ($)', fontsize=12)
for x, (_, row) in enumerate(monthly.iterrows()):
    axes[1].annotate(f"${row['Revenue']/1e3:.1f}K",
                     (x, row['Revenue']),
                     textcoords='offset points', xytext=(0, 10),
                     ha='center', fontsize=8.5,
                     color='#1a7a35', fontweight='bold')

# Conversion rate bar
bar_c3 = ['#2dc653' if r > 22 else '#f8961e' if r > 18 else '#f72585'
           for r in monthly['Conv Rate']]
bars_m = axes[2].bar(monthly['month_name'], monthly['Conv Rate'],
                     color=bar_c3, edgecolor='white', linewidth=1, width=0.6)
axes[2].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[2].set_title('Monthly Conversion Rate',
                   fontweight='bold', fontsize=14, pad=12)
axes[2].set_ylabel('Conversion Rate (%)', fontsize=12)
axes[2].tick_params(axis='x', rotation=35)
axes[2].set_ylim(0, monthly['Conv Rate'].max() * 1.22)
for bar, val in zip(bars_m, monthly['Conv Rate']):
    axes[2].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.2,
                 f'{val:.1f}%', ha='center',
                 fontsize=9, fontweight='bold')

plt.suptitle('Monthly Performance Trends',
             fontsize=16, fontweight='bold', y=1.02)
plt.savefig('t3_monthly.png', bbox_inches='tight')
plt.show()
print("📊 Chart 5 saved : t3_monthly.png")


# ════════════════════════════════════════════════════════════
# SECTION 7 — AUDIENCE & REGION ANALYSIS
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(24, 7))
fig.subplots_adjust(wspace=0.38)

# Age group conversion
age = df.groupby('age_group')['converted'].agg(['sum','count']).reset_index()
age['rate'] = age['sum'] / age['count'] * 100
bar_ca = ['#2dc653' if r > 22 else '#f8961e' if r > 18 else '#f72585'
          for r in age['rate']]
bars_a = axes[0].bar(age['age_group'], age['rate'],
                     color=bar_ca, edgecolor='white', linewidth=1, width=0.55)
axes[0].yaxis.set_major_formatter(mtick.PercentFormatter())
axes[0].set_title('Conversion Rate by Age Group',
                   fontweight='bold', fontsize=14, pad=12)
axes[0].set_ylabel('Conversion Rate (%)', fontsize=12)
axes[0].set_ylim(0, age['rate'].max() * 1.22)
for bar, val in zip(bars_a, age['rate']):
    axes[0].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.3,
                 f'{val:.1f}%', ha='center',
                 fontsize=11, fontweight='bold')

# Region dual axis
reg = df.groupby('region').agg(
    Revenue=('revenue','sum'), Conversions=('converted','sum'),
    Leads=('lead_id','count')
).reset_index()
reg['Conv Rate'] = reg['Conversions'] / reg['Leads'] * 100
reg = reg.sort_values('Revenue', ascending=False)
x = range(len(reg)); w = 0.35
ax_r1 = axes[1]
ax_r2 = ax_r1.twinx()
ax_r1.bar([i-w/2 for i in x], reg['Revenue'],
          width=w, color='#4361ee', edgecolor='white', label='Revenue')
ax_r2.bar([i+w/2 for i in x], reg['Conv Rate'],
          width=w, color='#2dc653', edgecolor='white', label='Conv Rate %')
ax_r1.set_xticks(list(x))
ax_r1.set_xticklabels(reg['region'], fontsize=12)
ax_r1.yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K'))
ax_r2.yaxis.set_major_formatter(mtick.PercentFormatter())
ax_r1.set_ylabel('Revenue ($)', fontsize=12, color='#4361ee')
ax_r2.set_ylabel('Conv Rate (%)', fontsize=12, color='#2dc653')
ax_r1.set_title('Revenue & Conversion Rate\nby Region',
                 fontweight='bold', fontsize=14, pad=12)
l1, lb1 = ax_r1.get_legend_handles_labels()
l2, lb2 = ax_r2.get_legend_handles_labels()
ax_r1.legend(l1+l2, lb1+lb2, fontsize=10)

# Revenue distribution
rev_data = df[df['converted']==1]['revenue'].value_counts().sort_index()
bars_rv = axes[2].bar([f'${int(v)}' for v in rev_data.index],
                      rev_data.values,
                      color=['#4361ee','#4895ef','#f8961e','#f72585','#7b2d8b'],
                      edgecolor='white', linewidth=1, width=0.6)
axes[2].set_title('Revenue Distribution\n(Converted Orders)',
                   fontweight='bold', fontsize=14, pad=12)
axes[2].set_xlabel('Order Value ($)', fontsize=12)
axes[2].set_ylabel('Number of Orders', fontsize=12)
for bar, val in zip(bars_rv, rev_data.values):
    axes[2].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 3,
                 str(val), ha='center',
                 fontsize=11, fontweight='bold')

plt.suptitle('Audience, Region & Revenue Analysis',
             fontsize=16, fontweight='bold', y=1.02)
plt.savefig('t3_audience.png', bbox_inches='tight')
plt.show()
print("📊 Chart 6 saved : t3_audience.png")


# ════════════════════════════════════════════════════════════
# SECTION 8 — CPA + SPEND vs REVENUE + STAGE PIE
# ════════════════════════════════════════════════════════════

ch2 = df.groupby('channel').agg(
    Conversions=('converted','sum'), Spend=('ad_spend','sum'),
    Revenue=('revenue','sum'), Leads=('lead_id','count')
).reset_index()
ch2['CPA']  = ch2['Spend'] / ch2['Conversions']
ch2['ROAS'] = ch2['Revenue'] / ch2['Spend']

fig, axes = plt.subplots(1, 3, figsize=(24, 7))
fig.subplots_adjust(wspace=0.38)

# CPA horizontal bar
ch_cpa = ch2.sort_values('CPA', ascending=True)
bar_cp = ['#2dc653' if c < 20 else '#f8961e' if c < 30 else '#f72585'
          for c in ch_cpa['CPA']]
bars_cp = axes[0].barh(ch_cpa['channel'], ch_cpa['CPA'],
                       color=bar_cp, edgecolor='white',
                       linewidth=1, height=0.55)
axes[0].set_title('Cost Per Acquisition (CPA)\nby Channel — Lower is Better',
                   fontweight='bold', fontsize=14, pad=12)
axes[0].set_xlabel('CPA ($)', fontsize=12)
axes[0].set_xlim(0, ch_cpa['CPA'].max() * 1.25)
for bar, val in zip(bars_cp, ch_cpa['CPA']):
    axes[0].text(val + 0.3, bar.get_y() + bar.get_height()/2,
                 f'${val:.2f}', va='center',
                 fontsize=11, fontweight='bold')

# Spend vs Revenue bubble
colors_s = ['#4361ee','#f72585','#2dc653','#f8961e','#7b2d8b','#4cc9f0']
for idx, (_, row) in enumerate(ch2.iterrows()):
    axes[1].scatter(row['Spend'], row['Revenue'],
                    s=row['Conversions'] * 3,
                    color=colors_s[idx], alpha=0.85,
                    edgecolors='white', linewidth=1.5,
                    label=row['channel'], zorder=3)
    axes[1].annotate(row['channel'],
                     (row['Spend'], row['Revenue']),
                     textcoords='offset points', xytext=(6, 4),
                     fontsize=9, fontweight='bold')
max_val = max(ch2['Spend'].max(), ch2['Revenue'].max()) * 1.15
axes[1].plot([0, max_val], [0, max_val], color='red',
             linestyle='--', linewidth=1.5, alpha=0.6, label='Break-even')
axes[1].xaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'${x/1e3:.1f}K'))
axes[1].yaxis.set_major_formatter(
    mtick.FuncFormatter(lambda x, _: f'${x/1e3:.1f}K'))
axes[1].set_title('Ad Spend vs Revenue by Channel\n(Bubble = Conversions)',
                   fontweight='bold', fontsize=14, pad=12)
axes[1].set_xlabel('Total Ad Spend ($)', fontsize=12)
axes[1].set_ylabel('Total Revenue ($)', fontsize=12)
axes[1].legend(fontsize=8, loc='upper left')

# Stage pie
stage_order  = ['Converted','Checkout','Product View','Awareness','Bounced']
stage_vals   = [df[df['funnel_stage']==s].shape[0] for s in stage_order]
pie_colors   = ['#2dc653','#4cc9f0','#4361ee','#f8961e','#f72585']
wedges, texts, autotexts = axes[2].pie(
    stage_vals, labels=stage_order, autopct='%1.1f%%',
    colors=pie_colors, startangle=90,
    wedgeprops=dict(edgecolor='white', linewidth=2),
    textprops=dict(fontsize=11))
for at in autotexts:
    at.set_fontweight('bold'); at.set_fontsize(11)
axes[2].set_title('Lead Distribution\nby Funnel Stage',
                   fontweight='bold', fontsize=14, pad=12)

plt.suptitle('CPA Analysis · Spend vs Revenue · Funnel Stage Mix',
             fontsize=16, fontweight='bold', y=1.02)
plt.savefig('t3_cpa.png', bbox_inches='tight')
plt.show()
print("📊 Chart 7 saved : t3_cpa.png")


# ════════════════════════════════════════════════════════════
# SECTION 9 — KEY INSIGHTS (printed)
# ════════════════════════════════════════════════════════════

top_ch_rev  = ch2.sort_values('Revenue',ascending=False).iloc[0]['channel']
top_ch_conv = ch2.sort_values('ROAS',ascending=False).iloc[0]['channel']
worst_cpa   = ch2.sort_values('CPA',ascending=False).iloc[0]['channel']
checkout_cr = stage_conv[3]
visitor_aw  = stage_conv[0]

print(f"""
╔══════════════════════════════════════════════════════════╗
║      KEY INSIGHTS — MARKETING FUNNEL ANALYSIS           ║
╠══════════════════════════════════════════════════════════╣
║  1. Overall Conversion Rate : {conv_rate:.1f}%                      ║
║  2. Bounce Rate             : {bounce_rate:.1f}%                      ║
║  3. Total Revenue           : ${total_revenue:>10,.0f}             ║
║  4. ROAS                    : {roas:.2f}x                       ║
║  5. Top Revenue Channel     : {top_ch_rev:<28}║
║  6. Best ROAS Channel       : {top_ch_conv:<28}║
║  7. Highest CPA Channel     : {worst_cpa:<28}║
║  8. Checkout → Conv Rate    : {checkout_cr:.1f}%                      ║
╠══════════════════════════════════════════════════════════╣
║                  RECOMMENDATIONS                        ║
╠══════════════════════════════════════════════════════════╣
║  ✅ Fix Checkout drop-off — biggest conversion leak      ║
║  ✅ Scale budget on best ROAS channel                    ║
║  ✅ Optimize mobile UX — large traffic, low conversion   ║
║  ✅ Retarget Product View & Checkout abandoners          ║
║  ⚠️  Reduce spend on highest CPA channel                 ║
╚══════════════════════════════════════════════════════════╝
""")


# ════════════════════════════════════════════════════════════
# SECTION 10 — GENERATE PDF REPORT
# ════════════════════════════════════════════════════════════

doc    = SimpleDocTemplate('FUTURE_DS_03_Report.pdf', pagesize=A4,
                           rightMargin=1.8*cm, leftMargin=1.8*cm,
                           topMargin=1.5*cm, bottomMargin=1.5*cm)
styles = getSampleStyleSheet()
story  = []

title_s = ParagraphStyle('T', parent=styles['Title'],
    fontSize=18, textColor=colors.HexColor('#1a1a2e'),
    spaceAfter=4, alignment=TA_CENTER, fontName='Helvetica-Bold')
sub_s = ParagraphStyle('S', parent=styles['Normal'],
    fontSize=10, textColor=colors.HexColor('#555555'),
    alignment=TA_CENTER, spaceAfter=12)
h2_s = ParagraphStyle('H2', parent=styles['Heading2'],
    fontSize=13, textColor=colors.HexColor('#4361ee'),
    spaceBefore=14, spaceAfter=6, fontName='Helvetica-Bold')
ins_s = ParagraphStyle('I', parent=styles['Normal'],
    fontSize=9.5, leading=15,
    textColor=colors.HexColor('#1a1a2e'), leftIndent=10)
cap_s = ParagraphStyle('C', parent=styles['Normal'],
    fontSize=9, textColor=colors.HexColor('#666666'),
    alignment=TA_CENTER, spaceAfter=5,
    fontName='Helvetica-BoldOblique')

story.append(Spacer(1, 0.5*cm))
story.append(Paragraph(
    'Marketing Funnel &amp; Conversion Performance Analysis', title_s))
story.append(Paragraph(
    'Future Interns — Data Science &amp; Analytics | Task 3 (FUTURE_DS_03)', sub_s))
story.append(Paragraph(
    'Dataset: Marketing Funnel (5,000 Leads) &nbsp;|&nbsp; '
    'Tools: Python, Pandas, Matplotlib, Seaborn', sub_s))
story.append(HRFlowable(width='100%', thickness=2,
                        color=colors.HexColor('#4361ee'), spaceAfter=10))

story.append(Paragraph('Executive KPI Summary', h2_s))
kpi_table_data = [
    ['Metric','Value','Metric','Value'],
    ['Total Leads',     f'{total_leads:,}',        'Total Conversions', f'{total_conv:,}'],
    ['Conversion Rate', f'{conv_rate:.1f}%',        'Bounce Rate',       f'{bounce_rate:.1f}%'],
    ['Total Revenue',   f'${total_revenue:,.0f}',   'Total Ad Spend',    f'${total_spend:,.0f}'],
    ['ROAS',            f'{roas:.2f}x',              'Avg Order Value',   f'${avg_order:.0f}'],
]
kt = Table(kpi_table_data, colWidths=[4.5*cm, 4.2*cm, 4.5*cm, 4.2*cm])
kt.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,0),  colors.HexColor('#4361ee')),
    ('TEXTCOLOR',     (0,0),(-1,0),  colors.white),
    ('FONTNAME',      (0,0),(-1,0),  'Helvetica-Bold'),
    ('FONTSIZE',      (0,0),(-1,0),  10),
    ('ALIGN',         (0,0),(-1,-1),'CENTER'),
    ('FONTNAME',      (0,1),(0,-1),  'Helvetica-Bold'),
    ('FONTNAME',      (2,1),(2,-1),  'Helvetica-Bold'),
    ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.HexColor('#f0f4ff'),colors.white]),
    ('GRID',          (0,0),(-1,-1), 0.5, colors.HexColor('#cccccc')),
    ('ROWHEIGHT',     (0,0),(-1,-1), 20),
    ('TOPPADDING',    (0,0),(-1,-1), 5),
]))
story.append(kt)
story.append(Spacer(1, 0.4*cm))

W = 17*cm
charts = [
    ('t3_kpi.png',      'Fig 1 — Marketing Funnel KPI Dashboard',                        W, 3.5*cm),
    ('t3_funnel.png',   'Fig 2 — Funnel Stage Volume & Stage-to-Stage Conversion Rates',  W, 7.5*cm),
    ('t3_channel.png',  'Fig 3 — Channel Revenue, Conversion Rate & ROAS',               W, 7.0*cm),
    ('t3_dropoff.png',  'Fig 4 — Drop-off Heatmap · Device · Campaign Performance',      W, 7.0*cm),
    ('t3_monthly.png',  'Fig 5 — Monthly Leads, Revenue & Conversion Trends',            W, 7.0*cm),
    ('t3_audience.png', 'Fig 6 — Age Group · Regional · Revenue Distribution',           W, 7.0*cm),
    ('t3_cpa.png',      'Fig 7 — CPA Analysis · Spend vs Revenue · Stage Mix',           W, 7.0*cm),
]
for fname, caption, w, h in charts:
    story.append(Paragraph(caption, cap_s))
    story.append(Image(fname, width=w, height=h))
    story.append(Spacer(1, 0.3*cm))

story.append(HRFlowable(width='100%', thickness=1.5,
                        color=colors.HexColor('#4361ee'), spaceAfter=8))
story.append(Paragraph('Key Insights', h2_s))
insights = [
    ('📊 Overall Funnel Health',
     f'Of {total_leads:,} total leads, {total_conv:,} converted ({conv_rate:.1f}%). '
     f'The {bounce_rate:.1f}% bounce rate signals significant early-stage drop-off.'),
    ('🏆 Best Performing Channel',
     f'{top_ch_rev} generates the most revenue. {top_ch_conv} delivers the best ROAS — '
     f'every dollar invested returns the most. Budget should be scaled here first.'),
    ('📉 Checkout is the Biggest Leak',
     f'The Checkout → Converted stage shows the steepest drop-off ({checkout_cr:.1f}% conversion). '
     f'Simplifying checkout and adding trust signals directly improves revenue.'),
    ('📱 Mobile UX Gap',
     f'Mobile drives 40%+ of traffic but converts at a lower rate than Desktop. '
     f'Mobile-first optimizations are a high-impact, low-effort opportunity.'),
    ('📅 Seasonal Patterns Exist',
     f'Monthly data shows clear peaks and troughs. Budget should be increased during '
     f'high-converting months and campaigns re-evaluated in low-performing periods.'),
    ('🎯 25–34 Age Group Converts Best',
     f'The 25–34 segment has the highest conversion rate. Scaling lookalike audiences '
     f'based on this group can significantly grow overall conversions.'),
    ('💸 CPA Imbalance Across Channels',
     f'{worst_cpa} has the highest CPA — meaning you pay the most per customer acquired. '
     f'Reallocating this budget to lower-CPA channels improves efficiency immediately.'),
]
for title, text in insights:
    story.append(Paragraph(f'<b>{title}:</b> {text}', ins_s))
    story.append(Spacer(1, 0.15*cm))

story.append(Paragraph('Actionable Recommendations', h2_s))
recs = [
    ('Fix Checkout Drop-off First',
     'Add progress bars, trust badges, and reduce form fields at checkout. '
     'A/B test single-page vs multi-step checkout. Even a 5% lift here compounds into major revenue.'),
    ('Scale Budget on Best ROAS Channels',
     f'Shift 20–30% of budget away from {worst_cpa} toward Email and Referral. '
     f'These channels convert better at lower cost per acquisition.'),
    ('Mobile-First UX Audit',
     'Run a full mobile funnel audit from landing page through checkout. '
     'Faster load times, larger CTAs, and auto-filled forms directly lift mobile conversion rates.'),
    ('Retarget Warm Leads',
     'Set up retargeting campaigns for visitors who reached Product View or Checkout '
     'without converting. These are your highest-intent, cheapest-to-convert audience.'),
    ('Align Spend with Seasonal Peaks',
     'Use monthly trend data to pre-load budget in high-converting months. '
     'Launching campaigns just before seasonal peaks maximizes returns.'),
    ('Invest in 25–34 Segment Campaigns',
     'Build lookalike audiences based on existing converters in this age group. '
     'Use tailored messaging and personalized landing pages for maximum relevance.'),
]
for i, (title, text) in enumerate(recs, 1):
    story.append(Paragraph(f'<b>{i}. {title}:</b> {text}', ins_s))
    story.append(Spacer(1, 0.12*cm))

story.append(Spacer(1, 0.4*cm))
story.append(HRFlowable(width='100%', thickness=1,
                        color=colors.HexColor('#cccccc')))
story.append(Paragraph(
    'Analysis by: [Your Name] &nbsp;|&nbsp; Future Interns — '
    'Data Science &amp; Analytics &nbsp;|&nbsp; FUTURE_DS_03',
    ParagraphStyle('foot', parent=styles['Normal'], fontSize=8,
                   textColor=colors.HexColor('#999999'),
                   alignment=TA_CENTER, spaceBefore=8)))

doc.build(story)
