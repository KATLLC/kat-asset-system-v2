import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.graph_objects as go
import plotly.express as px

# ==========================================
# HI-TECH EXECUTIVE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="KAT COMMAND CENTER",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ADVANCED CSS FOR MIDNIGHT GLASS LOOK
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Glassmorphism Card Style */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(5px);
        transition: transform 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(0, 255, 255, 0.3);
    }

    /* Custom Header Styling */
    .exec-header {
        font-family: 'Orbitron', sans-serif;
        color: #00D4FF;
        text-align: center;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 0px;
    }
    
    .pulse-bar {
        background: rgba(0, 212, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        font-size: 14px;
        color: #00D4FF;
        border: 1px solid #00D4FF;
        margin-bottom: 25px;
    }
    
    /* Hide Streamlit elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# DATA ENGINE
# ==========================================
def get_google_sheet_data():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keymap(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet_id = "1WySRL2qXuByeAXPVdEBk9nGWFKasn1vEvhP-yAYH2R4"
        return client.open_by_key(sheet_id)
    except Exception as e:
        st.error(f"🔴 SYSTEM CRITICAL: Connection Error. Check Secrets. {e}")
        return None

# ==========================================
# CORE DASHBOARD LOGIC
# ==========================================
def main():
    # --- HEADER ---
    st.markdown('<h1 class="exec-header">🌌 KAT COMMAND CENTER v2</h1>', unsafe_allow_html=True)
    
    workbook = get_google_sheet_data()
    if workbook is None:
        st.stop()

    # Fetch Data
    procurement = pd.DataFrame(workbook.worksheet("PROCUREMENT").get_all_records())
    sales = pd.DataFrame(workbook.worksheet("SALES").get_all_records())
    inventory = pd.DataFrame(workbook.worksheet("INVENTORY").get_all_records())
    settings = workbook.worksheet("SETTINGS").get_all_values()
    reference = workbook.worksheet("REFERENCE").get_all_values()

    # Live Currency Rate
    try:
        usd_aed_rate = float(reference[0][2]) 
    except:
        usd_aed_rate = 3.6725

    # --- TOP PULSE BAR ---
    st.markdown(f'<div class="pulse-bar">📡 SYSTEM ONLINE | LIVE USD/AED RATE: {usd_aed_rate} | FISCAL YEAR: 2026 | DATA REFRESH: ACTIVE</div>', unsafe_allow_html=True)

    # ==========================================
    # SIDEBAR FILTERS
    # ==========================================
    st.sidebar.markdown("### ⚙️ COMMAND FILTERS")
    all_categories = procurement['Asset Category'].unique().tolist() if not procurement.empty else ["All"]
    selected_cat = st.sidebar.selectbox("Filter by Asset Category", ["All"] + all_categories)

    # Apply Filtering
    if selected_cat != "All":
        proc_filtered = procurement[procurement['Asset Category'] == selected_cat]
        sales_filtered = sales[sales['Asset Category'] == selected_cat]
        inv_filtered = inventory[inventory['Asset Category'] == selected_cat]
    else:
        proc_filtered, sales_filtered, inv_filtered = procurement, sales, inventory

    # ==========================================
    # KPI CALCULATIONS
    # ==========================================
    # Row 1: Bottom Line
    total_rev_usd = sales_filtered['Total Revenue USD'].sum() if not sales_filtered.empty else 0
    total_rev_aed = total_rev_usd * usd_aed_rate
    gross_profit_usd = sales_filtered['Gross Profit USD'].sum() if not sales_filtered.empty else 0
    net_margin = (gross_profit_usd / total_rev_usd * 100) if total_rev_usd != 0 else 0
    
    # Use procurement cost for ROI
    total_cost_usd = proc_filtered['Total Procurement Cost'].sum() if not proc_filtered.empty else 1
    roi = (gross_profit_usd / total_cost_usd * 100)

    # Row 2: Cash Position (Settings)
    try:
        cap_in = float(settings[18][1]) # B19
        proc_spend = float(settings[19][1]) # B20
        cash_bal = float(settings[21][1]) # B22
        buying_power = float(settings[30][1]) # B31
    except:
        cap_in, proc_spend, cash_bal, buying_power = 0, 0, 0, 0

    # Row 3: Stock Health
    units_procured = proc_filtered['Qty'].sum() if not proc_filtered.empty else 0
    units_sold = sales_filtered['Qty Sold'].sum() if not sales_filtered.empty else 0
    units_rem = inv_filtered['Qty Remaining'].sum() if not inv_filtered.empty else 0
    inv_val_usd = inv_filtered['Total Landed Value USD'].sum() if not inv_filtered.empty else 0
    inv_val_aed = inv_val_usd * usd_aed_rate

    # ==========================================
    # VISUAL LAYOUT
    # ==========================================
    
    # SECTION 1: THE BOTTOM LINE (Neon Emerald/Blue)
    st.markdown("### 💰 Financial Performance")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Revenue USD", f"${total_rev_usd:,.0f}")
    c2.metric("Total Revenue AED", f"AED {total_rev_aed:,.0f}")
    c3.metric("Gross Profit USD", f"${gross_profit_usd:,.0f}", delta=f"{net_margin:.1f}% Margin")
    c4.metric("Net Margin", f"{net_margin:.2f}%")
    c5.metric("System ROI", f"{roi:.2f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # SECTION 2: CASH POSITION (Electric Blue/Amber)
    st.markdown("### 💵 Capital Command")
    c6, c7, c8, c9 = st.columns(4)
    c6.metric("Total Capital In", f"${cap_in:,.0f}")
    c7.metric("Buying Power", f"${buying_power:,.0f}")
    c8.metric("Procurement Spend", f"${proc_spend:,.0f}")
    c9.metric("Net Cash Balance", f"${cash_bal:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # SECTION 3: STOCK HEALTH (Amber/Silver)
    st.markdown("### 📦 Inventory Intelligence")
    c10, c11, c12, c13, c14 = st.columns(5)
    c10.metric("Units Procured", f"{units_procured:,.0f}")
    c11.metric("Units Sold", f"{units_sold:,.0f}")
    c12.metric("Units Remaining", f"{units_rem:,.0f}")
    c13.metric("Inv Value USD", f"${inv_val_usd:,.0f}")
    c14.metric("Inv Value AED", f"AED {inv_val_aed:,.0f}")

    st.markdown("---")

    # ==========================================
    # EXECUTIVE VISUALS
    # ==========================================
    st.markdown("### 📊 Executive Intelligence")
    v1, v2 = st.columns([1, 1])

    with v1:
        # BUDGET BURN GAUGE
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = proc_spend,
            title = {'text': "Capital Utilization (USD)", 'font': {'color': "#00D4FF", 'size': 20}},
            gauge = {
                'axis': {'range': [None, cap_in], 'tickcolor': "white"},
                'bar': {'color': "#00D4FF"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#00D4FF",
                'steps': [
                    {'range': [0, cap_in*0.7], 'color': "rgba(0, 255, 0, 0.1)"},
                    {'range': [cap_in*0.7, cap_in*0.9], 'color': "rgba(255, 255, 0, 0.1)"},
                    {'range': [cap_in*0.9, cap_in], 'color': "rgba(255, 0, 0, 0.1)"}
                ]
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white"},
            height=350, margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with v2:
        # STOCK DISTRIBUTION DONUT
        fig_donut = px.pie(
            values=[units_sold, units_rem], 
            names=["SOLD", "IN STOCK"],
            hole=0.7,
            color_discrete_sequence=["#00FFC8", "#FFD700"],
            title="Global Stock Status"
        )
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': "white"},
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # ==========================================
    # LOT LEVEL DRILL-DOWN
    # ==========================================
    st.markdown("### 📑 Lot Intelligence Matrix")
    if not inv_filtered.empty:
        # Professional Styling for Table
        cols_to_show = ['Lot Number', 'Asset Category', 'Qty Remaining', 'Landed Cost Per Unit USD', 'Landed Cost Per Unit AED']
        df_display = inv_filtered[cols_to_show]
        st.dataframe(df_display, use_container_width=True)
    else:
        st.info("No active lots found for this selection.")

    # FOOTER
    st.markdown("---")
    st.markdown(f'<div style="text-align: center; color: #666; font-size: 12px;">KAT ASSET TRADING v2 | SECURITY LEVEL: EXECUTIVE | LAST UPDATED: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
