import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="Calculadora de Calda Agronômica",
    page_icon="🌱",
    layout="wide"
)

# Estilização personalizada simulando o design da imagem
st.markdown("""
    <style>
        .main-header {
            background-color: #0b5127;
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            font-family: 'sans-serif';
            margin-bottom: 25px;
        }
        .metric-card {
            background-color: #f4fbf7;
            border: 2px solid #a3d9b7;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        }
        .metric-title {
            color: #2e7d32;
            font-weight: bold;
            font-size: 14px;
            text-transform: uppercase;
            margin-bottom: 5px;
        }
        .metric-value {
            color: #0b5127;
            font-size: 24px;
            font-weight: bold;
        }
        .section-title {
            color: #0b5127;
            font-size: 26px;
            font-weight: bold;
            text-align: center;
            margin-top: 30px;
            margin-bottom: 20px;
        }
        .obs-box {
            background-color: #e8f5e9;
            border-left: 5px solid #2e7d32;
            padding: 15px;
            border-radius: 5px;
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho Principal dinâmico
st.markdown("""
    <div class="main-header">
        <h1 style='margin:0; font-size: 28px;'>📢 APLICAÇÃO DE DESSECAÇÃO PRÉ MILHO</h1>
        <p style='margin:5px 0 0 0; font-size: 16px; opacity: 0.9;'>Configuração Dinâmica de Calda Agronômica</p>
    </div>
""", unsafe_allow_html=True)

# --- GERENCIAMENTO DE ESTADO (PRODUTOS) ---
if "lista_produtos" not in st.session_state:
    st.session_state.lista_produtos = [
        {"nome": "Klech Neutro", "dose_alq": 0.13, "unidade": "Lts"},
        {"nome": "Elimineite Ultra", "dose_alq": 1.20, "unidade": "Kg"},
        {"nome": "Gapper", "dose_alq": 750.0, "unidade": "Ml"}, 
        {"nome": "Aureo", "dose_alq": 1.00, "unidade": "Lts"},
        {"nome": "Animobor", "dose_alq": 0.26, "unidade": "Lts"},
    ]

# --- PAINEL LATERAL (INPUTS FORMULADOS) ---
st.sidebar.header("⚙️ Parâmetros da Aplicação")

# Entradas principais solicitadas por você
input_tanque = st.sidebar.number_input("Volume do Tanque (Lts)", min_value=100, max_value=20000, value=2500, step=100)
input_taxa_ha = st.sidebar.number_input("Taxa por Hectare (Lts/ha)", min_value=10.0, max_value=1000.0, value=110.0, step=5.0)
input_area_total_alq = st.sidebar.number_input("Área Total da Propriedade (Alqueires)", min_value=0.1, max_value=5000.0, value=9.37, step=0.1)

# --- APLICAÇÃO DA SUA FÓRMULA ---
total_ha_por_tanque = input_tanque / input_taxa_ha if input_taxa_ha > 0 else 0
total_alq_por_tanque = total_ha_por_tanque * 2.42

# Cálculo do Volume de Calda Total da propriedade com base na autonomia calculada
# Conversão reversa para saber a taxa por alqueire: (Volume do Tanque / Total de Alqueires por Tanque)
taxa_l_alq = input_tanque / total_alq_por_tanque if total_alq_por_tanque > 0 else 0
volume_calda_total_propriedade = input_area_total_alq * taxa_l_alq

st.sidebar.markdown("---")
st.sidebar.subheader("➕ Adicionar Novo Produto")

novo_nome = st.sidebar.text_input("Nome do Produto", placeholder="Ex: Glyphosate")
# Suas unidades personalizadas incluídas aqui:
nova_unidade = st.sidebar.selectbox("Unidade", ["Kg", "Lts", "Gr", "Ml"])
nova_dose = st.sidebar.number_input("Dose por Alqueire", min_value=0.01, max_value=5000.0, value=1.0, step=0.01)

if st.sidebar.button("➕ Adicionar Produto à Calda", use_container_width=True):
    if novo_nome.strip() != "":
        st.session_state.lista_produtos.append({
            "nome": novo_nome,
            "dose_alq": nova_dose,
            "unidade": nova_unidade
        })
        st.sidebar.success(f"'{novo_nome}' adicionado com sucesso!")
        st.rerun()
    else:
        st.sidebar.error("Por favor, digite o nome do produto.")

if st.sidebar.button("🔄 Resetar para Lista Original", use_container_width=True):
    del st.session_state.lista_produtos
    st.rerun()


# --- CARDS DE MÉTRICAS PRINCIPAIS (AUTONOMIA DO TANQUE) ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">💧 Volume Tanque</div><div class="metric-value">{input_tanque} Lts</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-title">📉 Taxa Hectare</div><div class="metric-value">{input_taxa_ha} Lts/ha</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">🌾 Ha por Tanque</div><div class="metric-value">{total_ha_por_tanque:,.2f} ha</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">📐 Alq por Tanque</div><div class="metric-value">{total_alq_por_tanque:,.2f} alq</div></div>', unsafe_allow_html=True)

# --- SEÇÃO DA TABELA DE COMPOSIÇÃO DA CALDA ---
st.markdown('<div class="section-title">🍏 COMPOSIÇÃO DA CALDA POR TANQUE</div>', unsafe_allow_html=True)

dados_tabela = []
for p in st.session_state.lista_produtos:
    dose_alq_str = f"{p['dose_alq']:.2f} {p['unidade']}/alq" if p['nome'] != "Gapper" else f"{int(p['dose_alq'])} Ml/alq"
        
    # Nova regra: Dose por tanque = Dose por Alqueire * Total de Alqueires por Tanque
    dose_tanque = p["dose_alq"] * total_alq_por_tanque
    
    dados_tabela.append({
        "PRODUTO": p["nome"],
        "DOSE (POR ALQUEIRE)": dose_alq_str,
        "DOSE RECOMENDADA (POR TANQUE)": f"{dose_tanque:,.2f} {p['unidade']}/tanque"
    })

st.table(dados_tabela)

# Painel inferior de Observações Técnicas e Volume Total da Propriedade
st.markdown(f"""
    <div class="obs-box">
        <h4 style='margin:0 0 10px 0; color: #0b5127;'>ℹ️ INFORMAÇÕES GERAIS DA PROPRIEDADE</h4>
        <ul style='margin:0; padding-left:20px; color: #333;'>
            <li><b>Área Total Informada:</b> {input_area_total_alq} alqueires.</li>
            <li><b>Volume de Calda Total para a propriedade:</b> {volume_calda_total_propriedade:,.1f} Lts necessários.</li>
            <li><b>Fator de Conversão Utilizado:</b> 1 Alqueire = 2.42 Hectares.</li>
            <li>Recomenda-se pH da água entre <b>5,5 e 6,5</b>.</li>
            <li>Utilizar <b>EPI adequado</b> durante o preparo e aplicação da calda.</li>
        </ul>
    </div>
    <br>
    <div style='text-align:center; font-size:12px; color:#777; font-weight:bold;'>
        RECEITA AGRONÔMICA • USO EXCLUSIVO AGRÍCOLA • Seguir legislação e recomendação técnica.
    </div>
""", unsafe_allow_html=True)
