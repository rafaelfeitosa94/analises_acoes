import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import base64

# =========================================================
# CONFIG PAGE
# =========================================================

st.set_page_config(
    page_title="Champions League Sirène 2026",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# COLORS - TONS DE LARANJA
# =========================================================

PRIMARY      = "#FF8C00"      # Laranja principal
PRIMARY_DARK = "#CC7000"      # Laranja escuro
SECONDARY    = "#FFA500"      # Laranja médio
ACCENT       = "#FFB347"      # Laranja claro

BG    = "#0B0F14"
TEXT  = "#FFFFFF"
MUTED = "#9CA3AF"
GRID  = "rgba(255,255,255,0.06)"

# =========================================================
# PLOTLY BASE
# =========================================================

def base_layout(height=400):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, family="Arial, sans-serif"),
        margin=dict(l=10, r=80, t=30, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT, family="Arial, sans-serif")),
    )

# =========================================================
# CSS
# =========================================================

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    background-color: {BG} !important;
    color: {TEXT} !important;
    font-family: 'Barlow', sans-serif !important;
}}
.main {{ background-color: {BG}; }}
.block-container {{ padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px; }}
header[data-testid="stHeader"] {{ height: 0px; }}
[data-testid="stToolbar"] {{ visibility: hidden; height: 0px; }}
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #121720 0%, #0B0F14 100%);
    border-right: 1px solid rgba(255,140,0,0.1);
}}
section[data-testid="stSidebar"] * {{ color: {TEXT} !important; font-family: 'Barlow', sans-serif !important; }}
h1,h2,h3,h4,h5,h6 {{ font-family: 'Barlow Condensed', sans-serif !important; color: {TEXT} !important; }}
p, span, label, div {{ color: {TEXT} !important; font-family: 'Barlow', sans-serif !important; }}

/* ---- METRIC CARDS ---- */
.metric-card {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border: 1px solid rgba(255,140,0,0.25);
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: transform .25s ease, border-color .25s ease;
    box-shadow: 0 6px 24px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.04);
    height: 100%;
    text-align: center;
}}
.metric-card:hover {{ transform: translateY(-3px); border-color: rgba(255,140,0,.6); }}
.metric-card::after {{
    content: '';
    position: absolute;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(255,140,0,.10) 0%, transparent 70%);
    top: -40px; right: -40px;
}}
.metric-value {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    color: {PRIMARY} !important;
    line-height: 1;
    letter-spacing: -0.3px;
}}
.metric-label {{
    color: {MUTED} !important;
    margin-top: .45rem;
    font-size: .78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .07em;
    font-family: 'Barlow', sans-serif;
}}
.metric-variation {{
    color: {ACCENT} !important;
    font-size: .80rem;
    margin-top: .35rem;
    font-family: 'Barlow', sans-serif;
}}

/* ---- SECTION CARDS ---- */
.section-card {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border-radius: 20px;
    padding: 1.4rem 1.6rem;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 8px 32px rgba(0,0,0,.35);
    margin-bottom: 1.5rem;
}}
.section-title {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: {PRIMARY} !important;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: .05em;
}}
.sub-header {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    color: {PRIMARY} !important;
    margin: 1.5rem 0 1rem;
    border-bottom: 2px solid {PRIMARY};
    padding-bottom: 0.5rem;
    display: inline-block;
    text-transform: uppercase;
    letter-spacing: .04em;
}}

/* ---- DATAFRAME ---- */
[data-testid="stDataFrame"] {{
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,.05) !important;
}}
[data-testid="stDataFrame"] thead tr th {{
    background-color: #1a1d24 !important;
    color: {PRIMARY} !important;
    font-family: 'Barlow', sans-serif !important;
}}
[data-testid="stDataFrame"] tbody tr {{
    background-color: #0e1117 !important;
    color: {TEXT} !important;
    font-family: 'Barlow', sans-serif !important;
}}
[data-testid="stDataFrame"] tbody tr:hover {{
    background-color: #1a1d24 !important;
}}

/* ---- SUMMARY CARDS ---- */
.summary-card {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border: 1px solid rgba(255,140,0,0.25);
    border-radius: 16px;
    padding: 1rem 0.9rem;
    text-align: center;
    transition: all 0.25s ease;
    height: 100%;
}}
.summary-card:hover {{
    transform: translateY(-2px);
    border-color: rgba(255,140,0,.6);
}}
.summary-value {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    color: {PRIMARY} !important;
    line-height: 1.2;
    margin-bottom: 0.35rem;
}}
.summary-label {{
    font-size: 0.75rem;
    font-weight: 600;
    color: {TEXT} !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.25rem;
    font-family: 'Barlow', sans-serif;
}}
.summary-sub {{
    font-size: 0.72rem;
    color: {MUTED} !important;
    margin-top: 0.2rem;
    font-family: 'Barlow', sans-serif;
}}
.summary-name {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: {PRIMARY} !important;
    line-height: 1.2;
    margin-bottom: 0.35rem;
}}

