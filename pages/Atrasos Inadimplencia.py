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
    "Percentual da carteira com atraso entre 15 e 90 dias - Total": 21003,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Total": 21004,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Total": 21005,

}

saldos_novos1 = {
    "Percentual da carteira com atraso entre 15 e 90 dias - Total": 21006,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Total": 21007,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Desconto de duplicatas e recebíveis": 21008,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Desconto de cheques": 21009,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Antecipação de faturas de cartão de crédito": 21010,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Capital de giro com prazo de até 365 dias": 21011,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Capital de giro com prazo superior a 365 dias": 21012,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Capital de giro rotativo": 21013,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Capital de giro total": 21014,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Conta garantida": 21015,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Cheque especial": 21016,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Aquisição de veículos": 21017,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Aquisição de outros bens": 21018,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Aquisição de bens total": 21019,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Arrendamento mercantil de veículos": 21020,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Arrendamento mercantil de outros bens": 21021,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Arrendamento mercantil total": 21022,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Vendor": 21023,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Compror": 21024,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Cartão de crédito rotativo": 21025,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Cartão de crédito parcelado": 21026,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Cartão de crédito total": 21027,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Adiantamento sobre contratos de câmbio (ACC)": 21028,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Financiamento a importações": 21029,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Financiamento a exportações": 21030,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Repasse externo": 21031,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Outros créditos livres": 21032,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Total": 21033,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Cheque especial": 21034,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Crédito pessoal não consignado": 21035,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Crédito pessoal não consignado vinculado à composição de dívidas": 21036,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Crédito pessoal consignado para trabalhadores do setor privado": 21037,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Crédito pessoal consignado para trabalhadores do setor público": 21038,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Crédito pessoal consignado para aposentados e pensionistas do INSS": 21039,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Crédito pessoal consignado total": 21040,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Crédito pessoal total": 21041,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Aquisição de veículos": 21042,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Aquisição de outros bens": 21043,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Aquisição de bens total": 21044,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Arrendamento mercantil de veículos": 21045,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Arrendamento mercantil de outros bens": 21046,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Arrendamento mercantil total": 21047,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Cartão de crédito rotativo": 21048,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Cartão de crédito parcelado": 21049,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Cartão de crédito total": 21050,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Desconto de cheques": 21051,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Outros créditos livres": 21052,
}
saldos_novos2 = {
    "Percentual da carteira com atraso entre 15 e 90 dias - Total": 21053,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Total": 21054,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Crédito rural com taxas de mercado": 21055,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Crédito rural com taxas reguladas": 21056,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Crédito rural total": 21057,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Financiamento imobiliário com taxas de mercado": 21058,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Financiamento imobiliário com taxas reguladas": 21059,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Financiamento imobiliário total": 21060,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Capital de giro com recursos do BNDES": 21061,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Financiamento de investimentos com recursos do BNDES": 21062,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Financiamento agroindustrial com recursos do BNDES": 21063,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Financiamento com recursos do BNDES total": 21064,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas jurídicas - Outros créditos direcionados": 21065,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Total": 21066,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Crédito rural com taxas de mercado": 21067,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Crédito rural com taxas reguladas": 21068,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Crédito rural total": 21069,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Financiamento imobiliário com taxas de mercado": 21070,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Financiamento imobiliário com taxas reguladas": 21071,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Financiamento imobiliário total": 21072,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Capital de giro com recursos do BNDES": 21073,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Financiamento de investimentos com recursos do BNDES": 21074,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Financiamento agroindustrial com recursos do BNDES": 21075,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Financiamento com recursos do BNDES total": 21076,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Microcrédito destinado a consumo": 21077,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Microcrédito destinado a microempreendedores": 21078,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Microcrédito total": 21080,
    "Percentual da carteira com atraso entre 15 e 90 dias - Pessoas físicas - Outros créditos direcionados": 21081,

    }

saldos_novos3 = {
    "Inadimplência da carteira - Total": 21082,
    "Inadimplência da carteira - Pessoas jurídicas - Total": 21083,
    "Inadimplência da carteira - Pessoas físicas - Total": 21084,

}

