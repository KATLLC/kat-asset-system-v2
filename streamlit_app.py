# ============================================================
# KAT — IT Asset Business System v2
# Professional Streamlit Dashboard
# ============================================================

import streamlit as st
import gspread
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
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
# CUSTOM CSS — Professional Dark Header / Light Body
# ============================================================
st.markdown("""
<style>
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global */
* { font-family: 'Inter', sans-serif !important; }
.main { background-color: #F0F4F8; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Hide Streamlit default elements */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── HEADER ─────────────────────────────────────────────── */
.kat-header {
    background: linear-gradient(135deg, #0A1628 0%, #1B3A6B 50%, #2471A3 100%);
    padding: 18px 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    position: sticky;
    top: 0;
    z-index: 999;
}
.kat-logo-area {
    display: flex;
    align-items: center;
    gap: 14px;
}
.kat-logo-img {
    height: 48px;
    width: auto;
}
.kat-header-title {
    color: white;
    font-size: 11px;
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.7;
    margin-top: 2px;
}
.kat-company-name {
    color: white;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
}
.kat-header-right {
    text-align: right;
}
.kat-live-badge {
    background: rgba(39, 174, 96, 0.2);
    border: 1px solid rgba(39, 174, 96, 0.5);
    color: #2ECC71;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    margin-bottom: 4px;
    display: inline-block;
}
.kat-timestamp {
    color: rgba(255,255,255,0.5);
    font-size: 11px;
}
.kat-rate {
    color: rgba(255,255,255,0.8);
    font-size: 12px;
    font-weight: 500;
    margin-top: 2px;
}

/* ── SECTION HEADERS ────────────────────────────────────── */
.section-header {
    background: linear-gradient(90deg, #1B3A6B, #2471A3);
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 20px 16px 12px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── KPI CARDS ──────────────────────────────────────────── */
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-top: 4px solid #2471A3;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 80px; height: 80px;
    background: linear-gradient(135deg, rgba(36,113,163,0.05), transparent);
    border-radius: 0 0 0 80px;
}
.kpi-card.green { border-top-color: #27AE60; }
.kpi-card.red { border-top-color: #E74C3C; }
.kpi-card.gold { border-top-color: #F39C12; }
.kpi-card.purple { border-top-color: #9B59B6; }
.kpi-card.teal { border-top-color: #1ABC9C; }

.kpi-icon {
    font-size: 22px;
    margin-bottom: 8px;
    display: block;
}
.kpi-label {
    font-size: 10px;
    font-weight: 700;
    color: #95A5A6;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 26px;
    font-weight: 800;
    color: #1B3A6B;
    line-height: 1;
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}
.kpi-sub {
    font-size: 11px;
    color: #BDC3C7;
    font-weight: 400;
}
.kpi-delta-pos {
    font-size: 11px;
    color: #27AE60;
    font-weight: 600;
    margin-top: 4px;
}
.kpi-delta-neg {
    font-size: 11px;
    color: #E74C3C;
    font-weight: 600;
    margin-top: 4px;
}

/* ── PROGRESS BARS ──────────────────────────────────────── */
.progress-wrap {
    background: #EEF2F9;
    border-radius: 8px;
    height: 8px;
    overflow: hidden;
    margin-top: 10px;
}
.progress-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.8s ease;
}

/* ── METRIC ROW ─────────────────────────────────────────── */
.metric-row {
    background: white;
    border-radius: 12px;
    padding: 16px 20px;
    margin: 6px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.metric-label {
    font-size: 13px;
    color: #5D6D7E;
    font-weight: 500;
}
.metric-value {
    font-size: 15px;
    color: #1B3A6B;
    font-weight: 700;
}

/* ── BODY PADDING ───────────────────────────────────────── */
.dashboard-body {
    padding: 0 8px 32px 8px;
    background: #F0F4F8;
}

/* ── DIVIDER ────────────────────────────────────────────── */
.kat-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #D5E8F5, transparent);
    margin: 8px 16px;
}

/* ── CHART CONTAINER ────────────────────────────────────── */
.chart-container {
    background: white;
    border-radius: 14px;
    padding: 4px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin: 6px 0;
}

/* ── STATUS BADGE ───────────────────────────────────────── */
.status-badge {
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: inline-block;
}
.badge-green { background: #D5F5E3; color: #1E8449; }
.badge-gold  { background: #FEF9E7; color: #B7770D; }
.badge-red   { background: #FADBD8; color: #C0392B; }
.badge-blue  { background: #D6EAF8; color: #1A5276; }

/* ── MOBILE RESPONSIVE ──────────────────────────────────── */
@media (max-width: 768px) {
    .kat-header { padding: 12px 16px; flex-wrap: wrap; gap: 8px; }
    .kat-company-name { font-size: 16px; }
    .kat-logo-img { height: 36px; }
    .kpi-value { font-size: 20px; }
    .section-header { font-size: 11px; padding: 8px 14px; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# GOOGLE SHEETS CONNECTION
# ============================================================
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]
SHEET_ID = "1WySRL2qXuByeAXPVdEBk9nGWFKasn1vEvhP-yAYH2R4"
LOGO_URL = "https://drive.google.com/uc?export=view&id=18MShHQWnYrGtNFCKICQ7Ss166R101__7"

@st.cache_resource(ttl=600)
def get_client():
    creds_dict = json.loads(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(
        creds_dict, scopes=SCOPES)
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
                cleaned = str(val).replace(
                    '$','').replace(',','').replace(
                    '%','').replace('AED','').strip()
                return float(cleaned) if cleaned else default
            except:
                return default

        # Load SETTINGS
        settings = get_sheet('SETTINGS')
        def get_setting(row, col=1):
            try:
                return settings[row-1][col]
            except:
                return 0

        # Load PROCUREMENT
        proc_data = get_sheet('PROCUREMENT')

        # Load INVENTORY
        inv_data = get_sheet('INVENTORY')

        # Load LANDED COST
        lc_data = get_sheet('LANDED COST')

        # Load SALES
        sales_data = get_sheet('SALES')

        # Load CAPITAL LOG
        cap_data = get_sheet('CAPITAL LOG')

        # Load SHIPMENTS
        ship_data = get_sheet('SHIPMENTS')

        # Load REFERENCE
        ref_data = get_sheet('REFERENCE')

        # ── REFERENCE VALUES ──────────────────────────────
        usd_aed_rate = safe_float(ref_data[5][1] if len(ref_data) > 5 else 3.6725, 3.6725)
        bank_rate = safe_float(ref_data[6][1] if len(ref_data) > 6 else 3.67, 3.67)

        # ── SETTINGS VALUES ───────────────────────────────
        total_capital    = safe_float(get_setting(7))
        proc_spend       = safe_float(get_setting(8))
        total_revenue    = safe_float(get_setting(9))
        cash_balance     = safe_float(get_setting(10))
        inv_value_usd    = safe_float(get_setting(11))
        inv_value_aed    = safe_float(get_setting(12))
        biz_value        = safe_float(get_setting(13))
        roi_capital      = safe_float(get_setting(14))
        auction_budget   = safe_float(get_setting(18))
        spent_auctions   = safe_float(get_setting(19))
        avail_bidding    = safe_float(get_setting(20))
        pct_used         = safe_float(get_setting(21))
        pct_avail        = safe_float(get_setting(22))
        avg_days_ship    = safe_float(get_setting(31))
        avg_days_clear   = safe_float(get_setting(32))
        cost_efficiency  = safe_float(get_setting(33))
        freight_pct      = safe_float(get_setting(34))
        customs_pct      = safe_float(get_setting(35))
        avg_days_stock   = safe_float(get_setting(36))
        outstanding_pay  = safe_float(get_setting(40))
        break_even       = safe_float(get_setting(41))
        avg_landed_unit  = safe_float(get_setting(42))
        avg_sale_unit    = safe_float(get_setting(43))
        units_procured   = safe_float(get_setting(47))
        units_sold       = safe_float(get_setting(48))
        units_remaining  = safe_float(get_setting(49))
        stock_sold_pct   = safe_float(get_setting(50))
        turnover_ratio   = safe_float(get_setting(51))
        best_category    = get_setting(55)

        # ── LOT COUNTS ────────────────────────────────────
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

        # ── GROSS PROFIT ──────────────────────────────────
        gross_profit = 0
        margin_pct = 0
        roi_pct = 0

        if len(lc_data) > 5:
            total_landed_sum = 0
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

        # ── CAPITAL HISTORY ───────────────────────────────
        cap_history = []
        if len(cap_data) > 5:
            for row in cap_data[5:]:
                if len(row) > 4 and row[2]:
                    cap_history.append({
                        'Date': row[0],
                        'Type': row[1],
                        'Gross': safe_float(row[2]),
                        'Fee': safe_float(row[3]),
                        'Net': safe_float(row[4]),
                        'Running': safe_float(row[5]) if len(row) > 5 else 0,
                        'Notes': row[6] if len(row) > 6 else ''
                    })

        # ── INVENTORY TABLE ───────────────────────────────
        inv_table = []
        if len(inv_data) > 5:
            for row in inv_data[5:]:
                if len(row) > 8 and row[0]:
                    inv_table.append({
                        'Lot': row[0],
                        'Shipment': row[1],
                        'Category': row[2],
                        'Description': row[3],
                        'Procured': safe_float(row[5]),
                        'Sold': safe_float(row[6]),
                        'Remaining': safe_float(row[7]),
                        'Cost/Unit': safe_float(row[8]),
                        'Total Value': safe_float(row[10]),
                        'Status': row[14] if len(row) > 14 else ''
                    })

        # ── SALES TABLE ───────────────────────────────────
        sales_table = []
        if len(sales_data) > 5:
            for row in sales_data[5:]:
                if len(row) > 13 and row[1]:
                    sales_table.append({
                        'Sale ID': row[0],
                        'Date': row[1],
                        'Buyer': row[3],
                        'Lot': row[4],
                        'Qty Sold': safe_float(row[7]),
                        'Revenue AED': safe_float(row[12]),
                        'Revenue USD': safe_float(row[13]),
                        'Profit USD': safe_float(row[16]),
                        'Margin': safe_float(row[18]),
                        'Status': row[21] if len(row) > 21 else ''
                    })

        # ── COST BREAKDOWN ────────────────────────────────
        cost_breakdown = {
            'Purchase Cost': proc_spend,
            'Freight': 0,
            'Customs Duty': 0,
            'VAT': 0,
            'Agent Fees': 0,
            'Local Transport': 0,
            'US Logistics': 0
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

        # ── SHIPMENT SUMMARY ──────────────────────────────
        ship_table = []
        if len(ship_data) > 5:
            for row in ship_data[5:]:
                if len(row) > 7 and row[0]:
                    ship_table.append({
                        'Shipment ID': row[0],
                        'Date': row[1],
                        'Mode': row[2],
                        'Port': row[5],
                        'Type': row[6],
                        'Qty': safe_float(row[7]),
                        'Lots': safe_float(row[8]),
                        'Freight': safe_float(row[15]),
                        'CIF': safe_float(row[16]),
                        'Status': row[22] if len(row) > 22 else ''
                    })

        return {
            'usd_aed_rate': usd_aed_rate,
            'bank_rate': bank_rate,
            'total_capital': total_capital,
            'proc_spend': proc_spend,
            'total_revenue': total_revenue,
            'cash_balance': cash_balance,
            'inv_value_usd': inv_value_usd,
            'inv_value_aed': inv_value_aed,
            'biz_value': biz_value,
            'roi_capital': roi_capital,
            'auction_budget': auction_budget,
            'spent_auctions': spent_auctions,
            'avail_bidding': avail_bidding,
            'pct_used': pct_used,
            'pct_avail': pct_avail,
            'avg_days_ship': avg_days_ship,
            'avg_days_clear': avg_days_clear,
            'cost_efficiency': cost_efficiency,
            'freight_pct': freight_pct,
            'customs_pct': customs_pct,
            'avg_days_stock': avg_days_stock,
            'outstanding_pay': outstanding_pay,
            'break_even': break_even,
            'avg_landed_unit': avg_landed_unit,
            'avg_sale_unit': avg_sale_unit,
            'units_procured': units_procured,
            'units_sold': units_sold,
            'units_remaining': units_remaining,
            'stock_sold_pct': stock_sold_pct,
            'turnover_ratio': turnover_ratio,
            'best_category': best_category,
            'gross_profit': gross_profit,
            'margin_pct': margin_pct,
            'roi_pct': roi_pct,
            'lots_procured': lots_procured,
            'lots_sold': lots_sold,
            'lots_in_stock': lots_in_stock,
            'cap_history': cap_history,
            'inv_table': inv_table,
            'sales_table': sales_table,
            'cost_breakdown': cost_breakdown,
            'ship_table': ship_table,
            'timestamp': datetime.now().strftime("%d %b %Y  %H:%M")
        }
    except Exception as e:
        st.error(f"Data load error: {e}")
        return None

# ============================================================
# HELPERS
# ============================================================
def fmt_usd(val):
    if val is None: return "$0.00"
    return f"${val:,.2f}"

def fmt_aed(val):
    if val is None: return "AED 0.00"
    return f"AED {val:,.2f}"

def fmt_pct(val):
    if val is None: return "0.00%"
    return f"{val*100:.2f}%"

def fmt_num(val):
    if val is None: return "0"
    return f"{int(val):,}"

def health_color(val, good_thresh, warn_thresh, higher_is_better=True):
    if higher_is_better:
        if val >= good_thresh: return "green"
        if val >= warn_thresh: return "gold"
        return "red"
    else:
        if val <= good_thresh: return "green"
        if val <= warn_thresh: return "gold"
        return "red"

def kpi_card(icon, label, value, sub="", color="blue", delta=None):
    delta_html = ""
    if delta is not None:
        if delta >= 0:
            delta_html = f'<div class="kpi-delta-pos">▲ {delta}</div>'
        else:
            delta_html = f'<div class="kpi-delta-neg">▼ {abs(delta)}</div>'
    return f"""
    <div class="kpi-card {color}">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
        {delta_html}
    </div>
    """

def progress_bar(pct, color="#2471A3"):
    pct_clamped = min(max(pct * 100, 0), 100)
    return f"""
    <div class="progress-wrap">
        <div class="progress-fill"
             style="width:{pct_clamped:.1f}%;
                    background:linear-gradient(90deg,{color},{color}99);">
        </div>
    </div>
    """

def section_hdr(icon, title):
    st.markdown(
        f'<div class="section-header">'
        f'{icon}&nbsp;&nbsp;{title}'
        f'</div>',
        unsafe_allow_html=True
    )

def divider():
    st.markdown(
        '<div class="kat-divider"></div>',
        unsafe_allow_html=True
    )

# ============================================================
# LOAD DATA
# ============================================================
data = load_data()
if data is None:
    st.error("Unable to load data. Please check connection.")
    st.stop()

d = data

# ============================================================
# HEADER
# ============================================================
st.markdown(f"""
<div class="kat-header">
    <div class="kat-logo-area">
        <img src="{LOGO_URL}"
             class="kat-logo-img"
             onerror="this.style.display='none'"/>
        <div>
            <div class="kat-header-title">
                IT Asset Business System v2
            </div>
        </div>
    </div>
    <div class="kat-header-right">
        <div class="kat-company-name">
            Key Asset Technologies
        </div>
        <div class="kat-live-badge">🟢 LIVE DATA</div>
        <div class="kat-timestamp">
            Updated: {d['timestamp']}
        </div>
        <div class="kat-rate">
            USD/AED: {d['usd_aed_rate']:.4f}
            &nbsp;|&nbsp;
            Bank: {d['bank_rate']:.4f}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="dashboard-body">', unsafe_allow_html=True)

# ============================================================
# SECTION 1 — CAPITAL OVERVIEW
# ============================================================
section_hdr("💰", "CAPITAL OVERVIEW")

col1, col2, col3, col4 = st.columns(4)

with col1:
    clr = health_color(d['cash_balance'], 1000, 0)
    st.markdown(kpi_card(
        "🏦", "CASH BALANCE",
        fmt_usd(d['cash_balance']),
        "Capital - Spent + Revenue",
        clr
    ), unsafe_allow_html=True)

with col2:
    st.markdown(kpi_card(
        "💵", "TOTAL CAPITAL INJECTED",
        fmt_usd(d['total_capital']),
        "Total funds received",
        "blue"
    ), unsafe_allow_html=True)

with col3:
    clr = health_color(d['avail_bidding'], 2000, 500)
    st.markdown(kpi_card(
        "🎯", "AVAILABLE FOR BIDDING",
        fmt_usd(d['avail_bidding']),
        f"{fmt_pct(d['pct_avail'])} of budget free",
        clr
    ), unsafe_allow_html=True)

with col4:
    clr = health_color(d['pct_used'], 0.3, 0.7, higher_is_better=False)
    st.markdown(kpi_card(
        "📊", "CAPITAL DEPLOYED",
        fmt_pct(d['pct_used']),
        fmt_usd(d['spent_auctions']) + " spent",
        clr
    ), unsafe_allow_html=True)

# Capital utilization bar
st.markdown(f"""
<div style="margin:8px 0 4px 0;">
    <div style="display:flex;justify-content:space-between;
                font-size:11px;color:#7F8C8D;margin-bottom:4px;">
        <span>Capital Utilization</span>
        <span>{fmt_pct(d['pct_used'])} deployed of {fmt_usd(d['total_capital'])}</span>
    </div>
    {progress_bar(d['pct_used'],"#1B3A6B")}
</div>
""", unsafe_allow_html=True)

divider()

# ============================================================
# SECTION 2 — PROFITABILITY
# ============================================================
section_hdr("📈", "PROFITABILITY")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(kpi_card(
        "💰", "TOTAL REVENUE",
        fmt_usd(d['total_revenue']),
        "All sales collected",
        "green" if d['total_revenue'] > 0 else "gold"
    ), unsafe_allow_html=True)

with col2:
    clr = "green" if d['gross_profit'] > 0 else "red"
    st.markdown(kpi_card(
        "📈", "GROSS PROFIT",
        fmt_usd(d['gross_profit']),
        "Revenue minus landed cost",
        clr
    ), unsafe_allow_html=True)

with col3:
    clr = "green" if d['margin_pct'] > 0 else "red"
    st.markdown(kpi_card(
        "🎯", "GROSS MARGIN",
        fmt_pct(d['margin_pct']),
        "Profit / Revenue",
        clr
    ), unsafe_allow_html=True)

with col4:
    clr = "green" if d['roi_pct'] > 0 else "red"
    st.markdown(kpi_card(
        "🔄", "ROI",
        fmt_pct(d['roi_pct']),
        "Profit / Landed Cost",
        clr
    ), unsafe_allow_html=True)

with col5:
    clr = "green" if d['break_even'] >= 1 else "gold"
    st.markdown(kpi_card(
        "⚖️", "BREAK EVEN",
        fmt_pct(min(d['break_even'], 1)),
        "Revenue / Procurement",
        clr
    ), unsafe_allow_html=True)

# Break even progress
st.markdown(f"""
<div style="margin:8px 0 4px 0;">
    <div style="display:flex;justify-content:space-between;
                font-size:11px;color:#7F8C8D;margin-bottom:4px;">
        <span>Break Even Progress</span>
        <span>Gap: {fmt_usd(max(d['proc_spend']-d['total_revenue'],0))}</span>
    </div>
    {progress_bar(min(d['break_even'],1),"#27AE60")}
</div>
""", unsafe_allow_html=True)

divider()

# ============================================================
# SECTION 3 — INVENTORY HEALTH
# ============================================================
section_hdr("📦", "INVENTORY HEALTH")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(kpi_card(
        "📥", "LOTS PROCURED",
        fmt_num(d['lots_procured']),
        f"{fmt_num(d['units_procured'])} total units",
        "blue"
    ), unsafe_allow_html=True)

with col2:
    clr = "green" if d['lots_sold'] > 0 else "gold"
    st.markdown(kpi_card(
        "📤", "LOTS SOLD",
        fmt_num(d['lots_sold']),
        f"{fmt_num(d['units_sold'])} units | {fmt_pct(d['stock_sold_pct'])}",
        clr
    ), unsafe_allow_html=True)

with col3:
    st.markdown(kpi_card(
        "🏭", "LOTS IN STOCK",
        fmt_num(d['lots_in_stock']),
        f"{fmt_num(d['units_remaining'])} units remaining",
        "teal"
    ), unsafe_allow_html=True)

with col4:
    st.markdown(kpi_card(
        "💎", "INVENTORY VALUE",
        fmt_usd(d['inv_value_usd']),
        "At landed cost",
        "purple"
    ), unsafe_allow_html=True)

# Stock movement bar
sold_pct = d['stock_sold_pct']
st.markdown(f"""
<div style="margin:8px 0 4px 0;">
    <div style="display:flex;justify-content:space-between;
                font-size:11px;color:#7F8C8D;margin-bottom:4px;">
        <span style="color:#27AE60;font-weight:600;">
            ■ Sold: {fmt_num(d['units_sold'])} units
            ({fmt_pct(sold_pct)})
        </span>
        <span style="color:#E74C3C;font-weight:600;">
            ■ Remaining: {fmt_num(d['units_remaining'])} units
            ({fmt_pct(1-sold_pct)})
        </span>
    </div>
    <div style="display:flex;height:10px;
                border-radius:8px;overflow:hidden;gap:2px;">
        <div style="width:{sold_pct*100:.1f}%;
                    background:linear-gradient(90deg,#27AE60,#1E8449);
                    border-radius:8px 0 0 8px;min-width:2px;"></div>
        <div style="flex:1;
                    background:linear-gradient(90deg,#E74C3C,#C0392B);
                    border-radius:0 8px 8px 0;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

divider()

# ============================================================
# SECTION 4 — OPERATIONAL EFFICIENCY
# ============================================================
section_hdr("⚙️", "OPERATIONAL EFFICIENCY")

col1, col2, col3, col4 = st.columns(4)

with col1:
    clr = health_color(
        d['avg_days_ship'], 7, 14, higher_is_better=False)
    val = f"{d['avg_days_ship']:.1f} days" \
        if d['avg_days_ship'] > 0 else "—"
    st.markdown(kpi_card(
        "🚢", "AVG DAYS TO SHIP",
        val,
        "Purchase to shipment",
        clr
    ), unsafe_allow_html=True)

with col2:
    clr = health_color(
        d['avg_days_clear'], 5, 10, higher_is_better=False)
    val = f"{d['avg_days_clear']:.1f} days" \
        if d['avg_days_clear'] > 0 else "—"
    st.markdown(kpi_card(
        "🛃", "AVG DAYS TO CLEAR",
        val,
        "Arrival to cleared",
        clr
    ), unsafe_allow_html=True)

with col3:
    clr = health_color(
        d['cost_efficiency'], 1.2, 1.5, higher_is_better=False)
    val = f"{d['cost_efficiency']:.2f}x" \
        if d['cost_efficiency'] > 0 else "—"
    st.markdown(kpi_card(
        "📦", "COST EFFICIENCY",
        val,
        "Landed / Purchase cost",
        clr
    ), unsafe_allow_html=True)

with col4:
    clr = health_color(
        d['avg_days_stock'], 30, 60, higher_is_better=False)
    val = f"{d['avg_days_stock']:.0f} days" \
        if d['avg_days_stock'] > 0 else "—"
    st.markdown(kpi_card(
        "📅", "AVG DAYS IN STOCK",
        val,
        "Procurement to sale",
        clr
    ), unsafe_allow_html=True)

# Pipeline speed bar
total_pipeline = d['avg_days_ship'] + d['avg_days_clear']
pipeline_pct = min(total_pipeline / 30, 1) \
    if total_pipeline > 0 else 0
st.markdown(f"""
<div style="margin:8px 0 4px 0;">
    <div style="display:flex;justify-content:space-between;
                font-size:11px;color:#7F8C8D;margin-bottom:4px;">
        <span>Pipeline Speed</span>
        <span>Ship: {d['avg_days_ship']:.1f}d +
              Clear: {d['avg_days_clear']:.1f}d =
              {total_pipeline:.1f} days total</span>
    </div>
    {progress_bar(pipeline_pct,"#E74C3C")}
</div>
""", unsafe_allow_html=True)

divider()

# ============================================================
# SECTION 5 — SALES PERFORMANCE
# ============================================================
section_hdr("🏆", "SALES PERFORMANCE")

col1, col2, col3, col4 = st.columns(4)

with col1:
    clr = "green" if d['lots_sold'] > 0 else "gold"
    st.markdown(kpi_card(
        "🏷️", "LOTS SOLD",
        fmt_num(d['lots_sold']),
        f"of {fmt_num(d['lots_procured'])} procured",
        clr
    ), unsafe_allow_html=True)

with col2:
    rev_per_lot = d['total_revenue'] / d['lots_sold'] \
        if d['lots_sold'] > 0 else 0
    st.markdown(kpi_card(
        "💵", "REVENUE PER LOT",
        fmt_usd(rev_per_lot),
        "Average per deal",
        "green" if rev_per_lot > 0 else "gold"
    ), unsafe_allow_html=True)

with col3:
    profit_per_lot = d['gross_profit'] / d['lots_sold'] \
        if d['lots_sold'] > 0 else 0
    clr = "green" if profit_per_lot > 0 else "red"
    st.markdown(kpi_card(
        "📈", "PROFIT PER LOT",
        fmt_usd(profit_per_lot),
        "Average profit per deal",
        clr
    ), unsafe_allow_html=True)

with col4:
    best = d['best_category'] \
        if d['best_category'] else "No sales yet"
    st.markdown(kpi_card(
        "🏆", "BEST CATEGORY",
        best,
        "Highest margin category",
        "green" if d['best_category'] else "gold"
    ), unsafe_allow_html=True)

# Lots sold progress
lots_pct = d['lots_sold'] / d['lots_procured'] \
    if d['lots_procured'] > 0 else 0
st.markdown(f"""
<div style="margin:8px 0 4px 0;">
    <div style="display:flex;justify-content:space-between;
                font-size:11px;color:#7F8C8D;margin-bottom:4px;">
        <span>Lots Sold Progress</span>
        <span>{fmt_num(d['lots_sold'])} of
              {fmt_num(d['lots_procured'])} lots sold
              ({fmt_pct(lots_pct)})</span>
    </div>
    {progress_bar(lots_pct,"#2471A3")}
</div>
""", unsafe_allow_html=True)

divider()

# ============================================================
# SECTION 6 — CHARTS
# ============================================================
section_hdr("📊", "VISUAL ANALYTICS")

col1, col2 = st.columns(2)

# Cost Structure Pie Chart
with col1:
    st.markdown(
        '<div class="chart-container">',
        unsafe_allow_html=True
    )
    cb = d['cost_breakdown']
    labels = [k for k,v in cb.items() if v > 0]
    values = [v for v in cb.values() if v > 0]

    colors = [
        '#1B3A6B','#2471A3','#27AE60',
        '#E74C3C','#F39C12','#9B59B6','#1ABC9C'
    ]

    fig_pie = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker=dict(
            colors=colors[:len(labels)],
            line=dict(color='white', width=2)
        ),
        textfont=dict(
            size=11, color='white',
            family='Inter'
        ),
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>'
                      '$%{value:,.2f}<br>'
                      '%{percent}<extra></extra>'
    )])

    fig_pie.add_annotation(
        text=f"<b>Total</b><br>"
             f"${sum(values):,.0f}",
        x=0.5, y=0.5,
        font=dict(size=12, color='#1B3A6B',
                  family='Inter'),
        showarrow=False
    )

    fig_pie.update_layout(
        title=dict(
            text="<b>Cost Structure</b>",
            font=dict(size=14, color='#1B3A6B',
                      family='Inter'),
            x=0.5
        ),
        showlegend=True,
        legend=dict(
            font=dict(size=10, color='#1B3A6B'),
            orientation='v',
            x=1, y=0.5
        ),
        margin=dict(t=50, b=20, l=20, r=100),
        height=320,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    st.plotly_chart(
        fig_pie,
        use_container_width=True,
        config={'displayModeBar': False}
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Landed Cost Waterfall
with col2:
    st.markdown(
        '<div class="chart-container">',
        unsafe_allow_html=True
    )
    cb = d['cost_breakdown']
    total_landed = sum(cb.values())

    wf_labels = list(cb.keys()) + ['TOTAL LANDED']
    wf_values = list(cb.values()) + [0]
    measures = ['relative'] * len(cb) + ['total']

    fig_wf = go.Figure(go.Waterfall(
        name="Cost",
        orientation='v',
        measure=measures,
        x=wf_labels,
        y=wf_values,
        text=[f"${v:,.0f}" for v in wf_values],
        textposition='outside',
        textfont=dict(
            size=10, color='#1B3A6B',
            family='Inter'
        ),
        increasing=dict(
            marker=dict(color='#2471A3')
        ),
        totals=dict(
            marker=dict(color='#1B3A6B')
        ),
        connector=dict(
            line=dict(color='#E8ECF1',
                      width=1, dash='dot')
        )
    ))

    fig_wf.update_layout(
        title=dict(
            text="<b>Landed Cost Build-Up</b>",
            font=dict(size=14, color='#1B3A6B',
                      family='Inter'),
            x=0.5
        ),
        margin=dict(t=50, b=60, l=40, r=20),
        height=320,
        paper_bgcolor='white',
        plot_bgcolor='#FAFBFD',
        xaxis=dict(
            tickfont=dict(size=9, color='#5D6D7E'),
            tickangle=-20
        ),
        yaxis=dict(
            tickfont=dict(size=9),
            gridcolor='#E8ECF1',
            tickprefix='$'
        ),
        showlegend=False
    )
    st.plotly_chart(
        fig_wf,
        use_container_width=True,
        config={'displayModeBar': False}
    )
    st.markdown('</div>', unsafe_allow_html=True)

divider()

# ============================================================
# SECTION 7 — GAUGES
# ============================================================
section_hdr("🎯", "BUSINESS HEALTH GAUGES")

col1, col2, col3 = st.columns(3)

def gauge_chart(title, value, max_val,
                suffix="%", color="#2471A3"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        number=dict(
            suffix=suffix,
            font=dict(size=28, color='#1B3A6B',
                      family='Inter')
        ),
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(size=13, color='#1B3A6B',
                      family='Inter')
        ),
        gauge=dict(
            axis=dict(
                range=[0, max_val],
                tickfont=dict(size=9)
            ),
            bar=dict(color=color, thickness=0.3),
            bgcolor='#F0F4F8',
            borderwidth=0,
            steps=[
                dict(range=[0, max_val*0.33],
                     color='#FADBD8'),
                dict(range=[max_val*0.33, max_val*0.66],
                     color='#FEF9E7'),
                dict(range=[max_val*0.66, max_val],
                     color='#D5F5E3')
            ],
            threshold=dict(
                line=dict(color='#1B3A6B', width=2),
                thickness=0.75,
                value=value
            )
        )
    ))
    fig.update_layout(
        height=220,
        margin=dict(t=40, b=10, l=20, r=20),
        paper_bgcolor='white',
        font=dict(family='Inter')
    )
    return fig

with col1:
    st.markdown(
        '<div class="chart-container">',
        unsafe_allow_html=True
    )
    st.plotly_chart(
        gauge_chart(
            "Stock Sold %",
            d['stock_sold_pct'] * 100,
            100, "%", "#27AE60"
        ),
        use_container_width=True,
        config={'displayModeBar': False}
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown(
        '<div class="chart-container">',
        unsafe_allow_html=True
    )
    st.plotly_chart(
        gauge_chart(
            "Capital Deployed %",
            d['pct_used'] * 100,
            100, "%", "#2471A3"
        ),
        use_container_width=True,
        config={'displayModeBar': False}
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown(
        '<div class="chart-container">',
        unsafe_allow_html=True
    )
    st.plotly_chart(
        gauge_chart(
            "Break Even Progress",
            min(d['break_even'], 1) * 100,
            100, "%", "#F39C12"
        ),
        use_container_width=True,
        config={'displayModeBar': False}
    )
    st.markdown('</div>', unsafe_allow_html=True)

divider()

# ============================================================
# SECTION 8 — INVENTORY TABLE
# ============================================================
section_hdr("📋", "LIVE INVENTORY STATUS")

if d['inv_table']:
    df_inv = pd.DataFrame(d['inv_table'])

    def status_badge(status):
        if status == 'Sold Out':
            return '🟢 Sold Out'
        elif status == 'Partial':
            return '🟡 Partial'
        elif status == 'In Stock':
            return '🔵 In Stock'
        elif status == 'Pending Shipment':
            return '⚪ Pending'
        return status

    df_inv['Status'] = df_inv['Status'].apply(status_badge)
    df_inv['Cost/Unit'] = df_inv['Cost/Unit'].apply(
        lambda x: f"${x:,.2f}")
    df_inv['Total Value'] = df_inv['Total Value'].apply(
        lambda x: f"${x:,.2f}")
    df_inv['Procured'] = df_inv['Procured'].apply(
        lambda x: f"{int(x):,}")
    df_inv['Sold'] = df_inv['Sold'].apply(
        lambda x: f"{int(x):,}")
    df_inv['Remaining'] = df_inv['Remaining'].apply(
        lambda x: f"{int(x):,}")

    st.markdown(
        '<div class="chart-container" '
        'style="padding:16px;">',
        unsafe_allow_html=True
    )
    st.dataframe(
        df_inv[[
            'Lot','Category','Description',
            'Procured','Sold','Remaining',
            'Cost/Unit','Total Value','Status'
        ]],
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No inventory data yet. Enter lots in PROCUREMENT.")

divider()

# ============================================================
# SECTION 9 — RECENT SALES
# ============================================================
section_hdr("💵", "RECENT SALES")

if d['sales_table']:
    df_sales = pd.DataFrame(d['sales_table'])
    df_sales = df_sales.sort_values(
        'Date', ascending=False).head(10)

    df_sales['Revenue USD'] = df_sales['Revenue USD'].apply(
        lambda x: f"${x:,.2f}")
    df_sales['Profit USD'] = df_sales['Profit USD'].apply(
        lambda x: f"${x:,.2f}")
    df_sales['Margin'] = df_sales['Margin'].apply(
        lambda x: f"{x*100:.1f}%")
    df_sales['Qty Sold'] = df_sales['Qty Sold'].apply(
        lambda x: f"{int(x):,}")

    st.markdown(
        '<div class="chart-container" '
        'style="padding:16px;">',
        unsafe_allow_html=True
    )
    st.dataframe(
        df_sales[[
            'Date','Buyer','Lot','Qty Sold',
            'Revenue USD','Profit USD','Margin','Status'
        ]],
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No sales recorded yet.")

divider()

# ============================================================
# SECTION 10 — CAPITAL INJECTION HISTORY
# ============================================================
section_hdr("🏦", "CAPITAL INJECTION HISTORY")

if d['cap_history']:
    df_cap = pd.DataFrame(d['cap_history'])
    df_cap['Gross'] = df_cap['Gross'].apply(
        lambda x: f"${x:,.2f}")
    df_cap['Fee'] = df_cap['Fee'].apply(
        lambda x: f"${x:,.2f}")
    df_cap['Net'] = df_cap['Net'].apply(
        lambda x: f"${x:,.2f}")
    df_cap['Running'] = df_cap['Running'].apply(
        lambda x: f"${x:,.2f}")

    st.markdown(
        '<div class="chart-container" '
        'style="padding:16px;">',
        unsafe_allow_html=True
    )
    st.dataframe(
        df_cap[[
            'Date','Type','Gross','Fee','Net',
            'Running','Notes'
        ]],
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info(
        "No capital injections yet. "
        "Add entries in CAPITAL LOG."
    )

divider()

# ============================================================
# SECTION 11 — SHIPMENT TRACKER
# ============================================================
section_hdr("🚢", "SHIPMENT TRACKER")

if d['ship_table']:
    df_ship = pd.DataFrame(d['ship_table'])
    df_ship['Freight'] = df_ship['Freight'].apply(
        lambda x: f"${x:,.2f}")
    df_ship['CIF'] = df_ship['CIF'].apply(
        lambda x: f"${x:,.2f}")
    df_ship['Qty'] = df_ship['Qty'].apply(
        lambda x: f"{int(x):,}")
    df_ship['Lots'] = df_ship['Lots'].apply(
        lambda x: f"{int(x):,}")

    st.markdown(
        '<div class="chart-container" '
        'style="padding:16px;">',
        unsafe_allow_html=True
    )
    st.dataframe(
        df_ship[[
            'Shipment ID','Date','Mode',
            'Port','Type','Lots','Qty',
            'Freight','CIF','Status'
        ]],
        use_container_width=True,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info(
        "No shipments yet. "
        "Add entries in SHIPMENTS."
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown(f"""
<div style="
    background:linear-gradient(135deg,#0A1628,#1B3A6B);
    padding:20px 32px;
    margin-top:20px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    border-radius:12px;
">
    <div style="color:rgba(255,255,255,0.5);font-size:11px;">
        Key Asset Technologies &copy; 2025
        &nbsp;|&nbsp;
        IT Asset Business System v2
    </div>
    <div style="color:rgba(255,255,255,0.5);font-size:11px;">
        Data refreshes every 10 minutes
        &nbsp;|&nbsp;
        Last updated: {d['timestamp']}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
