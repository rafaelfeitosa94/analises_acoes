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
import hashlib

# Configuração da página (DEVE SER O PRIMEIRO COMANDO STREAMLIT)
st.set_page_config(
    page_title="Dia do consumidor Bendito",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SISTEMA DE LOGIN
# ============================================

# Configurações de usuários (em produção, use um banco de dados)
# As senhas são armazenadas como hash por segurança
USERS = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "bendito": hashlib.sha256("bendito2026".encode()).hexdigest(),
    "gerente": hashlib.sha256("bendito123".encode()).hexdigest(),
    "marketing": hashlib.sha256("impettus123".encode()).hexdigest(),
}

def check_password(username, password):
    """Verifica se o usuário e senha estão corretos"""
    if username in USERS:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == USERS[username]
    return False

def login_screen():
    """Exibe a tela de login"""
    # CSS para a tela de login
    st.markdown("""
    <style>
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
        background: linear-gradient(135deg, #0e1117 0%, #1a2a0f 100%);
    }

    .login-title {
        text-align: center;
        color: #96c734;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .login-subtitle {
        text-align: center;
        color: #FAFAFA;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    .login-error {
        background-color: rgba(255, 68, 68, 0.1);
        border-left: 4px solid #ff4444;
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        color: #ff8888;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Logo na tela de login
    logo = load_logo()
    if logo:
        buffered = BytesIO()
        logo.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{img_str}" width="200" style="display: block;">
        </div>
        """, unsafe_allow_html=True)
    
    # Card de login
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Dia do Consumidor Bendito 💵</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-subtitle">Acesso ao Dashboard</div>', unsafe_allow_html=True)
        
        # Formulário de login
        with st.form("login_form"):
            username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button("🔓 Entrar", use_container_width=True)
            
            if submit:
                if username and password:
                    if check_password(username, password):
                        st.session_state["authenticated"] = True
                        st.session_state["username"] = username
                        st.rerun()
                    else:
                        st.markdown('<div class="login-error">❌ Usuário ou senha incorretos!</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="login-error">⚠️ Preencha todos os campos!</div>', unsafe_allow_html=True)
        
        # Informações de acesso (apenas para demonstração - remova em produção)
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; font-size: 0.8rem; opacity: 0.6;">
            <p>🔐 Credenciais de demonstração:</p>
            <p><strong>admin</strong> / admin123</p>
            <p><strong>bendito</strong> / pascoa2026</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Função para fazer logout"""
    if st.sidebar.button("🚪 Sair do Sistema", use_container_width=True):
        for key in ["authenticated", "username"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# ============================================
# DASHBOARD PRINCIPAL
# ============================================

# Função para carregar o logo
@st.cache_data
def load_logo():
    try:
        url = "https://grupoimpettus.com.br/wp-content/uploads/2024/09/grupo-impettus-logo-branco-bendito.png"
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img
    except:
        return None

# CSS personalizado com cores verdes
def apply_custom_css():
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
        color: #96c734 !important;
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
    
    .sub-header {
        font-size: 1.5rem;
        color: #96c734;
        margin-bottom: 1rem;
        border-bottom: 3px solid #96c734;
        padding-bottom: 0.5rem;
        font-weight: 600;
    }
    .metric-card {
        background: linear-gradient(135deg, #5a8a1e 0%, #96c734 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(150,199,52,0.2);
        text-align: center;
        border: 1px solid #96c734;
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
        background: linear-gradient(135deg, #5a8a1e 0%, #96c734 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(150,199,52,0.2);
        height: 100%;
    }
    .ranking-title {
        color: white;
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        border-bottom: 2px solid #96c734;
        padding-bottom: 0.5rem;
    }
    .ranking-item {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        margin: 0.8rem 0;
        border-radius: 10px;
        border-left: 5px solid #96c734;
        transition: transform 0.2s;
    }
    .ranking-item:hover {
        transform: translateX(5px);
        background-color: rgba(150, 199, 52, 0.2);
    }
    .ranking-item strong {
        color: white;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.3rem;
    }
    .ranking-item .ranking-value {
        color: #96c734;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .ranking-item .ranking-label {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
    }
    .ranking-badge {
        background-color: #96c734;
        color: #1a1d24;
        font-weight: bold;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .filter-section {
        background: linear-gradient(135deg, #1a2a0f 0%, #0a1a0f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #96c734;
    }
    .summary-card {
        background: linear-gradient(135deg, #5a8a1e 0%, #96c734 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #96c734;
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

def main_dashboard():
    """Função principal do dashboard"""
    apply_custom_css()
    
    # Carregar o logo
    logo = load_logo()
    
    # Sidebar com informações do usuário e filtros
    with st.sidebar:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #5a8a1e 0%, #96c734 100%); 
                    padding: 1rem; 
                    border-radius: 10px; 
                    margin-bottom: 1rem;
                    text-align: center;">
            <div style="color: white; font-size: 1.2rem; font-weight: bold;">👤 Usuário</div>
            <div style="color: #1a1d24; font-size: 1rem; font-weight: bold;">{st.session_state.get('username', 'Usuário')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h2 style="color: #96c734;">🎯 Filtros</h2>', unsafe_allow_html=True)
    
    # CABEÇALHO CENTRALIZADO
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-bottom: 2rem; padding: 1rem; background: linear-gradient(135deg, #1a2a0f 0%, #0a1a0f 100%); border-radius: 20px; box-shadow: 0 4px 15px rgba(150,199,52,0.1); width: 100%;">
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
            '<p style="color:#96c734;font-weight:bold;text-align:center;">Logo não disponível</p>',
            unsafe_allow_html=True
        )
    
    # Título principal
    st.markdown("""
    <h1 style="font-size: 2.5rem; color: #96c734; font-weight: bold; margin-bottom: 0.5rem; text-shadow: 2px 2px 4px rgba(150,199,52,0.1); text-align: center;">💵 Dia do Consumidor Bendito 2026 💵</h1>
    """, unsafe_allow_html=True)
    
    # Subtítulo
    st.markdown("""
    <div style="display: flex; justify-content: center; width: 100%; margin-top: 0.5rem;">
        <p style="background: linear-gradient(135deg, #5a8a1e 0%, #96c734 100%); color: white; font-weight: bold; font-size: 1.2rem; padding: 0.8rem 2rem; border-radius: 50px; box-shadow: 0 4px 10px rgba(150,199,52,0.3); margin: 0; display: inline-block; text-align: center;">De 15/03 à 20/03</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dados fornecidos
    data = {
        'MARCA': ['BENDITO'] * 4,
        'LOJA': ['BEN BARÃO', 'BEN BARRA SHOPPING', 'BEN DOWNTOWN', 'BEN LEBLON'],
        'FAT_2026': [25596.66, 20205.11, 12484.69, 20984.43],
        'TC_2026': [664, 589, 268, 609],
        'TM_2026': [38.54918674698795, 34.30409168081494, 46.58466417910448, 34.4571921182266],
        'FAT_2025': [21116.62, 21431.27, 14861.93, 20181.53],
        'TC_2025': [569, 531, 323, 569],
        'TM_2025': [37.11181019332162, 40.36020715630885, 46.01216718266254, 35.468418277680136],
        'PROD_PROMOCIONADO': ['PRODUTOS VARIADOS COM 10%'] * 4,
        'QUANTIDADE_BOTÃO': [74, 76, 40, 59],
        'TORTA OMG 15/03': [0, 0, 0, 0],
        'BROWNIE C/ SORVETE 16/03': [0, 1, 0, 0],
        'COOKIES TRADICIONAIS  17/03': [21, 14, 2, 16],
        'TORTA OMG 18/03': [0, 0, 0, 0],
        'CROQUE MOUNSIEUR 19/03': [1, 1, 1, 1],
        'CAFÉS TRADICIONAIS 20/03': [52, 60, 37, 42],
        'COMPOSICAO_PROD': ['PRODUTOS VARIADOS'] * 4,
        'QUANTIDADE': [74, 76, 40, 59],
        'VALOR_VENDA_PROD': [823, 911.4, 456.2000000000001, 676.3000000000002],
        'PART.(%)': [0.032152632413760235, 0.04510740104854663, 0.03654075511686714, 0.032228657151993176]
    }
    
    df = pd.DataFrame(data)
    
    # Filtros na sidebar
    with st.sidebar:
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
        
        logout()  # Botão de logout
    
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
        tm_medio = fat_total_2026 / clientes_total if clientes_total > 0 else 0
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
        st.markdown('<h3 style="color: #96c734;">🏆 Ranking de Faturamento 2026</h3>', unsafe_allow_html=True)
        
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
            color_continuous_scale=['#c8e6a5', '#96c734']
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
        st.markdown('<h3 style="color: #96c734;">📈 Comparativo 2025 vs 2026</h3>', unsafe_allow_html=True)
        
        df_comp = df_filtrado[['LOJA', 'FAT_2026', 'FAT_2025']].copy()
        df_comp = df_comp.dropna(subset=['FAT_2025'])
        
        if not df_comp.empty:
            df_comp['VARIACAO_%'] = ((df_comp['FAT_2026'] - df_comp['FAT_2025']) / df_comp['FAT_2025']) * 100
            df_comp = df_comp.sort_values('VARIACAO_%', ascending=False).reset_index(drop=True)
            
            cores = ['#96c734' if x >= 0 else "#c8e6a5" for x in df_comp['VARIACAO_%']]
            
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
    
    # Análise do produto promocional
    st.markdown('<h2 class="sub-header">🍺 Análise do Produto Promocionado</h2>', unsafe_allow_html=True)
    
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
                color_discrete_sequence=['#96c734', '#5a8a1e', '#c8e6a5', '#7cb342', '#8bc34a']
            )
            fig_prod.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_prod, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #96c734;">📊 Participação no Faturamento</h3>', unsafe_allow_html=True)
        
        df_part = df_filtrado.nlargest(10, 'PART.(%)')[['LOJA', 'PART.(%)', 'VALOR_VENDA_PROD']].copy()
        df_part['PART.(%)'] = df_part['PART.(%)'] * 100
        
        fig_part = px.bar(
            df_part,
            x='LOJA',
            y='PART.(%)',
            title='% de Participação do Produto no Faturamento',
            labels={'PART.(%)': 'Participação (%)', 'LOJA': 'Loja'},
            color='PART.(%)',
            color_continuous_scale=['#c8e6a5', '#96c734'],
            text=df_part['PART.(%)'].round(2).astype(str) + '%'
        )
        fig_part.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig_part, use_container_width=True)
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
        f"<p style='text-align: center; color: #96c734;'>Dashboard desenvolvido com Streamlit • Dados atualizados em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>",
        unsafe_allow_html=True
    )

# ============================================
# CONTROLE DE AUTENTICAÇÃO
# ============================================

def main():
    """Função principal que controla o fluxo de autenticação"""
    
    # Inicializar estado de autenticação
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    # Verificar se o usuário está autenticado
    if st.session_state["authenticated"]:
        # Usuário autenticado - mostrar dashboard
        main_dashboard()
    else:
        # Usuário não autenticado - mostrar tela de login
        login_screen()

# Executar o aplicativo
if __name__ == "__main__":
    main()