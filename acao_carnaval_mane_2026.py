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
    page_title="Dashboard Mané - Análise de Vendas",
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
    color: #FF4D4D !important;
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
        url = "https://botecomane.com.br/wp-content/uploads/2024/06/mane-logo-vermelho.png"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# CSS personalizado com cores vermelho sangue e vermelho claro
st.markdown("""
<style>
    .sub-header {
        font-size: 1.5rem;
        color: #FF4D4D;
        margin-bottom: 1rem;
        border-bottom: 3px solid #FF9999;
        padding-bottom: 0.5rem;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #8B0000 0%, #FF4D4D 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(139,0,0,0.3);
        text-align: center;
        border: 1px solid #FF9999;
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
        background: linear-gradient(135deg, #8B0000 0%, #B22222 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(139,0,0,0.3);
        height: 100%;
    }
    .ranking-title {
        color: #FF9999;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        border-bottom: 2px solid #FF9999;
        padding-bottom: 0.5rem;
    }
    .ranking-item {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        border-left: 5px solid #FF9999;
        backdrop-filter: blur(5px);
        transition: transform 0.2s;
    }
    .ranking-item:hover {
        transform: translateX(5px);
        background-color: rgba(255, 153, 153, 0.2);
    }
    .ranking-item strong {
        color: white;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    .ranking-item .ranking-value {
        color: #FF9999;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .ranking-item .ranking-label {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
    }
    .ranking-badge {
        background-color: #FF4D4D;
        color: #8B0000;
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
        box-shadow: 0 2px 10px rgba(139,0,0,0.2);
        margin-bottom: 1rem;
    }
    .filter-section {
        background: linear-gradient(135deg, #2a1a1a 0%, #3d1e1e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #FF9999;
    }
    .st-emotion-cache-16idsys p {
        color: #FF4D4D;
    }
    .st-emotion-cache-1dj0hjr {
        color: #FF4D4D;
    }
    footer {
        color: #FF4D4D;
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
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-bottom: 2rem; padding: 1rem; background: linear-gradient(135deg, #2a1a1a 0%, #3d1e1e 100%); border-radius: 20px; box-shadow: 0 4px 15px rgba(139,0,0,0.2); width: 100%;">
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
        '<p style="color:#FF4D4D;font-weight:bold;text-align:center;">Logo não disponível</p>',
        unsafe_allow_html=True
    )

# Título principal
st.markdown("""
<h1 style="font-size: 2.5rem; color: #FF4D4D; font-weight: bold; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(139,0,0,0.3); text-align: center;">🍺 CARNAVAL MANÉ 2026</h1>
""", unsafe_allow_html=True)

# Subtítulo com gradiente vermelho
st.markdown("""
<div style="display: flex; justify-content: center; width: 100%; margin-top: 0.5rem;">
    <p style="background: linear-gradient(135deg, #8B0000 0%, #FF4D4D 100%); color: white; font-weight: bold; font-size: 1.2rem; padding: 0.8rem 2rem; border-radius: 50px; box-shadow: 0 4px 10px rgba(139,0,0,0.4); margin: 0; display: inline-block; text-align: center;">Análise de Performance - 2025 vs 2026</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Dados fornecidos
data = {
    'MARCA': ['MANÉ', 'MANÉ', 'MANÉ', 'MANÉ', 'MANÉ', 'MANÉ', 'MANÉ', 'MANÉ', 'MANÉ', 'MANÉ', 
              'MANÉ', 'MANÉ', 'MANÉ', 'MANÉ', 'MANÉ', 'MANÉ', 'MANÉ'],
    
    'LOJA': ['MAN RECREIO', 'MAN COPACABANA', 'MAN NITERÓI', 'MAN NOVA IGUAÇÚ', 'MAN PARK SHOP CG', 
             'MAN VILA DA PENHA', 'MAN CENTRO RJ', 'MAN BÚZIOS', 'MAN COLLAB CABO FRIO', 'MAN COLLAB VALQUEIRE', 
             'MAN IPANEMA', 'MAN ITAIPAVA', 'MAN MACAÉ', 'MAN NOVA AMÉRICA', 'MAN OLEGÁRIO', 'MAN RIO DAS OSTRAS', 
             'MAN VILA VELHA'],
    
    'FAT_2026': [32879.36, 49782.32, 101136.15, 41398.28, 20697.32, 
                  3417.29, 1106.99, 106240.13, 41643.6, 9505.41, 
                  58215.7, 42273.15, 97718.28, 36650.12, 38624.21, 13948.9, 82042.02],
    
    'TC_2026': [398, 578, 1039, 464, 266, 
                59, 30, 988, 489, 178, 
                837, 331, 1019, 392, 341, 153, 1395],
    
    'TM_2026': [82.61, 86.13, 97.34, 89.22, 77.81, 
                57.92, 36.90, 107.53, 85.16, 53.40, 
                69.55, 127.71, 95.90, 93.50, 113.27, 91.17, 58.81],
    
    'FAT_2025': [38595.29, 52623.25, 121689.53, None, 32386.1, 
                 9856.87, None, 119645.46, 48740.86, 14686.81, 
                 82617.81, 30939.0, 80535.54, 62534.94, 51614.84, 53967.16, None],
    
    'TC_2025': [347, 642, 1179, None, 393, 
                165, None, 1092, 603, 160, 
                1555, 465, 1080, 898, 740, 942, None],
    
    'TM_2025': [111.23, 81.97, 103.21, None, 82.41, 
                59.74, None, 109.57, 80.83, 91.79, 
                53.13, 66.54, 74.57, 69.64, 69.75, 57.29, None],
    
    'PROD_PROMOCIONADO': ['AÇÃO CARNAVAL 26'] * 17,
    
    'COMPOSICAO_PROD': ['TULIPA OU CANECA AMSTEL'] * 17,
    
    'QUANTIDADE': [32, 27, 26, 3, 2, 
                   2, 1, 0, 0, 0, 
                   0, 0, 0, 0, 0, 0, 0],
    
    'VALOR_VENDA_PROD': [1907, 1859, 2805, 3987, 1490, 
                         106, 44, 1144, 2066, 1430, 
                         3742, 198, 2013, 3693, 2384, 1016, 4126],
    
    'PART.(%)': [0.0580, 0.0373, 0.0277, 0.0963, 0.0720, 
                 0.0310, 0.0397, 0.0108, 0.0496, 0.1504, 
                 0.0643, 0.0047, 0.0206, 0.1008, 0.0617, 0.0728, 0.0503]
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
    st.markdown('<h3 style="color: #FF4D4D;">🏆 Ranking de Faturamento 2026</h3>', unsafe_allow_html=True)
    
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
        color_continuous_scale=['#FF9999', '#8B0000']
    )
    fig_ranking.update_layout(
        height=400, 
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FF4D4D'),
        yaxis={'categoryorder': 'total ascending'}  # Forçar ordenação ascendente no eixo Y
    )
    st.plotly_chart(fig_ranking, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FF4D4D;">📈 Comparativo 2025 vs 2026</h3>', unsafe_allow_html=True)
    
    # Preparar dados para o gráfico
    df_comp = df_filtrado[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
    df_comp = df_comp.dropna(subset=['FAT_2025'])
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name='2026',
        x=df_comp['LOJA'],
        y=df_comp['FAT_2026'],
        marker_color='#8B0000'
    ))
    fig_comp.add_trace(go.Bar(
        name='2025',
        x=df_comp['LOJA'],
        y=df_comp['FAT_2025'],
        marker_color='#FF9999'
    ))
    
    fig_comp.update_layout(
        title='Faturamento por Loja',
        xaxis_title='Loja',
        yaxis_title='Faturamento (R$)',
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FF4D4D')
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
            color_discrete_sequence=['#8B0000', '#B22222', '#FF4D4D', '#FF9999', '#DC143C']
        )
        fig_prod.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FF4D4D')
        )
        st.plotly_chart(fig_prod, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FF4D4D;">📊 Participação no Faturamento</h3>', unsafe_allow_html=True)
    
    df_part = df_filtrado.nlargest(10, 'PART.(%)')[['LOJA', 'PART.(%)', 'VALOR_VENDA_PROD']].copy()
    df_part['PART.(%)'] = df_part['PART.(%)'] * 100
    
    fig_part = px.bar(
        df_part,
        x='LOJA',
        y='PART.(%)',
        title='% de Participação do Produto no Faturamento',
        labels={'PART.(%)': 'Participação (%)', 'LOJA': 'Loja'},
        color='PART.(%)',
        color_continuous_scale=['#FF9999', '#8B0000'],
        text=df_part['PART.(%)'].round(1).astype(str) + '%'
    )
    fig_part.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FF4D4D')
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
    "<p style='text-align: center; color: #FF4D4D;'>Dashboard desenvolvido com Streamlit • Dados atualizados em {}</p>".format(
        datetime.now().strftime("%d/%m/%Y %H:%M")
    ),
    unsafe_allow_html=True

)
