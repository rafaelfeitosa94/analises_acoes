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
    page_title="Dashboard Espetto - Análise de Vendas",
    page_icon="🍺",
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

# CSS personalizado com cores laranja e amarelo
st.markdown("""
<style>
    .sub-header {
        font-size: 1.5rem;
        color: #FF8C00;
        margin-bottom: 1rem;
        border-bottom: 3px solid #FFD700;
        padding-bottom: 0.5rem;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #FF8C00 0%, #FFA500 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255,140,0,0.2);
        text-align: center;
        border: 1px solid #FFD700;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: white;
    }
    .metric-label {
        font-size: 1rem;
        color: white !important;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    .metric-variation {
        color: #98FB98;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    .ranking-container {
        background: linear-gradient(135deg, #FF8C00 0%, #FFA500 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(255,140,0,0.2);
        height: 100%;
    }
    .ranking-title {
        color: #FFD700;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        border-bottom: 2px solid #FFD700;
        padding-bottom: 0.5rem;
    }
    .ranking-item {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        backdrop-filter: blur(5px);
        transition: transform 0.2s;
    }
    .ranking-item:hover {
        transform: translateX(5px);
        background-color: rgba(255, 215, 0, 0.2);
    }
    .ranking-item strong {
        color: white;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    .ranking-item .ranking-value {
        color: #FFD700;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .ranking-item .ranking-label {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
    }
    .ranking-badge {
        background-color: #FFA500;
        color: #FF8C00;
        font-weight: bold;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .section-card {
        background-color: #161a22;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(255,140,0,0.1);
        margin-bottom: 1rem;
    }
    .filter-section {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFF8E7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #FFD700;
    }
    .st-emotion-cache-16idsys p {
        color: #FF8C00;
    }
    .st-emotion-cache-1dj0hjr {
        color: #FF8C00;
    }
    footer {
        color: #FF8C00;
    }
    .center-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# Carregar o logo
logo = load_logo()

# CABEÇALHO CENTRALIZADO
st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-bottom: 2rem; padding: 1rem; background: linear-gradient(135deg, #FFF3E0 0%, #FFF8E7 100%); border-radius: 20px; box-shadow: 0 4px 15px rgba(255,140,0,0.1); width: 100%;">
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
        '<p style="color:#FF8C00;font-weight:bold;text-align:center;">Logo não disponível</p>',
        unsafe_allow_html=True
    )

# Título principal
st.markdown("""
<h1 style="font-size: 2.5rem; color: #FF8C00; font-weight: bold; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(255,140,0,0.1); text-align: center;">🍺 CARNAVAL ESPETTO 2026</h1>
""", unsafe_allow_html=True)

# Subtítulo com gradiente laranja
st.markdown("""
<div style="display: flex; justify-content: center; width: 100%; margin-top: 0.5rem;">
    <p style="background: linear-gradient(135deg, #FF8C00 0%, #FFA500 100%); color: white; font-weight: bold; font-size: 1.2rem; padding: 0.8rem 2rem; border-radius: 50px; box-shadow: 0 4px 10px rgba(255,140,0,0.3); margin: 0; display: inline-block; text-align: center;">Análise de Performance - 2025 vs 2026</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Dados fornecidos
data = {
    'MARCA': ['ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 
              'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO',
              'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO',
              'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO'],
    
    'LOJA': ['BARRA SUL', 'AEROTOWN', 'AMERICANA', 'PENÍNSULA', 'NEW YORK', 'JARDINS', 'ALPHAVILLE', 'ANDRADINA', 
             'BELA VISTA', 'CARREFOUR CAXIAS', 'CAXIAS SHOPPING', 'CHÁCARA SANTO ANTÔNIO', 'GOIÂNIA', 'GRANDE RIO', 
             'GUADALUPE', 'ICARAÍ', 'OLEGÁRIO', 'PANAMBY', 'PARK SHOPPING', 'PIRATININGA', 'QUIOSQUE CABO FRIO', 
             'QUIOSQUE MACAÉ', 'QUIOSQUE NORTE SHOPPING', 'RECREIO', 'RIO DAS OSTRAS', 'SALVADOR', 'SULACAP', 
             'TATUAPÉ', 'UBERLÂNDIA', 'VALQUEIRE', 'VILLA LOBOS', 'VISTA ALEGRE'],
    
    'FAT_2026': [53473.31, 29055.01, 25443.49, 70948.43, 49960.22, 34755.29, 61746.77, 16452.39, 
                  501.48, 5717.73, 36519.87, 16850.06, 10530.97, 51336.04, 8215.92, 71577.01, 
                  177746.18, 9094.11, 39515.98, 31331.82, 2155.3, 3727.04, 5891.46, 97165.26, 
                  28773.7, 24622.33, 43303.06, 21339.65, 19066.19, 15901.26, 145020.48, 1671.98],
    
    'TC_2026': [666, 493, 214, 806, 681, 548, 605, 68, 
                9, 120, 532, 283, 154, 564, 142, 866, 
                1719, 59, 522, 488, 44, 106, 174, 1145, 
                236, 235, 418, 411, 176, 445, 857, 12],
    
    'TM_2026': [80.29, 58.94, 118.89, 88.03, 73.36, 63.42, 102.06, 241.95, 
                55.72, 47.65, 68.65, 59.54, 68.38, 91.02, 57.86, 82.65, 
                103.40, 154.14, 75.70, 64.20, 48.98, 35.16, 33.86, 84.86, 
                121.92, 104.78, 103.60, 51.92, 108.33, 35.73, 169.22, 139.33],
    
    'FAT_2025': [48092.97, 30482.41, None, 12947.31, 31610.86, 18357.53, 58151.42, 18091.31, 
                 None, 7871.6, 29127.83, 14150.61, 4811.33, 34324.63, 13818.37, 97488.37, 
                 145777.91, 22300.09, 47112.1, 62600.31, 3242.46, 5958.93, 6731.09, 79942.73, 
                 49784.14, 37625.07, None, None, 37514.92, 23291.46, None, 22516.78],
    
    'TC_2025': [684, 430, None, 174, 434, 286, 594, 127, 
                None, 174, 506, 193, 62, 740, 186, 1484, 
                1431, 214, 542, 814, 65, 128, 168, 1045, 
                925, 605, None, None, 456, 264, None, 310],
    
    'TM_2025': [70.31, 70.89, None, 74.41, 72.84, 64.19, 97.90, 142.45, 
                None, 45.24, 57.56, 73.32, 77.60, 46.38, 74.29, 65.69, 
                101.87, 104.21, 86.92, 76.90, 49.88, 46.55, 40.07, 76.50, 
                53.82, 62.19, None, None, 82.27, 88.23, None, 72.63],
    
    'PROD_PROMOCIONADO': ['AÇÃO CARNAVAL 26'] * 32,
    
    'COMPOSICAO_PROD': ['CANECA OU TULIPA AMSTEL'] * 32,
    
    'QUANTIDADE': [41, 39, 22, 14, 7, 5, 0, 0, 
                   0, 0, 0, 0, 0, 0, 0, 0, 
                   0, 0, 0, 0, 0, 0, 0, 0, 
                   0, 0, 0, 0, 0, 0, 0, 0],
    
    'VALOR_VENDA_PROD': [1740, 2712.60, 2004, 1872, 1334, 770, 2680, 338.30, 
                         30, 484, 1992, 0, 660, 7980, 1496, 3200, 
                         2100, 716, 3500.99, 0, 179, 189, 641, 6374, 
                         1184, 292, 3363.74, 542, 310, 0, 2084, 168],
    
    'PART.(%)': [0.0325, 0.0934, 0.0788, 0.0264, 0.0267, 0.0222, 0.0434, 0.0206, 
                 0.0598, 0.0846, 0.0545, None, 0.0627, 0.1554, 0.1821, 0.0447, 
                 0.0118, 0.0787, 0.0886, None, 0.0831, 0.0507, 0.1088, 0.0656, 
                 0.0411, 0.0119, 0.0777, 0.0254, 0.0163, 0, 0.0144, 0.1005]
}

df = pd.DataFrame(data)

# Sidebar para filtros
with st.sidebar:
    st.markdown('<h2 style="color: #FF8C00;">🎯 Filtros</h2>', unsafe_allow_html=True)
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    
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
    
    st.markdown('</div>', unsafe_allow_html=True)

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
    fat_total_2026 = df_filtrado['FAT_2026'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_2026:,.2f}</div>
        <div class="metric-label" style="color: white;">Faturamento Total 2026</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    fat_total_2025 = df_filtrado['FAT_2025'].sum() if not df_filtrado['FAT_2025'].isna().all() else 0
    variacao = ((fat_total_2026 - fat_total_2025) / fat_total_2025 * 100) if fat_total_2025 > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_2025:,.2f}</div>
        <div class="metric-label" style="color: white;">Faturamento Total 2025</div>
        <div class="metric-variation">{variacao:+.1f}% vs 2025</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    clientes_total = df_filtrado['TC_2026'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{clientes_total:,.0f}</div>
        <div class="metric-label" style="color: white;">Total de Clientes 2026</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    tm_medio = df_filtrado['TM_2026'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {tm_medio:,.2f}</div>
        <div class="metric-label" style="color: white;">Ticket Médio Médio</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Gráficos em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FF8C00;">🏆 Ranking de Faturamento 2026</h3>', unsafe_allow_html=True)
    
    # CORREÇÃO: Ordenar do MAIOR para o MENOR e depois inverter o eixo Y
    df_ranking = df_filtrado.nlargest(10, 'FAT_2026')[['LOJA', 'FAT_2026']].copy()
    
    # Inverter a ordem para que o maior fique no topo
    df_ranking = df_ranking.sort_values('FAT_2026', ascending=True)
    
    fig_ranking = px.bar(
        df_ranking,
        x='FAT_2026',
        y='LOJA',
        orientation='h',
        title='Top 10 Lojas por Faturamento',
        labels={'FAT_2026': 'Faturamento (R$)', 'LOJA': 'Loja'},
        color='FAT_2026',
        color_continuous_scale=['#FFD700', '#FF8C00']
    )
    fig_ranking.update_layout(
        height=400, 
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FF8C00'),
        yaxis={'categoryorder': 'total ascending'}  # Forçar ordenação ascendente no eixo Y
    )
    st.plotly_chart(fig_ranking, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FF8C00;">📈 Comparativo 2025 vs 2026</h3>', unsafe_allow_html=True)
    
    # Preparar dados para o gráfico
    df_comp = df_filtrado[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
    df_comp = df_comp.dropna(subset=['FAT_2025'])
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name='2026',
        x=df_comp['LOJA'],
        y=df_comp['FAT_2026'],
        marker_color='#FF8C00'
    ))
    fig_comp.add_trace(go.Bar(
        name='2025',
        x=df_comp['LOJA'],
        y=df_comp['FAT_2025'],
        marker_color='#FFD700'
    ))
    
    fig_comp.update_layout(
        title='Faturamento por Loja',
        xaxis_title='Loja',
        yaxis_title='Faturamento (R$)',
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FF8C00')
    )
    st.plotly_chart(fig_comp, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Ranking detalhado com novo estilo
st.markdown('<h2 class="sub-header">📋 Ranking Detalhado por Performance</h2>', unsafe_allow_html=True)

# Criar colunas para diferentes rankings
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

# Análise do produto promocional
st.markdown('<h2 class="sub-header">🍺 Análise do Produto Promocionado</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    # Gráfico de vendas do produto por loja
    df_prod = df_filtrado[df_filtrado['QUANTIDADE'] > 0][['LOJA', 'QUANTIDADE', 'VALOR_VENDA_PROD']].copy()
    
    if not df_prod.empty:
        fig_prod = px.pie(
            df_prod,
            values='VALOR_VENDA_PROD',
            names='LOJA',
            title='Distribuição da Venda do Produto Promocional',
            color_discrete_sequence=['#FF8C00', '#FFA500', '#FFD700', '#FFB347', '#FFA07A']
        )
        fig_prod.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FF8C00')
        )
        st.plotly_chart(fig_prod, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FF8C00;">📊 Participação no Faturamento</h3>', unsafe_allow_html=True)
    
    df_part = df_filtrado.nlargest(10, 'PART.(%)')[['LOJA', 'PART.(%)', 'VALOR_VENDA_PROD']].copy()
    df_part['PART.(%)'] = df_part['PART.(%)'] * 100
    
    fig_part = px.bar(
        df_part,
        x='LOJA',
        y='PART.(%)',
        title='% de Participação do Produto no Faturamento',
        labels={'PART.(%)': 'Participação (%)', 'LOJA': 'Loja'},
        color='PART.(%)',
        color_continuous_scale=['#FFD700', '#FF8C00'],
        text=df_part['PART.(%)'].round(1).astype(str) + '%'
    )
    fig_part.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FF8C00')
    )
    st.plotly_chart(fig_part, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tabela de dados completa
st.markdown('<h2 class="sub-header">📊 Dados Completos</h2>', unsafe_allow_html=True)

# Formatar dados para exibição
df_display = df_filtrado.copy()
df_display['FAT_2026'] = df_display['FAT_2026'].apply(lambda x: f'R$ {x:,.2f}')
df_display['FAT_2025'] = df_display['FAT_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
df_display['TM_2026'] = df_display['TM_2026'].apply(lambda x: f'R$ {x:,.2f}')
df_display['TM_2025'] = df_display['TM_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
df_display['VALOR_VENDA_PROD'] = df_display['VALOR_VENDA_PROD'].apply(lambda x: f'R$ {x:,.2f}')
df_display['PART.(%)'] = df_display['PART.(%)'].apply(lambda x: f'{x*100:.2f}%' if pd.notna(x) else 'N/A')

st.dataframe(
    df_display,
    use_container_width=True,
    height=400,
    column_config={
        "MARCA": "Marca",
        "LOJA": "Loja",
        "FAT_2026": "Faturamento 2026",
        "TC_2026": "Clientes 2026",
        "TM_2026": "Ticket Médio 2026",
        "FAT_2025": "Faturamento 2025",
        "TC_2025": "Clientes 2025",
        "TM_2025": "Ticket Médio 2025",
        "PROD_PROMOCIONADO": "Produto",
        "COMPOSICAO_PROD": "Composição",
        "QUANTIDADE": "Qtd Vendida",
        "VALOR_VENDA_PROD": "Valor Venda",
        "PART.(%)": "Participação"
    }
)

# Rodapé
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #FF8C00;'>Dashboard desenvolvido com Streamlit • Dados atualizados em {}</p>".format(
        datetime.now().strftime("%d/%m/%Y %H:%M")
    ),
    unsafe_allow_html=True
)