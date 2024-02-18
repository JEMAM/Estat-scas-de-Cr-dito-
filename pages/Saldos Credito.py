import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from pandas.tseries.offsets import BMonthBegin

# Dicionários de saldos
saldos_novos = {
    "Saldo de crédito ampliado - Total": 28183,
    "Saldo de empréstimos total ao setor não financeiro": 28184,
    "Saldo de empréstimos do SFN ao setor não financeiro": 28185,
    "Saldo de empréstimos de OSF ao setor não financeiro": 28186,
    "Saldo de empréstimos de fundos governamentais ao setor não financeiro": 28187,
    "Saldo de títulos de dívida - Total": 28188,
    "Saldo de títulos públicos": 28189,
    "Saldo de títulos privados": 28190,
    "Saldo de instrumentos de securitização": 28191,
    "Saldo de dívida externa - Total": 28192,
    "Saldo de dívida externa - Empréstimos": 28193,
    "Saldo de dívida externa - Títulos emitidos no mercado externo": 28194,
    "Saldo de dívida externa - Títulos emitidos no mercado doméstico": 28195,
    # Adicione mais entradas conforme necessário
}

saldos_novos1 = {
    "Saldo de crédito ampliado - Total": 28183,
    "Saldo de empréstimos total ao setor não financeiro": 28184,
    "Saldo de empréstimos do SFN ao setor não financeiro": 28185,
    "Saldo de empréstimos de OSF ao setor não financeiro": 28186,
    "Saldo de empréstimos de fundos governamentais ao setor não financeiro": 28187,
    "Saldo de títulos de dívida - Total": 28188,
    "Saldo de títulos públicos": 28189,
    "Saldo de títulos privados": 28190,
    "Saldo de instrumentos de securitização": 28191,
    "Saldo de dívida externa - Total": 28192,
    "Saldo de dívida externa - Empréstimos": 28193,
    "Saldo de dívida externa - Títulos emitidos no mercado externo": 28194,
    "Saldo de dívida externa - Títulos emitidos no mercado doméstico": 28195,
    "Saldo de crédito ampliado ao governo - Total": 28196,
    "Saldo de empréstimos do SFN ao governo": 28197,
    "Saldo de títulos públicos - Governo geral": 28198,
    "Saldo de dívida externa - Concedido ao governo - Total": 28199,
    "Saldo de dívida externa - Empréstimos ao governo": 28200,
    "Saldo de dívida externa - Títulos públicos emitidos no mercado externo": 28201,
    "Saldo de dívida externa - Títulos públicos emitidos no mercado doméstico": 28202,
    # Adicione mais entradas conforme necessário
}

saldos_novos2 = {
    "Saldo de crédito ampliado a empresas e famílias - Total": 28203,
    "Saldo de empréstimos a empresas e famílias - Total": 28204,
    "Saldo de empréstimos do SFN a empresas e famílias": 28205,
    "Saldo de empréstimos de OSF a empresas e famílias": 28206,
    "Saldo de empréstimos de fundos governamentais a empresas e famílias": 28207,
    "Saldo de títulos de dívida emitidos por empresas e famílias - Total": 28208,
    "Saldo de títulos privados emitidos por empresas e famílias": 28209,
    "Saldo de instrumentos de securitização - devedores empresas e famílias": 28210,
   "Saldo de dívida externa - Concedido a empresas e famílias - Total": 28211,
    "Saldo de dívida externa - Empréstimos a empresas e famílias": 28212,
    "Saldo de dívida externa - Títulos privados emitidos no mercado externo": 28213,
    "Saldo de dívida externa - Títulos privados emitidos no mercado doméstico": 28214,
    "Saldo de crédito ampliado a empresas - Total": 28846,
    "Saldo de empréstimos a empresas - Total": 28847,
    "Saldo de empréstimos do SFN a empresas": 28848,
    "Saldo de empréstimos de OSF a empresas": 28849,
    "Saldo de empréstimos de fundos governamentais a empresas": 28850,
    "Saldo de títulos de dívida emitidos por empresas - Total": 28851,
    "Saldo de títulos privados emitidos por empresas": 28852,
    "Saldo de instrumentos de securitização - devedores empresas": 28853,
    "Saldo de dívida externa - Concedido a empresas - Total": 28854,
    "Saldo de dívida externa - Empréstimos a empresas": 28855,
    "Saldo de dívida externa - Títulos emitidos por empresas no mercado externo": 28856,
    "Saldo de dívida externa - Títulos emitidos por empresas no mercado doméstico": 28857,
    "Saldo de crédito ampliado a famílias - Total": 28858,
    "Saldo de empréstimos a famílias - Total": 28859,
    "Saldo de empréstimos do SFN a famílias": 28860,
    "Saldo de empréstimos de OSF a famílias": 28861,
    "Saldo de empréstimos de fundos governamentais a famílias": 28862,
    "Saldo de instrumentos de securitização - devedores famílias": 28863,
    "Saldo de dívida externa - Concedido a famílias - Total": 28864,
    "Saldo de dívida externa - Empréstimos a famílias": 28865,
    "Saldo de dívida externa - Títulos emitidos por famílias no mercado externo": 28866,
    # Adicione mais entradas conforme necessário
}

