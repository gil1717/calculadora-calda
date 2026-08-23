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
# Inicializa a lista base com os produtos da imagem caso ela não exista na memória da sessão
if "lista_produtos" not in st.session_state:
    st.session_state.lista_produtos = [
        {"nome": "Klech Neutro", "dose_alq": 0.13, "unidade": "L"},
        {"nome": "Elimineite Ultra", "dose_alq": 1.20, "unidade": "kg"},
        {"nome": "Gapper", "dose_alq": 0.75, "unidade": "L"}, 
        {"nome": "Aureo", "dose_alq": 1.00, "unidade": "L"},
        {"nome": "Animobor", "dose_alq": 0.26, "unidade": "L"},
    ]

# --- PAINEL LATERAL (INPUTS E BOTÃO) ---
st.sidebar.header("⚙️ Parâmetros da Aplicação")
input_tanque = st.sidebar.number_input("Volume do Tanque (L)", min_value=100, max_value=20000, value=2500, step=100)
input_alqueires = st.sidebar.number_input("Área total (Alqueires)", min_value=0.1, max_value=1000.0, value=9.37, step=0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("➕ Adicionar Novo Produto")

# Formulário para cadastrar novos itens direto pelo app
novo_nome = st.sidebar.text_input("Nome do Produto", placeholder="Ex: Glyphosate")
nova_unidade = st.sidebar.selectbox("Unidade", ["L", "kg"])
nova_dose = st.sidebar.number_input("Dose por Alqueire", min_value=0.01, max_value=50.0, value=1.0, step=0.01)

# O BOTÃO QUE VOCÊ PRECISAVA:
if st.sidebar.button("➕ Adicionar Produto à Calda", use_container_width=True):
    if novo_nome.strip() != "":
        # Adiciona o novo produto na lista da memória
        st.session_state.lista_produtos.append({
            "nome": novo_nome,
            "dose_alq": nova_dose,
            "unidade": nova_unidade
        })
        st.sidebar.success(f"'{novo_nome}' adicionado com sucesso!")
        # Atualiza a página para redesenhar a tabela na hora
        st.rerun()
    else:
        st.sidebar.error("Por favor, digite o nome do produto.")

# Botão opcional para resetar a lista original da imagem se precisar limpar os testes
if st.sidebar.button("🔄 Resetar para Lista Original", use_container_width=True):
    del st.session_state.lista_produtos
    st.rerun()


# --- CÁLCULOS MATEMÁTICOS ---
CONVERSAO_HA = 3.02 / 9.37  
TAXA_L_HA = 110.0            
calculo_ha = input_alqueires * CONVERSAO_HA
total_calda_necessaria = calculo_ha * TAXA_L_HA
taxa_l_alq = total_calda_necessaria / input_alqueires if input_alqueires > 0 else 0

# Cards de Métricas Principais
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">💧 Volume Tanque</div><div class="metric-value">{input_tanque} L</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-title">📐 Área (Alq)</div><div class="metric-value">{input_alqueires:,.2f} alq</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">🌾 Equivalente</div><div class="metric-value">{calculo_ha:,.2f} ha</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">📈 Taxa Alqueire</div><div class="metric-value">{taxa_l_alq:,.1f} L/alq</div></div>', unsafe_allow_html=True)
with col5:
    st.markdown(f'<div class="metric-card"><div class="metric-title">📉 Taxa Hectare</div><div class="metric-value">{TAXA_L_HA} L/ha</div></div>', unsafe_allow_html=True)

# --- SEÇÃO DA TABELA DE COMPOSIÇÃO DA CALDA ---
st.markdown('<div class="section-title">🍏 COMPOSIÇÃO DA CALDA</div>', unsafe_allow_html=True)

dados_tabela = []
for p in st.session_state.lista_produtos:
    # Formatação visual específica para manter os '750 mL' originais do Gapper
    if p["nome"] == "Gapper" and p["dose_alq"] == 0.75:
        dose_alq_str = "750 mL/alq"
    else:
        dose_alq_str = f"{p['dose_alq']:.2f} {p['unidade']}/alq"
        
    # Regra de cálculo proporcional para o tamanho do tanque
    taxa_padrao_alq = 266.6
    dose_tanque = (p["dose_alq"] * input_tanque) / taxa_padrao_alq
    
    dados_tabela.append({
        "PRODUTO": p["nome"],
        "DOSE (POR ALQUEIRE)": dose_alq_str,
        "DOSE RECOMENDADA (POR TANQUE)": f"{dose_tanque:,.2f} {p['unidade']}/tanque"
    })

# Exibe a tabela com as atualizações em tempo real
st.table(dados_tabela)

# Painel inferior de Observações Técnicas
st.markdown(f"""
    <div class="obs-box">
        <h4 style='margin:0 0 10px 0; color: #0b5127;'>ℹ️ OBSERVAÇÕES TÉCNICAS</h4>
        <ul style='margin:0; padding-left:20px; color: #333;'>
            <li><b>Aplicação:</b> Dessecação pré-plantio para milho.</li>
            <li><b>Volume de calda calculado:</b> {total_calda_necessaria:,.1f} L necessários para cobrir a área total de {input_alqueires} alq.</li>
            <li>Recomenda-se pH da água entre <b>5,5 e 6,5</b>.</li>
            <li>Utilizar <b>EPI adequado</b> durante o preparo e aplicação da calda.</li>
        </ul>
    </div>
    <br>
    <div style='text-align:center; font-size:12px; color:#777; font-weight:bold;'>
        RECEITA AGRONÔMICA • USO EXCLUSIVO AGRÍCOLA • Seguir legislação e recomendação técnica.
    </div>
""", unsafe_allow_html=True)
