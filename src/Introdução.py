import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Checkpoint 5 - 2ESPR", layout="wide")

# Barra lateral com informações
st.sidebar.markdown("""🧑‍💻 Desenvolvido por:
- Gabriel Mediotti - [Github](https://github.com/mediotti)
- Jó Sales - [Github](https://github.com/Josales9)
- Miguel Garcez de Carvalho - [Github](https://github.com/MiguelGarcez)
- Vinicius Souza e Silva - [Github](https://github.com/Vinissil)
""")

# Introdução
st.markdown("## Checkpoint 5 - 2ESPR")
st.markdown("### Introdução ao Problema")
st.write(
    """
    O mercado de Inteligência Artificial (AI), Machine Learning (ML) e Data Science (DS) está crescendo rapidamente,
    e entender as tendências salariais é crucial tanto para profissionais quanto para empresas.
    Este dashboard busca analisar a distribuição de salários desses profissionais ao longo dos anos,
    levando em conta fatores como experiência, tipo de contrato, localização e modelo de trabalho (remoto ou presencial).
    """
)

# Apresentação do Dataset
st.markdown("### Apresentação do Dataset")
st.write(
    """
    O conjunto de dados utilizado contém informações de salários entre 2020 e 2025 para profissionais de AI, ML e DS.
    Ele inclui variáveis como nível de experiência, tipo de emprego, título do cargo, salário em USD,
    local de trabalho, tamanho da empresa e taxa de trabalho remoto.
    """
)


st.markdown("#### Exemplo de Dados")
try:
    df = pd.read_csv("dataset.csv")
    st.dataframe(df.head())
except:
    st.warning("⚠️ Dataset não encontrado. Certifique-se de fazer o upload do arquivo.")

# Hipóteses e Perguntas
st.markdown("### Hipóteses e Perguntas Investigativas")
st.write(
    """
    Algumas perguntas que iremos explorar utilizando Intervalos de Confiança e Testes de Hipótese:
    
    - **Intervalos de Confiança:**  
      - Qual é o intervalo de confiança para o salário médio dos profissionais de AI/ML/DS?  
      - Há uma diferença significativa no intervalo de confiança do salário médio entre diferentes níveis de experiência?  
      - O intervalo de confiança para o salário médio de profissionais remotos é maior ou menor do que para os presenciais?  

    - **Testes de Hipótese:**  
      - O salário médio de profissionais com nível "Senior" é significativamente maior do que o de "Mid-level"?  
      - Existe uma diferença estatisticamente significativa entre os salários médios de empresas pequenas, médias e grandes?  
      - Profissionais que trabalham remotamente ganham salários significativamente diferentes dos que trabalham presencialmente?  
    """
)

# Estrutura Inicial do Dashboard
st.markdown("### Estrutura Inicial do Dashboard")
st.write(
    """
    O dashboard será dividido em:
    1. **Exploração dos Dados** – Estatísticas descritivas, gráficos de distribuição salarial.
    2. **Intervalos de Confiança** – Cálculo e visualização de intervalos para diferentes grupos.
    3. **Testes de Hipótese** – Análises estatísticas para validar hipóteses levantadas.
    4. **Conclusões e Insights** – Resumo dos achados mais importantes.
    """
)

# Finalização
st.markdown("🚀 Vamos explorar os dados e gerar insights valiosos!")

