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
    page_title="Dashboard Espetto - Análise ST. Patrick",
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
<h1 style="font-size: 2.5rem; color: #FFA500; font-weight: bold; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(255,140,0,0.1); text-align: center;">🍀 DIA DE ST. PATRICK ESPETTO 2026 🍻</h1>
""", unsafe_allow_html=True)

# Subtítulo
st.markdown("""
<div style="display: flex; justify-content: center; width: 100%; margin-top: 0.5rem;">
    <p style="background: linear-gradient(135deg, #CC7000 0%, #FF8C00 100%); color: white; font-weight: bold; font-size: 1.2rem; padding: 0.8rem 2rem; border-radius: 50px; box-shadow: 0 4px 10px rgba(255,140,0,0.3); margin: 0; display: inline-block; text-align: center;">Comparativo: ST. Patrick vs Média das últimas 4 terças até às 15:59</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Dados da planilha 'espetto (2)'
data = {
    'MARCA': ['ESPETTO'] * 35,
    'LOJA': [
        'ESP JARDINS', 'ESP OLEGÁRIO', 'ESP TATUAPÉ', 'ESP RECREIO', 'ESP PARK SHOP CG',
        'ESP ALPHAVILLE', 'ESP VILLA LOBOS', 'ESP NY', 'ESP GRANDE RIO', 'ESP SULACAP',
        'ESP ICARAÍ', 'ESP BARRA SUL', 'ESP CAXIAS SHOPPING', 'ESP VALQUEIRE LOUNGE', 'ESP ANDRADINA',
        'ESP RIO DAS OSTRAS', 'ESP VISTA ALEGRE', 'ESP PIRATININGA', 'ESP AEROTOWN', 'ESP AMERICANA',
        'ESP CHÁCARA ST', 'ESP SALVADOR', 'ESP GUADALUPE', 'ESP UBERLÂNDIA', 'ESP BELA VISTA',
        'ESP QUIOSQUE NORTE SHOP', 'ESP GOIÂNIA', 'ESP QUIOSQUE CABO FRIO', 'ESP CAXIAS CARREFOUR', 'ESP PANAMBY',
        'ESP QUIOSQUE MACAÉ', 'ESP ENGENHÃO', 'ESP SANTOS', 'ESP PENÍNSULA', 'ESP QUIOSQUE MACAÉ'
    ],
    'FAT_ST_PATRICK': [
        3742.93, 511.71, 1380.96, 0, 123,
        6511.08, 5220.50, 2221.08, 1337.58, 1029.5,
        0, 1220.67, 1366.40, 1750.15, 0,
        885.36, 0, 0, 1019.31, 656.88,
        602.56, 1057.8, 0, 0, 1104.56,
        447.29, 36.73, 0, 440.37, 0,
        0, 0, 0, 7415.79, 0
    ],
    'TC_ST_PATRICK': [
        51, 6, 21, 0, 2,
        50, 209, 25, 17, 8,
        0, 23, 8, 25, 0,
        7, 0, 0, 22, 7,
        9, 14, 0, 0, 21,
        11, 1, 0, 13, 0,
        0, 0, 0, 115, 0
    ],
    'TM_ST_PATRICK': [
        73.3907843137255, 85.285, 65.76, 0, 61.5,
        130.2216, 24.978468899521523, 88.8432, 78.68117647058824, 128.6875,
        0, 53.072608695652164, 170.8, 70.006, 0,
        126.48, 0, 0, 46.33227272727272, 93.84,
        66.9511111111111, 75.55714285714285, 0, 0, 52.59809523809523,
        40.66272727272728, 36.73, 0, 33.874615384615375, 0,
        0, 0, 0, 64.4851304347826, 0
    ],
    'FAT_TERÇAS_MEDIA': [
        2858.0375, 833.0966667, 1186.8175, 539.5825, 572.3133333,
        4590.905, 2821.4, 1761.79, 1192.73, 968.9266667,
        0, 1016.725, 1151.7025, 1174.36, 0,
        906.8333333, 372.84, 0, 620.4625, 616.07,
        495.73, 705.585, 0, 0, 1018.3625,
        376.0025, 74.75, 42.35, 639.175, 0,
        135.52, 0, 0, 6710.6075, 135.52
    ],
    'TC_TERÇAS_MEDIA': [
        42, 11, 17, 9, 7,
        46, 94, 25, 16, 8,
        0, 20, 7, 22, 0,
        5, 5, 0, 11, 8,
        6, 11, 0, 0, 19,
        11, 1, 1, 16, 0,
        2, 0, 0, 104, 2
    ],
    'TM_TERÇAS_MEDIA': [
        68.04494047619048, 75.73606060909091, 69.81279411764706, 59.95361111111111, 81.75904761904762,
        99.80228260869566, 30.014893617021276, 70.4716, 74.545625, 121.115833375,
        0, 50.83625, 164.52892857142858, 53.38, 0,
        181.36666666, 74.568, 0, 56.40568181818182, 77.00875,
        82.62166666666667, 64.1440909090909, 0, 0, 53.59802631578947,
        34.18204545454545, 74.75, 42.35, 39.9484375, 0,
        67.76, 0, 0, 64.52411057692308, 67.76
    ],
    'PROD_PROMOCIONADO': ['Happy Hour o dia todo'] * 35,
    'COMPOSICAO_PROD': ['CHOPP HEINEKEN E AMSTEL'] * 35,
    'QUANTIDADE': [5, 1, 3, 0, 9, 35, 0, 0, 3, 5, 0, 0, 7, 0, 0, 9, 0, 0, 0, 1, 0, 4, 0, 0, 1, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0],
    'VALOR_VENDA_PROD': [70, 15, 38, 0, 123, 524, 0, 0, 36, 56, 0, 0, 103, 0, 0, 114, 0, 0, 0, 13, 0, 56, 0, 0, 10, 45, 0, 0, 48, 0, 0, 0, 0, 0, 0],
    'PART.(%)': [
        0.01870192603121084, 0.029313478337339514, 0.02751708956088518, 0, 1,
        0.08047820023713424, 0, 0, 0.02691427802449199, 0.054395337542496355,
        0, 0, 0.07538056206088992, 0, 0,
        0.1287611818921117, 0, 0, 0, 0.01979052490561442,
        0, 0.05294006428436378, 0, 0, 0.009053378720938655,
        0.10060587091148918, 0, 0, 0.10899925063015195, 0,
        0, 0, 0, 0, 0
    ]
}

