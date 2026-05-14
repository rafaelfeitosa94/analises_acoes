import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO
import base64

# =========================================================
# CONFIG PAGE
# =========================================================

st.set_page_config(
    page_title="Dia do Beijo Mané 2026",
    page_icon="💋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# COLORS
# =========================================================

PRIMARY      = "#FF6666"
PRIMARY_DARK = "#8B0000"
SECONDARY    = "#CC3333"
ACCENT       = "#FF9999"

BG    = "#0B0F14"
TEXT  = "#FFFFFF"
MUTED = "#9CA3AF"
GRID  = "rgba(255,255,255,0.06)"

# =========================================================
# PLOTLY BASE — sem xaxis/yaxis para evitar conflito de kwargs
# =========================================================

def base_layout(height=400):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, family="sans-serif"),
        margin=dict(l=10, r=80, t=30, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT)),
    )

# =========================================================
# CSS
# =========================================================

st.markdown(f"""
<style>

html, body, [class*="css"] {{
    background-color: {BG} !important;
    color: {TEXT} !important;
    font-family: 'DM Sans', sans-serif;
}}
.main {{ background-color: {BG}; }}
.block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }}
header[data-testid="stHeader"] {{ height: 0px; }}
[data-testid="stToolbar"] {{ visibility: hidden; height: 0px; }}
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #121720 0%, #0B0F14 100%);
    border-right: 1px solid rgba(255,255,255,0.05);
}}
section[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
h1,h2,h3,h4,h5,h6 {{ font-family: 'Syne', sans-serif !important; color: {TEXT} !important; }}
p, span, label, div {{ color: {TEXT} !important; }}

.metric-card {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border: 1px solid rgba(255,102,102,0.18);
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    position: relative;
    overflow: hidden;
    transition: transform .25s ease, border-color .25s ease;
    box-shadow: 0 8px 32px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.04);
    height: 100%;
}}
.metric-card:hover {{ transform: translateY(-3px); border-color: rgba(255,102,102,.5); }}
.metric-card::after {{
    content: '';
    position: absolute;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(255,102,102,.15) 0%, transparent 70%);
    top: -50px; right: -50px;
}}
.metric-icon {{ font-size: 1.6rem; margin-bottom: .6rem; display: block; }}
.metric-value {{
    font-family: Helvetica, Arial, sans-serif;    
    font-size: 1.85rem;
    font-weight: 800;
    color: {TEXT} !important;
    line-height: 1;
    letter-spacing: -0.5px;
}}
.metric-label {{
    color: {MUTED} !important;
    margin-top: .5rem;
    font-size: .88rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: .06em;
}}
.metric-badge {{
    display: inline-block;
    margin-top: .6rem;
    padding: .2rem .7rem;
    border-radius: 999px;
    font-size: .82rem;
    font-weight: 700;
    background: rgba(255,102,102,.15);
    color: {PRIMARY} !important;
    border: 1px solid rgba(255,102,102,.25);
}}
.section-card {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border-radius: 20px;
    padding: 1.4rem 1.6rem;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 8px 32px rgba(0,0,0,.35);
    margin-bottom: 1.5rem;
}}
.section-title {{
    font-family: Helvetica, Arial, sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: {TEXT} !important;
    margin-bottom: 1rem;
}}
.sub-header {{
    font-family: Helvetica, Arial, sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    color: {PRIMARY} !important;
    margin: 1.5rem 0 1rem;
}}
[data-testid="stDataFrame"] {{
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,.05) !important;
}}

/* Summary Cards Estilo */
.summary-card {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border: 1px solid rgba(255,102,102,0.18);
    border-radius: 20px;
    padding: 1.2rem 1rem;
    text-align: center;
    transition: all 0.25s ease;
    height: 100%;
}}
.summary-card:hover {{
    transform: translateY(-2px);
    border-color: rgba(255,102,102,.5);
}}
.summary-value {{
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: {PRIMARY} !important;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}}
.summary-label {{
    font-size: 0.85rem;
    font-weight: 600;
    color: {TEXT} !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.3rem;
}}
.summary-sub {{
    font-size: 0.75rem;
    color: {MUTED} !important;
    margin-top: 0.25rem;
}}
.warning-card {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border: 1px solid rgba(255,102,102,0.18);
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    color: {MUTED} !important;
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD LOGO
# =========================================================

@st.cache_data
def load_logo():
    try:
        url = "https://botecomane.com.br/wp-content/uploads/2024/06/mane-logo-vermelho.png"
        r = requests.get(url, timeout=5)
        img = Image.open(BytesIO(r.content))
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except:
        return ""

img_b64 = load_logo()
img_tag = (f'<img src="data:image/png;base64,{img_b64}" width="200" '
           f'style="margin-bottom:1rem;">') if img_b64 else ""

# =========================================================
# HEADER
# =========================================================

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #151922 0%, #0B0F14 100%);
    padding: 2rem 2.5rem;
    border-radius: 24px;
    border: 1px solid rgba(255,102,102,0.14);
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
">
    <div style="position:absolute;top:-80px;left:50%;transform:translateX(-50%);
        width:400px;height:400px;
        background:radial-gradient(circle,rgba(255,102,102,.08) 0%,transparent 70%);
        pointer-events:none;"></div>
    {img_tag}
    <div style="font-family:'Syne',sans-serif;font-size:2.6rem;font-weight:800;
        color:#FF6666;letter-spacing:-1px;line-height:1.1;">
        💋 Dia do Beijo 2026
    </div>
    <div style="color:{MUTED};font-size:1rem;margin-top:.6rem;">
        Performance das lojas &nbsp;•&nbsp; 13/04/2026 vs 14/04/2025
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================

data = {
    'LOJA': [
        'MAN BÚZIOS', 'MAN VILA VELHA', 'MAN ITAIPAVA', 'MAN IPANEMA',
        'MAN SÃO GONÇALO', 'MAN NOVA AMÉRICA', 'MAN COPACABANA',
        'MAN COLLAB CABO FRIO', 'MAN MACAÉ', 'MAN RECREIO', 'MAN NOVA IGUAÇÚ',
        'MAN PARK SHOP CG', 'MAN COPA PRAIA', 'MAN COLLAB VALQUEIRE',
        'MAN RIO DAS OSTRAS'
    ],
    'FAT_2026': [
        9642.7, 5666.85, 4524.45, 3818.03, 3669.89, 3321.75, 2996.56,
        2994.31, 2666.08, 2296.63, 1919.47, 1875.53, 941.91, 749.46, 592.37
    ],
    'TC_2026': [
        129, 75, 44, 78, 54, 37, 64, 35, 42, 52, 31, 22, 20, 19, 13
    ],
    'TM_2026': [
        74.75, 75.56, 102.83, 48.95, 67.96, 89.78, 46.82, 85.55,
        63.48, 44.17, 61.92, 85.25, 47.10, 39.45, 45.57
    ],
    'FAT_2025': [
        6738.75, None, 1891.9, 2369.44, 4740.53, 3472.73, 4199.8,
        2573.9, 1593.13, 2571.92, None, 2168.66, 8872.16, 913.16, 1369.63
    ]
}

df_full = pd.DataFrame(data)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        f"<div style='font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;"
        f"color:{PRIMARY};margin-bottom:1rem;'>🎯 Filtros</div>",
        unsafe_allow_html=True
    )
    lojas_sel = st.multiselect(
        "Lojas",
        options=df_full["LOJA"].unique(),
        default=df_full["LOJA"].unique()
    )
    st.markdown("---")
    st.markdown(
        f"<div style='color:{MUTED};font-size:.8rem;'>Dia do Beijo Mané 2026<br>"
        f"Dashboard de Performance</div>",
        unsafe_allow_html=True
    )

df = df_full[df_full["LOJA"].isin(lojas_sel)].copy()
df_comp = df[(df["FAT_2025"].notna()) & (df["FAT_2025"] > 0)].copy()

# =========================================================
# RESUME DE PERFORMANCE
# =========================================================



# =========================================================
# METRICS
# =========================================================

fat_2025 = df_comp["FAT_2025"].sum() if not df_comp.empty else 0
fat_2026 = df_comp["FAT_2026"].sum() if not df_comp.empty else 0
clientes  = df["TC_2026"].sum()
ticket    = fat_2026 / clientes if clientes > 0 else 0
var       = ((fat_2026 - fat_2025) / fat_2025 * 100) if fat_2025 > 0 else 0

st.markdown('<div class="sub-header">📊 Visão Geral</div>', unsafe_allow_html=True)

def metric_card(col, icon, label, value, badge=""):
    badge_html = f'<div class="metric-badge">{badge}</div>' if badge else ""
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">{icon}</span>
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
            {badge_html}
        </div>
        """, unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
metric_card(c1, "📅", "Faturamento 2025",  f"R$ {fat_2025:,.0f}".replace(",", "."))
metric_card(c2, "💰", "Faturamento 2026",  f"R$ {fat_2026:,.0f}".replace(",", "."), f"{var:+.1f}% vs 2025")
metric_card(c3, "👥", "Total de Clientes", f"{clientes:,}".replace(",", "."))
metric_card(c4, "🎯", "Ticket Médio",      f"R$ {ticket:,.2f}".replace(",", "."))

st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

# =========================================================
# ROW 1: Ranking + Comparativo
# =========================================================

col1, col2 = st.columns(2)

# --- RANKING ---
with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏆 Ranking de Faturamento 2026</div>', unsafe_allow_html=True)

    ranking = df.sort_values("FAT_2026", ascending=True)
    n = len(ranking)
    colors = [PRIMARY if i == n - 1 else "rgba(255,102,102,0.55)" for i in range(n)]

    fig_rank = go.Figure(go.Bar(
        x=ranking["FAT_2026"],
        y=ranking["LOJA"].str.replace("MAN ", "", regex=False),
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=ranking["FAT_2026"].apply(lambda x: f"R$ {x:,.0f}".replace(",", ".")),
        textposition="outside",
        textfont=dict(color=TEXT, size=11),
        hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>",
    ))
    fig_rank.update_layout(**base_layout(430), bargap=0.35)
    fig_rank.update_xaxes(visible=False, gridcolor=GRID)
    fig_rank.update_yaxes(tickfont=dict(color=TEXT, size=11), gridcolor=GRID)

    st.plotly_chart(fig_rank, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# --- COMPARATIVO ---
with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Comparativo 2025 vs 2026</div>', unsafe_allow_html=True)

    comp_labels = df_comp["LOJA"].str.replace("MAN ", "", regex=False)

    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(
        x=comp_labels, y=df_comp["FAT_2025"],
        name="2025", mode="lines+markers",
        line=dict(color=PRIMARY_DARK, width=3),
        marker=dict(size=7, color=PRIMARY_DARK),
        fill="tozeroy", fillcolor="rgba(139,0,0,0.12)",
        hovertemplate="<b>%{x}</b><br>2025: R$ %{y:,.2f}<extra></extra>",
    ))
    fig_comp.add_trace(go.Scatter(
        x=comp_labels, y=df_comp["FAT_2026"],
        name="2026", mode="lines+markers",
        line=dict(color=PRIMARY, width=3),
        marker=dict(size=7, color=PRIMARY),
        fill="tozeroy", fillcolor="rgba(255,102,102,0.12)",
        hovertemplate="<b>%{x}</b><br>2026: R$ %{y:,.2f}<extra></extra>",
    ))
    fig_comp.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="right", x=1, font=dict(color=TEXT)),
    )
    fig_comp.update_xaxes(tickangle=-40, tickfont=dict(color=MUTED, size=10), gridcolor=GRID)
    fig_comp.update_yaxes(tickfont=dict(color=MUTED, size=10), gridcolor=GRID,
                          tickprefix="R$ ", tickformat=",.0f")

    st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ROW 2: Ticket Médio + Clientes + Crescimento
