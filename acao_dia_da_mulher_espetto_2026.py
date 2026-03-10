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

/* ===== NOVO: REDUZIR FONTE DAS MÉTRICAS ===== */
[data-testid="stMetricValue"] {
    font-size: 1.2rem !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.9rem !important;
}

[data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
}

/* Ajustar o espaçamento entre as colunas de métricas */
div[data-testid="column"] {
    padding: 0 5px !important;
}

/* Ajustar o container das métricas */
div[data-testid="stMetric"] {
    background-color: rgba(255, 255, 255, 0.05);
    padding: 10px;
    border-radius: 10px;
    border-left: 3px solid #FF8C00;
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
        color: #FFFFFF;
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
<h1 style="font-size: 2.5rem; color: #FF8C00; font-weight: bold; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(255,140,0,0.1); text-align: center;">💐 DIA DA MULHER ESPETTO 2026</h1>
""", unsafe_allow_html=True)

# Subtítulo com gradiente laranja
st.markdown("""
<div style="display: flex; justify-content: center; width: 100%; margin-top: 0.5rem;">
    <p style="background: linear-gradient(135deg, #FF8C00 0%, #FFA500 100%); color: white; font-weight: bold; font-size: 1.2rem; padding: 0.8rem 2rem; border-radius: 50px; box-shadow: 0 4px 10px rgba(255,140,0,0.3); margin: 0; display: inline-block; text-align: center;">Análise de Performance - 2025 vs 2026</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Dados corrigidos - TODAS AS LISTAS COM 29 ELEMENTOS
data = {
    'MARCA': ['ESPETTO'] * 29,
    
    'LOJA': ['ESP AMERICANA', 'ESP OLEGÁRIO', 'ESP VISTA ALEGRE', 'ESP AEROTOWN', 'ESP ANDRADINA', 
             'ESP ALPHAVILLE', 'ESP BARRA SUL', 'ESP CAXIAS CARREFOUR', 'ESP CAXIAS SHOPPING', 'ESP COPA PRAIA', 
             'ESP GOIÂNIA', 'ESP GUADALUPE', 'ESP ICARAÍ', 'ESP JARDINS', 'ESP NY', 
             'ESP PARK SHOP CG', 'ESP PENINSULA', 'ESP PIRATININGA', 'ESP QUIOSQUE CABO FRIO', 'ESP QUIOSQUE MACAÉ', 
             'ESP QUIOSQUE NORTE SHOP', 'ESP RECREIO', 'ESP RIO DAS OSTRAS', 'ESP SALVADOR', 'ESP SULACAP', 
             'ESP TATUAPÉ', 'ESP VALQUEIRE LOUNGE', 'ESP ENGENHÃO', 'ESP VILLA LOBOS'],
    
    'FAT_2026': [8885.36, 23279.15, 17458.83, 7659.03, 1731.13, 
                 12525.64, 11439.12, 4514.06, 20980.07, 20932.12, 
                 2039.18, 9405.26, 17974.16, 7831.92, 31379.06, 
                 53011.87, 15703.44, 23789.63, 3313.25, 4648.7, 
                 3871.35, 24940.05, 18903.47, 1008.78, 31203.83, 
                 11071.42, 4763.16, 419, 31113.61],
    
    'TC_2026': [87, 268, 179, 140, 17, 
                137, 150, 81, 276, 292, 
                58, 126, 271, 118, 248, 
                463, 187, 219, 66, 35, 
                93, 322, 137, 12, 250, 
                101, 131, 20, 237],
    
    'TM_2026': [102.13, 86.86, 97.54, 54.71, 101.83, 
                91.43, 76.26, 55.73, 76.01, 71.69, 
                35.16, 74.64, 66.33, 66.37, 126.53, 
                114.50, 83.98, 108.63, 50.20, 132.82, 
                41.63, 77.45, 137.98, 84.06, 124.82, 
                109.62, 36.36, 20.95, 131.28],
    
    'FAT_2025': [None, 26494.47, 21982.18, 5754.52, 13742.16, 
                 33240.88, 15128.88, 3129.92, 15385.06, 15461.64, 
                 3415.52, 10236.92, 31459.89, 7172.41, 17101.77, 
                 26831.5, 14188.17,42608.46, 3012.85, 2324.81, 
                 4083.97, 23725.26, 22545.41, 7029.87, None, 
                 None, None, 983, None],
    
    'TC_2025': [None, 243, 207, 80, 102, 
                314, 170, 64, 194, 244, 
                45, 139, 378, 117, 193, 
                297, 186, 477, 51, 63, 
                107, 295, 263, 155, None, 
                None, None, 39, None],
    
    'TM_2025': [None, 109.03, 106.19, 71.93, 134.73, 
                105.86, 88.99, 48.90, 79.30, 63.37, 
                75.90, 73.65, 83.23, 61.30, 88.61, 
                90.34, 7.62, 89.33, 59.08, 36.90, 
                38.17, 80.42, 85.72, 45.35, None, 
                None, None, 25.21, None],
    
    'PROD_PROMOCIONADO': ['AÇÃO DIA DA MULHER'] * 29,
    
    'COMPOSICAO_PROD': ['GAROTINHO AMSTEL'] * 29,
    
    'QUANTIDADE': [33, 12, 1] + [0] * 26,  # 3 valores não-zero + 26 zeros = 29
}

df = pd.DataFrame(data)

# Sidebar para filtros
with st.sidebar:
    st.markdown('<h2 style="color: #FF4D4D;">🎯 Filtros</h2>', unsafe_allow_html=True)
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
        min_value=float(df['FAT_2026'].min() if pd.notna(df['FAT_2026'].min()) else 0),
        max_value=float(df['FAT_2026'].max() if pd.notna(df['FAT_2026'].max()) else 0),
        value=(float(df['FAT_2026'].min() if pd.notna(df['FAT_2026'].min()) else 0), 
               float(df['FAT_2026'].max() if pd.notna(df['FAT_2026'].max()) else 0))
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Aplicar filtros
df_filtrado = df[
    (df['LOJA'].isin(lojas_selecionadas)) &
    (df['FAT_2026'] >= fat_min) &
    (df['FAT_2026'] <= fat_max)
].copy()

# Métricas principais
st.markdown('<h2 class="sub-header">📊 Visão Geral</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)


with col1:
    fat_total_2025= df_filtrado['FAT_2025'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_2025:,.2f}</div>
        <div class="metric-label" style="color: white;">Faturamento Total 2025</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    fat_total_2026=df_filtrado['FAT_2026'].sum() if not df_filtrado['FAT_2026'].isna().all() else 0
    variacao = ((fat_total_2026 - fat_total_2025) / fat_total_2025 * 100) if fat_total_2025 > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_2026:,.2f}</div>
        <div class="metric-label" style="color: white;">Faturamento Total 2026</div>
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
        <div class="metric-label" style="color: white;">Ticket Médio Médio 2026</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Gráficos em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FF4D4D;">🏆 Ranking de Faturamento 2026</h3>', unsafe_allow_html=True)
    
    # Ranking do MAIOR para o MENOR faturamento
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
    st.markdown('<h3 style="color: #FF4D4D;">📈 Comparativo 2025 vs 2026</h3>', unsafe_allow_html=True)
    
    # Preparar dados para o gráfico (removendo lojas sem dados de 2025)
    df_comp = df_filtrado[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
    df_comp = df_comp.dropna(subset=['FAT_2025'])
    
    if not df_comp.empty:
        # Calcular a variação percentual
        df_comp['VARIACAO_%'] = ((df_comp['FAT_2026'] - df_comp['FAT_2025']) / df_comp['FAT_2025']) * 100
        
        # Ordenar por variação percentual (decrescente)
        df_comp = df_comp.sort_values('VARIACAO_%', ascending=False).reset_index(drop=True)
        
        # Criar cores baseadas na variação (azul para positivo, vermelho para negativo)
        cores = ['#FF8C00' if x >= 0 else '#FF4D4D' for x in df_comp['VARIACAO_%']]
        
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
        
        # Adicionar linha de referência em 0%
        fig_comp.add_hline(y=0, line_dash="solid", line_color="#666", line_width=1)
        
        fig_comp.update_layout(
            title=None,
            xaxis_title=None,
            yaxis_title=None,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FF8C00', size=12),
            yaxis=dict(
                ticksuffix='%',
                gridcolor='rgba(255, 140, 0, 0.2)',
                gridwidth=1,
                zeroline=False
            ),
            xaxis=dict(
                tickangle=45,
                tickfont=dict(size=11)
            ),
            showlegend=False,
            margin=dict(l=40, r=40, t=20, b=80)
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
        
        # Mostrar tabela de dados similar à imagem
st.markdown("### 📊 Detalhamento por Loja")

# Formatar dados para tabela
df_display = df_comp.copy()
df_display['FAT_2025'] = df_display['FAT_2025'].apply(lambda x: f'R$ {x:,.2f}')
df_display['FAT_2026'] = df_display['FAT_2026'].apply(lambda x: f'R$ {x:,.2f}')
df_display['VARIACAO_%'] = df_display['VARIACAO_%'].apply(lambda x: f'{x:.1f}%')

# Renomear colunas
df_display.columns = ['Loja', 'Faturamento 2026', 'Faturamento 2025', 'Variação %']

# CENTRALIZAR TABELA
col_left, col_center, col_right = st.columns([1,4,1])

with col_center:
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Variação %": st.column_config.TextColumn(
                "Variação %",
                help="Percentual de variação 2026 vs 2025"
            )
        }
    )

