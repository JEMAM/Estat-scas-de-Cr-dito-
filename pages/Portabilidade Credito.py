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
    "Portabilidade de crédito: Demais modalidades - Pedidos efetivados": 28633,
"Portabilidade de crédito: Demais modalidades - Saldo portado": 28634,
"Portabilidade de crédito: Demais modalidades - Total de pedidos": 28632,
"Portabilidade de crédito: Aquisição de outros bens - Pedidos efetivados": 28639,
"Portabilidade de crédito: Aquisição de outros bens - Saldo portado": 28640,
"Portabilidade de crédito: Aquisição de outros bens - Total de pedidos": 28638,
"Portabilidade de crédito: Aquisição de Veículos - Pedidos efetivados": 28636,
"Portabilidade de crédito: Aquisição de Veículos - Saldo portado": 28637,
"Portabilidade de crédito: Aquisição de Veículos - Total de pedidos": 28635,
"Portabilidade de crédito: Crédito pessoal consignado - Pedidos efetivados": 28624,
"Portabilidade de crédito: Crédito pessoal consignado - Saldo portado": 28625,
"Portabilidade de crédito: Crédito pessoal consignado - Total de pedidos": 28623,
"Portabilidade de crédito: Crédito pessoal sem consignação - Pedidos efetivados": 28627,
"Portabilidade de crédito: Crédito pessoal sem consignação - Saldo portado": 28628,
"Portabilidade de crédito: Crédito pessoal sem consignação - Total de pedidos": 28626,
"Portabilidade de crédito: Home Equity - Pedidos efetivados": 28630,
"Portabilidade de crédito: Home Equity - Saldo portado": 28631,
"Portabilidade de crédito: Home Equity - Total de pedidos": 28629,
"Portabilidade de crédito: Imobiliário - Empreendimentos, exceto habitacional - Pedidos efetivados": 28648,
"Portabilidade de crédito: Imobiliário - Empreendimentos, exceto habitacional - Saldo portado": 28649,
"Portabilidade de crédito: Imobiliário - Empreendimentos, exceto habitacional - Total de pedidos": 28647,
"Portabilidade de crédito: Imobiliário - Habitacional SFH - Pedidos efetivados": 28642,
"Portabilidade de crédito: Imobiliário - Habitacional SFH - Saldo portado": 28643,
"Portabilidade de crédito: Imobiliário - Habitacional SFH - Total de pedidos": 28641,
"Portabilidade de crédito: Imobiliário - Habitacional SFI - Pedidos efetivados": 28645,
"Portabilidade de crédito: Imobiliário - Habitacional SFI - Saldo portado": 28646,
"Portabilidade de crédito: Imobiliário - Habitacional SFI - Total de pedidos": 28644,
"Portabilidade de crédito - Todas modalidades - Pedidos efetivados": 28651,
"Portabilidade de crédito - Todas modalidades - Saldo portado": 28652,
"Portabilidade de crédito - Todas modalidades - Total de pedidos": 28650,

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
st.sidebar.header('Portabilidade de Crédito')
opcoes_selecao1 = st.sidebar.multiselect('Selecione :', list(saldos_novos.keys()))


# Juntando todas as opções selecionadas
opcoes_selecao = opcoes_selecao1

# Carregar dados selecionados
dados_selecionados = {
    nome: carregar_dados(codigo)
    for dicionario in [saldos_novos]
    for nome, codigo in dicionario.items()
    if nome in opcoes_selecao
}



# Restante do código permanece o mesmo
# ...

# Exibir tabelas e gráficos um abaixo do outro
st.title('Portabilidade de Crédito em Reais e Unidades')
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