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
    page_title="Dia das Mães Mané 2026",
    page_icon="🌹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# COLORS - TONS DE VERMELHO (MARCA MANÉ)
# =========================================================

PRIMARY      = "#8B0000"      # Vermelho escuro principal
PRIMARY_DARK = "#5C0000"      # Vermelho mais escuro
SECONDARY    = "#B22222"      # Vermelho médio
ACCENT       = "#FF6666"      # Vermelho claro

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
    border-right: 1px solid rgba(139,0,0,0.1);
}}
section[data-testid="stSidebar"] * {{ color: {TEXT} !important; font-family: 'Barlow', sans-serif !important; }}
h1,h2,h3,h4,h5,h6 {{ font-family: 'Barlow Condensed', sans-serif !important; color: {TEXT} !important; }}
p, span, label, div {{ color: {TEXT} !important; font-family: 'Barlow', sans-serif !important; }}

/* ---- METRIC CARDS ---- */
.metric-card {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border: 1px solid rgba(139,0,0,0.25);
    border-radius: 16px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: transform .25s ease, border-color .25s ease;
    box-shadow: 0 6px 24px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.04);
    height: 100%;
    text-align: center;
}}
.metric-card:hover {{ transform: translateY(-3px); border-color: rgba(139,0,0,.6); }}
.metric-card::after {{
    content: '';
    position: absolute;
    width: 120px; height: 120px;
    background: radial-gradient(circle, rgba(139,0,0,.10) 0%, transparent 70%);
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
    border: 1px solid rgba(139,0,0,0.25);
    border-radius: 16px;
    padding: 1rem 0.9rem;
    text-align: center;
    transition: all 0.25s ease;
    height: 100%;
}}
.summary-card:hover {{
    transform: translateY(-2px);
    border-color: rgba(139,0,0,.6);
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
    border: 1px solid rgba(139,0,0,0.25);
    border-radius: 20px;
    padding: 1rem;
    text-align: center;
    color: {ACCENT} !important;
    font-family: 'Barlow', sans-serif;
    font-size: 0.9rem;
}}
.info-card {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border: 1px solid rgba(139,0,0,0.25);
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

/* ---- RANKING CARDS ---- */
.ranking-wrap {{
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
}}
.rank-card {{
    display: flex;
    align-items: center;
    gap: 0.9rem;
    background: rgba(139,0,0,0.06);
    border: 1px solid rgba(139,0,0,0.15);
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
    background: rgba(139,0,0,0.12);
    border-color: rgba(139,0,0,0.4);
    transform: translateX(4px);
}}
.rank-card.rank-1 {{ border-color: rgba(139,0,0,0.5); background: rgba(139,0,0,0.10); }}
.rank-card.rank-2 {{ border-color: rgba(178,34,34,0.35); }}
.rank-card.rank-3 {{ border-color: rgba(255,102,102,0.25); }}

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
    border-bottom: 1px solid rgba(139,0,0,0.2);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.ranking-outer {{
    background: linear-gradient(145deg, #181d28 0%, #0f131a 100%);
    border: 1px solid rgba(139,0,0,0.2);
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
        url = "https://botecomane.com.br/wp-content/uploads/2024/06/mane-logo-vermelho.png"
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
    border: 1px solid rgba(139,0,0,0.2);
    margin-bottom: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
">
    <div style="position:absolute;top:-80px;left:50%;transform:translateX(-50%);
        width:400px;height:400px;
        background:radial-gradient(circle,rgba(139,0,0,.08) 0%,transparent 70%);
        pointer-events:none;"></div>
    {img_tag}
    <div style="font-family:'Barlow Condensed', sans-serif;font-size:2.4rem;font-weight:800;
        color:#8B0000;letter-spacing:-0.5px;line-height:1.1;text-transform:uppercase;">
        🌹 Dia das Mães Mané 2026 🌹
    </div>
    <div style="color:{MUTED};font-size:0.92rem;margin-top:.5rem;font-family:'Barlow', sans-serif;">
        Performance das lojas &nbsp;•&nbsp; 09 à 10/05/2026 vs 10 à 11/05/2025
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================

data = {
    'MARCA': ['MANÉ'] * 19,
    'LOJA': [
        'MAN NITERÓI', 'MAN NOVA AMÉRICA', 'MAN SÃO GONÇALO', 'MAN NOVA IGUAÇÚ',
        'MAN VILA VELHA', 'MAN MACAÉ', 'MAN RIO DAS OSTRAS', 'MAN PARK SHOP CG',
        'MAN FLAMENGO', 'MAN VILA DA PENHA', 'MAN BÚZIOS', 'MAN COPA PRAIA',
        'MAN ITAIPAVA', 'MAN COLLAB VALQUEIRE', 'MAN RECREIO', 'MAN IPANEMA',
        'MAN COPACABANA', 'MAN COLLAB CABO FRIO', 'MAN OLEGÁRIO'
    ],
    'FAT_2026': [
        66628.04, 53658.56, 51281.30, 35154.88, 33784.95, 30964.88, 29635.87,
        28291.05, 25555.76, 22499.26, 18549.01, 18448.84, 16567.01, 12910.43,
        11936.42, 10610.61, 9569.13, 9502.96, 5314.21
    ],
    'TC_2026': [
        512, 469, 383, 356, 367, 224, 202, 210, 335, 262, 192, 247, 223,
        136, 141, 227, 124, 107, 54
    ],
    'TM_2026': [
        130.13, 114.41, 133.89, 98.75, 92.06, 138.24, 146.71, 134.72,
        76.29, 85.88, 96.61, 74.69, 74.29, 94.93, 84.66, 46.74, 77.17,
        88.81, 98.41
    ],
    'FAT_2025': [
        66808.82, 58182.41, 48542.83, None, None, 28180.64, 32518.15,
        30372.83, 17960.38, 26318.11, 27872.83, 12363.86, 14886.23,
        11022.24, 22844.57, 7072.90, 7181.39, 19824.74, 8691.22
    ],
    'TC_2025': [
        563, 698, 356, None, None, 207, 501, 216, 201, 253, 293, 146,
        187, 72, 153, 121, 68, 82, 114
    ],
    'TM_2025': [
        118.66575488454708, 83.355888252149, 136.35626404494383, None, None,
        136.1383574879227, 64.90648702594811, 140.61495370370372,
        89.35512437810945, 104.02415019762846, 95.12911262798636,
        84.68397260273973, 79.60550802139038, 153.08666666666667,
        149.31091503267973, 58.45371900826446, 105.60867647058824,
        241.76512195121953, 76.23877192982455
    ],
    'PROD_PROMOCIONADO': ['SEM PRODUTO'] * 19,
    'QUANTIDADE_BOTAO': [0] * 19,
    'COMPOSICAO_PROD': [''] * 19,
    'QUANTIDADE': [0] * 19,
    'VALOR_VENDA_PROD': [0] * 19,
    'PART.(%)': [0] * 19
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
        f"Dia das Mães Mané 2026<br>Dashboard de Performance</div>",
        unsafe_allow_html=True
    )

# Aplicar filtros
df_filtrado = df[
    (df['LOJA'].isin(lojas_selecionadas)) &
    (df['FAT_2026'] >= fat_min) &
    (df['FAT_2026'] <= fat_max)
]

# ==== CRIAR DATAFRAME APENAS COM LOJAS QUE TÊM AMBOS OS ANOS ====
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
    clientes_total = df_comparavel['TC_2026'].sum() if not df_comparavel.empty else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{clientes_total:,.0f}</div>
        <div class="metric-label">Total de Clientes 2026</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    tm_medio = fat_total_2026 / clientes_total if clientes_total > 0 else 0
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
            ⚠️ As seguintes lojas não possuem dados completos para 2025 e não estão incluídas nas métricas acima:<br>
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
            color_continuous_scale=['#FF6666', '#8B0000']
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
        st.markdown('<div style="text-align:center;padding:2rem;color:#8B0000;">Nenhuma loja com dados.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Comparativo 2025 vs 2026</div>', unsafe_allow_html=True)

    if not df_comparavel.empty:
        df_comp = df_comparavel[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
        df_comp['VARIACAO_%'] = ((df_comp['FAT_2026'] - df_comp['FAT_2025']) / df_comp['FAT_2025']) * 100
        df_comp = df_comp.reindex(df_comp['VARIACAO_%'].abs().nlargest(N_COMP).index)
        df_comp = df_comp.sort_values('VARIACAO_%', ascending=True)

        cores = [PRIMARY if x >= 0 else "#FF6666" for x in df_comp['VARIACAO_%']]
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
    """
    datasets: list of (title, rows)
      rows: list of (rank, loja, valor_str, label, pct_of_max)
    Returns a full self-contained HTML page for components.html()
    """
    PRIMARY      = "#8B0000"
    PRIMARY_DARK = "#5C0000"
    ACCENT       = "#FF6666"
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
                background:rgba(139,0,0,{bg_opacity});
                border:1px solid rgba(139,0,0,{border_opacity});
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
            border:1px solid rgba(139,0,0,.2); border-radius:18px; padding:18px 16px;
            box-shadow:0 8px 32px rgba(0,0,0,.4);">
            <div style="font-family:'Barlow Condensed',sans-serif; font-size:.95rem; font-weight:800;
                color:{PRIMARY}; text-transform:uppercase; letter-spacing:.08em;
                margin-bottom:14px; padding-bottom:10px;
                border-bottom:1px solid rgba(139,0,0,.2);">{title}</div>
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


if not df_filtrado.empty:
    # Faturamento
    top_fat = df_filtrado.nlargest(5, 'FAT_2026')[['LOJA','FAT_2026']].reset_index(drop=True)
    mx_fat = top_fat['FAT_2026'].max()
    rows_fat = [(i+1, r['LOJA'], f"R$ {r['FAT_2026']:,.0f}", "faturamento 2026", r['FAT_2026']/mx_fat)
                for i, r in top_fat.iterrows()]

    # Clientes
    top_cli = df_filtrado.nlargest(5, 'TC_2026')[['LOJA','TC_2026']].reset_index(drop=True)
    mx_cli = top_cli['TC_2026'].max()
    rows_cli = [(i+1, r['LOJA'], f"{r['TC_2026']:,.0f}", "clientes atendidos", r['TC_2026']/mx_cli)
                for i, r in top_cli.iterrows()]

    # Ticket médio
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
        st.markdown('<div style="text-align:center;padding:2rem;color:#8B0000;">Sem dados.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CLIENTES RADIAL (ApexCharts via HTML) ---
with col_rad:
    st.markdown('<div class="section-card" style="height:100%">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👥 Top Clientes por Loja</div>', unsafe_allow_html=True)

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
        st.markdown('<div style="text-align:center;padding:2rem;color:#8B0000;">Sem dados.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- CRESCIMENTO VS 2025 ---
with col_grow:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚀 Crescimento vs 2025 (%)</div>', unsafe_allow_html=True)

    if not df_comparavel.empty:
        df_grow = df_comparavel[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
        df_grow["VAR"] = ((df_grow["FAT_2026"] - df_grow["FAT_2025"]) / df_grow["FAT_2025"]) * 100
        df_grow = df_grow.sort_values("VAR", ascending=True)
        bar_col_var = [PRIMARY if v >= 0 else "#FF6666" for v in df_grow["VAR"]]

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
        st.markdown('<div style="text-align:center;padding:2rem;color:#8B0000;">Sem dados comparativos.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# TABELA DE DADOS COMPLETOS
# =========================================================

st.markdown('<div class="sub-header">📊 Dados Completos</div>', unsafe_allow_html=True)

if not df_filtrado.empty:
    df_display_full = df_filtrado.copy()
    df_display_full['FAT_2026'] = df_display_full['FAT_2026'].apply(lambda x: f'R$ {x:,.2f}')
    df_display_full['FAT_2025'] = df_display_full['FAT_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
    df_display_full['TM_2026'] = df_display_full['TM_2026'].apply(lambda x: f'R$ {x:,.2f}')
    df_display_full['TM_2025'] = df_display_full['TM_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
    df_display_full['VALOR_VENDA_PROD'] = df_display_full['VALOR_VENDA_PROD'].apply(lambda x: f'R$ {x:,.2f}')
    df_display_full['PART.(%)'] = df_display_full['PART.(%)'].apply(lambda x: f'{x*100:.4f}%')
    st.dataframe(df_display_full, use_container_width=True, height=400)
else:
    st.markdown('<div class="warning-card">⚠️ Nenhuma loja com dados para exibir.</div>', unsafe_allow_html=True)

st.markdown("---")

# =========================================================
# QUADRO DE AVISOS
# =========================================================

st.markdown("""
<div style="margin-top: 2rem;">
    <div class="info-card">
        <div class="info-title">
            📌 IMPORTANTE — NOTA SOBRE OS DADOS COMPARATIVOS
        </div>
        <div class="info-text">
            As lojas listadas abaixo ainda não haviam inaugurado na data de referência da coleta de dados de 2025, 
            portanto não possuem faturamento registrado para o ano de 2025:
        </div>
        <ul class="info-list">
            <li><strong style="color: #8B0000;">MAN NOVA IGUAÇÚ</strong> — Inaugurada após o período de coleta de 2025</li>
            <li><strong style="color: #8B0000;">MAN VILA VELHA</strong> — Inaugurada após o período de coleta de 2025</li>
        </ul>
        <div class="info-text" style="margin-top: 0.8rem;">
            🔍 Estas lojas são exibidas nos rankings e métricas de 2026, mas não entram nos cálculos de 
            <strong>variação percentual</strong>, <strong>comparativo 2025 vs 2026</strong> e 
            <strong>resumo de performance</strong> por não possuírem base de comparação no ano anterior.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")
st.markdown(
    f"<div style='text-align:center;color:{MUTED};padding:.8rem;font-size:.82rem;font-family:Barlow, sans-serif;'>"
    f"Dashboard Mané • Desenvolvido com Streamlit + Plotly • "
    f"Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    f"</div>",
    unsafe_allow_html=True
)
