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
    page_title="São Jorge Espetto 2026",
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
    .warning-card {
        background: linear-gradient(135deg, #8B0000 0%, #CC0000 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
    }
    .info-card {
        background: linear-gradient(135deg, #1a1d24 0%, #2a2d34 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #FFA500;
        margin-bottom: 1rem;
    }
    .info-title {
        color: #FFA500;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.8rem;
    }
    .info-text {
        color: #FAFAFA;
        font-size: 1rem;
        line-height: 1.5;
    }
    .info-list {
        color: #FAFAFA;
        margin-left: 1.5rem;
        margin-top: 0.5rem;
    }
    .info-list li {
        margin: 0.3rem 0;
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
<h1 style="font-size: 2.5rem; color: #FFA500; font-weight: bold; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(255,140,0,0.1); text-align: center;">⚔️ SÃO JORGE ESPETTO 2026 ⚔️</h1>
""", unsafe_allow_html=True)

# Subtítulo
st.markdown("""
<div style="display: flex; justify-content: center; width: 100%; margin-top: 0.5rem;">
    <p style="background: linear-gradient(135deg, #CC7000 0%, #FF8C00 100%); color: white; font-weight: bold; font-size: 1.2rem; padding: 0.8rem 2rem; border-radius: 50px; box-shadow: 0 4px 10px rgba(255,140,0,0.3); margin: 0; display: inline-block; text-align: center;">Comparativo - 2025 vs 2026</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Dados fornecidos
data = {
    'MARCA': ['ESPETTO'] * 31,
    'LOJA': [
        'ESP OLEGÁRIO', 'ESP ALPHAVILLE', 'ESP ICARAÍ', 'ESP NY', 'ESP PARK SHOP CG',
        'ESP RECREIO', 'ESP GRANDE RIO', 'ESP SULACAP', 'ESP JARDINS', 'ESP BARRA SUL',
        'ESP CAXIAS SHOPPING', 'ESP VALQUEIRE LOUNGE', 'ESP ANDRADINA', 'ESP VISTA ALEGRE',
        'ESP UBERLÂNDIA', 'ESP COPA PRAIA', 'ESP TATUAPÉ', 'ESP VILLA LOBOS', 'ESP CHÁCARA ST',
        'ESP GOIÂNIA', 'ESP RIO DAS OSTRAS', 'ESP AEROTOWN', 'ESP GUADALUPE', 'ESP SALVADOR',
        'ESP AMERICANA', 'ESP QUIOSQUE NORTE SHOP', 'ESP QUIOSQUE CABO FRIO', 'ESP BELA VISTA',
        'ESP QUIOSQUE MACAÉ', 'ESP CAXIAS CARREFOUR', 'ESP PENÍNSULA'
    ],
    'FAT_2026': [
        26988.83, 22487.80, 15858.06, 14469.57, 14138.31,
        13843.10, 12728.71, 11250.24, 10416.31, 8416.61,
        8240.01, 8061.23, 7789.83, 6242.23, 6207.71,
        5085.37, 4832.79, 4166.56, 4161.23, 4119.61,
        3729.35, 3226.67, 2517.26, 2304.06, 2048.08,
        1622.31, 1604.90, 1337.79, 1229.42, 1038.70,
        15555.06
    ],
    'TC_2026': [
        267, 255, 158, 145, 167,
        151, 136, 116, 155, 113,
        110, 198, 14, 101, 101,
        77, 91, 87, 100, 50,
        42, 49, 48, 29, 20,
        46, 32, 35, 30, 22,
        159
    ],
    'TM_2026': [
        101.08176029962547, 88.18745098039216, 100.36746835443037, 99.79013793103448, 84.66053892215568,
        91.67615894039736, 93.59345588235294, 96.98482758620689, 67.202, 74.48327433628319,
        74.90918181818182, 40.71328282828283, 556.4164285714286, 61.80425742574257, 61.46247524752475,
        66.04376623376623, 53.107582417582414, 47.89149425287357, 41.6123, 82.39219999999999,
        88.79404761904762, 65.85040816326531, 52.44291666666667, 79.4503448275862, 102.404,
        35.26760869565217, 50.153125, 38.22257142857143, 40.98066666666667, 47.21363636363637,
        97.83056603773585
    ],
    'FAT_2025': [
        14328.90, 16368.70, 14247.15, 10891.46, 17033.94,
        20099.14, 6668.36, None, 5217.72, 6393.17,
        7644.90, 11084.28, 6400.85, 6207.87, 3093.32,
        8833.07, None, None, 4420.36, 849.85,
        5110.04, 2597.70, 3468.89, 2150.62, None,
        1662.51, 899.84, None, 1673.95, 2084.52,
        12811.01
    ],
    'TC_2025': [
        138, 196, 159, 113, 186,
        179, 139, None, 83, 78,
        100, 42, 26, 92, 28,
        118, None, None, 58, 15,
        42, 32, 65, 28, None,
        43, 16, None, 29, 41,
        171
    ],
    'TM_2025': [
        103.83260869565217, 83.51377551020408, 89.60471698113207, 96.3846017699115, 91.58032258064516,
        112.28569832402235, 47.97381294964028, None, 62.86409638554217, 81.96371794871796,
        76.449, 263.9114285714286, 246.18653846153848, 67.47684782608695, 110.47571428571429,
        74.85652542372881, None, None, 76.21310344827586, 56.656666666666666,
        121.66761904761904, 81.178125, 53.36753846153846, 76.80785714285715, None,
        38.663023255813954, 56.24, None, 57.72241379310345, 50.8419512195122,
        74.91818713450293
    ],
    'DOSE DUPLA CAIPIRINHA': [
        3, 14, 0, 5, 2,
        2, 0, 0, 6, 0,
        0, 0, 0, 1, 2,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 1,
        0, 0, 0, 0, 0,
        9
    ],
    'CAIP MORANGO': [
        1, 9, 0, 0, 1,
        0, 0, 0, 2, 0,
        0, 0, 0, 7, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 1,
        0, 0, 0, 0, 0,
        0
    ],
    'CAIP LIMAO': [
        20, 0, 0, 5, 3,
        4, 0, 3, 5, 0,
        1, 3, 0, 6, 0,
        0, 0, 3, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        9
    ],
    'CAIP MARACUJA': [
        1, 0, 0, 0, 0,
        1, 1, 0, 0, 1,
        0, 0, 0, 1, 1,
        1, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0
    ],
    'CAIP ABACAXI': [
        0, 1, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 1,
        2, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0
    ],
    'CAIP KIWI': [
        0, 1, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 1,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0
    ],
    'CAIP TANGERINA': [
        0, 2, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0
    ],
    'CAIP MARACUJÁ C/ MANGA': [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0
    ],
    'CAIP MORANGO C/ AMORA': [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0
    ],
    'CAIP LIMAO SICILIANO C/ GENGIBRE': [
        0, 0, 0, 0, 0,
        0, 0, 1, 0, 1,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0
    ],
    'QUANTIDADE TOTAL': [
        25, 27, 0, 10, 6,
        7, 1, 4, 13, 2,
        1, 3, 0, 15, 4,
        3, 0, 4, 0, 0,
        0, 0, 0, 0, 2,
        0, 0, 0, 0, 0,
        18
    ],
    'PROD_PROMOCIONADO': ['DOSE DUPLA DE CAIPS'] * 31,
    'COMPOSICAO_PROD': ['CAIPIRINHAS DE CACHAÇA'] * 31,
    'QUANTIDADE': [
        3, 14, 0, 5, 2,
        2, 0, 0, 6, 0,
        0, 0, 0, 1, 2,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 1,
        0, 0, 0, 0, 0,
        9
    ],
    'VALOR_VENDA_PROD': [
        660, 208, 0, 75, 112,
        120, 28, 117, 128, 65,
        28, 85.71, 0, 392, 28,
        96, 0, 132, 0, 0,
        0, 0, 0, 0, 14,
        0, 0, 0, 0, 0,
        243
    ],
    'PART.(%)': [
        0.024454561387062722, 0.009249459707041151, 0, 0.005183291556003392, 0.00792173887826763,
        0.008668578569829012, 0.002199751585195986, 0.010399778138066388, 0.01228842075552667, 0.00772282427248025,
        0.0033980541285750865, 0.010632372479137798, 0, 0.06279807056132183, 0.004510519982408972,
        0.01887768244985124, 0, 0, 0, 0,
        0, 0, 0, 0, 0.006835670481621812,
        0, 0, 0, 0, 0,
        0.015621926241364548
    ]
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

# Aplicar filtros básicos
df_filtrado = df[
    (df['LOJA'].isin(lojas_selecionadas)) &
    (df['FAT_2026'] >= fat_min) &
    (df['FAT_2026'] <= fat_max)
]

# ==== CRIAR DATAFRAME APENAS COM LOJAS QUE TÊM AMBOS OS ANOS ====
df_comparavel = df_filtrado.dropna(subset=['FAT_2025', 'FAT_2026']).copy()

# Criar a coluna de variação percentual para o df_comparavel
if not df_comparavel.empty:
    df_comparavel['VARIACAO_%'] = ((df_comparavel['FAT_2026'] - df_comparavel['FAT_2025']) / df_comparavel['FAT_2025']) * 100

# Métricas principais (apenas lojas comparáveis)
st.markdown('<h2 class="sub-header">📊 Visão Geral</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if not df_comparavel.empty:
        fat_total_2025 = df_comparavel['FAT_2025'].sum()
    else:
        fat_total_2025 = 0
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
    if not df_comparavel.empty:
        clientes_total = df_comparavel['TC_2026'].sum()
    else:
        clientes_total = 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{clientes_total:,.0f}</div>
        <div class="metric-label">Total de Clientes 2026</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if not df_comparavel.empty:
        tm_medio = fat_total_2026 / clientes_total if clientes_total > 0 else 0
    else:
        tm_medio = 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {tm_medio:,.2f}</div>
        <div class="metric-label">Ticket Médio Médio 2026</div>
    </div>
    """, unsafe_allow_html=True)

# Adicionar aviso sobre lojas não comparáveis
lojas_nao_comparaveis = df_filtrado[~df_filtrado['LOJA'].isin(df_comparavel['LOJA'])]['LOJA'].tolist() if not df_comparavel.empty else df_filtrado['LOJA'].tolist()
if lojas_nao_comparaveis and len(lojas_nao_comparaveis) > 0:
    st.markdown(f"""
    <div style="margin-top: 1rem; margin-bottom: 1rem;">
        <div class="warning-card">
            ⚠️ As seguintes lojas não possuem dados completos para 2025 e não estão incluídas nas métricas acima:<br>
            <strong>{', '.join(lojas_nao_comparaveis)}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Gráficos em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFA500;">🏆 Ranking de Faturamento 2026</h3>', unsafe_allow_html=True)
    
    df_ranking = df_comparavel.nlargest(10, 'FAT_2026')[['LOJA', 'FAT_2026']].copy() if not df_comparavel.empty else pd.DataFrame()
    if not df_ranking.empty:
        df_ranking = df_ranking.sort_values('FAT_2026', ascending=True)
        
        fig_ranking = px.bar(
            df_ranking,
            x='FAT_2026',
            y='LOJA',
            orientation='h',
            title='Top Lojas por Faturamento (apenas lojas com dados 2025)',
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
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #FFA500;">
            Nenhuma loja com dados completos para exibir.
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFA500;">📈 Comparativo 2025 vs 2026</h3>', unsafe_allow_html=True)
    
    if not df_comparavel.empty:
        df_comp = df_comparavel[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
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
    else:
        st.markdown("""
        <div class="warning-card">
            ⚠️ Nenhuma loja possui dados completos para 2025 e 2026.<br>
            Não é possível exibir o comparativo.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Tabela de detalhamento (apenas lojas comparáveis)
st.markdown("### 📊 Detalhamento por Loja (Comparativo 2025 vs 2026)")

if not df_comparavel.empty:
    df_display = df_comparavel[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
    df_display['VARIACAO_%'] = ((df_display['FAT_2026'] - df_display['FAT_2025']) / df_display['FAT_2025']) * 100
    df_display['FAT_2025'] = df_display['FAT_2025'].apply(lambda x: f'R$ {x:,.2f}')
    df_display['FAT_2026'] = df_display['FAT_2026'].apply(lambda x: f'R$ {x:,.2f}')
    df_display['VARIACAO_%'] = df_display['VARIACAO_%'].apply(lambda x: f'{x:.1f}%')
    df_display.columns = ['Loja', 'Faturamento 2026', 'Faturamento 2025', 'Variação %']
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )
else:
    st.markdown("""
    <div class="warning-card">
        ⚠️ Nenhuma loja possui dados completos para 2025 e 2026.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# RESUMO COM CARDS (apenas lojas comparáveis)
st.markdown("### 📈 Resumo de Performance (Lojas com dados completos)")

if not df_comparavel.empty and 'VARIACAO_%' in df_comparavel.columns:
    media_variacao = df_comparavel['VARIACAO_%'].mean()
    total_crescimento = (df_comparavel['VARIACAO_%'] > 0).sum()
    total_queda = (df_comparavel['VARIACAO_%'] < 0).sum()
    melhor_loja = df_comparavel.loc[df_comparavel['VARIACAO_%'].idxmax(), 'LOJA']
    melhor_variacao = df_comparavel['VARIACAO_%'].max()
    pior_loja = df_comparavel.loc[df_comparavel['VARIACAO_%'].idxmin(), 'LOJA']
    pior_variacao = df_comparavel['VARIACAO_%'].min()

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
            <div class="summary-value">{len(df_comparavel)}</div>
            <div class="summary-label">🏪 Lojas Analisadas</div>
            <div class="summary-sub">Com dados completos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        fat_2025_total = df_comparavel['FAT_2025'].sum()
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1.5rem;">R$ {fat_2025_total/1000000:.1f}M</div>
            <div class="summary-label">💰 Faturamento 2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col7:
        fat_2026_total = df_comparavel['FAT_2026'].sum()
        variacao_total = ((fat_2026_total - fat_2025_total) / fat_2025_total * 100) if fat_2025_total > 0 else 0
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1.5rem;">R$ {fat_2026_total/1000000:.1f}M</div>
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

st.markdown("---")

# Ranking detalhado (apenas lojas comparáveis)
st.markdown('<h2 class="sub-header">📋 Ranking Detalhado por Performance</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="ranking-title">💰 TOP FATURAMENTO</div>', unsafe_allow_html=True)
    if not df_comparavel.empty:
        top_fat = df_comparavel.nlargest(5, 'FAT_2026')[['LOJA', 'FAT_2026']]
        for i, (idx, row) in enumerate(top_fat.iterrows(), 1):
            st.markdown(f"""
            <div class="ranking-item">
                <span class="ranking-badge">#{i}</span>
                <strong>{row['LOJA']}</strong>
                <div class="ranking-value">R$ {row['FAT_2026']:,.2f}</div>
                <div class="ranking-label">faturamento 2026</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="color: white; text-align: center; padding: 1rem;">Sem dados</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="ranking-title">👥 MAIS CLIENTES</div>', unsafe_allow_html=True)
    if not df_comparavel.empty:
        top_clientes = df_comparavel.nlargest(5, 'TC_2026')[['LOJA', 'TC_2026']]
        for i, (idx, row) in enumerate(top_clientes.iterrows(), 1):
            st.markdown(f"""
            <div class="ranking-item">
                <span class="ranking-badge">#{i}</span>
                <strong>{row['LOJA']}</strong>
                <div class="ranking-value">{row['TC_2026']:,.0f}</div>
                <div class="ranking-label">clientes atendidos</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="color: white; text-align: center; padding: 1rem;">Sem dados</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="ranking-title">💎 MAIOR TICKET MÉDIO</div>', unsafe_allow_html=True)
    if not df_comparavel.empty:
        top_tm = df_comparavel.nlargest(5, 'TM_2026')[['LOJA', 'TM_2026']]
        for i, (idx, row) in enumerate(top_tm.iterrows(), 1):
            st.markdown(f"""
            <div class="ranking-item">
                <span class="ranking-badge">#{i}</span>
                <strong>{row['LOJA']}</strong>
                <div class="ranking-value">R$ {row['TM_2026']:,.2f}</div>
                <div class="ranking-label">ticket médio</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="color: white; text-align: center; padding: 1rem;">Sem dados</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Análise do produto promocional
st.markdown('<h2 class="sub-header">🍺 Análise do Produto Promocionado</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    df_prod = df_comparavel[df_comparavel['QUANTIDADE'] > 0][['LOJA', 'QUANTIDADE', 'VALOR_VENDA_PROD']].copy() if not df_comparavel.empty else pd.DataFrame()
    
    if not df_prod.empty:
        fig_prod = px.pie(
            df_prod,
            values='VALOR_VENDA_PROD',
            names='LOJA',
            title='Distribuição de Venda do Produto Promocional',
            color_discrete_sequence=['#FF8C00', '#CC7000', '#FFA500', '#FFB347', '#FFA07A']
        )
        fig_prod.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig_prod, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #FFA500;">
            Nenhuma venda do produto promocional registrada.
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFA500;">📊 Participação no Faturamento</h3>', unsafe_allow_html=True)
    
    df_part = df_comparavel.nlargest(10, 'PART.(%)')[['LOJA', 'PART.(%)', 'VALOR_VENDA_PROD']].copy() if not df_comparavel.empty else pd.DataFrame()
    if not df_part.empty and df_part['PART.(%)'].sum() > 0:
        df_part['PART.(%)'] = df_part['PART.(%)'] * 100
        
        fig_part = px.bar(
            df_part,
            x='LOJA',
            y='PART.(%)',
            title='% de Participação do Produto no Faturamento',
            labels={'PART.(%)': 'Participação (%)', 'LOJA': 'Loja'},
            color='PART.(%)',
            color_continuous_scale=['#FFCC99', '#FF8C00'],
            text=df_part['PART.(%)'].round(2).astype(str) + '%'
        )
        fig_part.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig_part, use_container_width=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #FFA500;">
            Nenhuma participação relevante registrada.
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Tabela de dados completa (apenas lojas comparáveis)
st.markdown('<h2 class="sub-header">📊 Dados Completos</h2>', unsafe_allow_html=True)

if not df_comparavel.empty:
    df_display_full = df_comparavel.copy()
    df_display_full['FAT_2026'] = df_display_full['FAT_2026'].apply(lambda x: f'R$ {x:,.2f}')
    df_display_full['FAT_2025'] = df_display_full['FAT_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
    df_display_full['TM_2026'] = df_display_full['TM_2026'].apply(lambda x: f'R$ {x:,.2f}')
    df_display_full['TM_2025'] = df_display_full['TM_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
    df_display_full['VALOR_VENDA_PROD'] = df_display_full['VALOR_VENDA_PROD'].apply(lambda x: f'R$ {x:,.2f}')
    df_display_full['PART.(%)'] = df_display_full['PART.(%)'].apply(lambda x: f'{x*100:.4f}%')
else:
    df_display_full = pd.DataFrame()

if not df_display_full.empty:
    st.dataframe(
        df_display_full,
        use_container_width=True,
        height=400
    )
else:
    st.markdown("""
    <div class="warning-card">
        ⚠️ Nenhuma loja com dados completos para exibir.
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==== QUADRO DE AVISOS - FINAL ====
st.markdown("""
<div style="margin-top: 2rem;">
    <div class="info-card">
        <div class="info-title">
            📌 IMPORTANTE - NOTA SOBRE OS DADOS COMPARATIVOS
        </div>
        <div class="info-text">
            As lojas listadas abaixo ainda não haviam inaugurado na data de referência da coleta de dados de 2025, 
            portanto não possuem faturamento registrado para o ano de 2025:
        </div>
        <ul class="info-list">
            <li><strong style="color: #FFA500;">ESP SULACAP</strong> - Inaugurada após o período de coleta de 2025</li>
            <li><strong style="color: #FFA500;">ESP TATUAPÉ</strong> - Inaugurada após o período de coleta de 2025</li>
            <li><strong style="color: #FFA500;">ESP VILLA LOBOS</strong> - Inaugurada após o período de coleta de 2025</li>
            <li><strong style="color: #FFA500;">ESP AMERICANA</strong> - Inaugurada após o período de coleta de 2025</li>
            <li><strong style="color: #FFA500;">ESP BELA VISTA</strong> - Inaugurada após o período de coleta de 2025</li>
        </ul>
        <div class="info-text" style="margin-top: 0.8rem;">
            🔍 Estas lojas são exibidas nos rankings e métricas de 2026, mas não entram nos cálculos de 
            <strong>variação percentual</strong>, <strong>comparativo 2025 vs 2026</strong> e 
            <strong>resumo de performance</strong> por não possuírem base de comparação no ano anterior.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: #FFA500;'>Dashboard desenvolvido com Streamlit • Dados atualizados em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>",
    unsafe_allow_html=True)