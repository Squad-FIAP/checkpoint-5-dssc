import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from scipy import stats

st.set_page_config(page_title="Intervalo de Confiança", layout="wide")

df = pd.read_csv("src/dataset.csv")

media_salarial = df['salary_in_usd'].mean()
desvio_padrao = df['salary_in_usd'].std()

st.markdown(
    r"""
    ## Intervalos de Confiança
    O intervalo de confiança é uma ferramenta estatística que fornece uma faixa de valores dentro da qual
    podemos esperar que um parâmetro populacional (como a média) esteja localizado, com um certo nível de confiança.

    No contexto do nosso projeto, o parâmetro de interesse é o salário médio dos profissionais de AI/ML/DS. Vamos explorar algumas
    perguntas investigativas utilizando intervalos de confiança e testes de hipótese.

    ### Coletando Dados Auxiliares
    Para realizar os cálculos de intervalo de confiança, devemos coletar:

    #### Média
    A média pode ser dada pela fórmula:

    $ \mu = \frac{1}{n} \sum_{i=1}^{n} x_{i} $

    Onde:
    - $ \mu $ é a média populacional
    - $ n $ é o número de observações
    - $ x_{i} $ são os valores individuais

    Para o dataset, a média salarial pode ser calculada utilizando a coluna `salary_in_usd` (salário convertido para USD).

    ```python
    import pandas as pd
    import numpy as np
    import scipy.stats as stats

    # Carregar o dataset
    df = pd.read_csv("dataset.csv")

    # Calcular a média salarial
    media_salarial = df['salary_in_usd'].mean()
    ```
    """
)

st.markdown(
    f"""
    - Média Salarial Anual: **{media_salarial:.2f}** USD/ano
    - Média Salarial Mensal: **{media_salarial/12:.2f}** USD/mês
    
    > _Calculada a partir de **{len(df)} observações** com **{df['salary_in_usd'].isnull().sum()} valores ausentes** na coluna `salary_in_usd`._
    """
) 

st.markdown(
    r"""
    #### Desvio Padrão
    O desvio padrão pode ser calculado pela fórmula:

    $ \sigma=\sqrt{\frac{\sum (x_{i}-\mu )^2}{N-1}} $

    Onde:
    - $ \sigma $ é o desvio padrão
    - $ N $ é o número total de observações

    Para o dataset, o desvio padrão salarial pode ser calculado utilizando a coluna `salary_in_usd` (salário convertido para USD).
    ```python
    # Calcular o desvio padrão
    desvio_padrao = df['salary_in_usd'].std()
    ```
    """
)

st.markdown(
    f"""
    - Desvio Padrão: **{df['salary_in_usd'].std():.2f}**

    ### Distribuição Normal
    """
)

mu = media_salarial
sigma = desvio_padrao

fig, ax = plt.subplots(figsize=(15, 10))
sns.histplot(data=df['salary_in_usd']/1000, bins=80, kde=True, stat='probability', ax=ax)

ax.set_xlabel('Salário Anual (USD)')
ax.set_ylabel('Probabilidade')
ax.set_title('Distribuição Salarial de Profissionais em AI/ML/DS')

min_val = int(df['salary_in_usd'].min().min())
max_val = int(df['salary_in_usd'].max().max())
# ax.set_xticks(range(min_val, max_val + 1, 5000))
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}K'))

st.pyplot(fig)

st.markdown(
    r"""
    ### Perguntas e Hipóteses
    #### Qual é o intervalo de confiança para o salário médio dos profissionais de AI/ML/DS, para uma determinada senioridade?
    Para essa pergunta, iremos analisar os dados de profissionais de senioridade **Júnior**
        
    Para calcular o intervalo de confiança, iremos aplicar a seguinte fórmula:

    $$ IC = \bar{X} \pm t_{\alpha/2, \, df} \cdot \frac{s}{\sqrt{n}} $$

    Onde:

    - \( $ \bar{X} $ \): média amostral  
    - \( $ t_{\alpha/2, \, df} $ \): valor crítico da distribuição t de Student, considerando nível de significância \(\alpha\) e graus de liberdade \(df = n - 1\)  
    - \( $ s $ \): desvio padrão amostral  
    - \( $ n $ \): tamanho da amostra  
    - \( $ df $ \): graus de liberdade, calculado como \(n - 1\)
    
    Calculando, temos a seguinte distribuição de valores:
    """
)

salarios = df['salary_in_usd'].dropna()/1000

n = len(salarios)
media = np.mean(salarios)
desvio_amostral = np.std(salarios, ddof=1)
df_graus = n - 1


# Intervalo de confiança (ex: 95%)
conf = st.slider("Escolha o nível de confiança (%)", min_value=80, max_value=99, value=95)
alpha = 1 - (conf / 100)

# 🔢 Stats
n = len(salarios)
media = np.mean(salarios)
desvio_amostral = np.std(salarios, ddof=1)
graus_de_liberdade = n - 1
t_critico = stats.t.ppf(1 - alpha/2, df=graus_de_liberdade)
margem_erro = t_critico * (desvio_amostral / np.sqrt(n))
lim_inf = media - margem_erro
lim_sup = media + margem_erro

# 📊 Plot
fig, ax = plt.subplots(figsize=(15, 10))
sns.histplot(salarios, bins=40, kde=True, stat="probability", ax=ax)

# Faixa do intervalo (opcional)
ax.axvspan(lim_inf, lim_sup, color='skyblue', alpha=0.15)