# RESUMO
st.markdown("### 📈 Resumo")

col_left, col_center, col_right = st.columns([1,4,1])

with col_center:
    col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)

    with col_metric1:
        media_variacao = df_comp['VARIACAO_%'].mean()
        st.metric("Variação Média", f"{media_variacao:.1f}%")

    with col_metric2:
        total_crescimento = len(df_comp[df_comp['VARIACAO_%'] > 0])
        st.metric("Lojas em Crescimento", total_crescimento)

    with col_metric3:
        total_queda = len(df_comp[df_comp['VARIACAO_%'] < 0])
        st.metric("Lojas em Queda", total_queda)

    with col_metric4:
        melhor_loja = df_comp.loc[df_comp['VARIACAO_%'].idxmax(), 'LOJA']
        melhor_variacao = df_comp['VARIACAO_%'].max()
        st.metric("Melhor Performance", f"{melhor_loja} ({melhor_variacao:.1f}%)")

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
    st.markdown('<h3 style="color: #FF4D4D;">📊 Quantidade Promocionada por Loja</h3>', unsafe_allow_html=True)
    
    # Gráfico de quantidade vendida do produto por loja
    df_prod = df_filtrado[df_filtrado['QUANTIDADE'] > 0][['LOJA', 'QUANTIDADE']].copy()
    
    if not df_prod.empty:
        fig_prod = px.bar(
            df_prod,
            x='LOJA',
            y='QUANTIDADE',
            title='Quantidade Entregue do Garotinho Amstel por Loja',
            labels={'QUANTIDADE': 'Quantidade Entregue', 'LOJA': 'Loja'},
            color='QUANTIDADE',
            color_continuous_scale=['#FFD700', '#FF8C00'],
            text='QUANTIDADE'
        )
        fig_prod.update_traces(textposition='outside')
        fig_prod.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FF8C00'),
            xaxis={'categoryorder': 'total descending'}
        )
        st.plotly_chart(fig_prod, use_container_width=True)
    else:
        st.info("Não há vendas do produto promocional para as lojas selecionadas")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FF4D4D;">🥧 Distribuição do Produto Promocional</h3>', unsafe_allow_html=True)
    
    # Gráfico de pizza com a distribuição das quantidades
    df_prod_pie = df_filtrado[df_filtrado['QUANTIDADE'] > 0][['LOJA', 'QUANTIDADE']].copy()
    
    if not df_prod_pie.empty:
        fig_prod_pie = px.pie(
            df_prod_pie,
            values='QUANTIDADE',
            names='LOJA',
            title='Distribuição do Garotinho Amstel Entregue',
            color_discrete_sequence=['#FF8C00', '#FFA500', '#FFD700', '#FFB347', '#FFA07A']
        )
        fig_prod_pie.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FF8C00')
        )
        st.plotly_chart(fig_prod_pie, use_container_width=True)
    else:
        st.info("Não há dados de distribuição para o produto promocional")
    st.markdown('</div>', unsafe_allow_html=True)

# Tabela de dados completa
st.markdown('<h2 class="sub-header">📊 Dados Completos</h2>', unsafe_allow_html=True)

# Formatar dados para exibição
df_display = df_filtrado.copy()
df_display['FAT_2026'] = df_display['FAT_2026'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
df_display['FAT_2025'] = df_display['FAT_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
df_display['TM_2026'] = df_display['TM_2026'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')
df_display['TM_2025'] = df_display['TM_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) else 'N/A')

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
        "PROD_PROMOCIONADO": "Ação",
        "COMPOSICAO_PROD": "Composição",
        "QUANTIDADE": "Qtd Entregue"
    }
)

# Rodapé
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #FF4D4D;'>Dashboard desenvolvido com Streamlit • Dados atualizados em {}</p>".format(
        datetime.now().strftime("%d/%m/%Y %H:%M")
    ),
    unsafe_allow_html=True
)
