# Análise de Dados do Café: Respostas às Perguntas de Negócio

# Este notebook responde às seguintes perguntas:
# 1. Quais são os dias da semana com maior e menor volume de vendas?
# 2. Em quais horários do dia as vendas atingem o pico e quando são mais baixas?
# 3. Como o faturamento varia ao longo dos meses?
# 4. Quais produtos são os mais vendidos e quais têm o maior faturamento total?
# 5. Existem produtos com venda muito baixa que talvez devam ser removidos do cardápio?
# 6. Como os valores dos produtos influenciam o volume de vendas?
# 7. Em quais horários ou dias o café poderia precisar de mais funcionários no caixa?
# 8. Existem tendências semanais ou mensais?

# Bibliotecas usadas: Pandas, Matplotlib, Seaborn.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações visuais
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Carregar o dataset
df = pd.read_csv('cafe_df.csv')

# Converter 'Date' para datetime para análises temporais
df['Date'] = pd.to_datetime(df['Date'])

# Exibir overview
print(df.head())
print(df.info())
print(df.describe())

# 1. Quais são os dias da semana com maior e menor volume de vendas?

# Ordem dos dias
ordem_dias = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Agrupar por dia da semana
vendas_dia = df.groupby('Weekday').agg(
    volume=('money', 'count'),
    faturamento=('money', 'sum')
).reindex(ordem_dias).round(2)

# Identificar max/min
max_volume_dia = vendas_dia['volume'].idxmax()
min_volume_dia = vendas_dia['volume'].idxmin()
max_fat_dia = vendas_dia['faturamento'].idxmax()
min_fat_dia = vendas_dia['faturamento'].idxmin()

print(vendas_dia)
print(f"\nDia com maior volume: {max_volume_dia} ({vendas_dia['volume'].max()} transações)")
print(f"Dia com menor volume: {min_volume_dia} ({vendas_dia['volume'].min()} transações)")
print(f"Dia com maior faturamento: {max_fat_dia} (R$ {vendas_dia['faturamento'].max():,.2f})")
print(f"Dia com menor faturamento: {min_fat_dia} (R$ {vendas_dia['faturamento'].min():,.2f})")

# Gráfico
ax = vendas_dia.plot(kind='bar')
plt.title('Volume e Faturamento por Dia da Semana')

# Adicionar rótulos de dados
for container in ax.containers:
    for bar in container:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:,.0f}', ha='center', va='bottom')

plt.show()

# 2. Em quais horários do dia as vendas atingem o pico e quando são mais baixas?

# Agrupar por hora
vendas_hora = df.groupby('hour_of_day').agg(
    volume=('money', 'count'),
    faturamento=('money', 'sum')
).round(2)

# Identificar picos
pico_hora_vol = vendas_hora['volume'].idxmax()
baixa_hora_vol = vendas_hora['volume'].idxmin()

print(vendas_hora)
print(f"\nPico de volume: {pico_hora_vol}h ({vendas_hora['volume'].max()} transações)")
print(f"Baixa de volume: {baixa_hora_vol}h ({vendas_hora['volume'].min()} transações)")

# Gráfico
vendas_hora.plot(kind='line')
plt.title('Volume e Faturamento por Hora do Dia')
plt.xlabel('Hora do Dia')
plt.show()

# 3. Como o faturamento varia ao longo dos meses?
# Extrair mês-ano
df['mes_ano'] = df['Date'].dt.to_period('M')

# Agrupar
faturamento_mes = df.groupby('mes_ano')['money'].sum().round(2)

print(faturamento_mes)

# Gráfico
ax = faturamento_mes.plot(kind='bar')
plt.title('Faturamento por Mês')
plt.xlabel('Mês-Ano')
plt.ylabel('Faturamento Total (R$)')

plt.xticks(rotation=45, ha='right')  # Rotação nos labels de meses para melhor legibilidade
plt.tight_layout()
plt.show()

# 4. Quais produtos são os mais vendidos e quais têm o maior faturamento total?
# Agrupar por produto
produtos = df.groupby('coffee_name').agg(
    volume=('money', 'count'),
    faturamento=('money', 'sum')
).sort_values('volume', ascending=False).round(2)

print(produtos)

# Top 3
print(f"\nTop 3 mais vendidos: {produtos['volume'].head(3).index.tolist()}")
print(f"Top 3 maior faturamento: {produtos.sort_values('faturamento', ascending=False)['faturamento'].head(3).index.tolist()}")

# Gráfico
ax = produtos.plot(kind='bar')
plt.title('Volume e Faturamento por Produto')

# Adicionar rótulos de dados
for container in ax.containers:
    for bar in container:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f'{height:,.0f}', ha='center', va='bottom', fontsize=8)

# Rotacionar labels do eixo x (produtos)
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()

# 5. Existem produtos com venda muito baixa que talvez devam ser removidos do cardápio?
total_volume = df.shape[0]
threshold = total_volume * 0.05  # Ex: <5% do total
baixa_venda = produtos[produtos['volume'] < threshold]

print(baixa_venda)
print(f"\nSugestão: Remover {baixa_venda.index.tolist()} se volume < {threshold} transações.")

# 6. Como os valores dos produtos influenciam o volume de vendas?
# Preço médio por produto
preco_medio = df.groupby('coffee_name')['money'].mean().round(2)
produtos['preco_medio'] = preco_medio

# Correlação
correlacao = produtos['preco_medio'].corr(produtos['volume'])
print(f"Correlação preço-volume: {correlacao:.2f} (se negativa = preços altos vendem menos)")

# Gráfico
sns.scatterplot(x='preco_medio', y='volume', data=produtos)
plt.title('Preço vs. Volume de Vendas')
plt.show()

# 7. Em quais horários ou dias o café poderia precisar de mais funcionários no caixa?
# Volume por dia-hora
volume_dia_hora = df.groupby(['Weekday', 'hour_of_day'])['money'].count().unstack().reindex(ordem_dias)

media_volume = volume_dia_hora.mean().mean()
std_volume = volume_dia_hora.std().mean()
pico_threshold = media_volume + 2 * std_volume

picos = volume_dia_hora[volume_dia_hora > pico_threshold]

print(volume_dia_hora)
print(f"\nPicos (> {pico_threshold:.0f} transações):")
print(picos.dropna(how='all'))

# Heatmap
sns.heatmap(volume_dia_hora, cmap='YlGnBu')
plt.title('Volume por Dia e Hora')
plt.show()

print("\nSugestão: Mais funcionários nos picos identificados.")

# 8. Existem tendências semanais ou mensais?
# Tendência semanal (média)
media_semanal = vendas_dia['faturamento']

# Tendência mensal: Rolling average
faturamento_diario = df.groupby('Date')['money'].sum()
rolling = faturamento_diario.rolling(window=7).mean()

print("\nTendência semanal:")
print(media_semanal)

faturamento_diario.plot(label='Diário')
rolling.plot(label='Média Móvel 7 Dias')
plt.title('Tendências de Faturamento')
plt.legend()
plt.show()