# Linhas nos limites e na média
ax.axvline(media, color='blue', linestyle='--', label=f'Média: ${media:,.1f}K')
ax.axvline(lim_inf, color='skyblue', linestyle=':', linewidth=2, label='Limite Inferior')
ax.axvline(lim_sup, color='skyblue', linestyle=':', linewidth=2, label='Limite Superior')

# Anotações
ax.text(lim_inf, 0.01, f"{lim_inf:,.0f}", ha='right', va='bottom', fontsize=10, color='skyblue')
ax.text(lim_sup, 0.01, f"{lim_sup:,.0f}", ha='left', va='bottom', fontsize=10, color='skyblue')

# Título e legendas
ax.set_xlabel("Salário Anual (USD)")
ax.set_ylabel("Probabilidade")
ax.set_title(f"Distribuição Salarial com Intervalo de Confiança ({conf}%)")
ax.legend()

# Mostrar
st.pyplot(fig)

st.markdown(
    f"""
    Portanto, podemos afirmar que a média salarial anual dos profissionais de senioridade Junior está no intervalo: **({lim_inf:.1f}K, {lim_sup:.1f}K)** com **{conf}% de certeza**.
    """
)


st.markdown(
    f"""
    #### Há uma diferença significativa no intervalo de confiança do salário médio entre diferentes níveis de experiência?

    Para essa pergunta, iremos analisar os dados de profissionais de senioridade **Pleno** e **Sênior**.

    ##### Pleno    
    """
)


conf_2 = st.slider("Escolha o nível de confiança (%)", min_value=80, max_value=99, value=95, key="conf_2")

# Stats
salarios_pleno = df[df['experience_level'] == 'MI']['salary_in_usd'].dropna()/1000
salarios_senior = df[df['experience_level'] == 'SE']['salary_in_usd'].dropna()/1000

n_senior = len(salarios_senior)
n_pleno = len(salarios_pleno)

media_salarial_pleno = df[df['experience_level'] == 'MI']['salary_in_usd'].mean()
media_salarial_senior = df[df['experience_level'] == 'SE']['salary_in_usd'].mean()


mu_pleno = media_salarial_pleno
mu_senior = media_salarial_senior

desvio_amostral_pleno = np.std(salarios_pleno, ddof=1)
desvio_amostral_senior = np.std(salarios_senior, ddof=1)

sigma_pleno = desvio_amostral_pleno

alpha_2 = 1 - (conf_2 / 100)

graus_de_liberdade_pleno = n_pleno - 1
graus_de_liberdade_senior = n_senior - 1


t_critico_pleno = stats.t.ppf(1 - alpha/2, df=graus_de_liberdade_pleno)
t_critico_senior = stats.t.ppf(1 - alpha/2, df=graus_de_liberdade_senior)

margem_erro_pleno = t_critico_pleno * (desvio_amostral_pleno / np.sqrt(n_pleno))
margem_erro_senior = t_critico_senior * (desvio_amostral_senior / np.sqrt(n_senior))

lim_inf_senior = media_salarial_senior - margem_erro_senior
lim_sup_senior = media_salarial_senior + margem_erro_senior

lim_inf_pleno = media_salarial_pleno - margem_erro_pleno
lim_sup_pleno = media_salarial_pleno + margem_erro_pleno


# 📊 Plot
fig2, ax2 = plt.subplots(figsize=(15, 10))
sns.histplot(salarios_pleno, bins=40, kde=True, stat="probability", ax=ax2, color='orange', label='Pleno')
sns.histplot(salarios_senior, bins=40, kde=True, stat="probability", ax=ax2, color='blue', label='Sênior')

ax2.axvspan(lim_inf_pleno, lim_sup_pleno, color='orange', alpha=0.15)
ax2.axvline(media_salarial_pleno, color='orange', linestyle='--', label=f'Média Pleno: ${media_salarial_pleno:,.1f}K')
ax2.axvline(lim_inf_pleno, color='orange', linestyle=':', linewidth=2, label='Limite Inferior Pleno')
ax2.axvline(lim_sup_pleno, color='orange', linestyle=':', linewidth=2, label='Limite Superior Pleno')

ax2.axvspan(lim_inf_senior, lim_sup_senior, color='blue', alpha=0.15)
ax2.axvline(media_salarial_senior, color='blue', linestyle='--', label=f'Média Sênior: ${media_salarial_senior:,.1f}K')
ax2.axvline(lim_inf_senior, color='blue', linestyle=':', linewidth=2, label='Limite Inferior Sênior')
ax2.axvline(lim_sup_senior, color='blue', linestyle=':', linewidth=2, label='Limite Superior Sênior')

# Anotações
ax2.text(lim_inf_pleno, 0.01, f"{lim_inf_pleno:,.0f}", ha='right', va='bottom', fontsize=10, color='orange')
ax2.text(lim_sup_pleno, 0.01, f"{lim_sup_pleno:,.0f}", ha='left', va='bottom', fontsize=10, color='orange')

ax2.text(lim_inf_senior, 0.01, f"{lim_inf_senior:,.0f}", ha='right', va='bottom', fontsize=10, color='blue')
ax2.text(lim_sup_senior, 0.01, f"{lim_sup_senior:,.0f}", ha='left', va='bottom', fontsize=10, color='blue')

# Título e legendas
ax2.set_xlabel("Salário Anual (USD)")
ax2.set_ylabel("Probabilidade")
ax2.set_title(f"Distribuição Salarial com Intervalo de Confiança ({conf_2}%)")
ax2.legend()

# Mostrar
st.pyplot(fig2)
