# ============================================================
#  Customer Food Product & Preference Analysis Dashboard
#  Author  : Kavana Shree V
#  Dataset : Swiggy Food Delivery (50 000 orders)
# ============================================================

import os, warnings, zipfile
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🍽️ Food Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# GLOBAL CSS — Vibrant multi-color theme
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800;900&display=swap');

/* ── root & body ── */
html, body, [class*="css"], .stApp {
    font-family: 'Poppins', sans-serif !important;
    background: #0a0a0f !important;
    color: #f0f0f5 !important;
}

/* ── animated gradient background ── */
.stApp {
    background: linear-gradient(135deg,
        #0a0a0f 0%,
        #0d0d1a 25%,
        #0a0f1a 50%,
        #0d0a1a 75%,
        #0a0a0f 100%) !important;
    min-height: 100vh;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,
        #0d0d1f 0%,
        #110d2e 30%,
        #0d1a2e 60%,
        #0a1a1a 100%) !important;
    border-right: 2px solid rgba(255,100,100,0.2) !important;
}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #f0f0f5 !important;
}

/* ── sidebar nav buttons ── */
div[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    padding: 8px 14px !important;
    margin: 3px 0 !important;
    display: block !important;
    cursor: pointer !important;
    transition: all 0.3s !important;
    font-size: 0.88rem !important;
    color: #f0f0f5 !important;
}
div[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,100,100,0.2) !important;
    border-color: rgba(255,100,100,0.5) !important;
    transform: translateX(4px) !important;
}