saldos_novos4= {
    "Inadimplência da carteira - Total": 21085,
    "Inadimplência da carteira - Pessoas jurídicas - Total": 21086,
    "Inadimplência da carteira - Pessoas jurídicas - Desconto de duplicatas e recebíveis": 21087,
    "Inadimplência da carteira - Pessoas jurídicas - Desconto de cheques": 21088,
    "Inadimplência da carteira - Pessoas jurídicas - Antecipação de faturas de cartão de crédito": 21089,
    "Inadimplência da carteira - Pessoas jurídicas - Capital de giro com prazo de até 365 dias": 21090,
    "Inadimplência da carteira - Pessoas jurídicas - Capital de giro com prazo superior a 365 dias": 21091,
    "Inadimplência da carteira - Pessoas jurídicas - Capital de giro rotativo": 21092,
    "Inadimplência da carteira - Pessoas jurídicas - Capital de giro total": 21093,
    "Inadimplência da carteira - Pessoas jurídicas - Conta garantida": 21094,
    "Inadimplência da carteira - Pessoas jurídicas - Cheque especial": 21095,
    "Inadimplência da carteira - Pessoas jurídicas - Aquisição de veículos": 21096,
    "Inadimplência da carteira - Pessoas jurídicas - Aquisição de outros bens": 21097,
    "Inadimplência da carteira - Pessoas jurídicas - Aquisição de bens total": 21098,
    "Inadimplência da carteira - Pessoas jurídicas - Arrendamento mercantil de veículos": 21099,
    "Inadimplência da carteira - Pessoas jurídicas - Arrendamento mercantil de outros bens": 21100,
    "Inadimplência da carteira - Pessoas jurídicas - Arrendamento mercantil total": 21101,
    "Inadimplência da carteira - Pessoas jurídicas - Vendor": 21102,
    "Inadimplência da carteira - Pessoas jurídicas - Compror": 21103,
    "Inadimplência da carteira - Pessoas jurídicas - Cartão de crédito rotativo": 21104,
    "Inadimplência da carteira - Pessoas jurídicas - Cartão de crédito parcelado": 21105,
    "Inadimplência da carteira - Pessoas jurídicas - Cartão de crédito total": 21106,
    "Inadimplência da carteira - Pessoas jurídicas - Adiantamento sobre contratos de câmbio (ACC)": 21107,
    "Inadimplência da carteira - Pessoas jurídicas - Financiamento a importações": 21108,
    "Inadimplência da carteira - Pessoas jurídicas - Financiamento a exportações": 21109,
    "Inadimplência da carteira - Pessoas jurídicas - Repasse externo": 21110,
    "Inadimplência da carteira - Pessoas jurídicas - Outros créditos livres": 21111,
    "Inadimplência da carteira - Pessoas físicas - Total": 21112,
    "Inadimplência da carteira - Pessoas físicas - Cheque especial": 21113,
    "Inadimplência da carteira - Pessoas físicas - Crédito pessoal não consignado": 21114,
    "Inadimplência da carteira - Pessoas físicas - Crédito pessoal não consignado vinculado à composição de dívidas": 21115,
    "Inadimplência da carteira - Pessoas físicas - Crédito pessoal consignado para trabalhadores do setor privado": 21116,
    "Inadimplência da carteira - Pessoas físicas - Crédito pessoal consignado para trabalhadores do setor público": 21117,
    "Inadimplência da carteira - Pessoas físicas - Crédito pessoal consignado para aposentados e pensionistas do INSS": 21118,
    "Inadimplência da carteira - Pessoas físicas - Crédito pessoal consignado total": 21119,
    "Inadimplência da carteira - Pessoas físicas - Crédito pessoal total": 21120,
    "Inadimplência da carteira - Pessoas físicas - Aquisição de veículos": 21121,
    "Inadimplência da carteira - Pessoas físicas - Aquisição de outros bens": 21122,
    "Inadimplência da carteira - Pessoas físicas - Aquisição de bens total": 21123,
    "Inadimplência da carteira - Pessoas físicas - Arrendamento mercantil de veículos": 21124,
    "Inadimplência da carteira - Pessoas físicas - Arrendamento mercantil de outros bens": 21125,
    "Inadimplência da carteira - Pessoas físicas - Arrendamento mercantil total": 21126,
    "Inadimplência da carteira - Pessoas físicas - Cartão de crédito rotativo": 21127,
    "Inadimplência da carteira - Pessoas físicas - Cartão de crédito parcelado": 21128,
    "Inadimplência da carteira - Pessoas físicas - Cartão de crédito total": 21129,
    "Inadimplência da carteira - Pessoas físicas - Desconto de cheques": 21130,
    "Inadimplência da carteira - Pessoas físicas - Outros créditos livres": 21131,

}
saldos_novos5={
    "Inadimplência da carteira - Total": 21132,
    "Inadimplência da carteira - Pessoas jurídicas - Total": 21133,
    "Inadimplência da carteira - Pessoas jurídicas - Crédito rural com taxas de mercado": 21134,
    "Inadimplência da carteira - Pessoas jurídicas - Crédito rural com taxas reguladas": 21135,
    "Inadimplência da carteira - Pessoas jurídicas - Crédito rural total": 21136,
    "Inadimplência da carteira - Pessoas jurídicas - Financiamento imobiliário com taxas de mercado": 21137,
    "Inadimplência da carteira - Pessoas jurídicas - Financiamento imobiliário com taxas reguladas": 21138,
    "Inadimplência da carteira - Pessoas jurídicas - Financiamento imobiliário total": 21139,
    "Inadimplência da carteira - Pessoas jurídicas - Capital de giro com recursos do BNDES": 21140,
    "Inadimplência da carteira - Pessoas jurídicas - Financiamento de investimentos com recursos do BNDES": 21141,
    "Inadimplência da carteira - Pessoas jurídicas - Financiamento agroindustrial com recursos do BNDES": 21142,
    "Inadimplência da carteira - Pessoas jurídicas - Financiamento com recursos do BNDES total": 21143,
    "Inadimplência da carteira - Pessoas jurídicas - Outros créditos direcionados": 21144,
    "Inadimplência da carteira - Pessoas físicas - Total": 21145,
    "Inadimplência da carteira - Pessoas físicas - Crédito rural com taxas de mercado": 21146,
    "Inadimplência da carteira - Pessoas físicas - Crédito rural com taxas reguladas": 21147,
    "Inadimplência da carteira - Pessoas físicas - Crédito rural total": 21148,
    "Inadimplência da carteira - Pessoas físicas - Financiamento imobiliário com taxas de mercado": 21149,
    "Inadimplência da carteira - Pessoas físicas - Financiamento imobiliário com taxas reguladas": 21150,
    "Inadimplência da carteira - Pessoas físicas - Financiamento imobiliário total": 21151,
    "Inadimplência da carteira - Pessoas físicas - Capital de giro com recursos do BNDES": 21152,
    "Inadimplência da carteira - Pessoas físicas - Financiamento de investimentos com recursos do BNDES": 21153,
    "Inadimplência da carteira - Pessoas físicas - Financiamento agroindustrial com recursos do BNDES": 21154,
    "Inadimplência da carteira - Pessoas físicas - Financiamento com recursos do BNDES total": 21155,
    "Inadimplência da carteira - Pessoas físicas - Microcrédito destinado a consumo": 21156,
    "Inadimplência da carteira - Pessoas físicas - Microcrédito destinado a microempreendedores": 21157,
    "Inadimplência da carteira - Pessoas físicas - Microcrédito total": 21159,
    "Inadimplência da carteira - Pessoas físicas - Outros créditos direcionados": 21160,

}
saldos_novos6={
    "Inadimplência por porte da empresa - Grande": 27704,
    "Inadimplência por porte da empresa - Micro, Pequena e Média (MPMe)": 27703,
    "Maior risco da carteira - Pessoas jurídicas - Total": 27705,
    "Maior risco por porte da empresa - Grande": 27707,
    "Maior risco por porte da empresa - Micro, Pequena e Média (MPMe)": 27706,


}
saldos_novos7={
    "Inadimplência das instituições financeiras sob controle público - Total": 13667,
    "Inadimplência das instituições financeiras sob controle privado nacional - Total": 13673,
    "Inadimplência das instituições financeiras sob controle estrangeiro - Total": 13679,
    "Inadimplência das instituições financeiras sob controle privado - Total": 13685,

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
st.sidebar.header('Atraso das operações de 15 a 90 dias')
opcoes_selecao1 = st.sidebar.multiselect('Selecione:', list(saldos_novos.keys()))

# Multiselect para o segundo grupo de dicionários
st.sidebar.header('Atraso das operações com recursos livres de 15 a 90 dias')
opcoes_selecao2 = st.sidebar.multiselect('Selecione:', list(saldos_novos1.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Atraso das operações com recursos direcionados de 15 a 90 dias')
opcoes_selecao3 = st.sidebar.multiselect('Selecione:', list(saldos_novos2.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Inadimplência')
opcoes_selecao4 = st.sidebar.multiselect('Selecione:', list(saldos_novos3.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Inadimplência das operações com recursos livres')
opcoes_selecao5 = st.sidebar.multiselect('Selecione:', list(saldos_novos4.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Inadimplência das operações com recursos direcionados')
opcoes_selecao6 = st.sidebar.multiselect('Selecione:', list(saldos_novos5.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Inadimplência e maior nível de risco por porte de empresa')
opcoes_selecao7 = st.sidebar.multiselect('Selecione:', list(saldos_novos6.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Inadimplência segundo controle de capital')
opcoes_selecao8 = st.sidebar.multiselect('Selecione:', list(saldos_novos7.keys()))


# Juntando todas as opções selecionadas
opcoes_selecao = opcoes_selecao1 + opcoes_selecao2 + opcoes_selecao3 + opcoes_selecao4 + opcoes_selecao5 \
                 + opcoes_selecao6+opcoes_selecao7 + opcoes_selecao8

# Carregar dados selecionados
dados_selecionados = {
    nome: carregar_dados(codigo)
    for dicionario in [saldos_novos, saldos_novos1, saldos_novos2, saldos_novos3,saldos_novos4,saldos_novos5,
                       saldos_novos6, saldos_novos7]
    for nome, codigo in dicionario.items()
    if nome in opcoes_selecao
}



# Restante do código permanece o mesmo
# ...

# Exibir tabelas e gráficos um abaixo do outro
st.title('Atrasos e inadimplência %')
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
        st.write("Previsão - 4 casas decimais")
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
        fig = px.line(uniao,title='Ultimos 100 com a Previsão')

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