# Remover duplicatas e garantir dados únicos
df_clean = []
seen = set()
for item in zip(data['LOJA'], data['FAT_ST_PATRICK']):
    if item[0] not in seen:
        seen.add(item[0])
        idx = data['LOJA'].index(item[0])
        df_clean.append({k: data[k][idx] for k in data.keys()})

df = pd.DataFrame(df_clean)

# Calcular variação entre ST. Patrick e Média das Terças
df['VARIACAO_FAT_%'] = ((df['FAT_ST_PATRICK'] - df['FAT_TERÇAS_MEDIA']) / df['FAT_TERÇAS_MEDIA']) * 100
df['VARIACAO_TC_%'] = ((df['TC_ST_PATRICK'] - df['TC_TERÇAS_MEDIA']) / df['TC_TERÇAS_MEDIA']) * 100
df['VARIACAO_TM_%'] = ((df['TM_ST_PATRICK'] - df['TM_TERÇAS_MEDIA']) / df['TM_TERÇAS_MEDIA']) * 100

# Substituir infinitos por NaN
df = df.replace([np.inf, -np.inf], np.nan)

# Sidebar para filtros
with st.sidebar:
    st.markdown('<h2 style="color: #FFA500;">🎯 Filtros</h2>', unsafe_allow_html=True)
    
    # Filtro de lojas
    lojas_selecionadas = st.multiselect(
        "Selecione as lojas:",
        options=df['LOJA'].unique(),
        default=df['LOJA'].unique()
    )
    
    # Filtro de faixa de faturamento ST. Patrick
    fat_min, fat_max = st.slider(
        "Faixa de faturamento ST. Patrick (R$):",
        min_value=float(df['FAT_ST_PATRICK'].min()),
        max_value=float(df['FAT_ST_PATRICK'].max()),
        value=(float(df['FAT_ST_PATRICK'].min()), float(df['FAT_ST_PATRICK'].max()))
    )

# Aplicar filtros
df_filtrado = df[
    (df['LOJA'].isin(lojas_selecionadas)) &
    (df['FAT_ST_PATRICK'] >= fat_min) &
    (df['FAT_ST_PATRICK'] <= fat_max)
]

# Métricas principais
st.markdown('<h2 class="sub-header">📊 Visão Geral</h2>', unsafe_allow_html=True)