# =========================================================

col3, col4, col5 = st.columns([2, 1.2, 1.8])

# --- TICKET MÉDIO POR LOJA ---
with col3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💎 Ticket Médio por Loja</div>', unsafe_allow_html=True)

    tm_sorted  = df.sort_values("TM_2026", ascending=True)
    bar_colors = [PRIMARY if v >= ticket else "rgba(255,102,102,0.45)"
                  for v in tm_sorted["TM_2026"]]

    fig_tm = go.Figure(go.Bar(
        x=tm_sorted["TM_2026"],
        y=tm_sorted["LOJA"].str.replace("MAN ", "", regex=False),
        orientation="h",
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=tm_sorted["TM_2026"].apply(lambda x: f"R$ {x:.2f}"),
        textposition="outside",
        textfont=dict(color=TEXT, size=10),
        hovertemplate="<b>%{y}</b><br>TM: R$ %{x:.2f}<extra></extra>",
    ))
    fig_tm.add_vline(
        x=ticket, line_dash="dash", line_color=ACCENT,
        annotation_text=f"Média R$ {ticket:.2f}",
        annotation_font_color=ACCENT,
        annotation_position="top right",
    )
    fig_tm.update_layout(**base_layout(380), bargap=0.3)
    fig_tm.update_xaxes(visible=False)
    fig_tm.update_yaxes(tickfont=dict(color=TEXT, size=10))

    st.plotly_chart(fig_tm, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# --- CLIENTES RADIALBAR (ApexCharts via HTML) ---
import streamlit.components.v1 as components

with col4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👥 Top Clientes por Loja</div>', unsafe_allow_html=True)

    top4_tc   = df.nlargest(4, "TC_2026")
    max_tc    = top4_tc["TC_2026"].max()
    rb_values = (top4_tc["TC_2026"] / max_tc * 100).round(1).tolist()
    rb_labels = top4_tc["LOJA"].str.replace("MAN ", "", regex=False).tolist()
    rb_total  = int(df["TC_2026"].sum())
    rb_raw    = top4_tc["TC_2026"].tolist()

    radial_html = f"""
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
        <style>
            body {{ margin:0; background:transparent; }}
            #chart {{ background:transparent; }}
        </style>
    </head>
    <body>
        <div id="chart"></div>
        <script>
            var rawValues = {rb_raw};
            var options = {{
                series: {rb_values},
                chart: {{
                    height: 360,
                    type: "radialBar",
                    background: "transparent",
                    toolbar: {{ show: false }},
                }},
                theme: {{ mode: "dark" }},
                colors: ["{PRIMARY}", "{SECONDARY}", "{PRIMARY_DARK}", "{ACCENT}"],
                plotOptions: {{
                    radialBar: {{
                        offsetY: 0,
                        startAngle: 0,
                        endAngle: 270,
                        hollow: {{
                            margin: 5,
                            size: "30%",
                            background: "transparent",
                        }},
                        track: {{
                            background: "rgba(255,255,255,0.05)",
                            strokeWidth: "97%",
                        }},
                        dataLabels: {{
                            name: {{ fontSize: "13px", color: "#FFFFFF" }},
                            value: {{ fontSize: "12px", color: "#9CA3AF" }},
                            total: {{
                                show: true,
                                label: "Total",
                                color: "#FFFFFF",
                                fontSize: "14px",
                                fontWeight: 700,
                                formatter: function () {{ return "{rb_total}"; }}
                            }}
                        }}
                    }}
                }},
                labels: {rb_labels},
                legend: {{
                    show: true,
                    floating: true,
                    fontSize: "11px",
                    position: "left",
                    offsetX: 10,
                    offsetY: 10,
                    labels: {{ useSeriesColors: true }},
                    formatter: function(seriesName, opts) {{
                        return seriesName + ": " + rawValues[opts.seriesIndex];
                    }},
                    itemMargin: {{ vertical: 3 }},
                }},
                tooltip: {{
                    theme: "dark",
                    y: {{
                        formatter: function(val, opts) {{
                            return rawValues[opts.seriesIndex] + " clientes";
                        }}
                    }}
                }},
            }};
            var chart = new ApexCharts(document.querySelector("#chart"), options);
            chart.render();
        </script>
    </body>
    </html>
    """

    components.html(radial_html, height=375, scrolling=False)
    st.markdown("</div>", unsafe_allow_html=True)

# --- CRESCIMENTO ---
with col5:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚀 Crescimento vs 2025 (%)</div>', unsafe_allow_html=True)

    df_comp = df_comp.copy()
    df_comp["VAR"] = ((df_comp["FAT_2026"] - df_comp["FAT_2025"]) / df_comp["FAT_2025"]) * 100
    top_var = df_comp.sort_values("VAR", ascending=True)
    bar_col_var = [PRIMARY if v >= 0 else "#FF4444" for v in top_var["VAR"]]

    fig_growth = go.Figure(go.Bar(
        x=top_var["VAR"],
        y=top_var["LOJA"].str.replace("MAN ", "", regex=False),
        orientation="h",
        marker=dict(color=bar_col_var, line=dict(width=0)),
        text=top_var["VAR"].apply(lambda x: f"{x:+.1f}%"),
        textposition="outside",
        textfont=dict(color=TEXT, size=10),
        hovertemplate="<b>%{y}</b><br>Crescimento: %{x:+.1f}%<extra></extra>",
    ))
    fig_growth.add_vline(x=0, line_color=GRID, line_width=1)
    fig_growth.update_layout(**base_layout(380), bargap=0.3)
    fig_growth.update_xaxes(ticksuffix="%", tickfont=dict(color=MUTED, size=10), gridcolor=GRID)
    fig_growth.update_yaxes(tickfont=dict(color=TEXT, size=10))

    st.plotly_chart(fig_growth, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### 📈 Resumo de Performance (Lojas com dados completos)")

if not df_comp.empty:
    # Calcular variação percentual
    df_comp['VARIACAO_%'] = ((df_comp['FAT_2026'] - df_comp['FAT_2025']) / df_comp['FAT_2025']) * 100
    
    media_variacao = df_comp['VARIACAO_%'].mean()
    total_crescimento = (df_comp['VARIACAO_%'] > 0).sum()
    total_queda = (df_comp['VARIACAO_%'] < 0).sum()
    melhor_loja = df_comp.loc[df_comp['VARIACAO_%'].idxmax(), 'LOJA']
    melhor_variacao = df_comp['VARIACAO_%'].max()
    pior_loja = df_comp.loc[df_comp['VARIACAO_%'].idxmin(), 'LOJA']
    pior_variacao = df_comp['VARIACAO_%'].min()

    # Primeira linha de cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value">{media_variacao:.1f}%</div>
            <div class="summary-label">📊 Variação Média</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value">{total_crescimento}</div>
            <div class="summary-label">📈 Lojas em Crescimento</div>
            <div class="summary-sub">✅ Resultado positivo</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value">{total_queda}</div>
            <div class="summary-label">📉 Lojas em Queda</div>
            <div class="summary-sub">⚠️ Atenção necessária</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1.2rem;">{melhor_loja}</div>
            <div class="summary-label">🏆 Melhor Performance</div>
            <div class="summary-sub">+{melhor_variacao:.1f}% vs 2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Segunda linha de cards
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value">{len(df_comp)}</div>
            <div class="summary-label">🏪 Lojas Analisadas</div>
            <div class="summary-sub">Com dados completos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        fat_2025_total = df_comp['FAT_2025'].sum()
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1.5rem;">R$ {fat_2025_total/1000000:.3f}M</div>
            <div class="summary-label">💰 Faturamento 2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col7:
        fat_2026_total = df_comp['FAT_2026'].sum()
        variacao_total = ((fat_2026_total - fat_2025_total) / fat_2025_total * 100) if fat_2025_total > 0 else 0
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1.5rem;">R$ {fat_2026_total/1000000:.3f}M</div>
            <div class="summary-label">💰 Faturamento 2026</div>
            <div class="summary-sub">{variacao_total:+.1f}% vs 2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col8:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1rem;">{pior_loja}</div>
            <div class="summary-label">⚠️ Pior Performance</div>
            <div class="summary-sub">{pior_variacao:.1f}% vs 2025</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="warning-card">
        ⚠️ Não há dados suficientes para exibir o resumo de performance.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

# =========================================================
# TABLE
# =========================================================

st.markdown('<div class="sub-header">📋 Dados Completos</div>', unsafe_allow_html=True)

df_view = df.copy()
df_view.columns = ["Loja", "Faturamento 2026", "Clientes 2026", "Ticket Médio", "Faturamento 2025"]
df_view["Faturamento 2026"] = df_view["Faturamento 2026"].apply(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
df_view["Ticket Médio"] = df_view["Ticket Médio"].apply(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
df_view["Faturamento 2025"] = df_view["Faturamento 2025"].apply(
    lambda x: (f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    if pd.notna(x) else "—")

st.dataframe(df_view, use_container_width=True, height=450)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")
st.markdown(
    f"<div style='text-align:center;color:{MUTED};padding:.8rem;font-size:.85rem;'>"
    f"Dashboard Mané • Desenvolvido com Streamlit + Plotly • "
    f"Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    f"</div>",
    unsafe_allow_html=True
)
