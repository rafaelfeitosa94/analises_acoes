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
    page_title="Dia das Mães Mené 2026",
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
    color: #FF6666 !important;
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

/* ===== QUADRO DE AVISOS ===== */
.notice-board {
    background: linear-gradient(135deg, #2a1a1a 0%, #1a0f0f 100%);
    border-left: 5px solid #FF6666;
    padding: 1.5rem;
    border-radius: 15px;
    margin-top: 2rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 15px rgba(139,0,0,0.2);
}
.notice-title {
    color: #FF6666;
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.notice-item {
    color: #FAFAFA;
    padding: 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.95rem;
    border-bottom: 1px solid rgba(255,102,102,0.2);
}
.notice-item:last-child {
    border-bottom: none;
}
.notice-icon {
    font-size: 1.2rem;
    min-width: 30px;
}
.notice-text {
    flex: 1;
}
.notice-highlight {
    color: #FF6666;
    font-weight: bold;
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

# CSS personalizado com cores vermelho
st.markdown("""
<style>
    .sub-header {
        font-size: 1.5rem;
        color: #FF6666;
        margin-bottom: 1rem;
        border-bottom: 3px solid #FF6666;
        padding-bottom: 0.5rem;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #8B0000 0%, #B22222 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(139,0,0,0.2);
        text-align: center;
        border: 1px solid #FF6666;
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
        background: linear-gradient(135deg, #8B0000 0%, #B22222 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(139,0,0,0.2);
        height: 100%;
    }
    .ranking-title {
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        border-bottom: 2px solid #FF6666;
        padding-bottom: 0.5rem;
    }
    .ranking-item {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        border-left: 5px solid #FF6666;
        transition: transform 0.2s;
    }
    .ranking-item:hover {
        transform: translateX(5px);
        background-color: rgba(255, 102, 102, 0.2);
    }
    .ranking-item strong {
        color: white;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    .ranking-item .ranking-value {
        color: #FF6666;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .ranking-item .ranking-label {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
    }
    .ranking-badge {
        background-color: #FF6666;
        color: #8B0000;
        font-weight: bold;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .filter-section {
        background: linear-gradient(135deg, #2a1a1a 0%, #1a0f0f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #FF6666;
    }
    .summary-card {
        background: linear-gradient(135deg, #8B0000 0%, #B22222 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #FF6666;
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
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-bottom: 2rem; padding: 1rem; background: linear-gradient(135deg, #2a1a1a 0%, #1a0f0f 100%); border-radius: 20px; box-shadow: 0 4px 15px rgba(139,0,0,0.1); width: 100%;">
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
        '<p style="color:#FF6666;font-weight:bold;text-align:center;">Logo não disponível</p>',
        unsafe_allow_html=True
    )

# Título principal
st.markdown("""
<h1 style="font-size: 2.5rem; color: #FF6666; font-weight: bold; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(139,0,0,0.1); text-align: center;">🌹 Dia das Mães Mané 2026 🌹</h1>
""", unsafe_allow_html=True)

# Subtítulo
st.markdown("""
<div style="display: flex; justify-content: center; width: 100%; margin-top: 0.5rem;">
    <p style="background: linear-gradient(135deg, #8B0000 0%, #B22222 100%); color: white; font-weight: bold; font-size: 1.2rem; padding: 0.8rem 2rem; border-radius: 50px; box-shadow: 0 4px 10px rgba(139,0,0,0.3); margin: 0; display: inline-block; text-align: center;">09 E 10/05/2026 X 10 E 11/05/2025</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Dados fornecidos
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

# Criar um DataFrame apenas com lojas que têm dados completos para comparação
df_comparativo = df[(df['FAT_2025'] > 0) & (df['FAT_2026'] > 0)].copy()

# Sidebar para filtros
with st.sidebar:
    st.markdown('<h2 style="color: #FF6666;">🎯 Filtros</h2>', unsafe_allow_html=True)
    
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

# Filtrar também o DataFrame comparativo
df_comparativo_filtrado = df_comparativo[
    (df_comparativo['LOJA'].isin(lojas_selecionadas)) &
    (df_comparativo['FAT_2026'] >= fat_min) &
    (df_comparativo['FAT_2026'] <= fat_max)
]

# Métricas principais (usando apenas lojas com dados para 2025 e 2026)
st.markdown('<h2 class="sub-header">📊 Visão Geral</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    fat_total_2025 = df_comparativo_filtrado['FAT_2025'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_2025:,.2f}</div>
        <div class="metric-label">Faturamento Total 2025</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    fat_total_2026 = df_comparativo_filtrado['FAT_2026'].sum() if not df_comparativo_filtrado['FAT_2026'].isna().all() else 0
    variacao = ((fat_total_2026 - fat_total_2025) / fat_total_2025 * 100) if fat_total_2025 > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {fat_total_2026:,.2f}</div>
        <div class="metric-label">Faturamento Total 2026</div>
        <div class="metric-variation">{variacao:+.1f}% vs 2025</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    clientes_total = df_comparativo_filtrado['TC_2026'].sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{clientes_total:,.0f}</div>
        <div class="metric-label">Total de Clientes 2026</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    tm_medio = fat_total_2026 / clientes_total if clientes_total > 0 else 0
    tiquet_medio_2025 = fat_total_2025 / df_comparativo_filtrado['TC_2025'].sum() if df_comparativo_filtrado['TC_2025'].sum() > 0 else 0
    variacao_tm = ((tm_medio - tiquet_medio_2025) / tiquet_medio_2025 * 100) if tiquet_medio_2025 > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">R$ {tm_medio:,.2f}</div>
        <div class="metric-label">Ticket Médio Médio 2026</div>
        <div class="metric-variation">{variacao_tm:+.1f}% vs 2025</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Gráficos em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #FF6666;">🏆 Ranking de Faturamento 2026</h3>', unsafe_allow_html=True)
    
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
        color_continuous_scale=['#FF9999', '#8B0000']
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
    st.markdown('<h3 style="color: #FF6666;">📈 Comparativo 2025 vs 2026</h3>', unsafe_allow_html=True)
    
    # Usando apenas lojas com dados completos para o comparativo
    if not df_comparativo_filtrado.empty:
        df_comp = df_comparativo_filtrado[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
        df_comp['VARIACAO_%'] = ((df_comp['FAT_2026'] - df_comp['FAT_2025']) / df_comp['FAT_2025']) * 100
        df_comp = df_comp.sort_values('VARIACAO_%', ascending=False).reset_index(drop=True)
        
        cores = ['#FF6666' if x >= 0 else '#8B0000' for x in df_comp['VARIACAO_%']]
        
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
        st.warning("Nenhuma loja com dados completos para 2025 e 2026 no filtro selecionado.")

st.markdown("---")

# Tabela de detalhamento (apenas lojas com dados completos)
st.markdown("### 📊 Detalhamento por Loja (2025 vs 2026)")

if not df_comparativo_filtrado.empty:
    df_display = df_comparativo_filtrado[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
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
    st.info("Nenhuma loja com dados completos para 2025 e 2026 no filtro selecionado.")

st.markdown("---")

# RESUMO COM CARDS (apenas lojas com dados completos)
st.markdown("### 📈 Resumo de Performance")

if not df_comparativo_filtrado.empty:
    df_comp = df_comparativo_filtrado[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
    df_comp['VARIACAO_%'] = ((df_comp['FAT_2026'] - df_comp['FAT_2025']) / df_comp['FAT_2025']) * 100
    
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
            <div class="summary-sub">Com dados completos 2025/2026</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        fat_2025_total = df_comp['FAT_2025'].sum()
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1.5rem;">R$ {fat_2025_total/1000000:.1f}M</div>
            <div class="summary-label">💰 Faturamento 2025</div>
            <div class="summary-sub">Lojas com dados completos</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col7:
        fat_2026_total = df_comp['FAT_2026'].sum()
        var_total = ((fat_2026_total - fat_2025_total) / fat_2025_total * 100) if fat_2025_total > 0 else 0
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-value" style="font-size: 1.5rem;">R$ {fat_2026_total/1000000:.1f}M</div>
            <div class="summary-label">💰 Faturamento 2026</div>
            <div class="summary-sub">{var_total:+.1f}% vs 2025</div>
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
    st.warning("Nenhuma loja com dados completos para 2025 e 2026 no filtro selecionado.")

st.markdown("---")

# Ranking detalhado (usando df_filtrado completo para rankings gerais)
st.markdown('<h2 class="sub-header">📋 Ranking Detalhado por Performance</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.markdown('<div class="ranking-title">💰 TOP FATURAMENTO</div>', unsafe_allow_html=True)
    top_fat = df_filtrado[df_filtrado['FAT_2026'] > 0].nlargest(5, 'FAT_2026')[['LOJA', 'FAT_2026']]
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
    top_clientes = df_filtrado[df_filtrado['TC_2026'] > 0].nlargest(5, 'TC_2026')[['LOJA', 'TC_2026']]
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
    top_tm = df_filtrado[df_filtrado['TM_2026'] > 0].nlargest(5, 'TM_2026')[['LOJA', 'TM_2026']]
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
df_display_full['FAT_2025'] = df_display_full['FAT_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) and x > 0 else 'Sem dados')
df_display_full['TM_2026'] = df_display_full['TM_2026'].apply(lambda x: f'R$ {x:,.2f}')
df_display_full['TM_2025'] = df_display_full['TM_2025'].apply(lambda x: f'R$ {x:,.2f}' if pd.notna(x) and x > 0 else 'Sem dados')
df_display_full['VALOR_VENDA_PROD'] = df_display_full['VALOR_VENDA_PROD'].apply(lambda x: f'R$ {x:,.2f}')
df_display_full['PART.(%)'] = df_display_full['PART.(%)'].apply(lambda x: f'{x*100:.4f}%')

# Selecionar colunas para exibição
colunas_exibir = ['LOJA', 'FAT_2026', 'TC_2026', 'TM_2026', 'FAT_2025', 'TC_2025', 'TM_2025', 
                  'PROD_PROMOCIONADO', 'QUANTIDADE', 'VALOR_VENDA_PROD', 'PART.(%)']

st.dataframe(
    df_display_full[colunas_exibir],
    use_container_width=True,
    height=400
)

st.markdown("---")

# ===== QUADRO DE AVISOS =====
st.markdown("""
<div class="notice-board">
    <div class="notice-title">
        <span>📢</span>
        <span>AVISOS IMPORTANTES - METODOLOGIA</span>
    </div>
    <div class="notice-item">
        <div class="notice-icon">📊</div>
        <div class="notice-text">
            <span class="notice-highlight">Os indicadores comparativos (variação % entre 2025 e 2026)</span> levam em conta 
            <span class="notice-highlight">somente as lojas comparáveis</span> (que possuem faturamento em ambos os períodos).
        </div>
    </div>
    <div class="notice-item">
        <div class="notice-icon">🏪</div>
        <div class="notice-text">
            A loja <span class="notice-highlight">MAN CENTRO RJ</span> não abre aos fins de semana e feriados, 
            o que impacta diretamente sua performance comparativa.
        </div>
    </div>
    <div class="notice-item">
        <div class="notice-icon">💰</div>
        <div class="notice-text">
            O valor é referente ao faturamento bruto das lojas no período.
        </div>
    </div>
    <div class="notice-item">
        <div class="notice-icon">🚫</div>
        <div class="notice-text">
            As lojas <span class="notice-highlight">MAN NOVA IGUAÇÚ</span> e <span class="notice-highlight">MAN VILA VELHA</span> 
            não haviam inaugurado na data do evento em 2025, portanto não possuem dados comparativos para o período.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown(
    f"<p style='text-align: center; color: #FF6666;'>Dashboard desenvolvido com Streamlit • Dados atualizados em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>",
    unsafe_allow_html=True
)