saldos_novos3 = {
    "Saldo - Total": 20542,
    "Saldo - Pessoas jurídicas - Total": 20543,
    "Saldo - Pessoas jurídicas - Não rotativo": 28165,
    "Saldo - Pessoas jurídicas - Rotativo": 28166,
    "Saldo - Pessoas jurídicas - Desconto de duplicatas e recebíveis": 20544,
    "Saldo - Pessoas jurídicas - Desconto de cheques": 20545,
    "Saldo - Pessoas jurídicas - Antecipação de faturas de cartão de crédito": 20546,
    "Saldo - Pessoas jurídicas - Capital de giro com prazo de até 365 dias": 20547,
    "Saldo - Pessoas jurídicas - Capital de giro com prazo superior a 365 dias": 20548,
    "Saldo - Pessoas jurídicas - Capital de giro rotativo": 20549,
    "Saldo - Pessoas jurídicas - Capital de giro total": 20550,
    "Saldo - Pessoas jurídicas - Conta garantida": 20551,
    "Saldo - Pessoas jurídicas - Cheque especial": 20552,
    "Saldo - Pessoas jurídicas - Aquisição de veículos": 20553,
    "Saldo - Pessoas jurídicas - Aquisição de outros bens": 20554,
    "Saldo - Pessoas jurídicas - Aquisição de bens total": 20555,
    "Saldo - Pessoas jurídicas - Arrendamento mercantil de veículos": 20556,
    "Saldo - Pessoas jurídicas - Arrendamento mercantil de outros bens": 20557,
    "Saldo - Pessoas jurídicas - Arrendamento mercantil total": 20558,
    "Saldo - Pessoas jurídicas - Vendor": 20559,
    "Saldo - Pessoas jurídicas - Compror": 20560,
    "Saldo - Pessoas jurídicas - Cartão de crédito rotativo": 20561,
    "Saldo - Pessoas jurídicas - Cartão de crédito parcelado": 20562,
    "Saldo - Pessoas jurídicas - Cartão de crédito à vista": 20563,
    "Saldo - Pessoas jurídicas - Cartão de crédito total": 20564,
    "Saldo - Pessoas jurídicas - Adiantamento sobre contratos de câmbio (ACC)": 20565,
    "Saldo - Pessoas jurídicas - Financiamento a importações": 20566,
    "Saldo - Pessoas jurídicas - Financiamento a exportações": 20567,
    "Saldo - Pessoas jurídicas - Repasse externo": 20568,
    "Saldo - Pessoas jurídicas - Outros créditos livres": 20569,
    "Saldo - Pessoas físicas - Total": 20570,
    "Saldo - Pessoas físicas - Não rotativo": 20571,
    "Saldo - Pessoas físicas - Rotativo": 20572,
    "Saldo - Pessoas físicas - Cheque especial": 20573,
    "Saldo - Pessoas físicas - Crédito pessoal não consignado": 20574,
    "Saldo - Pessoas físicas - Crédito pessoal não consignado vinculado à composição de dívidas": 20575,
    "Saldo - Pessoas físicas - Crédito pessoal consignado para trabalhadores do setor privado": 20576,
    "Saldo - Pessoas físicas - Crédito pessoal consignado para trabalhadores do setor público": 20577,
    "Saldo - Pessoas físicas - Crédito pessoal consignado para aposentados e pensionistas do INSS": 20578,
    "Saldo - Pessoas físicas - Crédito pessoal consignado total": 20579,
    "Saldo - Pessoas físicas - Crédito pessoal total": 20580,
    "Saldo - Pessoas físicas - Aquisição de veículos": 20581,
    "Saldo - Pessoas físicas - Aquisição de outros bens": 20582,
    "Saldo - Pessoas físicas - Aquisição de bens total": 20583,
    "Saldo - Pessoas físicas - Arrendamento mercantil de veículos": 20584,
    "Saldo - Pessoas físicas - Arrendamento mercantil de outros bens": 20585,
    "Saldo - Pessoas físicas - Arrendamento mercantil total": 20586,
    "Saldo - Pessoas físicas - Cartão de crédito rotativo": 20587,
    "Saldo - Pessoas físicas - Cartão de crédito parcelado": 20588,
    "Saldo - Pessoas físicas - Cartão de crédito à vista": 20589,

}