/* ── KPI metric cards ── */
[data-testid="metric-container"] {
    border-radius: 16px !important;
    padding: 18px 20px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    backdrop-filter: blur(10px) !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.9rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: rgba(255,255,255,0.75) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* ── hero banner ── */
.hero-banner {
    background: linear-gradient(135deg,
        #ff4757 0%, #ff6b35 20%, #ffa502 40%,
        #2ed573 60%, #1e90ff 80%, #a55eea 100%);
    border-radius: 20px;
    padding: 40px 50px;
    text-align: center;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute; inset: 0;
    background: rgba(0,0,0,0.45);
    border-radius: 20px;
}
.hero-title {
    position: relative;
    font-size: 2.8rem;
    font-weight: 900;
    color: #ffffff;
    margin: 0;
    text-shadow: 0 2px 20px rgba(0,0,0,0.5);
    letter-spacing: -0.5px;
}
.hero-subtitle {
    position: relative;
    font-size: 1.05rem;
    color: rgba(255,255,255,0.88);
    margin-top: 8px;
    font-weight: 400;
}

/* ── section headers ── */
.sec-header {
    font-size: 1.4rem;
    font-weight: 800;
    margin: 10px 0 16px 0;
    padding: 10px 18px;
    border-radius: 10px;
    display: inline-block;
}
.sec-red    { background: linear-gradient(90deg,#ff4757,#ff6b6b); color:#fff; }
.sec-orange { background: linear-gradient(90deg,#ff6b35,#ffa502); color:#fff; }
.sec-green  { background: linear-gradient(90deg,#2ed573,#1abc9c); color:#fff; }
.sec-blue   { background: linear-gradient(90deg,#1e90ff,#00cec9); color:#fff; }
.sec-purple { background: linear-gradient(90deg,#a55eea,#6c5ce7); color:#fff; }
.sec-pink   { background: linear-gradient(90deg,#fd79a8,#e84393); color:#fff; }
.sec-gold   { background: linear-gradient(90deg,#fdcb6e,#e17055); color:#fff; }
.sec-teal   { background: linear-gradient(90deg,#00b894,#00cec9); color:#fff; }

/* ── nav pill bar (top) ── */
.nav-bar {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 24px;
}
.nav-pill {
    padding: 8px 20px;
    border-radius: 30px;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    border: 2px solid transparent;
    transition: all 0.3s;
    text-decoration: none;
    color: white !important;
}

/* ── divider ── */
.color-divider {
    height: 3px;
    background: linear-gradient(90deg,
        #ff4757,#ff6b35,#ffa502,#2ed573,#1e90ff,#a55eea,#fd79a8);
    border-radius: 3px;
    margin: 20px 0;
}

/* ── chart cards ── */
.chart-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 4px;
    margin-bottom: 8px;
}

/* ── info chip ── */
.chip {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 3px;
}
.chip-red    { background:rgba(255,71,87,0.2);  color:#ff4757; border:1px solid #ff4757; }
.chip-orange { background:rgba(255,165,2,0.2);  color:#ffa502; border:1px solid #ffa502; }
.chip-green  { background:rgba(46,213,115,0.2); color:#2ed573; border:1px solid #2ed573; }
.chip-blue   { background:rgba(30,144,255,0.2); color:#1e90ff; border:1px solid #1e90ff; }
.chip-purple { background:rgba(165,94,234,0.2); color:#a55eea; border:1px solid #a55eea; }

/* ── streamlit container bg ── */
.block-container { padding: 1.5rem 2rem 3rem 2rem !important; }

/* ── multiselect tags — solid vivid red, white text ── */
[data-baseweb="tag"] {
    background: #e02020 !important;
    color: #ffffff !important;
    border: 1px solid #ff4757 !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
}
[data-baseweb="tag"] span { color: #ffffff !important; }
[data-baseweb="tag"] svg  { fill: #ffffff !important; }

/* ── multiselect input box ── */
[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,71,87,0.5) !important;
    border-radius: 8px !important;
}

/* ── dropdown list ── */
[data-baseweb="menu"] {
    background: #1a0a1e !important;
    border: 1px solid rgba(255,71,87,0.3) !important;
    border-radius: 8px !important;
}
[role="option"] { background: transparent !important; color: #f0f0f5 !important; }
[role="option"]:hover, [aria-selected="true"] {
    background: rgba(255,71,87,0.3) !important;
    color: #ffffff !important;
}

/* ── slider track ── */
[data-testid="stSlider"] [class*="thumb"] { background: #ff4757 !important; }

hr { border-color: rgba(255,255,255,0.08) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# COLOUR PALETTES
# ─────────────────────────────────────────────────────────────
RAINBOW   = ["#ff4757","#ff6b35","#ffa502","#2ed573","#1e90ff",
             "#a55eea","#fd79a8","#00cec9","#fdcb6e","#e84393",
             "#6c5ce7","#00b894","#e17055","#74b9ff","#55efc4"]
WARM      = ["#ff4757","#ff6b35","#ffa502","#fdcb6e","#e17055",
             "#fd79a8","#e84393","#d63031","#ff7675","#fab1a0"]
COOL      = ["#1e90ff","#00cec9","#a55eea","#6c5ce7","#74b9ff",
             "#55efc4","#00b894","#0984e3","#81ecec","#b2bec3"]
GREEN_SEQ = ["#004d00","#006600","#008000","#1abc9c","#2ed573",
             "#55efc4","#a8e6cf","#d4f1da"]
RED_SEQ   = ["#4d0000","#800000","#c0392b","#e74c3c","#ff4757",
             "#ff6b6b","#ff9999","#ffcccc"]
ORANGE_SEQ= ["#4d1f00","#7d3200","#b44700","#e17055","#ff6b35",
             "#ffa502","#fdcb6e","#fff3cc"]
PURPLE_SEQ= ["#1a0033","#350067","#5f0099","#8e44ad","#a55eea",
             "#c39bd3","#d7bde2","#f0e6ff"]
BLUE_SEQ  = ["#001a4d","#003399","#0056b3","#0984e3","#1e90ff",
             "#74b9ff","#a8d8ea","#dff9fb"]

# chart bg
BG = "#0d0d1a"

def ct(fig, h=430):
    """Apply common dark theme to plotly figure."""
    fig.update_layout(
        paper_bgcolor=BG,
        plot_bgcolor="#111126",
        font=dict(color="#f0f0f5", family="Poppins, sans-serif", size=12),
        height=h,
        margin=dict(l=20, r=20, t=48, b=20),
        legend=dict(bgcolor="rgba(255,255,255,0.05)",
                    bordercolor="rgba(255,255,255,0.1)",
                    borderwidth=1),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
        title_font=dict(size=15, color="#ffffff"),
    )
    return fig

# KPI card background gradients
KPI_GRADS = [
    "linear-gradient(135deg,#ff4757 0%,#c0392b 100%)",
    "linear-gradient(135deg,#ff6b35 0%,#e17055 100%)",
    "linear-gradient(135deg,#ffa502 0%,#fdcb6e 100%)",
    "linear-gradient(135deg,#2ed573 0%,#00b894 100%)",
    "linear-gradient(135deg,#1e90ff 0%,#0984e3 100%)",
    "linear-gradient(135deg,#a55eea 0%,#6c5ce7 100%)",
    "linear-gradient(135deg,#fd79a8 0%,#e84393 100%)",
    "linear-gradient(135deg,#00cec9 0%,#00b894 100%)",
]
KPI_ICONS = ["🛒","👥","💵","💰","🧾","📦","⭐","🔁"]

def kpi_card(col, icon, label, value, grad):
    col.markdown(f"""
    <div style="background:{grad};border-radius:16px;padding:20px 18px;
                border:1px solid rgba(255,255,255,0.15);margin-bottom:6px;">
        <div style="font-size:1.9rem;margin-bottom:4px;">{icon}</div>
        <div style="font-size:0.72rem;font-weight:700;color:rgba(255,255,255,0.8);
                    text-transform:uppercase;letter-spacing:1px;">{label}</div>
        <div style="font-size:1.65rem;font-weight:900;color:#fff;margin-top:4px;">{value}</div>
    </div>""", unsafe_allow_html=True)

def divider():
    st.markdown('<div class="color-divider"></div>', unsafe_allow_html=True)

def section(text, style="sec-red"):
    st.markdown(f'<div class="{style} sec-header">{text}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DATA LOADING & CLEANING
# ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="⏳  Loading dataset …")
def load_data():
    zip_path  = "archive (2).zip"
    csv_name  = "swiggy_food_delivery_50000.csv"
    extracted = os.path.join("archive_extracted", csv_name)

    if os.path.exists(extracted):
        df = pd.read_csv(extracted)
    elif os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, "r") as z:
            with z.open(csv_name) as f:
                df = pd.read_csv(f)
    else:
        st.error("Dataset not found. Place 'archive (2).zip' in the same folder.")
        st.stop()

    df["Order_Date"]    = pd.to_datetime(df["Order_Date"],    errors="coerce")
    df["Delivery_Date"] = pd.to_datetime(df["Delivery_Date"], errors="coerce")
    df["Order_Time"]    = pd.to_datetime(df["Order_Time"],    format="%H:%M", errors="coerce")

    df["Hour"]      = df["Order_Time"].dt.hour
    df["Weekday"]   = df["Order_Date"].dt.day_name()
    df["Month"]     = df["Order_Date"].dt.month_name()
    df["Month_Num"] = df["Order_Date"].dt.month
    df["Year"]      = df["Order_Date"].dt.year
    df["IsWeekend"] = df["Order_Date"].dt.dayofweek >= 5

    def season(m):
        return ("Winter" if m in [12,1,2] else
                "Spring" if m in [3,4,5]  else
                "Summer" if m in [6,7,8]  else "Autumn")
    df["Season"] = df["Month_Num"].apply(season)

    def tod(h):
        if pd.isna(h): return "Unknown"
        return ("Morning" if 5<=h<12 else "Afternoon" if 12<=h<17
                else "Evening" if 17<=h<21 else "Night")
    df["TimeOfDay"] = df["Hour"].apply(tod)

    df["HasDiscount"] = df["Discount"] > 0
    df["ValueSegment"] = pd.cut(
        df["Order_Value"],
        bins=[0,200,400,700,1200,9999],
        labels=["<₹200","₹200-400","₹400-700","₹700-1200",">₹1200"]
    )

    cust_spend = df.groupby("Customer_ID")["Net_Revenue"].sum()
    q1, q3 = cust_spend.quantile(0.25), cust_spend.quantile(0.75)
    df["CustomerSegment"] = df["Customer_ID"].map(
        cust_spend.apply(lambda v: "Bronze" if v<=q1 else ("Silver" if v<=q3 else "Gold"))
    )
    return df

df_raw = load_data()

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:18px 0 10px 0;">
        <div style="font-size:3rem;">🍽️</div>
        <div style="font-size:1.15rem;font-weight:800;color:#ff4757;">Food Analytics</div>
        <div style="font-size:0.72rem;color:rgba(255,255,255,0.5);margin-top:2px;">
            by Kavana Shree V
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="color-divider"></div>', unsafe_allow_html=True)

    st.markdown("### 🗺️ City")
    all_cities = sorted(df_raw["City"].unique())
    sel_cities = st.multiselect("", all_cities, default=all_cities, key="city_f",
                                 label_visibility="collapsed")

    st.markdown("### 📋 Order Status")
    all_status = sorted(df_raw["Order_Status"].unique())
    sel_status = st.multiselect("", all_status, default=["Delivered"], key="stat_f",
                                 label_visibility="collapsed")

    st.markdown("### 🍕 Food Category")
    all_cats = sorted(df_raw["Food_Category"].unique())
    sel_cats = st.multiselect("", all_cats, default=all_cats, key="cat_f",
                               label_visibility="collapsed")

    st.markdown("### 📅 Date Range")
    mn, mx = df_raw["Order_Date"].min().date(), df_raw["Order_Date"].max().date()
    dr = st.date_input("", value=(mn, mx), min_value=mn, max_value=mx,
                        key="date_f", label_visibility="collapsed")

    st.markdown('<div class="color-divider"></div>', unsafe_allow_html=True)

    st.markdown("### 🧭 Navigate")
    page = st.radio("", [
        "🏠 Overview & KPIs",
        "🍽️ Food Preferences",
        "⏰ Time Analysis",
        "👥 Customer Behaviour",
        "🏪 Restaurant & City",
        "💰 Discount Behaviour",
        "🚴 Delivery Performance",
        "⭐ Rating Analysis",
    ], key="nav", label_visibility="collapsed")

    st.markdown('<div class="color-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;font-size:0.75rem;color:rgba(255,255,255,0.35);padding:6px 0;">
        📊 50,000 Orders · 8 Cities<br>15 Cuisines · 20 Categories
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_cities: df = df[df["City"].isin(sel_cities)]
if sel_status: df = df[df["Order_Status"].isin(sel_status)]
if sel_cats:   df = df[df["Food_Category"].isin(sel_cats)]
if len(dr)==2:
    df = df[(df["Order_Date"]>=pd.Timestamp(dr[0]))&(df["Order_Date"]<=pd.Timestamp(dr[1]))]


# ══════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW & KPIs
# ══════════════════════════════════════════════════════════════
if page == "🏠 Overview & KPIs":

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🍽️ Customer Food Preference Dashboard</div>
        <div class="hero-subtitle">
            Swiggy Food Delivery Analytics &nbsp;•&nbsp; 50,000 Orders &nbsp;•&nbsp;
            8 Cities &nbsp;•&nbsp; By Kavana Shree V
        </div>
    </div>""", unsafe_allow_html=True)

    # ── quick nav pills ──
    st.markdown("""
    <div class="nav-bar">
        <span class="nav-pill" style="background:#ff4757;">🏠 Overview</span>
        <span class="nav-pill" style="background:#ff6b35;">🍽️ Food</span>
        <span class="nav-pill" style="background:#ffa502;color:#222;">⏰ Time</span>
        <span class="nav-pill" style="background:#2ed573;color:#222;">👥 Customers</span>
        <span class="nav-pill" style="background:#1e90ff;">🏪 Restaurants</span>
        <span class="nav-pill" style="background:#a55eea;">💰 Discounts</span>
        <span class="nav-pill" style="background:#fd79a8;color:#222;">🚴 Delivery</span>
        <span class="nav-pill" style="background:#00cec9;color:#222;">⭐ Ratings</span>
    </div>
    <p style="text-align:center;font-size:0.78rem;color:rgba(255,255,255,0.4);margin-top:-10px;margin-bottom:20px;">
        ☝️ Use the left sidebar to navigate between sections
    </p>
    """, unsafe_allow_html=True)

    section("📊 Key Performance Indicators", "sec-red")

    cols = st.columns(4)
    vals = [
        ("Total Orders",    f"{len(df):,}"),
        ("Unique Customers",f"{df['Customer_ID'].nunique():,}"),
        ("Total Revenue",   f"₹{df['Order_Value'].sum()/1e6:.2f}M"),
        ("Net Revenue",     f"₹{df['Net_Revenue'].sum()/1e6:.2f}M"),
    ]
    for i,(lbl,val) in enumerate(vals):
        kpi_card(cols[i], KPI_ICONS[i], lbl, val, KPI_GRADS[i])

    cols2 = st.columns(4)
    vals2 = [
        ("Avg Order Value",    f"₹{df['Order_Value'].mean():.0f}"),
        ("Avg Qty / Order",    f"{df['Quantity'].mean():.2f}"),
        ("Avg Customer Rating",f"{df['Customer_Rating'].mean():.2f}" if df['Customer_Rating'].notna().any() else "N/A"),
        ("Repeat Customers",   f"{(df.groupby('Customer_ID')['Order_ID'].count()>1).sum():,}"),
    ]
    for i,(lbl,val) in enumerate(vals2):
        kpi_card(cols2[i], KPI_ICONS[i+4], lbl, val, KPI_GRADS[i+4])

    divider()
    section("📋 Data Quality & Order Status", "sec-orange")

    c1, c2, c3 = st.columns([1,1,1])

    with c1:
        status_df = df_raw["Order_Status"].value_counts().reset_index()
        status_df.columns = ["Status","Count"]
        fig = px.pie(status_df, names="Status", values="Count",
                     hole=0.58,
                     color_discrete_sequence=["#2ed573","#ff4757","#ffa502"],
                     title="Order Status Split")
        fig.update_traces(textinfo="percent+label",
                          marker=dict(line=dict(color=BG, width=3)))
        ct(fig, 380)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        pay_df = df_raw["Payment_Method"].value_counts().reset_index()
        pay_df.columns = ["Method","Count"]
        fig = px.pie(pay_df, names="Method", values="Count",
                     hole=0.58,
                     color_discrete_sequence=RAINBOW,
                     title="Payment Methods")
        fig.update_traces(textinfo="percent+label",
                          marker=dict(line=dict(color=BG, width=3)))
        ct(fig, 380)
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        dq = pd.DataFrame({
            "Metric" : ["Total Orders","Delivered","Cancelled","Delayed","Missing Rating","Duplicates"],
            "Value"  : [50000, 43953, 3487, 2560, 3487, 0],
            "Status" : ["info","good","bad","warn","warn","good"],
        })
        color_map = {"good":"#2ed573","bad":"#ff4757","warn":"#ffa502","info":"#1e90ff"}
        fig = go.Figure()
        for _, row in dq.iterrows():
            fig.add_trace(go.Bar(
                x=[row["Value"]], y=[row["Metric"]],
                orientation="h",
                marker_color=color_map[row["Status"]],
                text=f"{row['Value']:,}", textposition="outside",
                showlegend=False, name=row["Metric"]
            ))
        fig.update_layout(**{
            "paper_bgcolor":BG,"plot_bgcolor":"#111126",
            "font":dict(color="#f0f0f5",family="Poppins",size=11),
            "height":380,"margin":dict(l=20,r=60,t=48,b=20),
            "xaxis":dict(gridcolor="rgba(255,255,255,0.06)"),
            "yaxis":dict(gridcolor="rgba(255,255,255,0.06)"),
            "title":"Data Quality Summary",
            "title_font":dict(size=15,color="#ffffff"),
            "barmode":"overlay"
        })
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("📈 Monthly Order Trend", "sec-green")

    monthly = (df_raw.groupby(["Year","Month_Num"])
               .agg(Orders=("Order_ID","count"), Revenue=("Net_Revenue","sum"))
               .reset_index())
    monthly["Period"] = (monthly["Year"].astype(str) + "-" +
                         monthly["Month_Num"].astype(str).str.zfill(2))
    monthly = monthly.sort_values("Period")

    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(go.Bar(x=monthly["Period"], y=monthly["Orders"],
                         name="Orders", marker_color="#ff4757", opacity=0.85,
                         marker_line_color="rgba(0,0,0,0)"), secondary_y=False)
    fig.add_trace(go.Scatter(x=monthly["Period"], y=monthly["Revenue"],
                              name="Net Revenue", mode="lines+markers",
                              line=dict(color="#2ed573", width=3),
                              marker=dict(size=7, color="#2ed573",
                                          line=dict(color="#ffffff",width=1.5))),
                  secondary_y=True)
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor="#111126",
        font=dict(color="#f0f0f5",family="Poppins",size=12),
        height=420, margin=dict(l=20,r=20,t=50,b=40),
        title="Monthly Orders & Net Revenue (Full Dataset)",
        title_font=dict(size=15,color="#ffffff"),
        legend=dict(bgcolor="rgba(255,255,255,0.05)",bordercolor="rgba(255,255,255,0.1)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickangle=45),
    )
    fig.update_yaxes(title_text="Orders",    secondary_y=False, gridcolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(title_text="Revenue ₹", secondary_y=True,  gridcolor="rgba(255,255,255,0.06)")
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 2 — FOOD PREFERENCES
# ══════════════════════════════════════════════════════════════
elif page == "🍽️ Food Preferences":

    st.markdown("""<div class="hero-banner">
        <div class="hero-title">🍕 Food Preferences Analysis</div>
        <div class="hero-subtitle">Most popular categories, cuisines, order values & quantities</div>
    </div>""", unsafe_allow_html=True)

    section("🍕 Top Food Categories — Orders & Revenue", "sec-red")
    cat_agg = df.groupby("Food_Category").agg(
        Orders=("Order_ID","count"), Revenue=("Net_Revenue","sum"),
        AvgVal=("Order_Value","mean")
    ).sort_values("Orders").reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(cat_agg.sort_values("Orders"), y="Food_Category", x="Orders",
                     orientation="h", color="Orders",
                     color_continuous_scale=RED_SEQ, text="Orders",
                     title="Orders by Food Category")
        fig.update_traces(textposition="outside")
        ct(fig, 540)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(cat_agg.sort_values("Revenue"), y="Food_Category", x="Revenue",
                     orientation="h", color="Revenue",
                     color_continuous_scale=ORANGE_SEQ, text_auto=".2s",
                     title="Revenue by Food Category (₹)")
        ct(fig, 540)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🌍 Cuisine Rankings", "sec-orange")

    cui_agg = df.groupby("Cuisines").agg(
        Orders=("Order_ID","count"), Revenue=("Net_Revenue","sum")
    ).sort_values("Orders", ascending=False).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(cui_agg.sort_values("Orders"), y="Cuisines", x="Orders",
                     orientation="h", color="Orders",
                     color_continuous_scale=ORANGE_SEQ, text="Orders",
                     title="Orders by Cuisine")
        fig.update_traces(textposition="outside")
        ct(fig, 500)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.treemap(cui_agg, path=["Cuisines"], values="Revenue",
                          color="Revenue", color_continuous_scale=WARM,
                          title="Revenue Treemap — Cuisines")
        ct(fig, 500)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("💵 Order Value Distribution", "sec-green")

    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(df, x="Order_Value", nbins=60,
                           color_discrete_sequence=["#2ed573"],
                           title="Order Value Distribution (₹)")
        fig.add_vline(x=df["Order_Value"].mean(), line_color="#ff4757",
                      line_dash="dash",
                      annotation_text=f"Mean ₹{df['Order_Value'].mean():.0f}",
                      annotation_font_color="#ff4757")
        ct(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        seg_df = df.groupby("ValueSegment", observed=True)["Order_ID"].count().reset_index()
        seg_df.columns = ["Segment","Orders"]
        fig = px.pie(seg_df, names="Segment", values="Orders",
                     hole=0.55, color_discrete_sequence=RAINBOW,
                     title="Orders by Value Segment")
        fig.update_traces(textinfo="percent+label",
                          marker=dict(line=dict(color=BG, width=3)))
        ct(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("📦 Quantity Analysis", "sec-blue")

    c1, c2 = st.columns(2)
    with c1:
        q1 = df.groupby("Food_Category")["Quantity"].mean().sort_values().reset_index()
        fig = px.bar(q1, y="Food_Category", x="Quantity", orientation="h",
                     color="Quantity", color_continuous_scale=BLUE_SEQ,
                     title="Avg Quantity per Food Category")
        ct(fig, 500)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        q2 = df.groupby("Cuisines")["Quantity"].sum().sort_values().reset_index()
        fig = px.bar(q2, y="Cuisines", x="Quantity", orientation="h",
                     color="Quantity", color_continuous_scale=COOL,
                     title="Total Quantity Ordered by Cuisine")
        ct(fig, 500)
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 3 — TIME ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "⏰ Time Analysis":

    st.markdown("""<div class="hero-banner">
        <div class="hero-title">⏰ Time-Based Analysis</div>
        <div class="hero-subtitle">When do customers order? Hour · Day · Week · Month · Season</div>
    </div>""", unsafe_allow_html=True)

    section("🕐 Orders by Hour of Day", "sec-orange")
    hourly = df.groupby("Hour").agg(
        Orders=("Order_ID","count"), Revenue=("Net_Revenue","sum")
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(go.Bar(x=hourly["Hour"], y=hourly["Orders"],
                         name="Orders", marker_color="#ff6b35", opacity=0.9), secondary_y=False)
    fig.add_trace(go.Scatter(x=hourly["Hour"], y=hourly["Revenue"],
                              mode="lines+markers", name="Revenue",
                              line=dict(color="#2ed573",width=3),
                              marker=dict(size=7,color="#2ed573",
                                          line=dict(color="#fff",width=1.5))), secondary_y=True)
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor="#111126",
        font=dict(color="#f0f0f5",family="Poppins",size=12),
        height=430, margin=dict(l=20,r=20,t=50,b=30),
        title="Orders & Revenue by Hour of Day",
        title_font=dict(size=15,color="#fff"),
        legend=dict(bgcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", tickvals=list(range(0,24))),
    )
    fig.update_yaxes(title_text="Orders",    secondary_y=False, gridcolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(title_text="Revenue ₹", secondary_y=True,  gridcolor="rgba(255,255,255,0.06)")
    st.plotly_chart(fig, use_container_width=True)

    divider()
    c1, c2 = st.columns(2)
    with c1:
        section("🌅 Time of Day", "sec-green")
        tod_order = ["Morning","Afternoon","Evening","Night"]
        tod_colors = ["#ffa502","#ff6b35","#a55eea","#1e90ff"]
        tod_df = df.groupby("TimeOfDay")["Order_ID"].count().reset_index()
        tod_df.columns = ["TimeOfDay","Orders"]
        tod_df["TimeOfDay"] = pd.Categorical(tod_df["TimeOfDay"], tod_order, ordered=True)
        tod_df = tod_df.sort_values("TimeOfDay")
        fig = px.bar(tod_df, x="TimeOfDay", y="Orders",
                     color="TimeOfDay",
                     color_discrete_sequence=tod_colors,
                     title="Orders by Time of Day", text="Orders")
        fig.update_traces(textposition="outside")
        ct(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        section("📅 Weekday Pattern", "sec-blue")
        wd_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        wd_df = df.groupby("Weekday")["Order_ID"].count().reset_index()
        wd_df.columns = ["Weekday","Orders"]
        wd_df["Weekday"] = pd.Categorical(wd_df["Weekday"], wd_order, ordered=True)
        wd_df = wd_df.sort_values("Weekday")
        colors = ["#ff4757" if d in ["Saturday","Sunday"] else "#1e90ff"
                  for d in wd_df["Weekday"]]
        fig = go.Figure(go.Bar(x=wd_df["Weekday"], y=wd_df["Orders"],
                               marker_color=colors, text=wd_df["Orders"],
                               textposition="outside"))
        fig.update_layout(
            paper_bgcolor=BG, plot_bgcolor="#111126",
            font=dict(color="#f0f0f5",family="Poppins",size=12),
            height=400, margin=dict(l=20,r=20,t=50,b=30),
            title="Orders by Weekday (Red = Weekend)",
            title_font=dict(size=15,color="#fff"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
        )
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("📅 Monthly & Seasonal Trends", "sec-purple")

    c1, c2 = st.columns(2)
    with c1:
        mth = df.groupby(["Year","Month_Num","Month"]).agg(Orders=("Order_ID","count")).reset_index()
        mth["Period"] = mth["Year"].astype(str)+"-"+mth["Month_Num"].astype(str).str.zfill(2)
        mth = mth.sort_values("Period")
        fig = px.area(mth, x="Period", y="Orders",
                      title="Monthly Order Trend",
                      color_discrete_sequence=["#a55eea"])
        fig.update_traces(line_width=2.5, fillcolor="rgba(165,94,234,0.2)")
        ct(fig, 420)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        season_df = df.groupby("Season")["Order_ID"].count().reset_index()
        season_df.columns = ["Season","Orders"]
        fig = px.bar(season_df, x="Season", y="Orders",
                     color="Season",
                     color_discrete_map={"Winter":"#74b9ff","Spring":"#2ed573",
                                          "Summer":"#ffa502","Autumn":"#e17055"},
                     title="Orders by Season", text="Orders")
        fig.update_traces(textposition="outside")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🔥 Order Heatmap — Weekday × Hour", "sec-red")

    heat = df.groupby(["Weekday","Hour"])["Order_ID"].count().reset_index()
    heat.columns = ["Weekday","Hour","Orders"]
    wd_ord = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    heat_piv = heat.pivot(index="Weekday",columns="Hour",values="Orders").fillna(0)
    heat_piv = heat_piv.reindex(wd_ord)

    fig = px.imshow(heat_piv,
                    color_continuous_scale=["#0d0d1a","#4d1f00","#ff6b35","#ffa502","#2ed573"],
                    title="Heatmap: Weekday × Hour of Day",
                    labels=dict(x="Hour",y="Weekday",color="Orders"),
                    aspect="auto")
    ct(fig, 430)
    st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🍕 Food Category by Time of Day", "sec-gold")

    tod_food = df.groupby(["TimeOfDay","Food_Category"])["Order_ID"].count().reset_index()
    tod_food.columns = ["TimeOfDay","Food_Category","Orders"]
    fig = px.bar(tod_food, x="TimeOfDay", y="Orders", color="Food_Category",
                 color_discrete_sequence=RAINBOW,
                 title="Food Category Orders by Time of Day", barmode="stack",
                 category_orders={"TimeOfDay":["Morning","Afternoon","Evening","Night"]})
    ct(fig, 490)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 4 — CUSTOMER BEHAVIOUR
# ══════════════════════════════════════════════════════════════
elif page == "👥 Customer Behaviour":

    st.markdown("""<div class="hero-banner">
        <div class="hero-title">👥 Customer Behaviour Analysis</div>
        <div class="hero-subtitle">Repeat customers · Order frequency · Spending · Value segments</div>
    </div>""", unsafe_allow_html=True)

    cust_agg = df.groupby("Customer_ID").agg(
        TotalOrders   =("Order_ID","count"),
        TotalSpend    =("Order_Value","sum"),
        AvgSpend      =("Order_Value","mean"),
        TotalRevenue  =("Net_Revenue","sum"),
        AvgRating     =("Customer_Rating","mean"),
        FavCat        =("Food_Category", lambda x: x.mode()[0] if len(x)>0 else "Unknown"),
        FavCuisine    =("Cuisines",      lambda x: x.mode()[0] if len(x)>0 else "Unknown"),
        Segment       =("CustomerSegment",lambda x: x.mode()[0] if len(x)>0 else "Bronze")
    ).reset_index()

    repeat_mask = cust_agg["TotalOrders"] > 1
    repeat_pct  = repeat_mask.mean()*100

    cols = st.columns(4)
    kpi_card(cols[0],"👥","Total Customers",  f"{len(cust_agg):,}",         KPI_GRADS[0])
    kpi_card(cols[1],"🔁","Repeat Customers", f"{repeat_mask.sum():,}",      KPI_GRADS[1])
    kpi_card(cols[2],"📈","Repeat Rate",      f"{repeat_pct:.1f}%",          KPI_GRADS[2])
    kpi_card(cols[3],"💵","Avg Total Spend",  f"₹{cust_agg['TotalSpend'].mean():.0f}", KPI_GRADS[3])

    divider()
    section("📊 Order Frequency & Avg Spend", "sec-red")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(cust_agg, x="TotalOrders", nbins=12,
                           color_discrete_sequence=["#ff4757"],
                           title="Orders per Customer Distribution")
        fig.add_vline(x=cust_agg["TotalOrders"].mean(), line_color="#ffa502",
                      line_dash="dash",
                      annotation_text=f"Mean {cust_agg['TotalOrders'].mean():.1f}",
                      annotation_font_color="#ffa502")
        ct(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.histogram(cust_agg, x="AvgSpend", nbins=50,
                           color_discrete_sequence=["#a55eea"],
                           title="Avg Spend per Customer (₹)")
        ct(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("💎 Customer Value Segments", "sec-gold")
    c1, c2 = st.columns(2)
    with c1:
        seg_cnt = cust_agg["Segment"].value_counts().reset_index()
        seg_cnt.columns = ["Segment","Customers"]
        fig = px.pie(seg_cnt, names="Segment", values="Customers",
                     hole=0.58,
                     color="Segment",
                     color_discrete_map={"Gold":"#fdcb6e","Silver":"#b2bec3","Bronze":"#e17055"},
                     title="Customer Value Segments")
        fig.update_traces(textinfo="percent+label",
                          marker=dict(line=dict(color=BG,width=3)))
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        seg_sp = cust_agg.groupby("Segment")[["TotalSpend","AvgSpend"]].mean().reset_index()
        fig = px.bar(seg_sp, x="Segment", y=["TotalSpend","AvgSpend"],
                     barmode="group",
                     color_discrete_sequence=["#fdcb6e","#ff4757"],
                     title="Avg Total & Order Spend by Segment")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🍽️ Favourite Food & Cuisine", "sec-green")
    c1, c2 = st.columns(2)
    with c1:
        fav_cat = cust_agg["FavCat"].value_counts().reset_index()
        fav_cat.columns = ["Category","Customers"]
        fig = px.bar(fav_cat.sort_values("Customers"), y="Category", x="Customers",
                     orientation="h", color="Customers",
                     color_continuous_scale=GREEN_SEQ,
                     title="Most Preferred Food Category")
        ct(fig, 500)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fav_cui = cust_agg["FavCuisine"].value_counts().reset_index()
        fav_cui.columns = ["Cuisine","Customers"]
        fig = px.bar(fav_cui.sort_values("Customers"), y="Cuisine", x="Customers",
                     orientation="h", color="Customers",
                     color_continuous_scale=BLUE_SEQ,
                     title="Most Preferred Cuisine")
        ct(fig, 500)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("📈 RFM Scatter: Orders vs Total Spend", "sec-purple")
    sample = cust_agg.sample(min(2000,len(cust_agg)), random_state=42)
    fig = px.scatter(sample, x="TotalOrders", y="TotalSpend",
                     color="Segment", size="AvgSpend",
                     color_discrete_map={"Gold":"#fdcb6e","Silver":"#b2bec3","Bronze":"#e17055"},
                     title="Total Orders vs Total Spend per Customer (sample 2000)",
                     hover_data=["FavCat","FavCuisine"], opacity=0.75)
    ct(fig, 500)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 5 — RESTAURANT & CITY
# ══════════════════════════════════════════════════════════════
elif page == "🏪 Restaurant & City":

    st.markdown("""<div class="hero-banner">
        <div class="hero-title">🏪 Restaurant & Location Analysis</div>
        <div class="hero-subtitle">City demand · Restaurant rankings · Cuisine by location</div>
    </div>""", unsafe_allow_html=True)

    city_agg = df.groupby("City").agg(
        Orders   =("Order_ID","count"),
        Revenue  =("Net_Revenue","sum"),
        Customers=("Customer_ID","nunique"),
        AvgVal   =("Order_Value","mean"),
        AvgRating=("Customer_Rating","mean")
    ).reset_index().sort_values("Orders", ascending=False)

    section("🗺️ City-Wise Demand", "sec-blue")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(city_agg.sort_values("Orders"), y="City", x="Orders",
                     orientation="h", color="City",
                     color_discrete_sequence=RAINBOW,
                     title="Total Orders by City", text="Orders")
        fig.update_traces(textposition="outside")
        ct(fig, 450)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(city_agg, x="Orders", y="Revenue",
                         size="Customers", color="City", text="City",
                         color_discrete_sequence=RAINBOW,
                         title="City: Orders vs Revenue (bubble = customers)",
                         size_max=60)
        fig.update_traces(textposition="top center")
        ct(fig, 450)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🌍 Cuisine Preference by City", "sec-orange")

    city_cui = df.groupby(["City","Cuisines"])["Order_ID"].count().reset_index()
    city_cui.columns = ["City","Cuisines","Orders"]
    fig = px.bar(city_cui, x="City", y="Orders", color="Cuisines",
                 color_discrete_sequence=RAINBOW,
                 title="Cuisine Distribution by City", barmode="stack")
    ct(fig, 510)
    st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🏆 Top Restaurant Performance", "sec-red")

    rest_agg = df.groupby(["Restaurant_Name","City"]).agg(
        Orders   =("Order_ID","count"),
        Revenue  =("Net_Revenue","sum"),
        AvgRating=("Customer_Rating","mean"),
        AvgVal   =("Order_Value","mean")
    ).reset_index().sort_values("Orders", ascending=False)

    top_n = st.slider("Show Top N Restaurants", 5, 30, 15, key="rest_slider")
    top_rest = rest_agg.head(top_n)

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(top_rest.sort_values("Orders"), y="Restaurant_Name", x="Orders",
                     orientation="h", color="City",
                     color_discrete_sequence=RAINBOW,
                     title=f"Top {top_n} Restaurants — Orders")
        ct(fig, 560)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(top_rest, x="Orders", y="Revenue",
                         color="City", size="AvgVal",
                         hover_name="Restaurant_Name",
                         color_discrete_sequence=RAINBOW,
                         title="Restaurant Orders vs Revenue")
        ct(fig, 560)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("⭐ Avg Customer Rating by City", "sec-teal")
    fig = px.bar(city_agg.sort_values("AvgRating"), y="City", x="AvgRating",
                 orientation="h", color="City",
                 color_discrete_sequence=RAINBOW,
                 range_x=[3.5,5], text_auto=".2f",
                 title="Average Customer Rating by City")
    ct(fig, 380)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 6 — DISCOUNT BEHAVIOUR
# ══════════════════════════════════════════════════════════════
elif page == "💰 Discount Behaviour":

    st.markdown("""<div class="hero-banner">
        <div class="hero-title">💰 Discount Behaviour Analysis</div>
        <div class="hero-subtitle">Do discounts drive more orders, higher spend or repeat purchases?</div>
    </div>""", unsafe_allow_html=True)

    disc   = df[df["HasDiscount"]]
    nodisc = df[~df["HasDiscount"]]

    cols = st.columns(4)
    kpi_card(cols[0],"🎟️","Discounted Orders",    f"{len(disc):,}",                           KPI_GRADS[0])
    kpi_card(cols[1],"🚫","Non-Discounted Orders", f"{len(nodisc):,}",                         KPI_GRADS[1])
    kpi_card(cols[2],"💵","Avg Value w/ Discount", f"₹{disc['Order_Value'].mean():.0f}",       KPI_GRADS[4])
    kpi_card(cols[3],"💵","Avg Value w/o Discount",f"₹{nodisc['Order_Value'].mean():.0f}",     KPI_GRADS[5])

    divider()
    section("📊 Discount Impact on Value & Quantity", "sec-red")
    c1, c2 = st.columns(2)
    with c1:
        cmp = pd.DataFrame({
            "Group":["With Discount","No Discount"],
            "Avg Value":[disc["Order_Value"].mean(), nodisc["Order_Value"].mean()],
            "Avg Quantity":[disc["Quantity"].mean(), nodisc["Quantity"].mean()],
        })
        fig = px.bar(cmp, x="Group", y=["Avg Value","Avg Quantity"],
                     barmode="group",
                     color_discrete_sequence=["#ff4757","#2ed573"],
                     title="Avg Order Value & Quantity: Discount vs No Discount")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(df.sample(3000, random_state=1),
                         x="Discount", y="Order_Value",
                         color="HasDiscount",
                         color_discrete_map={True:"#ff4757",False:"#1e90ff"},
                         opacity=0.5,
                         title="Discount Amount vs Order Value (3000 sample)")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🔁 Discounts & Repeat Purchases", "sec-green")
    cust_d = df.groupby("Customer_ID").agg(
        TotalOrders     =("Order_ID","count"),
        DiscountedOrders=("HasDiscount","sum"),
        AvgSpend        =("Order_Value","mean")
    ).reset_index()
    cust_d["DiscountRate"] = cust_d["DiscountedOrders"] / cust_d["TotalOrders"]
    cust_d["IsRepeat"]     = cust_d["TotalOrders"] > 1

    c1, c2 = st.columns(2)
    with c1:
        rd = cust_d.groupby("IsRepeat")["DiscountRate"].mean().reset_index()
        rd["IsRepeat"] = rd["IsRepeat"].map({True:"Repeat",False:"One-time"})
        fig = px.bar(rd, x="IsRepeat", y="DiscountRate",
                     color="IsRepeat",
                     color_discrete_sequence=["#2ed573","#ffa502"],
                     title="Avg Discount Rate: Repeat vs One-time",
                     text_auto=".1%")
        fig.update_traces(textposition="outside")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(cust_d.sample(min(2000,len(cust_d)),random_state=2),
                         x="DiscountRate", y="AvgSpend",
                         color="IsRepeat",
                         color_discrete_map={True:"#2ed573",False:"#ffa502"},
                         opacity=0.65,
                         title="Discount Rate vs Avg Spend per Customer")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🍕 Avg Discount by Food Category & Cuisine", "sec-purple")
    c1, c2 = st.columns(2)
    with c1:
        cd = df.groupby("Food_Category")["Discount"].mean().sort_values().reset_index()
        fig = px.bar(cd, y="Food_Category", x="Discount", orientation="h",
                     color="Discount", color_continuous_scale=PURPLE_SEQ,
                     title="Avg Discount by Food Category (₹)")
        ct(fig, 500)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        cc = df.groupby("Cuisines")["Discount"].mean().sort_values().reset_index()
        fig = px.bar(cc, y="Cuisines", x="Discount", orientation="h",
                     color="Discount", color_continuous_scale=WARM,
                     title="Avg Discount by Cuisine (₹)")
        ct(fig, 500)
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 7 — DELIVERY PERFORMANCE
# ══════════════════════════════════════════════════════════════
elif page == "🚴 Delivery Performance":

    st.markdown("""<div class="hero-banner">
        <div class="hero-title">🚴 Delivery Performance Analysis</div>
        <div class="hero-subtitle">Delivery time · Distance · Delays · Performance by city & food</div>
    </div>""", unsafe_allow_html=True)

    cols = st.columns(4)
    kpi_card(cols[0],"⏱️","Avg Delivery Time",   f"{df['Delivery_Time'].mean():.1f} min", KPI_GRADS[0])
    kpi_card(cols[1],"📏","Avg Distance",          f"{df['Delivery_Distance'].mean():.2f} km", KPI_GRADS[2])
    kpi_card(cols[2],"⚡","Fastest Delivery",      f"{df['Delivery_Time'].min()} min",       KPI_GRADS[3])
    kpi_card(cols[3],"🐢","Slowest Delivery",      f"{df['Delivery_Time'].max()} min",       KPI_GRADS[0])

    divider()
    section("📊 Delivery Time & Distance Distributions", "sec-orange")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(df, x="Delivery_Time", nbins=50,
                           color_discrete_sequence=["#ff6b35"],
                           title="Delivery Time Distribution (minutes)")
        fig.add_vline(x=df["Delivery_Time"].mean(), line_color="#2ed573",
                      line_dash="dash",
                      annotation_text=f"Mean {df['Delivery_Time'].mean():.1f}m",
                      annotation_font_color="#2ed573")
        ct(fig, 400)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.histogram(df, x="Delivery_Distance", nbins=50,
                           color_discrete_sequence=["#a55eea"],
                           title="Delivery Distance Distribution (km)")
        fig.add_vline(x=df["Delivery_Distance"].mean(), line_color="#ffa502",
                      line_dash="dash",
                      annotation_text=f"Mean {df['Delivery_Distance'].mean():.1f}km",
                      annotation_font_color="#ffa502")
        ct(fig, 400)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🔗 Distance vs Delivery Time", "sec-green")
    fig = px.scatter(df.sample(3000, random_state=5),
                     x="Delivery_Distance", y="Delivery_Time",
                     color="Order_Status",
                     color_discrete_map={"Delivered":"#2ed573","Cancelled":"#ff4757","Delayed":"#ffa502"},
                     opacity=0.65, trendline="ols",
                     trendline_scope="overall",
                     trendline_color_override="#ffffff",
                     title="Delivery Distance vs Delivery Time (sample 3000)")
    ct(fig, 500)
    st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🏙️ Delivery Performance by City", "sec-blue")
    city_del = df.groupby("City").agg(
        AvgTime   =("Delivery_Time","mean"),
        AvgDist   =("Delivery_Distance","mean"),
        DelayedPct=("Order_Status", lambda x: (x=="Delayed").mean()*100)
    ).reset_index()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(city_del.sort_values("AvgTime"), y="City", x="AvgTime",
                     orientation="h", color="City",
                     color_discrete_sequence=RAINBOW,
                     title="Avg Delivery Time by City (min)", text_auto=".1f")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(city_del.sort_values("DelayedPct"), y="City", x="DelayedPct",
                     orientation="h",
                     color="DelayedPct",
                     color_continuous_scale=["#2ed573","#ffa502","#ff4757"],
                     title="% Delayed Orders by City", text_auto=".1f")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🍕 Delivery Time by Food Category", "sec-purple")
    cat_del = df.groupby("Food_Category")["Delivery_Time"].mean().sort_values().reset_index()
    fig = px.bar(cat_del, y="Food_Category", x="Delivery_Time",
                 orientation="h", color="Delivery_Time",
                 color_continuous_scale=PURPLE_SEQ,
                 title="Avg Delivery Time by Food Category (min)", text_auto=".1f")
    ct(fig, 520)
    st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# PAGE 8 — RATING ANALYSIS
# ══════════════════════════════════════════════════════════════
elif page == "⭐ Rating Analysis":

    st.markdown("""<div class="hero-banner">
        <div class="hero-title">⭐ Customer Rating Analysis</div>
        <div class="hero-subtitle">What drives satisfaction? Ratings vs food · delivery · spending · location</div>
    </div>""", unsafe_allow_html=True)

    df_r = df[df["Customer_Rating"].notna()].copy()

    cols = st.columns(4)
    kpi_card(cols[0],"⭐","Avg Rating",    f"{df_r['Customer_Rating'].mean():.2f} / 5", KPI_GRADS[3])
    kpi_card(cols[1],"🌟","5-Star Orders", f"{(df_r['Customer_Rating']==5).sum():,}",   KPI_GRADS[2])
    kpi_card(cols[2],"💔","1-Star Orders", f"{(df_r['Customer_Rating']==1).sum():,}",   KPI_GRADS[0])
    kpi_card(cols[3],"📝","Rated Orders",  f"{len(df_r):,}",                            KPI_GRADS[4])

    divider()
    section("📊 Rating Distribution", "sec-green")
    c1, c2 = st.columns(2)
    with c1:
        rc = df_r["Customer_Rating"].value_counts().sort_index().reset_index()
        rc.columns = ["Rating","Count"]
        fig = px.bar(rc, x="Rating", y="Count",
                     color="Rating",
                     color_discrete_sequence=["#ff4757","#e17055","#ffa502","#2ed573","#1e90ff"],
                     title="Rating Distribution", text="Count")
        fig.update_traces(textposition="outside")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.funnel(rc.sort_values("Rating", ascending=False),
                        x="Count", y=rc.sort_values("Rating",ascending=False)["Rating"].astype(str)+"★",
                        color_discrete_sequence=["#1e90ff","#2ed573","#ffa502","#e17055","#ff4757"],
                        title="Rating Funnel Chart")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🍕 Rating by Food Category & Cuisine", "sec-orange")
    c1, c2 = st.columns(2)
    with c1:
        cr = df_r.groupby("Food_Category")["Customer_Rating"].mean().sort_values().reset_index()
        fig = px.bar(cr, y="Food_Category", x="Customer_Rating",
                     orientation="h", color="Customer_Rating",
                     color_continuous_scale=GREEN_SEQ, range_x=[3.5,5],
                     title="Avg Rating by Food Category", text_auto=".2f")
        ct(fig, 500)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        cui_r = df_r.groupby("Cuisines")["Customer_Rating"].mean().sort_values().reset_index()
        fig = px.bar(cui_r, y="Cuisines", x="Customer_Rating",
                     orientation="h", color="Customer_Rating",
                     color_continuous_scale=BLUE_SEQ, range_x=[3.5,5],
                     title="Avg Rating by Cuisine", text_auto=".2f")
        ct(fig, 500)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("⏱️ Delivery Time vs Rating", "sec-blue")
    c1, c2 = st.columns(2)
    with c1:
        bins   = [0,15,25,35,45,60,100]
        labels = ["0-15","15-25","25-35","35-45","45-60","60+"]
        df_r["TimeGroup"] = pd.cut(df_r["Delivery_Time"], bins=bins, labels=labels)
        tg = df_r.groupby("TimeGroup", observed=True)["Customer_Rating"].mean().reset_index()
        fig = px.bar(tg, x="TimeGroup", y="Customer_Rating",
                     color="Customer_Rating",
                     color_continuous_scale=["#ff4757","#ffa502","#2ed573"],
                     title="Avg Rating by Delivery Time Bucket",
                     text_auto=".2f", range_y=[3.5,5])
        fig.update_traces(textposition="outside")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(df_r.sample(min(3000,len(df_r)),random_state=7),
                         x="Delivery_Time", y="Customer_Rating",
                         color="Food_Category",
                         color_discrete_sequence=RAINBOW,
                         opacity=0.55,
                         title="Delivery Time vs Customer Rating")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("💵 Rating by Order Value & Payment", "sec-red")
    c1, c2 = st.columns(2)
    with c1:
        vr = df_r.groupby("ValueSegment", observed=True)["Customer_Rating"].mean().reset_index()
        fig = px.bar(vr, x="ValueSegment", y="Customer_Rating",
                     color="Customer_Rating",
                     color_continuous_scale=["#ff4757","#ffa502","#2ed573"],
                     title="Avg Rating by Order Value Segment",
                     text_auto=".2f", range_y=[3.5,5])
        fig.update_traces(textposition="outside")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        pr = df_r.groupby("Payment_Method")["Customer_Rating"].mean().sort_values().reset_index()
        fig = px.bar(pr, y="Payment_Method", x="Customer_Rating",
                     orientation="h",
                     color="Payment_Method",
                     color_discrete_sequence=RAINBOW, range_x=[3.5,5],
                     title="Avg Rating by Payment Method", text_auto=".2f")
        ct(fig, 420)
        st.plotly_chart(fig, use_container_width=True)

    divider()
    section("🏆 Top-Rated Restaurants (min 50 orders)", "sec-teal")
    rest_r = df_r.groupby(["Restaurant_Name","City"]).agg(
        AvgRating=("Customer_Rating","mean"),
        Orders   =("Order_ID","count")
    ).reset_index()
    rest_r = rest_r[rest_r["Orders"]>=50].sort_values("AvgRating",ascending=False).head(15)
    fig = px.bar(rest_r.sort_values("AvgRating"),
                 y="Restaurant_Name", x="AvgRating",
                 orientation="h", color="City",
                 color_discrete_sequence=RAINBOW,
                 title="Top 15 Restaurants by Avg Rating",
                 text_auto=".2f", range_x=[3.5,5])
    ct(fig, 540)
    st.plotly_chart(fig, use_container_width=True)
