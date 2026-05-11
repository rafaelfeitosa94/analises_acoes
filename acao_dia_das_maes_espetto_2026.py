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
    page_title="Dia das Mães Espetto 2026",
    page_icon="🌹",
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
<h1 style="font-size: 2.5rem; color: #FFA500; font-weight: bold; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(255,140,0,0.1); text-align: center;">🌹 Dia das Mães Espetto 2026 🌹</h1>
""", unsafe_allow_html=True)

# Subtítulo
st.markdown("""
<div style="display: flex; justify-content: center; width: 100%; margin-top: 0.5rem;">
    <p style="background: linear-gradient(135deg, #CC7000 0%, #FF8C00 100%); color: white; font-weight: bold; font-size: 1.2rem; padding: 0.8rem 2rem; border-radius: 50px; box-shadow: 0 4px 10px rgba(255,140,0,0.3); margin: 0; display: inline-block; text-align: center;">De 08 à 10/05/2026 x 09 à 11/05/2025</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Dados fornecidos
data = {
    'MARCA': ['ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO'],
    'LOJA': ['ESP GRANDE RIO', 'ESP BARRA SUL', 'ESP RECREIO', 'ESP JARDINS', 'ESP OLEGÁRIO', 'ESP ALPHAVILLE', 'ESP ICARAÍ', 'ESP AMERICANA', 'ESP PENINSULA', 'ESP VALQUEIRE LOUNGE', 'ESP PARK SHOP CG', 'ESP SULACAP', 'ESP NY', 'ESP VILLA LOBOS', 'ESP ANDRADINA', 'ESP PIRATININGA', 'ESP CAXIAS SHOPPING', 'ESP RIO DAS OSTRAS', 'ESP VISTA ALEGRE', 'ESP UBERLÂNDIA', 'ESP TATUAPÉ', 'ESP COPA PRAIA', 'ESP GOIÂNIA', 'ESP AEROTOWN', 'ESP QUIOSQUE NORTE SHOP', 'ESP CHÁCARA ST', 'ESP GUADALUPE', 'ESP CAXIAS CARREFOUR', 'ESP QUIOSQUE MACAÉ', 'ESP BELA VISTA', 'ESP SALVADOR', 'ESP QUIOSQUE CABO FRIO', 'ESP ENGENHÃO'],
    'AÇÃO DIA DAS MÃES': [6, 6, 3, 3, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'LINGUICINHA E PÃO DE ALHO': [3, 3, 1, 2, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'PASTEL CARNE (3 UND)': [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'PASTEL QUEIJO (3 UND)': [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'PASTEL CAMARÃO (3 UND)': [2, 2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'MIX TRADICIONAL MEIA': [3, 6, 0, 3, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'CHURRASCO MISTO MEIA': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'ESPETTÃO BOVINO': [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'FAT_2026': [40550.53, 23275.94, 34763.85, 14460.8, 29991.74, 59679.17, 37726.61, 18045.89, 14274.86, 85244.41, 40244.55, 39527.08, 38544.52, 37336.82, 27232.66, 26171.38, 24456.69, 19071.79, 18886.88, 18495.38, 18213.84, 16278.19, 15055.81, 14556.75, 9982.0, 9064.26, 7546.78, 6831.32, 6636.66, 5294.8, 5194.1, 4088.9, 461.0],
    'TC_2026': [497, 324, 374, 226, 333, 509, 435, 159, 178, 1137, 405, 589, 350, 236, 90, 291, 298, 155, 307, 287, 228, 238, 152, 172, 239, 185, 162, 132, 169, 101, 69, 81, 27],
    'TM_2026': [81.59060362, 71.83932099, 92.95147059, 63.98584071, 90.06528529, 117.2478782, 86.72783908, 113.4961635, 80.1958427, 74.97309587, 99.36925926, 67.10879457, 110.1272, 158.2068644, 302.5851111, 89.93601375, 82.06942953, 123.0438065, 61.52078176, 64.44383275, 79.88526316, 68.3957563, 99.05138158, 84.63226744, 41.76569038, 48.996, 46.58506173, 51.75242424, 39.27017751, 52.42376238, 75.27681159, 50.48024691, 17.07407407],
    'FAT_2025': [57791.99, 26589.53, 34294.69, 42947.15, 31214.01, 58092.61, 56365.07, None, 31097.21, 116011.27, 88965.24, None, 66667.09, None, 15720.02, 76702.42, 44155.29, 45164.66, 42752.7, 34501.56, None, 30899.79, 5672.71, 11369.27, 12812.28, 10991.31, 25652.87, 8952.21, 12702.43, None, 14406.08, 6696.85, 2409.4],
    'TC_2025': [929, 292, 435, 411, 331, 527, 645, None, 423, 149, 806, None, 531, None, 97, 681, 475, 422, 354, 361, None, 433, 111, 177, 308, 138, 359, 165, 225, None, 132, 100, 120],
    'TM_2025': [62.20881593, 91.06003425, 78.83836782, 104.4942822, 94.30214502, 110.2326565, 87.38770543, None, 73.51586288, 778.5991275, 110.3787097, None, 125.5500753, None, 162.0620619, 112.6320411, 92.95850526, 107.0252607, 120.770339, 95.57218837, None, 71.36210162, 51.1054955, 64.23316384, 41.59831169, 79.64717391, 71.4564624, 54.25581818, 56.45524444, None, 109.1369697, 66.9685, 20.07833333],
    'PROD_PROMOCIONADO': ['AÇÃO DIA DAS MÃES'] * 33,
    'COMPOSICAO_PROD': ['ENTRADA + PRATO PRA COMPARTILHAR + TORTINHA'] * 33,
    'QUANTIDADE': [6, 6, 3, 3, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'VALOR_VENDA_PROD': [1193.82, 1193.82, 596.91, 596.91, 397.94, 198.97, 198.97, 198.97, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    'PART.(%)': [0.029440306, 0.051289873, 0.017170423, 0.041277799, 0.01326832, 0.003333994, 0.005273996, 0.011025779, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
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