/* ---- WARNING / INFO ---- */
.warning-card {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border: 1px solid rgba(255,140,0,0.25);
    border-radius: 20px;
    padding: 1rem;
    text-align: center;
    color: {ACCENT} !important;
    font-family: 'Barlow', sans-serif;
    font-size: 0.9rem;
}}
.info-card {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border: 1px solid rgba(255,140,0,0.25);
    border-radius: 20px;
    padding: 1.5rem;
    border-left: 5px solid {PRIMARY};
    margin-bottom: 1rem;
}}
.info-title {{
    color: {PRIMARY} !important;
    font-size: 1.1rem;
    font-weight: bold;
    margin-bottom: 0.8rem;
    font-family: 'Barlow Condensed', sans-serif;
    text-transform: uppercase;
    letter-spacing: .04em;
}}
.info-text {{
    color: {TEXT} !important;
    font-size: 0.92rem;
    line-height: 1.5;
    font-family: 'Barlow', sans-serif;
}}
.info-list {{
    color: {TEXT} !important;
    margin-left: 1.5rem;
    margin-top: 0.5rem;
    font-family: 'Barlow', sans-serif;
    font-size: 0.9rem;
}}
.info-list li {{
    margin: 0.3rem 0;
}}

/* ---- RANKING CARDS (NOVO ESTILO) ---- */
.ranking-wrap {{
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
}}
.rank-card {{
    display: flex;
    align-items: center;
    gap: 0.9rem;
    background: rgba(255,140,0,0.06);
    border: 1px solid rgba(255,140,0,0.15);
    border-radius: 14px;
    padding: 0.75rem 1rem;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}}
.rank-card::before {{
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, {PRIMARY}, {ACCENT});
    border-radius: 3px 0 0 3px;
}}
.rank-card:hover {{
    background: rgba(255,140,0,0.12);
    border-color: rgba(255,140,0,0.4);
    transform: translateX(4px);
}}
.rank-card.rank-1 {{ border-color: rgba(255,140,0,0.5); background: rgba(255,140,0,0.10); }}
.rank-card.rank-2 {{ border-color: rgba(255,165,0,0.35); }}
.rank-card.rank-3 {{ border-color: rgba(255,179,71,0.25); }}

.rank-num {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: {PRIMARY} !important;
    min-width: 32px;
    text-align: center;
    line-height: 1;
}}
.rank-num.gold   {{ color: #FFD700 !important; }}
.rank-num.silver {{ color: #C0C0C0 !important; }}
.rank-num.bronze {{ color: #CD7F32 !important; }}

.rank-bar-wrap {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    min-width: 0;
}}
.rank-loja {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.92rem;
    font-weight: 700;
    color: {TEXT} !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-transform: uppercase;
    letter-spacing: .03em;
}}
.rank-bar-bg {{
    height: 5px;
    background: rgba(255,255,255,0.07);
    border-radius: 99px;
    overflow: hidden;
}}
.rank-bar-fill {{
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, {PRIMARY_DARK}, {ACCENT});
    transition: width 0.6s ease;
}}

.rank-val {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: {PRIMARY} !important;
    white-space: nowrap;
    text-align: right;
    min-width: fit-content;
}}
.rank-val-sub {{
    font-size: 0.68rem;
    color: {MUTED} !important;
    text-align: right;
    font-family: 'Barlow', sans-serif;
    white-space: nowrap;
}}

.ranking-section-title {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1rem;
    font-weight: 800;
    color: {PRIMARY} !important;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-bottom: 0.9rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,140,0,0.2);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.ranking-outer {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border: 1px solid rgba(255,140,0,0.2);
    border-radius: 20px;
    padding: 1.4rem 1.4rem 1.2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,.35);
    height: 100%;
}}

