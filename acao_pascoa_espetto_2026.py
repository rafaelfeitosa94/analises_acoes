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

# Configuração da página
st.set_page_config(
    page_title="🐰Pascoa Espetto 2026",
    page_icon="🐰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* ===== FUNDO GLOBAL ===== */
html, body, [class*="css"] {
    background-color: #0e1117 !important;
    color: #FAFAFA !important;
}

/* Container principal */
.main {
    background-color: #0e1117 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0e1117 !important;
}

/* ===== DATAFRAMES ===== */
[data-testid="stDataFrame"] {
    background-color: #0e1117 !important;
}

[data-testid="stDataFrame"] div {
    color: #FAFAFA !important;
}

/* Cabeçalho das tabelas */
[data-testid="stDataFrame"] thead tr th {
    background-color: #1a1d24 !important;
    color: #FFA500 !important;
}

/* Linhas da tabela */
[data-testid="stDataFrame"] tbody tr {
    background-color: #0e1117 !important;
    color: #FAFAFA !important;
}

/* Hover linha */
[data-testid="stDataFrame"] tbody tr:hover {
    background-color: #1a1d24 !important;
}

/* ===== TEXTOS STREAMLIT ===== */
h1, h2, h3, h4, h5, h6, p, span, label {
    color: #FAFAFA !important;
}

/* ===== SELECTS E INPUTS ===== */
.stSelectbox, .stMultiSelect, .stSlider {
    color: #FAFAFA !important;
}

/* ===== CARDS ===== */
.section-card {
    background-color: #161a22 !important;
    color: #FAFAFA !important;
    padding: 1.5rem;
    border-radius: 15px;
    margin-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Remove espaço branco do topo */
.block-container {
    padding-top: 0rem !important;
}

/* Remove header padding extra */
header[data-testid="stHeader"] {
    height: 0px;
}

/* Remove toolbar space */
[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0px;
    position: fixed;
}
</style>
""", unsafe_allow_html=True)

# Função para carregar o logo
@st.cache_data
def load_logo():
    try:
        url = "https://blogfranquia.espettocarioca.com.br/wp-content/uploads/2023/09/logo-site.png"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# CSS personalizado com cores laranja
st.markdown("""
<style>
    .sub-header {
        font-size: 1.5rem;
        color: #FFA500;
        margin-bottom: 1rem;
        border-bottom: 3px solid #FFA500;
        padding-bottom: 0.5rem;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #CC7000 0%, #FF8C00 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255,140,0,0.2);
        text-align: center;
        border: 1px solid #FFA500;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: white;
    }
    .metric-label {
        font-size: 1rem;
        color: white;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    .metric-variation {
        color: white;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    .ranking-container {
        background: linear-gradient(135deg, #CC7000 0%, #FF8C00 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255,140,0,0.2);
        height: 100%;
    }
    .ranking-title {
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        border-bottom: 2px solid #FFA500;
        padding-bottom: 0.5rem;
    }
    .ranking-item {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        border-left: 5px solid #FFA500;
        transition: transform 0.2s;
    }
    .ranking-item:hover {
        transform: translateX(5px);
        background-color: rgba(255, 165, 0, 0.2);
    }
    .ranking-item strong {
        color: white;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    .ranking-item .ranking-value {
        color: #FFA500;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .ranking-item .ranking-label {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
    }
    .ranking-badge {
        background-color: #FFA500;
        color: #CC7000;
        font-weight: bold;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .filter-section {
        background: linear-gradient(135deg, #2a1a0f 0%, #1a0f0a 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #FFA500;
    }
    .summary-card {
        background: linear-gradient(135deg, #CC7000 0%, #FF8C00 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #FFA500;
        transition: transform 0.2s;
    }
    .summary-card:hover {
        transform: translateY(-5px);
    }
    .summary-value {
        font-size: 2rem;
        font-weight: bold;
        color: white;
    }
    .summary-label {
        color: white;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    .summary-sub {
        color: white;
        font-size: 0.8rem;
        margin-top: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Carregar o logo
logo = load_logo()

# CABEÇALHO CENTRALIZADO
st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-bottom: 2rem; padding: 1rem; background: linear-gradient(135deg, #2a1a0f 0%, #1a0f0a 100%); border-radius: 20px; box-shadow: 0 4px 15px rgba(255,140,0,0.1); width: 100%;">
""", unsafe_allow_html=True)

# Logo centralizado
if logo:
    buffered = BytesIO()
    logo.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    st.markdown(f"""
    <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
        <img src="data:image/png;base64,{img_str}" width="250" style="display: block;">
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(
        '<p style="color:#FFA500;font-weight:bold;text-align:center;">Logo não disponível</p>',
        unsafe_allow_html=True
    )

# Título principal
st.markdown("""
<h1 style="font-size: 2.5rem; color: #FFA500; font-weight: bold; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(255,140,0,0.1); text-align: center;">🐰 PÁSCOA ESPETTO 2026 🥕</h1>
""", unsafe_allow_html=True)

# Subtítulo
st.markdown("""
<div style="display: flex; justify-content: center; width: 100%; margin-top: 0.5rem;">
    <p style="background: linear-gradient(135deg, #CC7000 0%, #FF8C00 100%); color: white; font-weight: bold; font-size: 1.2rem; padding: 0.8rem 2rem; border-radius: 50px; box-shadow: 0 4px 10px rgba(255,140,0,0.3); margin: 0; display: inline-block; text-align: center;">Mês completo de Abril/2026</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Dados fornecidos
data = {
    'MARCA': ['ESPETTO'] * 33,
    'LOJA': [
        'ESP ALPHAVILLE', 'ESP VILLA LOBOS', 'ESP VALQUEIRE LOUNGE', 'ESP OLEGÁRIO', 'ESP PENINSULA',
        'ESP NY', 'ESP RECREIO', 'ESP GRANDE RIO', 'ESP PARK SHOP CG', 'ESP COPA PRAIA',
        'ESP SULACAP', 'ESP JARDINS', 'ESP BARRA SUL', 'ESP ICARAÍ', 'ESP ANDRADINA',
        'ESP CAXIAS SHOPPING', 'ESP PIRATININGA', 'ESP UBERLÂNDIA', 'ESP GOIÂNIA', 'ESP TATUAPÉ',
        'ESP VISTA ALEGRE', 'ESP AMERICANA', 'ESP RIO DAS OSTRAS', 'ESP CHÁCARA ST', 'ESP SALVADOR',
        'ESP AEROTOWN', 'ESP BELA VISTA', 'ESP GUADALUPE', 'ESP QUIOSQUE NORTE SHOP', 'ESP QUIOSQUE MACAÉ',
        'ESP CAXIAS CARREFOUR', 'ESP QUIOSQUE CABO FRIO', 'ESP ENGENHÃO'
    ],
    'FAT_2026': [
        706253.5, 605020.6, 567714.72, 491809.33, 353695.81,
        344985.98, 344205.55, 310249.65, 286023.15, 279751.87,
        275303.92, 267306.08, 245254.24, 239986.49, 220263.43,
        192612.43, 191486.73, 186135.37, 179120.76, 167449.42,
        155437.75, 149207.96, 136453.85, 112275.84, 103401.37,
        101775.52, 91664.69, 71800.95, 67716.09, 44470.46,
        43832.31, 30872.35, 11494.2
    ],
    'TC_2026': [
        6495, 9044, 7746, 5253, 4695,
        3317, 3910, 3282, 3414, 3582,
        2772, 3887, 3544, 2940, 893,
        2769, 2146, 3565, 2011, 1999,
        2058, 1188, 1277, 2319, 1180,
        1565, 1211, 1218, 1737, 1043,
        911, 617, 507
    ],
    'TM_2026': [
        108.74, 66.9, 73.29, 93.62, 75.33,
        104.01, 88.03, 94.53, 83.78, 78.1,
        99.32, 68.77, 69.2, 81.63, 246.66,
        69.56, 89.23, 52.21, 89.07, 83.77,
        75.53, 125.6, 106.86, 48.42, 87.63,
        65.03, 75.69, 58.95, 38.98, 42.64,
        48.11, 50.04, 22.67
    ],
    'FAT_2025': [
        563816.97, 1659428.13, 534195.68, 338682.86, 249743.15,
        293441.26, 254398.18, 213668.05, 294465.39, 369023.74,
        3231964.04, 250335.62, 190609.79, 308306.72, 159310.66,
        184131.74, 525292.33, 208864.86, 40063.1, 745839.66,
        148174.06, 935721.26, 232803.52, 131430.33, 103844.35,
        85882.72, 318880.08, 121974.79, 59549.96, 49682.89,
        60579.87, 33683.84, 23663.5
    ],
    'TC_2025': [
        5878, 25649, 1614, 3116, 3792,
        3083, 2983, 5350, 3293, 5527,
        27678, 3167, 2293, 3695, 925,
        2712, 4753, 2415, 696, 9608,
        1826, 7811, 2441, 1524, 1235,
        1384, 4653, 1939, 1542, 1086,
        1268, 583, 1082
    ],
    'TM_2025': [
        95.9198656005444, 64.69757612382548, 330.97625774473363, 108.69154685494223, 65.86053533755275,
        95.18042815439507, 85.28266174991619, 39.937953271028036, 89.42161858487701, 66.76745793377962,
        116.77014379651709, 79.04503315440479, 83.12681639773223, 83.43889580514208, 172.22774054054054,
        67.8951843657817, 110.51805806858825, 86.48648447204968, 57.56192528735632, 77.62694213155704,
        81.1468017524644, 119.7953219818205, 95.37219172470299, 86.24037401574802, 84.08449392712551,
        62.05398843930636, 68.53214700193423, 62.90602888086642, 38.618651102464334, 45.748517495395944,
        47.775922712933756, 57.776740994854194, 21.870147874306838
    ],
    'PROD_PROMOCIONADO': [''] * 33,
    'COMPOSICAO_PROD': [''] * 33,
    'QUANTIDADE': [0] * 33,
    'VALOR_VENDA_PROD': [0] * 33,
    'PART.(%)': [0] * 33
}

df = pd.DataFrame(data)

# Sidebar para filtros
with st.sidebar:
    st.markdown('<h2 style="color: #FFA500;">🎯 Filtros</h2>', unsafe_allow_html=True)
    
    # Filtro de lojas
    lojas_selecionadas = st.multiselect(
        "Selecione as lojas:",
        options=df['LOJA'].unique(),
        default=df['LOJA'].unique()
    )
    
    # Filtro de faixa de faturamento
    fat_min, fat_max = st.slider(
        "Faixa de faturamento 2026 (R$):",
        min_value=float(df['FAT_2026'].min()),
        max_value=float(df['FAT_2026'].max()),
        value=(float(df['FAT_2026'].min()), float(df['FAT_2026'].max()))
    )

# Aplicar filtros
df_filtrado = df[
    (df['LOJA'].isin(lojas_selecionadas)) &
    (df['FAT_2026'] >= fat_min) &
    (df['FAT_2026'] <= fat_max)
]

# Métricas principais
st.markdown('<h2 class="sub-header">📊 Visão Geral</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    fat_total_2025 = df_filtrado['FAT_2025'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_2025:,.2f}</div>
        <div class="metric-label">Faturamento Total 2025</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    fat_total_2026 = df_filtrado['FAT_2026'].sum() if not df_filtrado['FAT_2026'].isna().all() else 0
    variacao = ((fat_total_2026 - fat_total_2025) / fat_total_2025 * 100) if fat_total_2025 > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_2026:,.2f}</div>
        <div class="metric-label">Faturamento Total 2026</div>
        <div class="metric-variation">{variacao:+.1f}% vs 2025</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    clientes_total = df_filtrado['TC_2026'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{clientes_total:,.0f}</div>
        <div class="metric-label">Total de Clientes 2026</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    tm_medio = df_filtrado['TM_2026'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {tm_medio:,.2f}</div>
        <div class="metric-label">Ticket Médio Médio 2026</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Gráficos em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFA500;">🏆 Ranking de Faturamento 2026</h3>', unsafe_allow_html=True)
    
    df_ranking = df_filtrado.nlargest(10, 'FAT_2026')[['LOJA', 'FAT_2026']].copy()
    df_ranking = df_ranking.sort_values('FAT_2026', ascending=True)
    
    fig_ranking = px.bar(
        df_ranking,
        x='FAT_2026',
        y='LOJA',
        orientation='h',
        title='Top Lojas por Faturamento',
        labels={'FAT_2026': 'Faturamento (R$)', 'LOJA': 'Loja'},
        color='FAT_2026',
        color_continuous_scale=['#FFCC99', '#FF8C00']
    )
    fig_ranking.update_layout(
        height=400, 
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig_ranking, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFA500;">📈 Comparativo 2025 vs 2026</h3>', unsafe_allow_html=True)
    
    df_comp = df_filtrado[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
    df_comp = df_comp.dropna(subset=['FAT_2025'])
    
    if not df_comp.empty:
        df_comp['VARIACAO_%'] = ((df_comp['FAT_2026'] - df_comp['FAT_2025']) / df_comp['FAT_2025']) * 100
        df_comp = df_comp.sort_values('VARIACAO_%', ascending=False).reset_index(drop=True)
        
        cores = ['#FF8C00' if x >= 0 else "#FFCC99" for x in df_comp['VARIACAO_%']]
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            x=df_comp['LOJA'],
            y=df_comp['VARIACAO_%'],
            marker_color=cores,
            text=df_comp['VARIACAO_%'].round(1).astype(str) + '%',
            textposition='outside',
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>%{x}</b><br>' +
                         'Variação: %{y:.1f}%<br>' +
                         '2025: R$ %{customdata[0]:,.2f}<br>' +
                         '2026: R$ %{customdata[1]:,.2f}<extra></extra>',
            customdata=df_comp[['FAT_2025', 'FAT_2026']].values,
            width=0.6
        ))
        
        fig_comp.add_hline(y=0, line_dash="solid", line_color="#666", line_width=1)
        
        fig_comp.update_layout(
            title=None,
            xaxis_title=None,
            yaxis_title=None,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            yaxis=dict(
                ticksuffix='%',
                gridcolor='rgba(255,255,255,0.1)',
                gridwidth=1,
                zeroline=False
            ),
            xaxis=dict(
                tickangle=45,
                tickfont=dict(size=11, color='white')
            ),
            showlegend=False,
            margin=dict(l=40, r=40, t=20, b=80)
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("---")

# Tabela de detalhamento
st.markdown("### 📊 Detalhamento por Loja")

df_display = df_comp.copy()
df_display['FAT_2025'] = df_display['FAT_2025'].apply(lambda x: f'R$ {x:,.2f}')
df_display['FAT_2026'] = df_display['FAT_2026'].apply(lambda x: f'R$ {x:,.2f}')
df_display['VARIACAO_%'] = df_display['VARIACAO_%'].apply(lambda x: f'{x:.1f}%')
df_display.columns = ['Loja', 'Faturamento 2026', 'Faturamento 2025', 'Variação %']

st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# RESUMO COM CARDS
st.markdown("### 📈 Resumo de Performance")

if not df_comp.empty:
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
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1.5rem;">R$ {fat_total_2025/1000000:.1f}M</div>
            <div class="summary-label">💰 Faturamento 2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col7:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1.5rem;">R$ {fat_total_2026/1000000:.1f}M</div>
            <div class="summary-label">💰 Faturamento 2026</div>
            <div class="summary-sub">{variacao:+.1f}% vs 2025</div>
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

st.markdown("---")

# Ranking detalhado
st.markdown('<h2 class="sub-header">📋 Ranking Detalhado por Performance</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="ranking-title">💰 TOP FATURAMENTO</div>', unsafe_allow_html=True)
    top_fat = df_filtrado.nlargest(5, 'FAT_2026')[['LOJA', 'FAT_2026']]
    for i, (idx, row) in enumerate(top_fat.iterrows(), 1):
        st.markdown(f"""
        <div class="ranking-item">
            <span class="ranking-badge">#{i}</span>
            <strong>{row['LOJA']}</strong>
            <div class="ranking-value">R$ {row['FAT_2026']:,.2f}</div>
            <div class="ranking-label">faturamento 2026</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="ranking-title">👥 MAIS CLIENTES</div>', unsafe_allow_html=True)
    top_clientes = df_filtrado.nlargest(5, 'TC_2026')[['LOJA', 'TC_2026']]
    for i, (idx, row) in enumerate(top_clientes.iterrows(), 1):
        st.markdown(f"""
        <div class="ranking-item">
            <span class="ranking-badge">#{i}</span>
            <strong>{row['LOJA']}</strong>
            <div class="ranking-value">{row['TC_2026']:,.0f}</div>
            <div class="ranking-label">clientes atendidos</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="ranking-title">💎 MAIOR TICKET MÉDIO</div>', unsafe_allow_html=True)
    top_tm = df_filtrado.nlargest(5, 'TM_2026')[['LOJA', 'TM_2026']]
    for i, (idx, row) in enumerate(top_tm.iterrows(), 1):
        st.markdown(f"""
        <div class="ranking-item">
            <span class="ranking-badge">#{i}</span>
            <strong>{row['LOJA']}</strong>
            <div class="ranking-value">R$ {row['TM_2026']:,.2f}</div>
            <div class="ranking-label">ticket médio</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Tabela de dados completa
st.markdown('<h2 class="sub-header">📊 Dados Completos</h2>', unsafe_allow_html=True)

df_display_full = df_filtrado.copy()
df_display_full['FAT_2026'] = df_display_full['FAT_2026'].apply(lambda x: f'R$ {x:,.2f}')
df_display_full['FAT_2025'] = df_display_full['FAT_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
df_display_full['TM_2026'] = df_display_full['TM_2026'].apply(lambda x: f'R$ {x:,.2f}')
df_display_full['TM_2025'] = df_display_full['TM_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
df_display_full['VALOR_VENDA_PROD'] = df_display_full['VALOR_VENDA_PROD'].apply(lambda x: f'R$ {x:,.2f}')
df_display_full['PART.(%)'] = df_display_full['PART.(%)'].apply(lambda x: f'{x*100:.4f}%')

st.dataframe(
    df_display_full,
    use_container_width=True,
    height=400
)

# Rodapé
st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: #FFA500;'>Dashboard desenvolvido com Streamlit • Dados atualizados em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>",
    unsafe_allow_html=True
)