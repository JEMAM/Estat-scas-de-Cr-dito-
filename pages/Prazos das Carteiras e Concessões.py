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
    "Prazo médio da carteira - Total": 20924,
    "Prazo médio da carteira - Pessoas jurídicas - Total": 20925,
    "Prazo médio da carteira - Pessoas físicas - Total": 20926,

}

saldos_novos1 = {
    "Prazo médio da carteira - Total": 20927,
    "Prazo médio da carteira - Pessoas jurídicas - Total": 20928,
    "Prazo médio da carteira - Pessoas jurídicas - Desconto de duplicatas e recebíveis": 20929,
    "Prazo médio da carteira - Pessoas jurídicas - Desconto de cheques": 20930,
    "Prazo médio da carteira - Pessoas jurídicas - Antecipação de faturas de cartão de crédito": 20931,
    "Prazo médio da carteira - Pessoas jurídicas - Capital de giro com prazo de até 365 dias": 20932,
    "Prazo médio da carteira - Pessoas jurídicas - Capital de giro com prazo superior a 365 dias": 20933,
    "Prazo médio da carteira - Pessoas jurídicas - Capital de giro rotativo": 20934,
    "Prazo médio da carteira - Pessoas jurídicas - Capital de giro total": 20935,
    "Prazo médio da carteira - Pessoas jurídicas - Conta garantida": 20936,
    "Prazo médio da carteira - Pessoas jurídicas - Cheque especial": 20937,
    "Prazo médio da carteira - Pessoas jurídicas - Aquisição de veículos": 20938,
    "Prazo médio da carteira - Pessoas jurídicas - Aquisição de outros bens": 20939,
    "Prazo médio da carteira - Pessoas jurídicas - Aquisição de bens total": 20940,
    "Prazo médio da carteira - Pessoas jurídicas - Arrendamento mercantil de veículos": 20941,
    "Prazo médio da carteira - Pessoas jurídicas - Arrendamento mercantil de outros bens": 20942,
    "Prazo médio da carteira - Pessoas jurídicas - Arrendamento mercantil total": 20943,
    "Prazo médio da carteira - Pessoas jurídicas - Vendor": 20944,
    "Prazo médio da carteira - Pessoas jurídicas - Compror": 20945,
    "Prazo médio da carteira - Pessoas jurídicas - Cartão de crédito rotativo": 20946,
    "Prazo médio da carteira - Pessoas jurídicas - Cartão de crédito parcelado": 20947,
    "Prazo médio da carteira - Pessoas jurídicas - Cartão de crédito total": 20948,
    "Prazo médio da carteira - Pessoas jurídicas - Adiantamento sobre contratos de câmbio (ACC)": 20949,
    "Prazo médio da carteira - Pessoas jurídicas - Financiamento a importações": 20950,
    "Prazo médio da carteira - Pessoas jurídicas - Financiamento a exportações": 20951,
    "Prazo médio da carteira - Pessoas jurídicas - Repasse externo": 20952,
    "Prazo médio da carteira - Pessoas jurídicas - Outros créditos livres": 20953,
    "Prazo médio da carteira - Pessoas físicas - Total": 20954,
    "Prazo médio da carteira - Pessoas físicas - Cheque especial": 20955,
    "Prazo médio da carteira - Pessoas físicas - Crédito pessoal não consignado": 20956,
    "Prazo médio da carteira - Pessoas físicas - Crédito pessoal não consignado vinculado à composição de dívidas": 20957,
    "Prazo médio da carteira - Pessoas físicas - Crédito pessoal consignado para trabalhadores do setor privado": 20958,
    "Prazo médio da carteira - Pessoas físicas - Crédito pessoal consignado para trabalhadores do setor público": 20959,
    "Prazo médio da carteira - Pessoas físicas - Crédito pessoal consignado para aposentados e pensionistas do INSS": 20960,
    "Prazo médio da carteira - Pessoas físicas - Crédito pessoal consignado total": 20961,
    "Prazo médio da carteira - Pessoas físicas - Crédito pessoal total": 20962,
    "Prazo médio da carteira - Pessoas físicas - Aquisição de veículos": 20963,
    "Prazo médio da carteira - Pessoas físicas - Aquisição de outros bens": 20964,
    "Prazo médio da carteira - Pessoas físicas - Aquisição de bens total": 20965,
    "Prazo médio da carteira - Pessoas físicas - Arrendamento mercantil de veículos": 20966,
    "Prazo médio da carteira - Pessoas físicas - Arrendamento mercantil de outros bens": 20967,
    "Prazo médio da carteira - Pessoas físicas - Arrendamento mercantil total": 20968,
    "Prazo médio da carteira - Pessoas físicas - Cartão de crédito rotativo": 20969,
    "Prazo médio da carteira - Pessoas físicas - Cartão de crédito parcelado": 20970,
    "Prazo médio da carteira - Pessoas físicas - Cartão de crédito total": 20971,
    "Prazo médio da carteira - Pessoas físicas - Desconto de cheques": 20972,
    "Prazo médio da carteira - Pessoas físicas - Outros créditos livres": 20973,

}