/* ---- OTHER ---- */
.stSelectbox, .stMultiSelect, .stSlider {{
    color: {TEXT} !important;
    font-family: 'Barlow', sans-serif !important;
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD LOGO
# =========================================================

@st.cache_data
def load_logo():
    try:
        url = "https://sirene.com.br/wp/wp-content/uploads/2022/04/cropped-logo-sirene-x.png"
        response = requests.get(url, timeout=5)
        img = Image.open(BytesIO(response.content))
        buf = BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except:
        return ""

img_b64 = load_logo()
img_tag = (f'<img src="data:image/png;base64,{img_b64}" width="230" '
           f'style="margin-bottom:1rem; display: block; margin-left: auto; margin-right: auto;">') if img_b64 else ""

# =========================================================
# HEADER
# =========================================================

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #151922 0%, #0B0F14 100%);
    padding: 1.8rem 2.5rem;
    border-radius: 24px;
    border: 1px solid rgba(255,140,0,0.2);
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
">
    <div style="position:absolute;top:-80px;left:50%;transform:translateX(-50%);
        width:400px;height:400px;
        background:radial-gradient(circle,rgba(255,140,0,.08) 0%,transparent 70%);
        pointer-events:none;"></div>
    {img_tag}
    <div style="font-family:'Barlow Condensed', sans-serif;font-size:2.4rem;font-weight:800;
        color:#FF8C00;letter-spacing:-0.5px;line-height:1.1;text-transform:uppercase;">
        🗼 Champions League Sirène 2026 ⚽
    </div>
    <div style="color:{MUTED};font-size:0.92rem;margin-top:.5rem;font-family:'Barlow', sans-serif;">
        Comparativo &nbsp;•&nbsp; 19 à 31/05/2026 vs 19/05 à 01/06/2025
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================

data = {
    'MARCA': ['SIRÈNE'] * 10,
    'LOJA': [
        'SIR BATEL', 'SIR TAQUARAL', 'SIR TORRES', 'SIR CIDADE BAIXA',
        'SIR TRAJANO', 'SIR FLEMING', 'SIR CAXIAS', 'SIR PORTÃO',
        'SIR MARINGÁ', 'SIR ALTO DA GLORIA'
    ],
    'FAT_2026': [
        78121.77, 29131.14, 36191.32, 28143.87, 23349.35,
        74173.25, 36255.88, 27196.08, 25118.66, 24114.24
    ],
    'TC_2026': [
        2019, 389, 834, 899, 629, 2276, 979, 369, 606, 748
    ],
    'TM_2026': [
        38.69329866, 74.88724936, 43.39486811, 31.30575083, 37.12138315,
        32.58930141, 37.03358529, 73.70211382, 41.44993399, 32.23828877
    ],
    'FAT_2025': [
        70745.51, 23100.93, 26203.68, 26087.39, None,
        62234.40, 33257.78, 27156.60, 17658.23, 30559.09
    ],
    'TC_2025': [
        2185, 388, 817, 735, None,
        2018, 1003, 362, 495, 949
    ],
    'TM_2025': [
        32.37780778, 59.53847938, 32.07304774, 35.49304762, None,
        30.83964321, 33.15830508, 75.01823204, 35.67319192, 32.20135933
    ],
    'PROD_PROMOCIONADO': ['CHAMPIONS LEAGUE CHOPP 3 POR 2'] * 10,
    'COMPOSICAO_PROD': ['CHOPP HEINEKEN'] * 10,
    'QUANTIDADE': [76, 37, 33, 17, 8, 0, 0, 0, 0, 0],
    'TOTAL CHOPP HEINEKEN': [339, 376, 443, 191, 120, 0, 124, 151, 0, 69],
    'VALOR_VENDA_PROD': [
        3040.76, 1160.37, 717.90, 378.17, 206.08,
        0.00, 0.00, 0.00, 0.00, 0.00
    ],
    'PART.(%)': [
        0.038923337, 0.039832633, 0.019836248, 0.013437029, 0.008825942,
        None, None, None, None, None
    ]
}

df = pd.DataFrame(data)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        f"<div style='font-family:Barlow Condensed, sans-serif;font-size:1.15rem;font-weight:800;"
        f"color:{PRIMARY};margin-bottom:1rem;text-transform:uppercase;letter-spacing:.05em;'>🎯 Filtros</div>",
        unsafe_allow_html=True
    )
    
    lojas_selecionadas = st.multiselect(
        "Selecione as lojas:",
        options=df['LOJA'].unique(),
        default=df['LOJA'].unique()
    )
    
    fat_min, fat_max = st.slider(
        "Faixa de faturamento 2026 (R$):",
        min_value=float(df['FAT_2026'].min()),
        max_value=float(df['FAT_2026'].max()),
        value=(float(df['FAT_2026'].min()), float(df['FAT_2026'].max()))
    )
    
    st.markdown("---")
    st.markdown(
        f"<div style='color:{MUTED};font-size:.78rem;font-family:Barlow, sans-serif;'>"
        f"Champions League Sirène 2026<br>Dashboard de Performance</div>",
        unsafe_allow_html=True
    )

# Aplicar filtros
df_filtrado = df[
    (df['LOJA'].isin(lojas_selecionadas)) &
    (df['FAT_2026'] >= fat_min) &
    (df['FAT_2026'] <= fat_max)
]

# ==== CRIAR DATAFRAME APENAS COM LOJAS QUE TÊM AMBOS OS ANOS ====
# df_comparavel: usado SOMENTE em análises que exigem comparação com 2025
df_comparavel = df_filtrado.dropna(subset=['FAT_2025', 'FAT_2026']).copy()

if not df_comparavel.empty:
    df_comparavel['VARIACAO_%'] = ((df_comparavel['FAT_2026'] - df_comparavel['FAT_2025']) / df_comparavel['FAT_2025']) * 100

# =========================================================
# MÉTRICAS PRINCIPAIS
# =========================================================

st.markdown('<div class="sub-header">📊 Visão Geral</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    fat_total_2025 = df_comparavel['FAT_2025'].sum() if not df_comparavel.empty else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_2025:,.2f}</div>
        <div class="metric-label">Faturamento Total 2025</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if not df_comparavel.empty:
        fat_total_2026 = df_comparavel['FAT_2026'].sum()
        fat_total_2025_comp = df_comparavel['FAT_2025'].sum()
        variacao = ((fat_total_2026 - fat_total_2025_comp) / fat_total_2025_comp * 100) if fat_total_2025_comp > 0 else 0
    else:
        fat_total_2026 = 0
        variacao = 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_2026:,.2f}</div>
        <div class="metric-label">Faturamento Total 2026</div>
        <div class="metric-variation">{variacao:+.1f}% vs 2025</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    # CORRIGIDO: usa df_filtrado para incluir Trajano
    clientes_total = df_filtrado['TC_2026'].sum() if not df_filtrado.empty else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{clientes_total:,.0f}</div>
        <div class="metric-label">Total de Clientes 2026</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    fat_total_2026_all = df_filtrado['FAT_2026'].sum() if not df_filtrado.empty else 0
    tm_medio = fat_total_2026_all / clientes_total if clientes_total > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {tm_medio:,.2f}</div>
        <div class="metric-label">Ticket Médio Médio 2026</div>
    </div>
    """, unsafe_allow_html=True)

lojas_nao_comparaveis = df_filtrado[~df_filtrado['LOJA'].isin(df_comparavel['LOJA'])]['LOJA'].tolist() if not df_comparavel.empty else df_filtrado['LOJA'].tolist()
if lojas_nao_comparaveis:
    st.markdown(f"""
    <div style="margin-top: 1rem; margin-bottom: 1rem;">
        <div class="warning-card">
            ⚠️ As seguintes lojas não possuem dados completos para 2025 e não estão incluídas nas métricas comparativas:<br>
            <strong>{', '.join(lojas_nao_comparaveis)}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# ROW 1: Ranking + Comparativo
# =========================================================

col1, col2 = st.columns(2)

N_RANK  = 10
N_COMP  = 10
CHART_H = 420

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏆 Ranking de Faturamento 2026</div>', unsafe_allow_html=True)

    # CORRIGIDO: usa df_filtrado para incluir todas as lojas (inclusive Trajano)
    if not df_filtrado.empty:
        df_ranking = df_filtrado.nlargest(N_RANK, 'FAT_2026')[['LOJA', 'FAT_2026']].copy()
        df_ranking = df_ranking.sort_values('FAT_2026', ascending=True)

        fig_ranking = px.bar(
            df_ranking,
            x='FAT_2026',
            y='LOJA',
            orientation='h',
            labels={'FAT_2026': 'Faturamento (R$)', 'LOJA': ''},
            color='FAT_2026',
            color_continuous_scale=['#FFB347', '#FF8C00']
        )
        fig_ranking.update_layout(
            height=CHART_H,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT, family="Barlow, sans-serif", size=11),
            margin=dict(l=10, r=90, t=20, b=10),
            yaxis={'categoryorder': 'total ascending',
                   'tickfont': dict(color=TEXT, size=11)},
            xaxis={'tickprefix': 'R$ ', 'gridcolor': GRID,
                   'tickfont': dict(color=MUTED, size=10)},
            coloraxis_showscale=False,
            bargap=0.28,
        )
        st.plotly_chart(fig_ranking, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown('<div style="text-align:center;padding:2rem;color:#FF8C00;">Nenhuma loja encontrada.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Comparativo 2025 vs 2026</div>', unsafe_allow_html=True)

    # Mantém df_comparavel — exige dados de 2025
    if not df_comparavel.empty:
        df_comp = df_comparavel[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
        df_comp['VARIACAO_%'] = ((df_comp['FAT_2026'] - df_comp['FAT_2025']) / df_comp['FAT_2025']) * 100
        df_comp = df_comp.reindex(df_comp['VARIACAO_%'].abs().nlargest(N_COMP).index)
        df_comp = df_comp.sort_values('VARIACAO_%', ascending=True)

        cores = [PRIMARY if x >= 0 else "#FF6B35" for x in df_comp['VARIACAO_%']]
        y_font_size = 11

        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            x=df_comp['VARIACAO_%'],
            y=df_comp['LOJA'],
            orientation='h',
            marker_color=cores,
            text=df_comp['VARIACAO_%'].round(1).astype(str) + '%',
            textposition='outside',
            textfont=dict(color=TEXT, size=9, family="Barlow, sans-serif"),
            hovertemplate='<b>%{y}</b><br>Variação: %{x:.1f}%<extra></extra>',
        ))

        fig_comp.add_vline(x=0, line_color=GRID, line_width=1)
        fig_comp.update_layout(
            height=CHART_H,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT, family="Barlow, sans-serif"),
            margin=dict(l=10, r=70, t=20, b=10),
            xaxis=dict(ticksuffix='%', gridcolor=GRID,
                       tickfont=dict(color=MUTED, size=10)),
            yaxis=dict(tickfont=dict(color=TEXT, size=y_font_size)),
            showlegend=False,
            bargap=0.28,
        )
        st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown('<div class="warning-card">⚠️ Nenhuma loja possui dados completos para 2025 e 2026.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# RESUMO DE PERFORMANCE
# =========================================================

st.markdown("### 📈 Resumo de Performance (Lojas com dados completos)")

if not df_comparavel.empty:
    media_variacao = df_comparavel['VARIACAO_%'].mean()
    total_crescimento = (df_comparavel['VARIACAO_%'] > 0).sum()
    total_queda = (df_comparavel['VARIACAO_%'] < 0).sum()
    melhor_loja = df_comparavel.loc[df_comparavel['VARIACAO_%'].idxmax(), 'LOJA']
    melhor_variacao = df_comparavel['VARIACAO_%'].max()
    pior_loja = df_comparavel.loc[df_comparavel['VARIACAO_%'].idxmin(), 'LOJA']
    pior_variacao = df_comparavel['VARIACAO_%'].min()
    fat_2025_total = df_comparavel['FAT_2025'].sum()
    fat_2026_total = df_comparavel['FAT_2026'].sum()
    variacao_total = ((fat_2026_total - fat_2025_total) / fat_2025_total * 100) if fat_2025_total > 0 else 0

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
            <div class="summary-name">{melhor_loja}</div>
            <div class="summary-label">🏆 Melhor Performance</div>
            <div class="summary-sub">+{melhor_variacao:.1f}% vs 2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value">{len(df_comparavel)}</div>
            <div class="summary-label">🏪 Lojas Analisadas</div>
            <div class="summary-sub">Com dados completos</div>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value">R$ {fat_2025_total/1000000:.1f}M</div>
            <div class="summary-label">💰 Faturamento 2025</div>
        </div>
        """, unsafe_allow_html=True)
    with col7:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value">R$ {fat_2026_total/1000000:.1f}M</div>
            <div class="summary-label">💰 Faturamento 2026</div>
            <div class="summary-sub">{variacao_total:+.1f}% vs 2025</div>
        </div>
        """, unsafe_allow_html=True)
    with col8:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-name">{pior_loja}</div>
            <div class="summary-label">⚠️ Pior Performance</div>
            <div class="summary-sub">{pior_variacao:.1f}% vs 2025</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown('<div class="warning-card">⚠️ Não há dados suficientes para exibir o resumo de performance.</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

# =========================================================
# TABELA DE DETALHAMENTO
# =========================================================

st.markdown('<div class="sub-header">📊 Detalhamento por Loja (Comparativo 2025 vs 2026)</div>', unsafe_allow_html=True)

if not df_comparavel.empty:
    df_display = df_comparavel[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
    df_display['VARIACAO_%'] = ((df_display['FAT_2026'] - df_display['FAT_2025']) / df_display['FAT_2025']) * 100
    df_display['FAT_2025'] = df_display['FAT_2025'].apply(lambda x: f'R$ {x:,.2f}')
    df_display['FAT_2026'] = df_display['FAT_2026'].apply(lambda x: f'R$ {x:,.2f}')
    df_display['VARIACAO_%'] = df_display['VARIACAO_%'].apply(lambda x: f'{x:.1f}%')
    df_display.columns = ['Loja', 'Faturamento 2026', 'Faturamento 2025', 'Variação %']
    st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.markdown('<div class="warning-card">⚠️ Nenhuma loja possui dados completos para 2025 e 2026.</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# RANKING DETALHADO — usa components.html para evitar
# sanitização do Streamlit que quebra HTML customizado
# =========================================================
import streamlit.components.v1 as components

st.markdown('<div class="sub-header">📋 Ranking Detalhado por Performance</div>', unsafe_allow_html=True)

def build_ranking_iframe(datasets):
    PRIMARY      = "#FF8C00"
    PRIMARY_DARK = "#CC7000"
    ACCENT       = "#FFB347"
    BG_CARD      = "#181d28"
    BG_DARK      = "#0f131a"
    TEXT         = "#FFFFFF"
    MUTED        = "#9CA3AF"

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    medal_colors = {1: "#FFD700", 2: "#C0C0C0", 3: "#CD7F32"}

    cols_html = ""
    for title, rows in datasets:
        items = ""
        for rank, loja, valor_str, label, pct in rows:
            bar_pct = int(pct * 100)
            num = medals.get(rank, f"#{rank}")
            num_color = medal_colors.get(rank, PRIMARY)
            border_opacity = "0.55" if rank == 1 else ("0.35" if rank == 2 else ("0.22" if rank == 3 else "0.12"))
            bg_opacity = "0.13" if rank == 1 else ("0.08" if rank <= 3 else "0.05")
            items += f"""
            <div style="
                display:flex; align-items:center; gap:12px;
                background:rgba(255,140,0,{bg_opacity});
                border:1px solid rgba(255,140,0,{border_opacity});
                border-left:3px solid {PRIMARY};
                border-radius:12px; padding:10px 14px;
                margin-bottom:8px;
                transition:all .2s ease;
            ">
                <div style="font-size:1.4rem; min-width:30px; text-align:center;
                    color:{num_color}; font-family:'Barlow Condensed',sans-serif;
                    font-weight:800; line-height:1;">{num}</div>
                <div style="flex:1; min-width:0;">
                    <div style="font-family:'Barlow Condensed',sans-serif; font-size:.85rem;
                        font-weight:700; color:{TEXT}; text-transform:uppercase;
                        letter-spacing:.03em; white-space:nowrap; overflow:hidden;
                        text-overflow:ellipsis;">{loja}</div>
                    <div style="height:4px; background:rgba(255,255,255,.07);
                        border-radius:99px; margin-top:5px; overflow:hidden;">
                        <div style="height:100%; width:{bar_pct}%;
                            background:linear-gradient(90deg,{PRIMARY_DARK},{ACCENT});
                            border-radius:99px;"></div>
                    </div>
                </div>
                <div style="text-align:right; white-space:nowrap;">
                    <div style="font-family:'Barlow Condensed',sans-serif; font-size:1.05rem;
                        font-weight:800; color:{PRIMARY};">{valor_str}</div>
                    <div style="font-size:.68rem; color:{MUTED}; font-family:'Barlow',sans-serif;">{label}</div>
                </div>
            </div>"""

        cols_html += f"""
        <div style="flex:1; background:linear-gradient(145deg,{BG_CARD} 0%,{BG_DARK} 100%);
            border:1px solid rgba(255,140,0,.2); border-radius:18px; padding:18px 16px;
            box-shadow:0 8px 32px rgba(0,0,0,.4);">
            <div style="font-family:'Barlow Condensed',sans-serif; font-size:.95rem; font-weight:800;
                color:{PRIMARY}; text-transform:uppercase; letter-spacing:.08em;
                margin-bottom:14px; padding-bottom:10px;
                border-bottom:1px solid rgba(255,140,0,.2);">{title}</div>
            {items}
        </div>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:transparent; font-family:'Barlow',sans-serif; }}
  .cols {{ display:flex; gap:16px; }}
</style>
</head>
<body>
  <div class="cols">{cols_html}</div>
</body>
</html>"""


# CORRIGIDO: usa df_filtrado para incluir Trajano nos rankings de 2026
if not df_filtrado.empty:
    # Faturamento — todas as lojas
    top_fat = df_filtrado.nlargest(5, 'FAT_2026')[['LOJA','FAT_2026']].reset_index(drop=True)
    mx_fat = top_fat['FAT_2026'].max()
    rows_fat = [(i+1, r['LOJA'], f"R$ {r['FAT_2026']:,.0f}", "faturamento 2026", r['FAT_2026']/mx_fat)
                for i, r in top_fat.iterrows()]

    # Clientes — todas as lojas
    top_cli = df_filtrado.nlargest(5, 'TC_2026')[['LOJA','TC_2026']].reset_index(drop=True)
    mx_cli = top_cli['TC_2026'].max()
    rows_cli = [(i+1, r['LOJA'], f"{r['TC_2026']:,.0f}", "clientes atendidos", r['TC_2026']/mx_cli)
                for i, r in top_cli.iterrows()]

    # Ticket médio — todas as lojas
    top_tm = df_filtrado.nlargest(5, 'TM_2026')[['LOJA','TM_2026']].reset_index(drop=True)
    mx_tm = top_tm['TM_2026'].max()
    rows_tm = [(i+1, r['LOJA'], f"R$ {r['TM_2026']:,.2f}", "ticket médio", r['TM_2026']/mx_tm)
               for i, r in top_tm.iterrows()]

    datasets = [
        ("💰 TOP FATURAMENTO 2026", rows_fat),
        ("👥 MAIS CLIENTES 2026",   rows_cli),
        ("💎 MAIOR TICKET MÉDIO 2026", rows_tm),
    ]
    components.html(build_ranking_iframe(datasets), height=370, scrolling=False)
else:
    st.warning("Sem dados para exibir ranking.")

st.markdown("---")

# =========================================================
# ROW EXTRA: Ticket Médio + Clientes Radial + Crescimento
# =========================================================
import streamlit.components.v1 as components

st.markdown('<div class="sub-header">📊 Análise Complementar</div>', unsafe_allow_html=True)

col_tm, col_rad, col_grow = st.columns([2, 1.3, 1.7])

# --- TICKET MÉDIO POR LOJA ---
with col_tm:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💎 Ticket Médio por Loja (2026)</div>', unsafe_allow_html=True)

    # CORRIGIDO: usa df_filtrado para incluir Trajano
    if not df_filtrado.empty:
        ticket = df_filtrado['TM_2026'].mean()
        tm_sorted = df_filtrado.sort_values("TM_2026", ascending=True)
        bar_colors_tm = [PRIMARY if v >= ticket else "rgba(255,102,102,0.55)" for v in tm_sorted["TM_2026"]]

        fig_tm = go.Figure(go.Bar(
            x=tm_sorted["TM_2026"],
            y=tm_sorted["LOJA"],
            orientation="h",
            marker=dict(color=bar_colors_tm, line=dict(width=0)),
            text=tm_sorted["TM_2026"].apply(lambda x: f"R$ {x:.2f}"),
            textposition="outside",
            textfont=dict(color=TEXT, size=9),
            hovertemplate="<b>%{y}</b><br>TM: R$ %{x:.2f}<extra></extra>",
        ))
        fig_tm.add_vline(
            x=ticket, line_dash="dash", line_color=ACCENT,
            annotation_text=f"Média R$ {ticket:.2f}",
            annotation_font_color=ACCENT,
            annotation_position="top right",
        )
        fig_tm.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT, family="Barlow, sans-serif"),
            margin=dict(l=10, r=90, t=20, b=10),
            height=420,
            bargap=0.25,
        )
        fig_tm.update_xaxes(visible=False)
        fig_tm.update_yaxes(tickfont=dict(color=TEXT, size=10))
        st.plotly_chart(fig_tm, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown('<div style="text-align:center;padding:2rem;color:#FF8C00;">Sem dados.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CLIENTES RADIAL (ApexCharts via HTML) ---
with col_rad:
    st.markdown('<div class="section-card" style="height:100%">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👥 Top Clientes por Loja</div>', unsafe_allow_html=True)

    # CORRIGIDO: usa df_filtrado para incluir Trajano
    if not df_filtrado.empty:
        top4_tc   = df_filtrado.nlargest(4, "TC_2026")
        max_tc    = top4_tc["TC_2026"].max()
        rb_values = (top4_tc["TC_2026"] / max_tc * 100).round(1).tolist()
        rb_labels = top4_tc["LOJA"].tolist()
        rb_total  = int(df_filtrado["TC_2026"].sum())
        rb_raw    = top4_tc["TC_2026"].tolist()

        radial_html = f"""
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
            <style>body{{margin:0;background:transparent;}} #chart{{background:transparent;}}</style>
        </head>
        <body>
            <div id="chart"></div>
            <script>
                var rawValues = {rb_raw};
                var options = {{
                    series: {rb_values},
                    chart: {{
                        height: 380,
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
                                size: "28%",
                                background: "transparent",
                            }},
                            track: {{
                                background: "rgba(255,255,255,0.05)",
                                strokeWidth: "97%",
                            }},
                            dataLabels: {{
                                name: {{ fontSize: "12px", color: "#FFFFFF" }},
                                value: {{ fontSize: "11px", color: "#9CA3AF" }},
                                total: {{
                                    show: true,
                                    label: "Total",
                                    color: "#FFFFFF",
                                    fontSize: "13px",
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
                        fontSize: "10px",
                        position: "left",
                        offsetX: 8,
                        offsetY: 12,
                        labels: {{ useSeriesColors: true }},
                        formatter: function(seriesName, opts) {{
                            return seriesName + ": " + rawValues[opts.seriesIndex];
                        }},
                        itemMargin: {{ vertical: 3 }},
                    }},
                    tooltip: {{
                        theme: "dark",
                        y: {{ formatter: function(val, opts) {{ return rawValues[opts.seriesIndex] + " clientes"; }} }}
                    }},
                }};
                var chart = new ApexCharts(document.querySelector("#chart"), options);
                chart.render();
            </script>
        </body>
        </html>
        """
        components.html(radial_html, height=400, scrolling=False)
    else:
        st.markdown('<div style="text-align:center;padding:2rem;color:#FF8C00;">Sem dados.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- CRESCIMENTO VS 2025 ---
with col_grow:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚀 Crescimento vs 2025 (%)</div>', unsafe_allow_html=True)

    # Mantém df_comparavel — exige dados de 2025
    if not df_comparavel.empty:
        df_grow = df_comparavel[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
        df_grow["VAR"] = ((df_grow["FAT_2026"] - df_grow["FAT_2025"]) / df_grow["FAT_2025"]) * 100
        df_grow = df_grow.sort_values("VAR", ascending=True)
        bar_col_var = [PRIMARY if v >= 0 else "#FF4444" for v in df_grow["VAR"]]

        fig_growth = go.Figure(go.Bar(
            x=df_grow["VAR"],
            y=df_grow["LOJA"],
            orientation="h",
            marker=dict(color=bar_col_var, line=dict(width=0)),
            text=df_grow["VAR"].apply(lambda x: f"{x:+.1f}%"),
            textposition="outside",
            textfont=dict(color=TEXT, size=9),
            hovertemplate="<b>%{y}</b><br>Crescimento: %{x:+.1f}%<extra></extra>",
        ))
        fig_growth.add_vline(x=0, line_color=GRID, line_width=1)
        fig_growth.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=TEXT, family="Barlow, sans-serif"),
            margin=dict(l=10, r=70, t=20, b=10),
            height=420,
            bargap=0.28,
        )
        fig_growth.update_xaxes(ticksuffix="%", tickfont=dict(color=MUTED, size=10), gridcolor=GRID)
        fig_growth.update_yaxes(tickfont=dict(color=TEXT, size=10))
        st.plotly_chart(fig_growth, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown('<div style="text-align:center;padding:2rem;color:#FF8C00;">Sem dados.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# ANÁLISE DO PRODUTO PROMOCIONAL
# =========================================================

st.markdown('<div class="sub-header">🍺 Análise do Produto Promocionado</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    # CORRIGIDO: usa df_filtrado para incluir Trajano
    df_prod = df_filtrado[df_filtrado['QUANTIDADE'] > 0][['LOJA', 'QUANTIDADE', 'VALOR_VENDA_PROD']].copy() if not df_filtrado.empty else pd.DataFrame()
    
    if not df_prod.empty:
        fig_prod = px.pie(
            df_prod,
            values='VALOR_VENDA_PROD',
            names='LOJA',
            title='Distribuição de Venda do Produto Promocional',
            color_discrete_sequence=[PRIMARY, SECONDARY, ACCENT, PRIMARY_DARK]
        )
        fig_prod.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT, family="Barlow, sans-serif"),
            legend=dict(font=dict(color=TEXT, size=10))
        )
        st.plotly_chart(fig_prod, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown('<div style="text-align:center;padding:2rem;color:#FF8C00;">Nenhuma venda do produto promocional registrada.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">📊 Participação no Faturamento</div>', unsafe_allow_html=True)
    
    # CORRIGIDO: usa df_filtrado para incluir Trajano
    df_part = df_filtrado[df_filtrado['PART.(%)'].notna()].nlargest(10, 'PART.(%)')[['LOJA', 'PART.(%)', 'VALOR_VENDA_PROD']].copy() if not df_filtrado.empty else pd.DataFrame()
    if not df_part.empty and df_part['PART.(%)'].sum() > 0:
        df_part['PART.(%)'] = df_part['PART.(%)'] * 100
        
        fig_part = px.bar(
            df_part,
            x='LOJA',
            y='PART.(%)',
            labels={'PART.(%)': 'Participação (%)', 'LOJA': ''},
            color='PART.(%)',
            color_continuous_scale=['#FFB347', '#FF8C00'],
            text=df_part['PART.(%)'].round(2).astype(str) + '%'
        )
        fig_part.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=TEXT, family="Barlow, sans-serif"),
            xaxis={'tickangle': 45, 'tickfont': dict(color=TEXT, size=10)},
            yaxis={'tickfont': dict(color=MUTED, size=10), 'gridcolor': GRID},
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_part, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown('<div style="text-align:center;padding:2rem;color:#FF8C00;">Nenhuma participação relevante registrada.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# TABELA DE DADOS COMPLETOS
# =========================================================

st.markdown('<div class="sub-header">📊 Dados Completos</div>', unsafe_allow_html=True)

# CORRIGIDO: usa df_filtrado para incluir Trajano
if not df_filtrado.empty:
    df_display_full = df_filtrado.copy()
    df_display_full['FAT_2026'] = df_display_full['FAT_2026'].apply(lambda x: f'R$ {x:,.2f}')
    df_display_full['FAT_2025'] = df_display_full['FAT_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
    df_display_full['TM_2026'] = df_display_full['TM_2026'].apply(lambda x: f'R$ {x:,.2f}')
    df_display_full['TM_2025'] = df_display_full['TM_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
    df_display_full['VALOR_VENDA_PROD'] = df_display_full['VALOR_VENDA_PROD'].apply(lambda x: f'R$ {x:,.2f}')
    df_display_full['PART.(%)'] = df_display_full['PART.(%)'].apply(lambda x: f'{x*100:.4f}%' if pd.notna(x) else 'N/A')
    st.dataframe(df_display_full, use_container_width=True, height=400)
else:
    st.markdown('<div class="warning-card">⚠️ Nenhuma loja encontrada.</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# QUADRO DE AVISOS
# =========================================================

import streamlit.components.v1 as components

components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Barlow:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: transparent; font-family: 'Barlow', sans-serif; padding: 1rem 0; }
</style>
</head>
<body>
<div style="background: #1a1a2e; border: 1px solid #FF8C00; border-radius: 12px; overflow: hidden;">

  <div style="background: rgba(255,140,0,0.15); border-bottom: 1px solid #FF8C00; padding: 0.75rem 1.25rem; display: flex; align-items: center; gap: 10px;">
    <span style="font-size: 16px;">&#128204;</span>
    <span style="font-size: 14px; font-weight: 600; color: #FF8C00; letter-spacing: 0.04em;">IMPORTANTE &#8212; NOTA SOBRE OS DADOS COMPARATIVOS</span>
  </div>

  <div style="padding: 1.25rem;">

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 1.25rem;">

      <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 1rem;">
        <div style="font-size: 12px; color: #aaa; margin-bottom: 6px; font-weight: 500;">&#128200; Total comparável</div>
        <div style="font-size: 28px; font-weight: 700; color: #4caf50;">+13%</div>
        <div style="font-size: 12px; color: #aaa; margin-top: 4px;">no faturamento</div>
      </div>

      <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 1rem;">
        <div style="font-size: 12px; color: #aaa; margin-bottom: 8px; font-weight: 500;">&#129372; Impacto da ação do balde</div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
          <span style="font-size: 13px; color: #ccc;">Taquaral</span>
          <span style="font-size: 13px; font-weight: 600; color: #4caf50;">+4,0%</span>
        </div>
        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
          <span style="font-size: 13px; color: #ccc;">Batel</span>
          <span style="font-size: 13px; font-weight: 600; color: #4caf50;">+3,9%</span>
        </div>
        <div style="display: flex; justify-content: space-between;">
          <span style="font-size: 13px; color: #ccc;">Torres</span>
          <span style="font-size: 13px; font-weight: 600; color: #4caf50;">+2,0%</span>
        </div>
      </div>

    </div>

    <div style="margin-bottom: 1rem;">
      <p style="margin: 0 0 0.75rem; font-size: 13px; color: #bbb; line-height: 1.6;">
        A loja abaixo foi inaugurada <strong style="color: #fff;">após o período de coleta de 2025</strong>
        e não possuem faturamento registrado para comparação:
      </p>
      <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        <span style="font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 6px; background: rgba(255,140,0,0.12); color: #FF8C00; border: 1px solid rgba(255,140,0,0.35);">Trajano</span>
      </div>
    </div>

    <div style="background: rgba(100,160,255,0.08); border: 1px solid rgba(100,160,255,0.25); border-radius: 8px; padding: 0.75rem 1rem; display: flex; gap: 10px; align-items: flex-start;">
      <span style="flex-shrink: 0; margin-top: 1px;">&#128269;</span>
      <p style="margin: 0; font-size: 13px; color: #b0c4de; line-height: 1.6;">
        A loja Trajano aparece em todos os rankings e análises de 2026, mas é <strong style="color: #fff;">excluída dos cálculos</strong>
        de <strong style="color: #fff;">variação percentual</strong>, <strong style="color: #fff;">comparativo 2025 vs 2026</strong>
        e <strong style="color: #fff;">resumo de performance</strong> por não possuir base de comparação no ano anterior.
      </p>
    </div>

  </div>
</div>
</body>
</html>
""", height=420, scrolling=False)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")
st.markdown(
    f"<div style='text-align:center;color:{MUTED};padding:.8rem;font-size:.82rem;font-family:Barlow, sans-serif;'>"
    f"Dashboard Espetto • Desenvolvido com Streamlit + Plotly • "
    f"Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    f"</div>",
    unsafe_allow_html=True
)