# ===== CÁLCULOS =====
fat_total_st_patrick = df_filtrado['FAT_ST_PATRICK'].sum()
fat_total_tercas = df_filtrado['FAT_TERÇAS_MEDIA'].sum()

variacao_total = ((fat_total_st_patrick - fat_total_tercas) / fat_total_tercas * 100) if fat_total_tercas > 0 else 0

# ===== COLUNAS =====
col1, col2, col3, col4 = st.columns(4)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_st_patrick:,.2f}</div>
        <div class="metric-label">Faturamento ST. Patrick 2026</div>
        <div class="metric-variation">{variacao_total:+.1f}% vs Média Terças</div>
    </div>
    """, unsafe_allow_html=True)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_tercas:,.2f}</div>
        <div class="metric-label">Média Faturamento Terças</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    clientes_total = df_filtrado['TC_ST_PATRICK'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{clientes_total:,.0f}</div>
        <div class="metric-label">Total Clientes ST. Patrick</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    tm_medio = df_filtrado[df_filtrado['TM_ST_PATRICK'] > 0]['TM_ST_PATRICK'].mean() if len(df_filtrado[df_filtrado['TM_ST_PATRICK'] > 0]) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {tm_medio:,.2f}</div>
        <div class="metric-label">Ticket Médio ST. Patrick</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Gráficos em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFA500;">🏆 Ranking de Faturamento ST. Patrick</h3>', unsafe_allow_html=True)
    
    df_ranking = df_filtrado.nlargest(10, 'FAT_ST_PATRICK')[['LOJA', 'FAT_ST_PATRICK']].copy()
    df_ranking = df_ranking[df_ranking['FAT_ST_PATRICK'] > 0].sort_values('FAT_ST_PATRICK', ascending=True)
    
    if not df_ranking.empty:
        fig_ranking = px.bar(
            df_ranking,
            x='FAT_ST_PATRICK',
            y='LOJA',
            orientation='h',
            title='Top Lojas por Faturamento',
            labels={'FAT_ST_PATRICK': 'Faturamento ST. Patrick (R$)', 'LOJA': 'Loja'},
            color='FAT_ST_PATRICK',
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
        st.info("Nenhuma loja com faturamento no ST. Patrick")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFA500;">📈 Comparativo ST. Patrick vs Média Terças</h3>', unsafe_allow_html=True)
    
    df_comp = df_filtrado[['LOJA', 'FAT_ST_PATRICK', 'FAT_TERÇAS_MEDIA', 'VARIACAO_FAT_%']].copy()
    df_comp = df_comp.dropna(subset=['VARIACAO_FAT_%'])
    df_comp = df_comp[df_comp['FAT_TERÇAS_MEDIA'] > 0]
    df_comp = df_comp.sort_values('VARIACAO_FAT_%', ascending=False).reset_index(drop=True)
    
    if not df_comp.empty:
        cores = ['#FF8C00' if x >= 0 else "#FFCC99" for x in df_comp['VARIACAO_FAT_%']]
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(
            x=df_comp['LOJA'],
            y=df_comp['VARIACAO_FAT_%'],
            marker_color=cores,
            text=df_comp['VARIACAO_FAT_%'].round(1).astype(str) + '%',
            textposition='outside',
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>%{x}</b><br>' +
                         'Variação: %{y:.1f}%<br>' +
                         'ST. Patrick: R$ %{customdata[0]:,.2f}<br>' +
                         'Média Terças: R$ %{customdata[1]:,.2f}<extra></extra>',
            customdata=df_comp[['FAT_ST_PATRICK', 'FAT_TERÇAS_MEDIA']].values,
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
        st.info("Dados insuficientes para comparação")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Tabela de detalhamento
st.markdown("### 📊 Detalhamento por Loja")

df_display = df_comp.copy()
df_display['FAT_TERÇAS_MEDIA'] = df_display['FAT_TERÇAS_MEDIA'].apply(lambda x: f'R$ {x:,.2f}')
df_display['FAT_ST_PATRICK'] = df_display['FAT_ST_PATRICK'].apply(lambda x: f'R$ {x:,.2f}')
df_display['VARIACAO_FAT_%'] = df_display['VARIACAO_FAT_%'].apply(lambda x: f'{x:.1f}%')
df_display.columns = ['Loja', 'ST. Patrick 2026', 'Média Terças', 'Variação %']

st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# RESUMO COM CARDS
st.markdown("### 📈 Resumo de Performance")

if not df_comp.empty:
    media_variacao = df_comp['VARIACAO_FAT_%'].mean()
    total_crescimento = (df_comp['VARIACAO_FAT_%'] > 0).sum()
    total_queda = (df_comp['VARIACAO_FAT_%'] < 0).sum()
    
    if total_crescimento > 0:
        melhor_loja = df_comp.loc[df_comp['VARIACAO_FAT_%'].idxmax(), 'LOJA']
        melhor_variacao = df_comp['VARIACAO_FAT_%'].max()
    else:
        melhor_loja = "N/A"
        melhor_variacao = 0
    
    if total_queda > 0:
        pior_loja = df_comp.loc[df_comp['VARIACAO_FAT_%'].idxmin(), 'LOJA']
        pior_variacao = df_comp['VARIACAO_FAT_%'].min()
    else:
        pior_loja = "N/A"
        pior_variacao = 0

    # Primeira linha de cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value">{media_variacao:.1f}%</div>
            <div class="summary-label">📊 Variação Média</div>
            <div class="summary-sub">ST. Patrick vs Média Terças</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value">{total_crescimento}</div>
            <div class="summary-label">📈 Lojas com Crescimento</div>
            <div class="summary-sub">✅ Superaram média das terças</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value">{total_queda}</div>
            <div class="summary-label">📉 Lojas com Queda</div>
            <div class="summary-sub">⚠️ Abaixo da média das terças</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1.2rem;">{melhor_loja}</div>
            <div class="summary-label">🏆 Melhor Performance</div>
            <div class="summary-sub">+{melhor_variacao:.1f}% vs Média Terças</div>
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
            <div class="summary-value" style="font-size: 1.5rem;">R$ {fat_total_tercas/1000:.1f}K</div>
            <div class="summary-label">💰 Média Faturamento Terças</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col7:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1.5rem;">R$ {fat_total_st_patrick/1000:.1f}K</div>
            <div class="summary-label">💰 Faturamento ST. Patrick</div>
            <div class="summary-sub">{variacao_total:+.1f}% vs Média Terças</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col8:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1rem;">{pior_loja}</div>
            <div class="summary-label">⚠️ Pior Performance</div>
            <div class="summary-sub">{pior_variacao:.1f}% vs Média Terças</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Ranking detalhado
st.markdown('<h2 class="sub-header">📋 Ranking Detalhado por Performance</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="ranking-title">💰 TOP FATURAMENTO ST. PATRICK</div>', unsafe_allow_html=True)
    top_fat = df_filtrado[df_filtrado['FAT_ST_PATRICK'] > 0].nlargest(5, 'FAT_ST_PATRICK')[['LOJA', 'FAT_ST_PATRICK']]
    if not top_fat.empty:
        for i, (idx, row) in enumerate(top_fat.iterrows(), 1):
            st.markdown(f"""
            <div class="ranking-item">
                <span class="ranking-badge">#{i}</span>
                <strong>{row['LOJA']}</strong>
                <div class="ranking-value">R$ {row['FAT_ST_PATRICK']:,.2f}</div>
                <div class="ranking-label">faturamento ST. Patrick</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhum dado disponível")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="ranking-title">👥 MAIS CLIENTES ST. PATRICK</div>', unsafe_allow_html=True)
    top_clientes = df_filtrado[df_filtrado['TC_ST_PATRICK'] > 0].nlargest(5, 'TC_ST_PATRICK')[['LOJA', 'TC_ST_PATRICK']]
    if not top_clientes.empty:
        for i, (idx, row) in enumerate(top_clientes.iterrows(), 1):
            st.markdown(f"""
            <div class="ranking-item">
                <span class="ranking-badge">#{i}</span>
                <strong>{row['LOJA']}</strong>
                <div class="ranking-value">{row['TC_ST_PATRICK']:,.0f}</div>
                <div class="ranking-label">clientes atendidos</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhum dado disponível")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="ranking-title">💎 MAIOR TICKET MÉDIO ST. PATRICK</div>', unsafe_allow_html=True)
    top_tm = df_filtrado[df_filtrado['TM_ST_PATRICK'] > 0].nlargest(5, 'TM_ST_PATRICK')[['LOJA', 'TM_ST_PATRICK']]
    if not top_tm.empty:
        for i, (idx, row) in enumerate(top_tm.iterrows(), 1):
            st.markdown(f"""
            <div class="ranking-item">
                <span class="ranking-badge">#{i}</span>
                <strong>{row['LOJA']}</strong>
                <div class="ranking-value">R$ {row['TM_ST_PATRICK']:,.2f}</div>
                <div class="ranking-label">ticket médio</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Nenhum dado disponível")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Análise do produto promocional
st.markdown('<h2 class="sub-header">🍺 Análise do Produto Promocional</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    df_prod = df_filtrado[df_filtrado['QUANTIDADE'] > 0][['LOJA', 'QUANTIDADE', 'VALOR_VENDA_PROD']].copy()
    
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
        st.info("Nenhum produto promocional vendido nas lojas selecionadas.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FFA500;">📊 Participação no Faturamento ST. Patrick</h3>', unsafe_allow_html=True)
    
    df_part = df_filtrado[df_filtrado['PART.(%)'] > 0].nlargest(10, 'PART.(%)')[['LOJA', 'PART.(%)', 'VALOR_VENDA_PROD']].copy()
    if not df_part.empty:
        df_part['PART.(%)'] = df_part['PART.(%)'] * 100
        
        fig_part = px.bar(
            df_part,
            x='LOJA',
            y='PART.(%)',
            title='% de Participação do Produto no Faturamento ST. Patrick',
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
        st.info("Nenhuma participação registrada.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Tabela de dados completa
st.markdown('<h2 class="sub-header">📊 Dados Completos</h2>', unsafe_allow_html=True)

df_display_full = df_filtrado.copy()
df_display_full['FAT_ST_PATRICK'] = df_display_full['FAT_ST_PATRICK'].apply(lambda x: f'R$ {x:,.2f}')
df_display_full['FAT_TERÇAS_MEDIA'] = df_display_full['FAT_TERÇAS_MEDIA'].apply(lambda x: f'R$ {x:,.2f}')
df_display_full['TM_ST_PATRICK'] = df_display_full['TM_ST_PATRICK'].apply(lambda x: f'R$ {x:,.2f}')
df_display_full['TM_TERÇAS_MEDIA'] = df_display_full['TM_TERÇAS_MEDIA'].apply(lambda x: f'R$ {x:,.2f}')
df_display_full['TC_ST_PATRICK'] = df_display_full['TC_ST_PATRICK'].apply(lambda x: f'{x:,.0f}')
df_display_full['TC_TERÇAS_MEDIA'] = df_display_full['TC_TERÇAS_MEDIA'].apply(lambda x: f'{x:,.0f}')
df_display_full['VALOR_VENDA_PROD'] = df_display_full['VALOR_VENDA_PROD'].apply(lambda x: f'R$ {x:,.2f}')
df_display_full['PART.(%)'] = df_display_full['PART.(%)'].apply(lambda x: f'{x*100:.4f}%')
df_display_full['VARIACAO_FAT_%'] = df_display_full['VARIACAO_FAT_%'].apply(lambda x: f'{x:.1f}%' if pd.notna(x) else 'N/A')
df_display_full['VARIACAO_TC_%'] = df_display_full['VARIACAO_TC_%'].apply(lambda x: f'{x:.1f}%' if pd.notna(x) else 'N/A')
df_display_full['VARIACAO_TM_%'] = df_display_full['VARIACAO_TM_%'].apply(lambda x: f'{x:.1f}%' if pd.notna(x) else 'N/A')

# Selecionar e renomear colunas para exibição
colunas_exibir = ['LOJA', 'FAT_ST_PATRICK', 'FAT_TERÇAS_MEDIA', 'VARIACAO_FAT_%', 
                  'TC_ST_PATRICK', 'TC_TERÇAS_MEDIA', 'VARIACAO_TC_%',
                  'TM_ST_PATRICK', 'TM_TERÇAS_MEDIA', 'VARIACAO_TM_%',
                  'PROD_PROMOCIONADO', 'COMPOSICAO_PROD', 'QUANTIDADE', 'VALOR_VENDA_PROD', 'PART.(%)']

df_display_full = df_display_full[colunas_exibir]
df_display_full.columns = ['Loja', 'ST. Patrick (R$)', 'Média Terças (R$)', 'Var. Fat. %',
                           'Clientes ST. Patrick', 'Clientes Média Terças', 'Var. Clientes %',
                           'Ticket Médio ST. Patrick', 'Ticket Médio Média Terças', 'Var. TM %',
                           'Produto Promocional', 'Composição Produto', 'Quantidade', 'Valor Venda', 'Participação %']

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