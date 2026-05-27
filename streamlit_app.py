# ============================================================
# KAT — IT Asset Business System v2
# Professional Streamlit Dashboard v2.2
# ============================================================

import streamlit as st
import gspread
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="KAT — Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif !important; }
.main { background-color: #F0F4F8; }
.block-container {
    padding: 0 48px 32px 48px !important;
    max-width: 100% !important;
}
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none; }

.kat-header {
    background: linear-gradient(135deg, #0A1628 0%, #1B3A6B 50%, #2471A3 100%);
    padding: 18px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    border-radius: 0 0 12px 12px;
    margin: 0 0 16px 0;
}
.kat-logo-area {
    display: flex;
    align-items: center;
    gap: 16px;
    background: white;
    padding: 10px 18px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.kat-logo-img {
    height: 48px;
    width: auto;
}
.kat-header-right { text-align: right; }
.kat-company-name {
    color: white;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
}
.kat-live-badge {
    background: rgba(39, 174, 96, 0.2);
    border: 1px solid rgba(39, 174, 96, 0.5);
    color: #2ECC71;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1px;
    margin-top: 6px;
    display: inline-block;
}

.section-header {
    background: linear-gradient(90deg, #1B3A6B, #2471A3);
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 18px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
    border-left: 4px solid #27AE60;
}

.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-top: 4px solid #2471A3;
    height: 100%;
}
.kpi-card.green { border-top-color: #27AE60; }
.kpi-card.red { border-top-color: #E74C3C; }
.kpi-card.gold { border-top-color: #F39C12; }
.kpi-card.purple { border-top-color: #9B59B6; }
.kpi-card.teal { border-top-color: #1ABC9C; }
.kpi-icon { font-size: 20px; margin-bottom: 6px; display: block; }
.kpi-label {
    font-size: 10px;
    font-weight: 700;
    color: #95A5A6;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 24px;
    font-weight: 800;
    color: #1B3A6B;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-sub { font-size: 11px; color: #BDC3C7; }

.prog-row {
    background: white;
    border-radius: 12px;
    padding: 14px 20px;
    margin: 8px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.prog-label-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.prog-title { font-size: 13px; font-weight: 600; color: #5D6D7E; }
.prog-pct { font-size: 14px; font-weight: 800; color: #1B3A6B; }
.prog-bar-bg {
    background: #EEF2F9;
    border-radius: 20px;
    height: 14px;
    overflow: hidden;
}
.prog-bar-fill {
    height: 100%;
    border-radius: 20px;
    transition: width 0.8s ease;
}
.prog-legend {
    display: flex;
    gap: 20px;
    margin-top: 10px;
    flex-wrap: wrap;
}
.prog-legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: #5D6D7E;
}
.prog-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
}

.chart-container {
    background: white;
    border-radius: 14px;
    padding: 8px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin: 6px 0;
}

@media (max-width: 768px) {
    .block-container { padding: 0 16px 24px 16px !important; }
    .kat-header { padding: 12px 16px; flex-wrap: wrap; gap: 8px; }
    .kat-company-name { font-size: 16px; }
    .kat-logo-img { height: 40px; }
    .kpi-value { font-size: 20px; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONNECTION
# ============================================================
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]
SHEET_ID = "1WySRL2qXuByeAXPVdEBk9nGWFKasn1vEvhP-yAYH2R4"
LOGO_URL = "https://drive.google.com/thumbnail?id=18MShHQWnYrGtNFCKICQ7Ss166R101__7&sz=w400"

@st.cache_resource(ttl=600)
def get_client():
    creds_dict = json.loads(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    return gspread.authorize(creds)

@st.cache_data(ttl=600)
def load_data():
    try:
        client = get_client()
        sh = client.open_by_key(SHEET_ID)

        def get_sheet(name):
            try:
                return sh.worksheet(name).get_all_values()
            except:
                return []

        def safe_float(val, default=0):
            try:
                if val is None or val == '' or val == 'None':
                    return default
                cleaned = str(val).replace('$','').replace(',','').replace('%','').replace('AED','').strip()
                return float(cleaned) if cleaned else default
            except:
                return default

        settings = get_sheet('SETTINGS')
        def gs(row, col=1):
            try:
                return settings[row-1][col]
            except:
                return 0

        inv_data = get_sheet('INVENTORY')
        lc_data = get_sheet('LANDED COST')
        ref_data = get_sheet('REFERENCE')

        usd_aed_rate = safe_float(ref_data[5][1] if len(ref_data) > 5 else 3.6725, 3.6725)

        total_capital = safe_float(gs(7))
        proc_spend = safe_float(gs(8))
        total_revenue = safe_float(gs(9))
        cash_balance = safe_float(gs(10))
        inv_value_usd = safe_float(gs(11))
        auction_budget = safe_float(gs(18))
        spent_auctions = safe_float(gs(19))
        avail_bidding = safe_float(gs(20))
        avg_days_ship = safe_float(gs(31))
        avg_days_clear = safe_float(gs(32))
        units_procured = safe_float(gs(47))
        units_sold = safe_float(gs(48))
        units_remaining = safe_float(gs(49))
        best_category = gs(55)

        # CALCULATE percentages from raw numbers
        # This avoids the formatting bug from SETTINGS sheet
        pct_used = (proc_spend / total_capital) if total_capital > 0 else 0
        pct_avail = (avail_bidding / total_capital) if total_capital > 0 else 0
        stock_sold_pct = (units_sold / units_procured) if units_procured > 0 else 0
        break_even = (total_revenue / proc_spend) if proc_spend > 0 else 0

        lots_procured = 0
        lots_sold = 0
        lots_in_stock = 0
        if len(inv_data) > 5:
            for row in inv_data[5:]:
                if len(row) > 14 and row[0]:
                    status = row[14]
                    lots_procured += 1
                    if status == 'Sold Out':
                        lots_sold += 1
                    elif status == 'Partial':
                        lots_sold += 1
                        lots_in_stock += 1
                    elif status in ['In Stock','Pending Shipment']:
                        lots_in_stock += 1

        gross_profit = 0
        margin_pct = 0
        roi_pct = 0
        total_landed_sum = 0
        if len(lc_data) > 5:
            total_revenue_sum = 0
            for row in lc_data[5:]:
                if len(row) > 40 and row[0]:
                    ak = safe_float(row[36])
                    an = safe_float(row[39])
                    total_landed_sum += ak
                    total_revenue_sum += an
            gross_profit = total_revenue_sum - total_landed_sum
            if total_revenue_sum > 0:
                margin_pct = gross_profit / total_revenue_sum
            if total_landed_sum > 0:
                roi_pct = gross_profit / total_landed_sum

        cost_breakdown = {
            'Purchase Cost': proc_spend,
            'US Logistics': 0,
            'Freight': 0,
            'Customs Duty': 0,
            'VAT': 0,
            'Agent Fees': 0,
            'Local Transport': 0
        }
        if len(lc_data) > 5:
            for row in lc_data[5:]:
                if len(row) > 40 and row[0]:
                    cost_breakdown['Freight'] += safe_float(row[14])
                    cost_breakdown['Customs Duty'] += safe_float(row[21])
                    cost_breakdown['VAT'] += safe_float(row[26])
                    cost_breakdown['Agent Fees'] += safe_float(row[30])
                    cost_breakdown['Local Transport'] += safe_float(row[31])
                    cost_breakdown['US Logistics'] += safe_float(row[35])

        return {
            'usd_aed_rate': usd_aed_rate,
            'total_capital': total_capital,
            'proc_spend': proc_spend,
            'total_revenue': total_revenue,
            'cash_balance': cash_balance,
            'inv_value_usd': inv_value_usd,
            'auction_budget': auction_budget,
            'spent_auctions': spent_auctions,
            'avail_bidding': avail_bidding,
            'pct_used': pct_used,
            'pct_avail': pct_avail,
            'avg_days_ship': avg_days_ship,
            'avg_days_clear': avg_days_clear,
            'units_procured': units_procured,
            'units_sold': units_sold,
            'units_remaining': units_remaining,
            'stock_sold_pct': stock_sold_pct,
            'best_category': best_category,
            'gross_profit': gross_profit,
            'margin_pct': margin_pct,
            'roi_pct': roi_pct,
            'break_even': break_even,
            'total_landed_sum': total_landed_sum,
            'lots_procured': lots_procured,
            'lots_sold': lots_sold,
            'lots_in_stock': lots_in_stock,
            'cost_breakdown': cost_breakdown,
            'timestamp': datetime.now().strftime("%d %b %Y  %H:%M")
        }
    except Exception as e:
        st.error(f"Data load error: {e}")
        return None

def fmt_usd(val):
    if val is None: return "$0.00"
    return f"${val:,.2f}"

def fmt_pct(val):
    if val is None: return "0.00%"
    return f"{val*100:.2f}%"

def fmt_num(val):
    if val is None: return "0"
    return f"{int(val):,}"

def health_color(val, good, warn, higher_is_better=True):
    if higher_is_better:
        if val >= good: return "green"
        if val >= warn: return "gold"
        return "red"
    else:
        if val <= good: return "green"
        if val <= warn: return "gold"
        return "red"

def kpi_card(icon, label, value, sub="", color="blue"):
    return f"""<div class="kpi-card {color}"><span class="kpi-icon">{icon}</span><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>"""

def progress_bar_row(title, pct, pct_label, fill_color, legend_items):
    pct_clamped = min(max(pct * 100, 0), 100)
    legend_html = ''.join([
        f'<div class="prog-legend-item"><span class="prog-dot" style="background:{item["color"]};"></span>{item["label"]}</div>'
        for item in legend_items
    ])
    return f"""<div class="prog-row"><div class="prog-label-row"><div class="prog-title">{title}</div><div class="prog-pct">{pct_label}</div></div><div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{pct_clamped:.1f}%;background:linear-gradient(90deg,{fill_color},{fill_color}cc);"></div></div><div class="prog-legend">{legend_html}</div></div>"""

def section_hdr(icon, title):
    st.markdown(f'<div class="section-header">{icon}&nbsp;&nbsp;{title}</div>', unsafe_allow_html=True)

# ============================================================
# LOAD
# ============================================================
data = load_data()
if data is None:
    st.error("Unable to load data.")
    st.stop()

d = data

# ============================================================
# HEADER
# ============================================================
st.markdown(f"""
<div class="kat-header">
    <div class="kat-logo-area">
        <img src="{LOGO_URL}" class="kat-logo-img" onerror="this.style.display='none'"/>
    </div>
    <div class="kat-header-right">
        <div class="kat-company-name">Key Asset Technologies</div>
        <div class="kat-live-badge">🟢 LIVE DATA</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECTION 1 — CAPITAL OVERVIEW
# ============================================================
section_hdr("💰", "CAPITAL OVERVIEW")

col1, col2, col3, col4 = st.columns(4)
with col1:
    clr = health_color(d['cash_balance'], 1000, 0)
    st.markdown(kpi_card("🏦", "CASH BALANCE", fmt_usd(d['cash_balance']), "Capital - Spent + Revenue", clr), unsafe_allow_html=True)
with col2:
    st.markdown(kpi_card("💵", "TOTAL CAPITAL INJECTED", fmt_usd(d['total_capital']), "Total funds received", "blue"), unsafe_allow_html=True)
with col3:
    clr = health_color(d['avail_bidding'], 2000, 500)
    st.markdown(kpi_card("🎯", "AVAILABLE FOR BIDDING", fmt_usd(d['avail_bidding']), f"{fmt_pct(d['pct_avail'])} of budget free", clr), unsafe_allow_html=True)
with col4:
    clr = health_color(d['pct_used'], 0.3, 0.7, higher_is_better=False)
    st.markdown(kpi_card("📊", "CAPITAL DEPLOYED", fmt_pct(d['pct_used']), fmt_usd(d['spent_auctions']) + " spent", clr), unsafe_allow_html=True)

# ============================================================
# SECTION 2 — PROFITABILITY
# ============================================================
section_hdr("📈", "PROFITABILITY")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(kpi_card("💰", "TOTAL REVENUE", fmt_usd(d['total_revenue']), "All sales collected", "green" if d['total_revenue'] > 0 else "gold"), unsafe_allow_html=True)
with col2:
    clr = "green" if d['gross_profit'] > 0 else "red"
    st.markdown(kpi_card("📈", "GROSS PROFIT", fmt_usd(d['gross_profit']), "Revenue minus landed cost", clr), unsafe_allow_html=True)
with col3:
    clr = "green" if d['margin_pct'] > 0 else "red"
    st.markdown(kpi_card("🎯", "GROSS MARGIN", fmt_pct(d['margin_pct']), "Profit / Revenue", clr), unsafe_allow_html=True)
with col4:
    clr = "green" if d['roi_pct'] > 0 else "red"
    st.markdown(kpi_card("🔄", "ROI", fmt_pct(d['roi_pct']), "Profit / Landed Cost", clr), unsafe_allow_html=True)
with col5:
    clr = "green" if d['break_even'] >= 1 else "gold"
    st.markdown(kpi_card("⚖️", "BREAK EVEN", fmt_pct(min(d['break_even'], 1)), "Revenue / Procurement", clr), unsafe_allow_html=True)

# ============================================================
# SECTION 3 — INVENTORY HEALTH
# ============================================================
section_hdr("📦", "INVENTORY HEALTH")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(kpi_card("📥", "LOTS PROCURED", fmt_num(d['lots_procured']), f"{fmt_num(d['units_procured'])} total units", "blue"), unsafe_allow_html=True)
with col2:
    clr = "green" if d['lots_sold'] > 0 else "gold"
    st.markdown(kpi_card("📤", "LOTS SOLD", fmt_num(d['lots_sold']), f"{fmt_num(d['units_sold'])} units | {fmt_pct(d['stock_sold_pct'])}", clr), unsafe_allow_html=True)
with col3:
    st.markdown(kpi_card("🏭", "LOTS IN STOCK", fmt_num(d['lots_in_stock']), f"{fmt_num(d['units_remaining'])} units remaining", "teal"), unsafe_allow_html=True)
with col4:
    st.markdown(kpi_card("💎", "INVENTORY VALUE", fmt_usd(d['inv_value_usd']), "At landed cost", "purple"), unsafe_allow_html=True)

# ============================================================
# SECTION 4 — SALES PERFORMANCE (moved above operations)
# ============================================================
section_hdr("🏆", "SALES PERFORMANCE")

col1, col2, col3, col4 = st.columns(4)
with col1:
    clr = "green" if d['units_sold'] > 0 else "gold"
    st.markdown(kpi_card("🏷️", "UNITS SOLD", fmt_num(d['units_sold']), f"of {fmt_num(d['units_procured'])} procured", clr), unsafe_allow_html=True)
with col2:
    rev_per_unit = d['total_revenue'] / d['units_sold'] if d['units_sold'] > 0 else 0
    st.markdown(kpi_card("💵", "REVENUE PER UNIT", fmt_usd(rev_per_unit), "Average price per unit", "green" if rev_per_unit > 0 else "gold"), unsafe_allow_html=True)
with col3:
    profit_per_unit = d['gross_profit'] / d['units_sold'] if d['units_sold'] > 0 else 0
    clr = "green" if profit_per_unit > 0 else "red"
    st.markdown(kpi_card("📈", "PROFIT PER UNIT", fmt_usd(profit_per_unit), "Average profit per unit", clr), unsafe_allow_html=True)
with col4:
    best = d['best_category'] if d['best_category'] else "No sales yet"
    st.markdown(kpi_card("🏆", "BEST CATEGORY", best, "Highest margin category", "green" if d['best_category'] else "gold"), unsafe_allow_html=True)

# ============================================================
# SECTION 5 — OPERATIONAL PROGRESS
# ============================================================
section_hdr("📊", "OPERATIONAL PROGRESS")

col_left, col_right = st.columns(2)

# Bar 1 — Capital Utilization
with col_left:
    st.markdown(progress_bar_row(
        title="Capital Utilization",
        pct=d['pct_used'],
        pct_label=fmt_pct(d['pct_used']),
        fill_color="#E67E22",
        legend_items=[
            {"color": "#E67E22", "label": f"Spent: {fmt_usd(d['proc_spend'])}"},
            {"color": "#27AE60", "label": f"Available: {fmt_usd(d['avail_bidding'])}"},
            {"color": "#2471A3", "label": f"Total: {fmt_usd(d['total_capital'])}"}
        ]
    ), unsafe_allow_html=True)

# Bar 2 — Stock Movement
with col_right:
    st.markdown(progress_bar_row(
        title="Stock Movement",
        pct=d['stock_sold_pct'],
        pct_label=fmt_pct(d['stock_sold_pct']),
        fill_color="#27AE60",
        legend_items=[
            {"color": "#27AE60", "label": f"Sold: {fmt_num(d['units_sold'])} units"},
            {"color": "#E67E22", "label": f"Remaining: {fmt_num(d['units_remaining'])} units"},
            {"color": "#2471A3", "label": f"Total: {fmt_num(d['units_procured'])} units"}
        ]
    ), unsafe_allow_html=True)

col_left, col_right = st.columns(2)

# Bar 3 — Break Even Progress
with col_left:
    st.markdown(progress_bar_row(
        title="Break Even Progress",
        pct=min(d['break_even'], 1),
        pct_label=fmt_pct(min(d['break_even'], 1)),
        fill_color="#27AE60",
        legend_items=[
            {"color": "#27AE60", "label": f"Revenue: {fmt_usd(d['total_revenue'])}"},
            {"color": "#E74C3C", "label": f"Gap to Cover: {fmt_usd(max(d['proc_spend'] - d['total_revenue'], 0))}"},
            {"color": "#2471A3", "label": f"Total Cost: {fmt_usd(d['proc_spend'])}"}
        ]
    ), unsafe_allow_html=True)

# Bar 4 — Units Sold vs Procured (replaced lots progress)
with col_right:
    st.markdown(progress_bar_row(
        title="Units Sold vs Procured",
        pct=d['stock_sold_pct'],
        pct_label=f"{fmt_pct(d['stock_sold_pct'])} ({fmt_num(d['units_sold'])} of {fmt_num(d['units_procured'])})",
        fill_color="#9B59B6",
        legend_items=[
            {"color": "#9B59B6", "label": f"Sold: {fmt_num(d['units_sold'])} units"},
            {"color": "#E67E22", "label": f"Remaining: {fmt_num(d['units_remaining'])} units"},
            {"color": "#2471A3", "label": f"Total: {fmt_num(d['units_procured'])} units"}
        ]
    ), unsafe_allow_html=True)

# Bar 5 — Pipeline Speed (full width)
total_pipeline = d['avg_days_ship'] + d['avg_days_clear']
pipeline_pct = min(total_pipeline / 30, 1) if total_pipeline > 0 else 0
st.markdown(progress_bar_row(
    title="Pipeline Speed (Purchase to Sale-Ready)",
    pct=pipeline_pct,
    pct_label=f"{total_pipeline:.1f} days of 30 day target",
    fill_color="#E74C3C" if total_pipeline > 14 else "#F39C12" if total_pipeline > 7 else "#27AE60",
    legend_items=[
        {"color": "#3498DB", "label": f"Ship Days: {d['avg_days_ship']:.1f}"},
        {"color": "#9B59B6", "label": f"Clear Days: {d['avg_days_clear']:.1f}"},
        {"color": "#E74C3C", "label": f"Target: under 14 days"}
    ]
), unsafe_allow_html=True)

# ============================================================
# SECTION 6 — VISUAL ANALYTICS
# ============================================================
section_hdr("📊", "VISUAL ANALYTICS")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    cb = d['cost_breakdown']
    labels = [k for k, v in cb.items() if v > 0]
    values = [v for v in cb.values() if v > 0]
    colors = ['#1B3A6B','#27AE60','#2471A3','#E74C3C','#F39C12','#9B59B6','#1ABC9C']
    fig_pie = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(colors=colors[:len(labels)], line=dict(color='white', width=2)),
        textfont=dict(size=11, color='white', family='Inter'),
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>'
    )])
    fig_pie.add_annotation(
        text=f"<b>Total</b><br>${sum(values):,.0f}",
        x=0.5, y=0.5,
        font=dict(size=12, color='#1B3A6B', family='Inter'),
        showarrow=False
    )
    fig_pie.update_layout(
        title=dict(text="<b>Cost Structure</b>", font=dict(size=14, color='#1B3A6B', family='Inter'), x=0.5),
        showlegend=True,
        legend=dict(font=dict(size=10, color='#1B3A6B'), orientation='v', x=1, y=0.5),
        margin=dict(t=50, b=20, l=20, r=100),
        height=320,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    cb = d['cost_breakdown']
    total_landed = sum(cb.values())
    wf_labels = list(cb.keys()) + ['TOTAL LANDED']
    wf_values = list(cb.values()) + [total_landed]
    measures = ['relative'] * len(cb) + ['total']
    fig_wf = go.Figure(go.Waterfall(
        name="Cost",
        orientation='v',
        measure=measures,
        x=wf_labels,
        y=wf_values,
        text=[f"${v:,.0f}" for v in wf_values],
        textposition='outside',
        textfont=dict(size=10, color='#1B3A6B', family='Inter'),
        increasing=dict(marker=dict(color='#2471A3')),
        totals=dict(marker=dict(color='#1B3A6B')),
        connector=dict(line=dict(color='#E8ECF1', width=1, dash='dot'))
    ))
    fig_wf.update_layout(
        title=dict(text="<b>Landed Cost Build-Up</b>", font=dict(size=14, color='#1B3A6B', family='Inter'), x=0.5),
        margin=dict(t=50, b=80, l=40, r=20),
        height=320,
        paper_bgcolor='white',
        plot_bgcolor='#FAFBFD',
        xaxis=dict(tickfont=dict(size=9, color='#5D6D7E'), tickangle=-30),
        yaxis=dict(tickfont=dict(size=9), gridcolor='#E8ECF1', tickprefix='$'),
        showlegend=False
    )
    st.plotly_chart(fig_wf, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown(f"""
<div style="
    background:linear-gradient(135deg,#0A1628,#1B3A6B);
    padding:20px 28px;
    margin: 24px 0;
    display:flex;
    justify-content:space-between;
    align-items:center;
    border-radius:12px;
">
    <div style="color:rgba(255,255,255,0.5);font-size:11px;">
        Key Asset Technologies &copy; 2025 &nbsp;|&nbsp; IT Asset Business System v2
    </div>
    <div style="color:rgba(255,255,255,0.5);font-size:11px;">
        Data refreshes every 10 minutes &nbsp;|&nbsp; Last updated: {d['timestamp']}
    </div>
</div>
""", unsafe_allow_html=True)
