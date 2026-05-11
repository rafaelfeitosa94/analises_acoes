import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
import requests
from io import BytesIO

# ======================================================
# CONFIGURAÇÃO DA PÁGINA
# ======================================================
st.set_page_config(
    page_title="BI Estratégico - Carteira Alta Renda",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======================================================
# LOGIN
# ======================================================

USUARIOS = {
    "admin": "123456",
    "gerente": "sicoob2026",
    "rafael": "123"
}

if "logado" not in st.session_state:
    st.session_state.logado = False

def fazer_login():
    
    st.markdown("""
    <style>
    .block-container{
        padding-top:1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])

    with col2:

        st.markdown("""
        <div style="
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0px 4px 25px rgba(0,0,0,0.1);
            margin-top: 80px;
        ">
        """, unsafe_allow_html=True)

        st.markdown("""
        <h1 style='text-align:center;color:#00A859;font-size:38px;'>
        SICOOB
        </h1>
        """, unsafe_allow_html=True)

        st.markdown("""
        <h3 style='text-align:center;color:gray;margin-bottom:30px;'>
        Login do Dashboard
        </h3>
        """, unsafe_allow_html=True)

        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar", use_container_width=True):

            if usuario in USUARIOS and USUARIOS[usuario] == senha:
                st.session_state.logado = True
                st.rerun()

            else:
                st.error("Usuário ou senha inválidos")

        st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.logado:
    fazer_login()
    st.stop()

# ======================================================
# CSS GLOBAL
# ======================================================

st.markdown("""
<style>

/* FUNDO */
html, body, [class*="css"] {
    background-color: #f1f5f9;
}

/* REMOVE ESPAÇO SUPERIOR */
.block-container {
    padding-top: 0rem;
}

/* REMOVE HEADER */
header[data-testid="stHeader"]{
    height:0px;
}

[data-testid="stToolbar"]{
    visibility:hidden;
    height:0px;
}

/* CARDS */
.metric-card {
    background: linear-gradient(135deg, #00A859 0%, #008C4A 100%);
    padding: 1.5rem;
    border-radius: 18px;
    text-align:center;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.1);
}

.metric-title{
    color:white;
    font-size:16px;
}

.metric-value{
    color:white;
    font-size:34px;
    font-weight:bold;
}

/* BOXES */
.section-card{
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.06);
}

/* TITULOS */
.sub-title{
    color:#0f172a;
    font-size:24px;
    font-weight:700;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# FUNÇÃO LOGO
# ======================================================

@st.cache_data
def get_logo():

    url = "https://vectorseek.com/wp-content/uploads/2023/09/Sicoob-Novo-Logo-Vector.svg-.png"

    response = requests.get(url)

    return base64.b64encode(response.content).decode()

logo = get_logo()

# ======================================================
# CABEÇALHO CENTRALIZADO
# ======================================================

st.markdown(f"""
<div style="
    width:100%;
    display:flex;
    justify-content:center;
    align-items:center;
    flex-direction:column;
    margin-top:10px;
    margin-bottom:30px;
">

    <img src="data:image/png;base64,{logo}" width="300">

    <h1 style="
        color:#0f172a;
        margin-top:10px;
        font-size:42px;
        font-weight:800;
        text-align:center;
    ">
        BI Estratégico - Carteira Alta Renda
    </h1>

    <p style="
        color:gray;
        font-size:18px;
        margin-top:-10px;
        text-align:center;
    ">
        Análise comercial da carteira PF Alto Relacionamento
    </p>

</div>
""", unsafe_allow_html=True)

# ======================================================
# DADOS
# ======================================================

cooperados = [
    {
        'nome': 'ELIZABETE DE SA CARVALHO PINTO TRINDADE',
        'quadrante': 'Q4',
        'diagnostico': 'Perfil conservador e pouco engajado',
        'risco': 'Baixo',
        'foco': 'Investimentos e seguros',
        'saldo': 720,
    },
    {
        'nome': 'JAYME DOS SANTOS CASTRO',
        'quadrante': 'Q2',
        'diagnostico': 'Cooperado premium e rentável',
        'risco': 'Moderado',
        'foco': 'Reorganização financeira',
        'saldo': -2200,
    },
    {
        'nome': 'FABIO PEREIRA DA CRUZ',
        'quadrante': 'Q1',
        'diagnostico': 'Perfil de atenção financeira',
        'risco': 'Alto',
        'foco': 'Renegociação financeira',
        'saldo': -3006,
    },
    {
        'nome': 'DAMIAO PEREIRA DA SILVA',
        'quadrante': 'Q1',
        'diagnostico': 'Perfil saudável',
        'risco': 'Baixo',
        'foco': 'Expansão de produtos',
        'saldo': 0.46,
    },
    {
        'nome': 'MARIA MOREIRA DA SILVA',
        'quadrante': 'Q1',
        'diagnostico': 'Relacionamento sólido',
        'risco': 'Baixo',
        'foco': 'Investimentos e previdência',
        'saldo': 9159,
    },
    {
        'nome': 'MAIRA MARQUES DE ALMEIDA',
        'quadrante': 'Q4',
        'diagnostico': 'Alta renda pouco ativa',
        'risco': 'Baixo',
        'foco': 'Ativação comercial',
        'saldo': 24,
    },
    {
        'nome': 'UILLIAN PETRONIO DOS SANTOS MONTEIRO',
        'quadrante': 'Q1',
        'diagnostico': 'Muito ativo e pressionado',
        'risco': 'Moderado',
        'foco': 'Controle de endividamento',
        'saldo': -2597,
    },
    {
        'nome': 'EDINALDO FERREIRA DA SILVA',
        'quadrante': 'Q2',
        'diagnostico': 'Rentável com dependência do rotativo',
        'risco': 'Moderado',
        'foco': 'Transformar cheque especial em crédito',
        'saldo': -4932,
    },
]

df = pd.DataFrame(cooperados)

# ======================================================
# MÉTRICAS
# ======================================================

total = len(df)
q1 = len(df[df["quadrante"] == "Q1"])
q2 = len(df[df["quadrante"] == "Q2"])
q4 = len(df[df["quadrante"] == "Q4"])

col1, col2, col3, col4 = st.columns(4)

cards = [
    ("Total Cooperados", total),
    ("Quadrante Q1", q1),
    ("Quadrante Q2", q2),
    ("Quadrante Q4", q4),
]

for col, (titulo, valor) in zip([col1,col2,col3,col4], cards):

    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{titulo}</div>
            <div class="metric-value">{valor}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ======================================================
# GRÁFICOS
# ======================================================

col1, col2 = st.columns(2)

with col1:

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown('<div class="sub-title">📊 Distribuição por Quadrante</div>', unsafe_allow_html=True)

    fig = px.pie(
        df,
        names='quadrante',
        hole=0.5,
        color='quadrante',
        color_discrete_map={
            'Q1':'#00A859',
            'Q2':'#FFC107',
            'Q4':'#EF4444'
        }
    )

    fig.update_layout(height=400)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col2:

    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    st.markdown('<div class="sub-title">⚠️ Distribuição por Risco</div>', unsafe_allow_html=True)

    risco = df['risco'].value_counts().reset_index()
    risco.columns = ['risco','total']

    fig2 = px.bar(
        risco,
        x='risco',
        y='total',
        color='risco',
        text='total',
        color_discrete_map={
            'Baixo':'#00A859',
            'Moderado':'#FFC107',
            'Alto':'#EF4444'
        }
    )

    fig2.update_layout(height=400)

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ======================================================
# TABELA
# ======================================================

st.markdown("""
<div class="section-card">
<div class="sub-title">
📋 Visão Estratégica da Carteira
</div>
""", unsafe_allow_html=True)

df_show = df.copy()

df_show["saldo"] = df_show["saldo"].apply(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

df_show.columns = [
    "Cooperado",
    "Quadrante",
    "Diagnóstico",
    "Risco",
    "Foco Comercial",
    "Saldo Conta"
]

st.dataframe(
    df_show,
    use_container_width=True,
    height=400
)

st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# ALERTAS
# ======================================================

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div class="section-card">
    <div class="sub-title">
    🎯 Principais Oportunidades
    </div>
    """, unsafe_allow_html=True)

    st.success("Open Finance para centralização")
    st.success("Expansão de investimentos")
    st.success("Previdência privada")
    st.success("Seguro de vida")
    st.success("Cross selling de crédito")

    st.markdown("</div>", unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="section-card">
    <div class="sub-title">
    🚨 Alertas da Carteira
    </div>
    """, unsafe_allow_html=True)

    st.warning("Uso elevado de cheque especial")
    st.warning("Dependência de rotativo")
    st.warning("Clientes Q4 pouco engajados")
    st.warning("Necessidade de retenção premium")
    st.warning("Baixa penetração em investimentos")

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# RODAPÉ
# ======================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(f"""
<div style="
    text-align:center;
    color:gray;
    font-size:14px;
">
Dashboard Estratégico Sicoob • Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')}
</div>
""", unsafe_allow_html=True)
