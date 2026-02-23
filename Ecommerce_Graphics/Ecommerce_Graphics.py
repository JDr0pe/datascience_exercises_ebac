import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

df = pd.read_csv('ecommerce_preparados.csv')

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

print(df.head())

# Tratamento de dados - Data Treatment 

# Generos - Genders Treatment
df['Gênero'] = df['Gênero'].apply(lambda g: 'Mulher' if any(word in str(g).lower() for word in ['mulher', 'feminino', 'menina', 'meninas']) 
                                  else 'Homem' if any(word in str(g).lower() for word in ['homem', 'masculino', 'menino', 'meninos']) 
                                  else 'Outro')


# Grafico de dispersão entre quantidade vendida e frequência do material - Scatter plot between quantity sold and frequency of the material.
sns.jointplot(x=df['Preço'], y=df['Qtd_Vendidos'], kind='scatter')
plt.show()

# Seleciona variáveis de interesse - Selects variables of interest
numeric_cols = ['Nota', 'N_Avaliações', 'Desconto', 'Qtd_Vendidos_Cod', 'Preço']

# Limpa e prepara dados tento certeza de que são numéricos - Cleans and prepares data ensuring they are numeric
df_numeric = df[numeric_cols].select_dtypes(include=[np.number]).dropna()
df_numeric = df_numeric.astype(float)

# Matriz de correlação - Correlation matrix
corr_matrix = df_numeric.corr()

# Mapa de calor da matriz de correlação - Heatmap of the correlation matrix
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, square=True, fmt='.2f')
plt.title('Mapa de Calor Correlações')
plt.show()

# Grafico de Barras entre Desconto e Gênero - Bar plot between Discount and Gender
sns.barplot(x=df['Gênero'], y=df['Desconto'])
plt.title('Desconto por Gênero')
plt.xlabel('Gênero')
plt.ylabel('Desconto (%)')
plt.xticks(rotation=45)
plt.show()

# Grafico de Pizza de Quantidade de Vendidos por Marca - Pie chart of Quantity Sold by Brand

# Agrupa por marca e soma a quantidade vendida, depois seleciona as 10 maiores - Groups by brand and sums the quantity sold, then selects the top 10
top_marcas = df.groupby('Marca')['Qtd_Vendidos_Cod'].sum().nlargest(10).reset_index()

# Grafico de pizza - Pie chart
plt.figure(figsize=(10,8))
plt.pie(top_marcas['Qtd_Vendidos_Cod'], labels=top_marcas['Marca'], autopct='%1.1f%%', startangle=90)
plt.title('Top 10 Marcas por Qtd_Vendidos_Cod Total')
plt.axis('equal')
plt.savefig('pizza_marcas_cod.png')
plt.show()

# Grafico de Densidade do Preço - Density plot of Price
sns.kdeplot(df['Preço'], shade=True)
plt.title('Densidade do Preço')
plt.xlabel('Preço')
plt.ylabel('Densidade')
plt.show()