saldos_novos4= {
    "Saldo - Total": 20593,
    "Saldo - Pessoas jurídicas - Total": 20594,
    "Saldo - Pessoas jurídicas - Crédito rural com taxas de mercado": 20595,
    "Saldo - Pessoas jurídicas - Crédito rural com taxas reguladas": 20596,
    "Saldo - Pessoas jurídicas - Crédito rural total": 20597,
    "Saldo - Pessoas jurídicas - Financiamento imobiliário com taxas de mercado": 20598,
    "Saldo - Pessoas jurídicas - Financiamento imobiliário com taxas reguladas": 20599,
    "Saldo - Pessoas jurídicas - Financiamento imobiliário total": 20600,
    "Saldo - Pessoas jurídicas - Capital de giro com recursos do BNDES": 20601,
    "Saldo - Pessoas jurídicas - Financiamento de investimentos com recursos do BNDES": 20602,
    "Saldo - Pessoas jurídicas - Financiamento agroindustrial com recursos do BNDES": 20603,
    "Saldo - Pessoas jurídicas - Financiamento com recursos do BNDES total": 20604,
   "Saldo - Pessoas jurídicas - Outros créditos direcionados": 20605,
    "Saldo - Pessoas físicas - Total": 20606,
    "Saldo - Pessoas físicas - Crédito rural com taxas de mercado": 20607,
    "Saldo - Pessoas físicas - Crédito rural com taxas reguladas": 20608,
    "Saldo - Pessoas físicas - Crédito rural total": 20609,
    "Saldo - Pessoas físicas - Financiamento imobiliário com taxas de mercado": 20610,
    "Saldo - Pessoas físicas - Financiamento imobiliário com taxas reguladas": 20611,
    "Saldo - Pessoas físicas - Financiamento imobiliário total": 20612,
    "Saldo - Pessoas físicas - Capital de giro com recursos do BNDES": 20613,
    "Saldo - Pessoas físicas - Financiamento de investimentos com recursos do BNDES": 20614,
    "Saldo - Pessoas físicas - Financiamento agroindustrial com recursos do BNDES": 20615,
    "Saldo - Pessoas físicas - Financiamento com recursos do BNDES total": 20616,
    "Saldo - Pessoas físicas - Microcrédito destinado a consumo": 20617,
    "Saldo - Pessoas físicas - Microcrédito destinado a microempreendedores": 20618,
    "Saldo - Pessoas físicas - Microcrédito total": 20620,
    "Saldo - Pessoas físicas - Outros créditos direcionados": 20621,
    "Saldo - Pessoas jurídicas - Financiamento com recursos do BNDES - Carteira própria": 21359,
    "Saldo - Pessoas jurídicas - Financiamento com recursos do BNDES - Repasses": 21360,
    "Saldo - Pessoas físicas - Financiamento com recursos do BNDES - Repasses": 21362,

}
saldos_novos5={
    "Saldo por porte da empresa - Grande": 27702,
    "Saldo por porte da empresa - Micro, Pequena e Média": 27701,

}
saldos_novos6={
"Saldo ao setor agropecuário": 22027,
"Saldo ao setor industrial - Total": 22043,
"Saldo ao setor industrial - Serviços industriais de utilidade pública (SIUP)": 22034,
"Saldo ao setor industrial - Construção": 22030,
"Saldo ao setor industrial - Alimentos": 27743,
"Saldo ao setor industrial - Açúcar": 27744,
"Saldo ao setor industrial - Têxtil, vestuário, couro e calçados": 27745,
"Saldo ao setor industrial - Papel e celulose": 27746,
"Saldo ao setor industrial - Petróleo, gás e álcool": 27747,
"Saldo ao setor industrial - Metalurgia e siderurgia": 27748,
"Saldo ao setor industrial - Química e farmacêutica": 27722,
"Saldo ao setor industrial - Bens de capital": 27723,
"Saldo ao setor industrial - Automobilística": 27724,
"Saldo ao setor industrial - Mineração": 27749,
"Saldo ao setor industrial - Obras de infraestrutura": 27725,
"Saldo ao setor industrial - Outros bens de consumo duráveis": 27726,
"Saldo ao setor industrial - Embalagens": 27727,
"Saldo ao setor industrial - Bens de consumo não duráveis": 27728,
"Saldo ao setor de serviços - Total": 22044,
"Saldo ao setor de serviços - Transportes": 22037,
"Saldo ao setor de serviços - Via terrestre (carga e passageiro)": 27729,
"Saldo ao setor de serviços - Meios aquaviário e aéreo": 27730,
"Saldo ao setor de serviços - Dutoviário": 27731,
"Saldo ao setor de serviços - Comércio": 22036,
"Saldo ao setor de serviços - Varejo - bens não duráveis": 27732,
"Saldo ao setor de serviços - Varejo - bens duráveis": 27733,
"Saldo ao setor de serviços - Atacado - bens duráveis e não-duráveis": 27734,
"Saldo ao setor de serviços - Geral - veículos automotores": 27735,
"Saldo ao setor de serviços - Geral - bens intermediários": 27736,
"Saldo ao setor de serviços - Geral - bens de capital": 27737,
"Saldo ao setor de serviços - Administração pública": 22039,
"Saldo ao setor de serviços - Serviços imobiliários": 27738,
"Saldo ao setor de serviços - Serviços de informação e comunicação": 27739,
"Saldo ao setor de serviços - Demais serviços prestados às famílias": 27740,
"Saldo ao setor de serviços - Demais serviços prestados às empresas": 27741,
"Saldo ao setor de serviços - Serviços financeiros": 27742,
"Saldo ao setor de serviços - Outros serviços": 22041,
"Saldo a outros setores": 22042,

}
saldos_novos7={
    "Saldo - Setor privado - Total": 22052,
    "Saldo - Setor privado - Pessoas jurídicas": 22047,
    "Saldo - Setor privado - Pessoas físicas": 22050,
    "Saldo - Setor público - Total": 22051,
    "Saldo - Setor público - Governo federal": 22025,
    "Saldo - Setor público - Governos estuduais e municipais": 22026,
    "Saldos sob controle público - Total": 2007,
    "Saldos sob controle privado - Total": 2043,
    "Saldos sob controle privado nacional - Total": 12106,
    "Saldos sob controle estrangeiro - Total": 12150,

}
saldos_novos8={
    "Saldo de crédito / PIB": 20622,
    "Saldo de crédito - Pessoas jurídicas / PIB": 20623,
    "Saldo de crédito - Pessoas físicas / PIB": 20624,
    "Saldo de crédito livre / PIB": 20625,
    "Saldo de crédito livre - Pessoas jurídicas / PIB": 20626,
    "Saldo de crédito livre - Pessoas físicas / PIB": 20627,
    "Saldo de crédito direcionado / PIB": 20628,
    "Saldo de crédito direcionado - Pessoas jurídicas / PIB": 20629,
    "Saldo de crédito direcionado - Pessoas físicas / PIB": 20630,
    "Saldo de crédito ampliado / PIB": 28215,
    "Saldo de crédito ampliado ao governo / PIB": 28216,
    "Saldo de crédito ampliado a empresas e famílias / PIB": 28217,
    "Saldo de crédito ampliado a empresas / PIB": 28867,
    "Saldo crédito ampliado a famílias / PIB": 28868,
    "Saldo ao setor agropecuário / PIB": 22059,
    "Saldo ao setor industrial / PIB - Construção": 22062,
    "Saldo ao setor industrial / PIB - Serviços industriais de utilidade pública (SIUP)": 22063,
    "Saldo ao setor industrial / PIB - Total": 22064,
    "Saldo ao setor de serviços / PIB - Comércio": 22065,
    "Saldo ao setor de serviços / PIB - Transportes": 22066,
    "Saldo ao setor de serviços / PIB - Administração pública": 22067,
    "Saldo ao setor de serviços / PIB - Outros serviços": 22068,
    "Saldo ao setor de serviços / PIB - Total": 22069,
    "Saldo a outros setores / PIB": 22070,
    "Saldo de crédito das instituições financeiras sob controle estrangeiro / PIB": 21302,
    "Saldo de crédito das instituições financeiras sob controle privado / PIB": 21299,
    "Saldo de crédito das instituições financeiras sob controle privado nacional / PIB": 21301,
    "Saldo de crédito das instituições financeiras sob controle público / PIB": 21300,

}
# Função para carregar dados usando a API do Banco Central
def carregar_dados(codigo):
    # Endpoint da API do Banco Central
    url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json'

    # Fazendo a solicitação HTTP
    response = requests.get(url)

    # Verificando se a solicitação foi bem-sucedida (código 200)
    if response.status_code == 200:
        # Convertendo os dados JSON para um DataFrame do Pandas
        dados = pd.DataFrame(response.json())
        # Convertendo a coluna 'valor' para tipo numérico
        dados['valor'] = pd.to_numeric(dados['valor'], errors='coerce')
        # Convertendo a coluna 'data' para tipo datetime
        dados['data'] = pd.to_datetime(dados['data'], errors='coerce')
        # Filtrando dados a partir de 2010
        dados = dados[dados['data'].dt.year >= 2010]
        # Configurando a coluna 'data' como índice
        dados.set_index('data', inplace=True)
        # Pegando os últimos 20 valores
        dados = dados.tail(100)
        return dados
    else:
        st.error(f"Erro ao carregar dados para código {codigo}. Status Code: {response.status_code}")
        return None

