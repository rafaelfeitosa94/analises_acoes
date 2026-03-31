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
    <p style="background: linear-gradient(135deg, #CC7000 0%, #FF8C00 100%); color: white; font-weight: bold; font-size: 1.2rem; padding: 0.8rem 2rem; border-radius: 50px; box-shadow: 0 4px 10px rgba(255,140,0,0.3); margin: 0; display: inline-block; text-align: center;">ST. Patrick vs Média das últimas 4 terças até às 16h e após às 20h</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Dados da planilha 'espetto (2)'
data = {
    'MARCA': ['ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO', 'ESPETTO'],

    'LOJA': ['ESP PENÍNSULA', 'ESP AEROTOWN', 'ESP ALPHAVILLE', 'ESP AMERICANA', 'ESP ANDRADINA', 'ESP BARRA SUL', 'ESP BELA VISTA', 'ESP CAXIAS CARREFOUR', 'ESP CAXIAS SHOPPING', 'ESP CHÁCARA ST', 'ESP COPA PRAIA', 'ESP GOIÂNIA', 'ESP GRANDE RIO', 'ESP GUADALUPE', 'ESP ICARAÍ', 'ESP JARDINS', 'ESP NY', 'ESP OLEGÁRIO', 'ESP PARK SHOP CG', 'ESP QUIOSQUE CABO FRIO', 'ESP QUIOSQUE MACAÉ', 'ESP QUIOSQUE NORTE SHOP', 'ESP RECREIO', 'ESP RIO DAS OSTRAS', 'ESP SALVADOR', 'ESP SULACAP', 'ESP TATUAPÉ', 'ESP VALQUEIRE LOUNGE', 'ESP VILLA LOBOS', 'ESP VISTA ALEGRE'],

    'FAT_ST_PATRICK': [7415.79, 1547.39, 17826.17, 836.08, 5576.96, 1931.73, 1316.35, 640.4, 2060.31, 3324.19, 10523.52, 447.54, 4312.75, 473.33, 817.0, 9472.17, 4610.36, 5570.56, 3446.67, 398.75, 78.96, 917.57, 5769.31, 913.67, 3623.17, 2812.94, 2218.18, 2005.3, 5220.5, 2467.3],

    'TC_ST_PATRICK': [115, 34, 142, 8, 18, 38, 25, 17, 11, 47, 118, 5, 34, 5, 13, 103, 48, 53, 46, 7, 1, 18, 51, 9, 26, 31, 32, 31, 209, 28],

    'TM_ST_PATRICK': [64.49, 45.51, 125.54, 104.51, 309.83, 50.83, 52.65, 37.67, 187.3, 70.73, 89.18, 89.51, 126.85, 94.67, 62.85, 91.96, 96.05, 105.1, 74.93, 56.96, 78.96, 50.98, 113.12, 101.52, 139.35, 90.74, 69.32, 64.69, 24.98, 88.12],

    'FAT_TERÇAS_MEDIA': [6710.61, 919.1, 13755.66, 1578.03, 1677.1, 4090.22, 1469.28, 928.96, 2648.3, 3720.45, 9746.65, 797.31, 4112.71, 1349.72, 1897.19, 6010.85, 4774.24, 4742.02, 3454.27, 454.67, 231.8, 1085.64, 5896.33, 2243.8, 1894.77, 3010.79, 2186.76, 1664.42, 2821.4, 3468.3],

    'TC_TERÇAS_MEDIA': [104, 17, 111, 17, 15, 58, 24, 22, 18, 55, 105, 12, 39, 12, 23, 84, 59, 43, 44, 6, 4, 21, 50, 14, 21, 25, 29, 29, 94, 51],

    'TM_TERÇAS_MEDIA': [64.53, 54.06, 123.92, 92.83, 111.81, 70.52, 61.22, 42.23, 147.13, 67.64, 92.83, 66.44, 105.45, 112.48, 82.49, 71.56, 80.92, 110.28, 78.51, 75.78, 57.95, 51.7, 117.93, 160.27, 90.23, 120.43, 75.41, 57.39, 30.01, 68.01],

    'PROD_PROMOCIONADO': ['Happy Hour o dia todo!'] * 30,

    'COMPOSICAO_PROD': ['Chopp Heineken ou Amstel'] * 30,

    'QUANTIDADE': [0, 11, 65, 1, 1, 1, 1, 5, 7, 5, 17, 0, 3, 14, 24, 10, 0, 35, 55, 26, 3, 17, 71, 9, 7, 17, 3, 0, 0, 11],

    'VALOR_VENDA_PROD': [0.0, 153.0, 962.0, 13.0, 9.95, 13.0, 10.0, 63.0, 103.0, 68.0, 169.15, 0.0, 36.0, 152.0, 198.9, 140.0, 0.0, 477.0, 679.0, 267.0, 42.0, 149.0, 742.0, 114.0, 98.0, 200.0, 38.0, 0.0, 0.0, 124.0],

    'PART.(%)': [0.0, 0.0989, 0.0540, 0.0155, 0.0018, 0.0067, 0.0076, 0.0984, 0.05, 0.0205, 0.0161, 0.0, 0.0083, 0.3211, 0.2435, 0.0148, 0.0, 0.0856, 0.1970, 0.6696, 0.5319, 0.1624, 0.1286, 0.1248, 0.0270, 0.0711, 0.0171, 0.0, 0.0, 0.0503]
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
