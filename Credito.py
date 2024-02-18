import streamlit as st

# Título
st.title('Explorando Estatísticas de Crédito')

# Explicação sobre estatísticas de crédito
st.header('Estatísticas de Crédito')

explicacoes = {
    'Saldos de crédito ampliado': 'Representa o montante total de crédito disponível no sistema financeiro, incluindo empréstimos, financiamentos e outros tipos de crédito concedidos por instituições financeiras.',
    'Saldos': 'Refere-se ao total de dívidas pendentes de pagamento, incluindo empréstimos pessoais, hipotecas, cartões de crédito, entre outros.',
    'Concessões': 'Indica a quantidade de novos empréstimos concedidos durante um determinado período de tempo.',
    'Indicadores de custo do crédito (ICC)': 'São métricas que medem o custo médio do crédito, ou seja, a taxa de juros média cobrada sobre os empréstimos concedidos.',
    'Spread do ICC': 'É a diferença entre a taxa de juros média cobrada nos empréstimos e a taxa de juros de referência, como a taxa básica de juros definida pelo banco central.',
    'Taxas de juros': 'Representam a porcentagem do valor emprestado que é cobrada como taxa de juros durante um determinado período de tempo.',
    'Spread': 'É a diferença entre a taxa de juros que as instituições financeiras pagam para captar recursos e a taxa de juros que cobram sobre os empréstimos concedidos.',
    'Prazos': 'Refere-se ao período de tempo estabelecido para o pagamento de um empréstimo ou financiamento.',
    'Atrasos e inadimplência': 'Indicam pagamentos em atraso ou não realizados, representando um indicador da saúde financeira dos tomadores de empréstimos.',
    'Provisões': 'Montante reservado pelas instituições financeiras para cobrir perdas esperadas de crédito devido a empréstimos inadimplentes.',
    'Endividamento das famílias': 'Refere-se à quantidade total de dívidas das famílias em relação à sua renda disponível.',
    'Pesquisa trimestral de condições de crédito': 'Levantamento realizado periodicamente para avaliar as condições do mercado de crédito, incluindo acesso ao crédito, taxas de juros, entre outros aspectos.',
    'Portabilidade de Crédito': 'Possibilidade de transferir um empréstimo ou financiamento de uma instituição financeira para outra, mantendo as condições contratuais originais.'
}

for item, explicacao in explicacoes.items():
    st.subheader(item)
    st.write(explicacao)

# Explicação sobre SARIMA
st.header('SARIMA (Seasonal Autoregressive Integrated Moving Average)')
st.write("""
O SARIMA é um modelo estatístico usado para prever valores futuros com base em padrões observados em dados temporais. 
Ele leva em consideração a tendência, sazonalidade e padrões de autocorrelação dos dados para fazer previsões.
""")

# Explicação sobre Decomposição da Série Temporal
st.header('Decomposição da Série Temporal')
st.write("""
A decomposição da série temporal é uma técnica usada para decompor uma série temporal em seus componentes principais, 
incluindo tendência, sazonalidade e resíduos. A tendência representa a direção geral dos dados ao longo do tempo, 
a sazonalidade captura padrões que se repetem em intervalos regulares e os resíduos são as variações aleatórias não explicadas pelos outros componentes. 
Essa decomposição ajuda a entender os padrões subjacentes nos dados e pode ser útil para fazer previsões futuras.
""")