saldos_novos2 = {
    "Prazo médio da carteira - Total": 20974,
    "Prazo médio da carteira - Pessoas jurídicas - Total": 20975,
    "Prazo médio da carteira - Pessoas jurídicas - Crédito rural com taxas de mercado": 20976,
    "Prazo médio da carteira - Pessoas jurídicas - Crédito rural com taxas reguladas": 20977,
    "Prazo médio da carteira - Pessoas jurídicas - Crédito rural total": 20978,
    "Prazo médio da carteira - Pessoas jurídicas - Financiamento imobiliário com taxas de mercado": 20979,
    "Prazo médio da carteira - Pessoas jurídicas - Financiamento imobiliário com taxas reguladas": 20980,
    "Prazo médio da carteira - Pessoas jurídicas - Financiamento imobiliário total": 20981,
    "Prazo médio da carteira - Pessoas jurídicas - Capital de giro com recursos do BNDES": 20982,
    "Prazo médio da carteira - Pessoas jurídicas - Financiamento de investimentos com recursos do BNDES": 20983,
    "Prazo médio da carteira - Pessoas jurídicas - Financiamento agroindustrial com recursos do BNDES": 20984,
    "Prazo médio da carteira - Pessoas jurídicas - Financiamento com recursos do BNDES total": 20985,
    "Prazo médio da carteira - Pessoas jurídicas - Outros créditos direcionados": 20986,
    "Prazo médio da carteira - Pessoas físicas - Total": 20987,
    "Prazo médio da carteira - Pessoas físicas - Crédito rural com taxas de mercado": 20988,
    "Prazo médio da carteira - Pessoas físicas - Crédito rural com taxas reguladas": 20989,
    "Prazo médio da carteira - Pessoas físicas - Crédito rural total": 20990,
    "Prazo médio da carteira - Pessoas físicas - Financiamento imobiliário com taxas de mercado": 20991,
    "Prazo médio da carteira - Pessoas físicas - Financiamento imobiliário com taxas reguladas": 20992,
    "Prazo médio da carteira - Pessoas físicas - Financiamento imobiliário total": 20993,
    "Prazo médio da carteira - Pessoas físicas - Capital de giro com recursos do BNDES": 20994,
    "Prazo médio da carteira - Pessoas físicas - Financiamento de investimentos com recursos do BNDES": 20995,
    "Prazo médio da carteira - Pessoas físicas - Financiamento agroindustrial com recursos do BNDES": 20996,
    "Prazo médio da carteira - Pessoas físicas - Financiamento com recursos do BNDES total": 20997,
    "Prazo médio da carteira - Pessoas físicas - Microcrédito destinado a consumo": 20998,
    "Prazo médio da carteira - Pessoas físicas - Microcrédito destinado a microempreendedores": 20999,
    "Prazo médio da carteira - Pessoas físicas - Microcrédito total": 21001,
    "Prazo médio da carteira - Pessoas físicas - Outros créditos direcionados": 21002,

}

saldos_novos3 = {
    "Prazo médio das novas operações - Total": 20852,
    "Prazo médio das novas operações - Pessoas jurídicas - Total": 20853,
    "Prazo médio das novas operações - Pessoas físicas - Total": 20854,

}