# Função para realizar a previsão usando SARIMAX
def fazer_previsao(dados, passos=6):
    modelo = SARIMAX(dados['valor'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    resultado = modelo.fit(disp=False)

    # Obtendo o último dia dos dados existentes
    ultimo_dia = pd.to_datetime(dados.index[-1])

    # Calculando o primeiro dia do mês seguinte ao último dia dos dados existentes
    primeiro_dia_proximo_mes = ultimo_dia + pd.DateOffset(months=1) - pd.DateOffset(days=ultimo_dia.day - 1)

    # Removendo horas, minutos, segundos e microssegundos da data
    primeiro_dia_proximo_mes = primeiro_dia_proximo_mes.replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculando o índice para a previsão
    previsao_index = pd.date_range(start=primeiro_dia_proximo_mes, periods=passos, freq='MS')

    # Realizando a previsão
    previsao = resultado.get_forecast(steps=passos, index=previsao_index)
    previsao_df = pd.DataFrame(previsao.predicted_mean.values, index=previsao_index, columns=['valor'])
    return previsao_df
    #return previsao, previsao_index


# Função para realizar a decomposição dos dados
def realizar_decomposicao(dados):
    try:
        resultado = seasonal_decompose(dados['valor'], model='additive', period=6)
        return resultado
    except ValueError as e:
        st.warning(f"Não foi possível realizar a decomposição: {e}")
        return None

# Sidebar
st.sidebar.title('Selecione os saldos:')

# Multiselect para o primeiro grupo de dicionários
st.sidebar.header('Saldos')
opcoes_selecao1 = st.sidebar.multiselect('Escolha os saldos', list(saldos_novos.keys()))

# Multiselect para o segundo grupo de dicionários
st.sidebar.header('Saldo-Governo Geral')
opcoes_selecao2 = st.sidebar.multiselect('Escolha os saldos', list(saldos_novos1.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Saldo-Familias e empresas')
opcoes_selecao3 = st.sidebar.multiselect('Escolha os saldos', list(saldos_novos2.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Saldo-Recursos livres')
opcoes_selecao4 = st.sidebar.multiselect('Escolha os saldos', list(saldos_novos3.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Saldo-Recursos Direcionados')
opcoes_selecao5 = st.sidebar.multiselect('Escolha os saldos', list(saldos_novos4.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Saldo-Por Porte da Empresa')
opcoes_selecao6 = st.sidebar.multiselect('Escolha os saldos', list(saldos_novos5.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Saldo-Por Atividade Economica')
opcoes_selecao7 = st.sidebar.multiselect('Escolha os saldos', list(saldos_novos6.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Saldo-Por tipo de Cliente e Controle de Capital')
opcoes_selecao8 = st.sidebar.multiselect('Escolha os saldos', list(saldos_novos7.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Percentual em Relação ao PIB')
opcoes_selecao9 = st.sidebar.multiselect('Escolha os saldos', list(saldos_novos8.keys()))

# Juntando todas as opções selecionadas
opcoes_selecao = opcoes_selecao1 + opcoes_selecao2 + opcoes_selecao3 + opcoes_selecao4 + opcoes_selecao5 \
                 + opcoes_selecao6+opcoes_selecao7 + opcoes_selecao8 + opcoes_selecao9

# Carregar dados selecionados
dados_selecionados = {
    nome: carregar_dados(codigo)
    for dicionario in [saldos_novos, saldos_novos1, saldos_novos2, saldos_novos3,saldos_novos4,saldos_novos5,
                       saldos_novos6, saldos_novos7,  saldos_novos8]
    for nome, codigo in dicionario.items()
    if nome in opcoes_selecao
}



# Restante do código permanece o mesmo
# ...

# Exibir tabelas e gráficos um abaixo do outro
st.title('Saldo de Crédito R$ (milhões)')
for nome, dados in dados_selecionados.items():
    if dados is not None:
        # Formatando a coluna 'data'
        dados.index = dados.index.strftime('%Y/%d/%m')

        # Exibindo tabela
        st.subheader(f'{nome} - Últimos 100 Valores:')
        # Slider para selecionar o número de dados a serem exibidos
        num_dados = st.slider(f'Selecione o número de dados para {nome}', min_value=1, max_value=len(dados), value=10)
        st.table(dados.tail(num_dados).style.format("{:.2f}"))

        # Exibindo estatísticas
        st.subheader('Estatísticas:')
        estatisticas = dados.describe()
        st.table(estatisticas.style.format("{:.2f}"))

        # Exibindo gráficos
        st.subheader('Gráfico e Previsão:')
        fig = px.line(dados, x=dados.index, y='valor', labels={'x': 'Data', 'y': 'Valor'},
                      title='Últimos 100 Valores')

        # Adicionando previsão ao gráfico
        passos = st.number_input(f'Número de passos para previsão de {nome}', value=6)
        #previsao, previsao_index = fazer_previsao(dados, passos)
        #previsao, previsao_df = fazer_previsao(dados, passos)
        previsao_df = fazer_previsao(dados, passos)
        #previsao_df = previsao_df['valor'].replace('\.\d+', '', regex=True).astype(float).round(2)
        
        #previsao_df.index = previsao_df.index.date

        #fig.add_trace(go.Scatter(x=previsao_index, y=previsao.predicted_mean, mode='lines', name='Previsão'))
        uniao = pd.concat([dados, previsao_df], axis=0)
        uniao.index = pd.to_datetime(uniao.index).date
        uniao = uniao.sort_index(ascending=False)
    
        st.dataframe(uniao)
        fig = px.line(uniao,title='Ultimos 100 com a Previsão - 4 casas decimais')

        fig.update_layout(showlegend=True, legend_title_text='Legenda', legend=dict(x=1, y=1))
        st.plotly_chart(fig)

        # Exibindo decomposição
        st.subheader(f'{nome} - Decomposição:')

        # Decomposição dos dados
        decomposicao = realizar_decomposicao(dados)

        # Criando gráficos para cada componente da decomposição
        if decomposicao:
            # Tendência
            fig_tendencia = px.line(x=decomposicao.trend.index, y=decomposicao.trend,
                                    labels={'x': 'Data', 'y': 'Tendência'})
            fig_tendencia.update_layout(title='Tendência')
            st.plotly_chart(fig_tendencia)

            # Sazonalidade
            fig_sazonalidade = px.line(x=decomposicao.seasonal.index, y=decomposicao.seasonal,
                                       labels={'x': 'Data', 'y': 'Sazonalidade'})
            fig_sazonalidade.update_layout(title='Sazonalidade')
            st.plotly_chart(fig_sazonalidade)

            # Resíduos
            fig_residuos = px.line(x=decomposicao.resid.index, y=decomposicao.resid,
                                   labels={'x': 'Data', 'y': 'Resíduos'})
            fig_residuos.update_layout(title='Resíduos')
            st.plotly_chart(fig_residuos)

            decomposicao_df = pd.DataFrame({
                'Tendência': decomposicao.trend,
                'Sazonalidade': decomposicao.seasonal,
                'Resíduos': decomposicao.resid
            })

            decomposicao_df= decomposicao_df.sort_index(ascending=False)
            decomposicao_df=decomposicao_df.style.format("{:.2f}")
            # Exibindo o DataFrame
            st.dataframe(decomposicao_df)