saldos_novos4= {
    "Prazo médio das novas operações - Total": 20855,
    "Prazo médio das novas operações - Pessoas jurídicas - Total": 20856,
    "Prazo médio das novas operações - Pessoas jurídicas - Desconto de duplicatas e recebíveis": 20857,
    "Prazo médio das novas operações - Pessoas jurídicas - Desconto de cheques": 20858,
    "Prazo médio das novas operações - Pessoas jurídicas - Antecipação de faturas de cartão de crédito": 20859,
    "Prazo médio das novas operações - Pessoas jurídicas - Capital de giro com prazo de até 365 dias": 20860,
    "Prazo médio das novas operações - Pessoas jurídicas - Capital de giro com prazo superior a 365 dias": 20861,
    "Prazo médio das novas operações - Pessoas jurídicas - Capital de giro rotativo": 20862,
    "Prazo médio das novas operações - Pessoas jurídicas - Capital de giro total": 20863,
    "Prazo médio das novas operações - Pessoas jurídicas - Aquisição de veículos": 20864,
    "Prazo médio das novas operações - Pessoas jurídicas - Aquisição de outros bens": 20865,
    "Prazo médio das novas operações - Pessoas jurídicas - Aquisição de bens total": 20866,
    "Prazo médio das novas operações - Pessoas jurídicas - Arrendamento mercantil de veículos": 20867,
    "Prazo médio das novas operações - Pessoas jurídicas - Arrendamento mercantil de outros bens": 20868,
    "Prazo médio das novas operações - Pessoas jurídicas - Arrendamento mercantil total": 20869,
    "Prazo médio das novas operações - Pessoas jurídicas - Vendor": 20870,
    "Prazo médio das novas operações - Pessoas jurídicas - Compror": 20871,
    "Prazo médio das novas operações - Pessoas jurídicas - Cartão de crédito parcelado": 20872,
    "Prazo médio das novas operações - Pessoas jurídicas - Adiantamento sobre contratos de câmbio (ACC)": 20873,
    "Prazo médio das novas operações - Pessoas jurídicas - Financiamento a importações": 20874,
    "Prazo médio das novas operações - Pessoas jurídicas - Financiamento a exportações": 20875,
    "Prazo médio das novas operações - Pessoas jurídicas - Repasse externo": 20876,
    "Prazo médio das novas operações - Pessoas jurídicas - Outros créditos livres": 20877,
    "Prazo médio das novas operações - Pessoas físicas - Total": 20878,
    "Prazo médio das novas operações - Pessoas físicas - Crédito pessoal não consignado": 20879,
    "Prazo médio das novas operações - Pessoas físicas - Crédito pessoal não consignado vinculado à composição de dívidas": 20880,
    "Prazo médio das novas operações - Pessoas físicas - Crédito pessoal consignado para trabalhadores do setor privado": 20881,
    "Prazo médio das novas operações - Pessoas físicas - Crédito pessoal consignado para trabalhadores do setor público": 20882,
    "Prazo médio das novas operações - Pessoas físicas - Crédito pessoal consignado para aposentados e pensionistas do INSS": 20883,
    "Prazo médio das novas operações - Pessoas físicas - Crédito pessoal consignado total": 20884,
    "Prazo médio das novas operações - Pessoas físicas - Crédito pessoal total": 20885,
    "Prazo médio das novas operações - Pessoas físicas - Aquisição de veículos": 20886,
    "Prazo médio das novas operações - Pessoas físicas - Aquisição de outros bens": 20887,
    "Prazo médio das novas operações - Pessoas físicas - Aquisição de bens total": 20888,
    "Prazo médio das novas operações - Pessoas físicas - Arrendamento mercantil de veículos": 20889,
    "Prazo médio das novas operações - Pessoas físicas - Arrendamento mercantil de outros bens": 20890,
    "Prazo médio das novas operações - Pessoas físicas - Arrendamento mercantil total": 20891,
    "Prazo médio das novas operações - Pessoas físicas - Cartão de crédito parcelado": 20892,
    "Prazo médio das novas operações - Pessoas físicas - Desconto de cheques": 20893,
    "Prazo médio das novas operações - Pessoas físicas - Outros créditos livres": 20894,

}
saldos_novos5={
    "Prazo médio das novas operações - Total": 20895,
    "Prazo médio das novas operações - Pessoas jurídicas - Total": 20896,
    "Prazo médio das novas operações - Pessoas jurídicas - Crédito rural com taxas de mercado": 20897,
    "Prazo médio das novas operações - Pessoas jurídicas - Crédito rural com taxas reguladas": 20898,
    "Prazo médio das novas operações - Pessoas jurídicas - Crédito rural total": 20899,
    "Prazo médio das novas operações - Pessoas jurídicas - Financiamento imobiliário com taxas de mercado": 20900,
    "Prazo médio das novas operações - Pessoas jurídicas - Financiamento imobiliário com taxas reguladas": 20901,
    "Prazo médio das novas operações - Pessoas jurídicas - Financiamento imobiliário total": 20902,
    "Prazo médio das novas operações - Pessoas jurídicas - Capital de giro com recursos do BNDES": 20903,
    "Prazo médio das novas operações - Pessoas jurídicas - Financiamento de investimentos com recursos do BNDES": 20904,
    "Prazo médio das novas operações - Pessoas jurídicas - Financiamento agroindustrial com recursos do BNDES": 20905,
    "Prazo médio das novas operações - Pessoas jurídicas - Financiamento com recursos do BNDES total": 20906,
    "Prazo médio das novas operações - Pessoas jurídicas - Outros créditos direcionados": 20907,
    "Prazo médio das novas operações - Pessoas físicas - Total": 20908,
    "Prazo médio das novas operações - Pessoas físicas - Crédito rural com taxas de mercado": 20909,
    "Prazo médio das novas operações - Pessoas físicas - Crédito rural com taxas reguladas": 20910,
    "Prazo médio das novas operações - Pessoas físicas - Crédito rural total": 20911,
    "Prazo médio das novas operações - Pessoas físicas - Financiamento imobiliário com taxas de mercado": 20912,
    "Prazo médio das novas operações - Pessoas físicas - Financiamento imobiliário com taxas reguladas": 20913,
    "Prazo médio das novas operações - Pessoas físicas - Financiamento imobiliário total": 20914,
    "Prazo médio das novas operações - Pessoas físicas - Capital de giro com recursos do BNDES": 20915,
    "Prazo médio das novas operações - Pessoas físicas - Financiamento de investimentos com recursos do BNDES": 20916,
    "Prazo médio das novas operações - Pessoas físicas - Financiamento agroindustrial com recursos do BNDES": 20917,
    "Prazo médio das novas operações - Pessoas físicas - Financiamento com recursos do BNDES total": 20918,
    "Prazo médio das novas operações - Pessoas físicas - Microcrédito destinado a consumo": 20919,
    "Prazo médio das novas operações - Pessoas físicas - Microcrédito destinado a microempreendedores": 20920,
    "Prazo médio das novas operações - Pessoas físicas - Microcrédito total": 20922,
    "Prazo médio das novas operações - Pessoas físicas - Outros créditos direcionados": 20923,

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
st.sidebar.header('Prazos das carteiras')
opcoes_selecao1 = st.sidebar.multiselect('Selecione:', list(saldos_novos.keys()))

# Multiselect para o segundo grupo de dicionários
st.sidebar.header('Prazos das carteiras com recursos livres')
opcoes_selecao2 = st.sidebar.multiselect('Selecione', list(saldos_novos1.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Prazos das carteiras com recursos direcionados')
opcoes_selecao3 = st.sidebar.multiselect('Selecione', list(saldos_novos2.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Prazos das concessões')
opcoes_selecao4 = st.sidebar.multiselect('Selecione', list(saldos_novos3.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Prazos das concessões com recursos livres')
opcoes_selecao5 = st.sidebar.multiselect('Selecione', list(saldos_novos4.keys()))

# Multiselect para o terceiro grupo de dicionários
st.sidebar.header('Prazos das concessões com recursos direcionados')
opcoes_selecao6 = st.sidebar.multiselect('Escolha os saldos', list(saldos_novos5.keys()))



# Juntando todas as opções selecionadas
opcoes_selecao = opcoes_selecao1 + opcoes_selecao2 + opcoes_selecao3 + opcoes_selecao4 + opcoes_selecao5 \
                 + opcoes_selecao6

# Carregar dados selecionados
dados_selecionados = {
    nome: carregar_dados(codigo)
    for dicionario in [saldos_novos, saldos_novos1, saldos_novos2, saldos_novos3,saldos_novos4,saldos_novos5]
    for nome, codigo in dicionario.items()
    if nome in opcoes_selecao
}



# Restante do código permanece o mesmo
# ...

# Exibir tabelas e gráficos um abaixo do outro
st.title('Prazos das Carteiras e das Concessões - Meses')
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