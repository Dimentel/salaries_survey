# импортируем библиотеку streamlit
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# Константы
DATA = 'data/inflation_salaries_data.csv'
df = pd.read_csv(
    'data/inflation_salaries_data.csv',
    sep=';',
    decimal=','
)
st.title('Заработные платы в России')
st.subheader('Номинальная заработная плата и инфляция')
# Посмотрим изменение заработной платы во времени
fig, ax = plt.subplots(ncols=1, nrows=2,
                       figsize=(18, 16),
                       sharex=True,
                       gridspec_kw={'height_ratios': (.5, .5)}
                       )
fig.layout = 'constrained'
fig.suptitle(
    'Номинальная начисленная средняя годовая заработная плата и инфляция по различным видам деятельности',
    fontsize=20
)
ax[0].set_title('Номинальная начисленная средняя годовая заработная плата', fontsize=16)
ax[0].grid(color='grey', linestyle='--')
ax[1].set_title('Инфляция', fontsize=16)
ax[1].grid(color='grey', which='both', linestyle='--')
ax[0].set_ylabel('Номинальная заработная плата, тыс руб', fontsize=16)
ax[0].set_yticks(range(0, 131, 10))
ax[1].set_ylabel('Инфляция за год, д.е.', fontsize=16)
ax[1].set_xlabel('Год', fontsize=16)
ax[1].set_xticks(range(1991, 2024, 1))
ax[1].set_xticklabels(range(1991, 2024, 1), rotation=90)
ax[0].plot(df[df['year']>=2000]['year'], df[df['year']>=2000]['building'] / 1000, label='строительство')
ax[0].plot(df[df['year']>=2000]['year'], df[df['year']>=2000]['production'] / 1000, label='обрабатывающие производства')
ax[0].plot(df[df['year']>=2000]['year'], df[df['year']>=2000]['education'] / 1000, label='образование')
ax[0].plot(df[df['year']>=2000]['year'], df[df['year']>=2000]['IT'] / 1000, label='информация и связь')
ax[0].plot(
    df['year'],
    df['all_economic'] / 1000,
    label='в целом по стране',
    linestyle='dotted'
)
ax[1].plot(df[df['year']>=2000]['year'], df[df['year']>=2000]['inflation'], label='инфляция')
ax[1].set_yscale('log')
ax[0].legend(loc='upper center')
ax[1].legend()
plt.show()
st.pyplot(fig)
st.markdown(
    '''
    Выводы:
- до 2000 года инфляция в некоторые годы была очень высокой и резко изменялась, а в последние 15-20 лет динамика
изменения инфляции снизилась;
- заработные платы за период с 2000 года до 2023 года в рассматриваемых видах деятельности выросли многократно, при
этом ни разу, кроме 2009 года, не наблюдается снижение заработной платы;
- наименьшие заработные платы из рассматриваемых видов деятельности наблюдаются в сфере образования, на всём
рассматриваемом периоде заработные платы в образовании ниже, чем в среднем по всем видам деятельности;
- наибольшие заработные платы из рассматриваемых видов деятельности наблюдаются в сфере информационных технологий и
связи, при этом они заметно выше, чем в среднем по всем видам деятельности;
- заработные платы в строительстве до 2014 года превышали заработные платы в обрабатывающем производстве, в период
с 2014 года по 2021 год, наоборот, в обрабатывающих производствах заработная плата выше, чем в строительстве. Начиная
с 2021 года заработные платы в строительстве и в обрабатывающих производствах ориентировочно одинаковы;
- начиная с 2012 года в строительстве заработные платы ниже, чем средняя по всем видам деятельности;
- начиная с 2005 года в обрабатывающих производствах заработные платы ниже, чем средняя по всем видам деятельности.
    '''
)

st.subheader('Заработная плата с учётом инфляции')

# Приведём все номинальные значения к 2024 году. Вычислим коэффициенты для перевода из каждого года в 2024 год
df['inflation_koef'] = (df['inflation'])[::-1].cumprod()[::-1]

# Вычислим заработные платы в ценах 2024 года
for area in ['all_economic', 'education', 'production', 'building', 'IT']:
    df[area + '_2024'] = df['inflation_koef'] * df[area]

# Посмотрим изменение заработной с учётом инфляции во времени
fig = plt.figure(figsize=(16, 8))
plt.title('Начисленная средняя годовая заработная плата с учётом инфляции', fontsize=16)
plt.grid(color='grey', linestyle='--')
plt.xlabel('Год', fontsize=16)
plt.ylabel('Заработная плата в ценах 2024 года, тыс руб', fontsize=16)
plt.yticks(range(0, 150, 10))
plt.xticks(range(2000, 2024, 1))
plt.plot(df['year'], df['building_2024'] / 1000, label='строительство')
plt.plot(df['year'], df['production_2024'] / 1000, label='обрабатывающие производства')
plt.plot(df['year'], df['education_2024'] / 1000, label='образование')
plt.plot(df['year'], df['IT_2024'] / 1000, label='информация и связь')
plt.plot(df['year'], df['all_economic_2024'] / 1000,
         label='в целом по стране', linestyle='dotted'
         )
plt.legend()
plt.show()
st.pyplot(fig)
st.markdown(
    '''
    Выводы:
- реальные заработные платы показывают небольшую динамику во времени, при этом наблюдаются как периоды роста, так и
периоды снижения, например 2009 год, 2015-2016 годы, а в сфере IT 2023 год;
- в 2020 году заработные платы в строительстве соответствуют уровню 2008 года, т.е. почти не поменялись за 12 лет;
- в остальном выводы по номинальным заработным платам справедливы и для реальных. 
    '''
)

st.subheader('ВВП, безработица и заработная плата')

# Приведём значения ВВП к 2024 году и округлим значения до 10 трлн руб. для уменьшения количества различных значений
df['vvp_2024'] = round((df['vvp'] * df['inflation_koef']) / 1e13) * 10

# уровень безработицы округлим до целого значения процентов
df['unemployment_rnd'] = round(100 * df['unemployment'])

# Построим сводную таблицу
avg_salary_pivot = df.pivot_table(index=['vvp_2024'], columns=['unemployment_rnd'],
                                  values=['all_economic_2024'], aggfunc=['mean'])
avg_salary_pivot = round(avg_salary_pivot)

# Построим тепловую карту
fig = plt.figure(figsize=(12, 8))  # задаём размер

# строим тепловую карту
plt.title('Заработная плата с учётом инфляции (в среднем по стране)', fontsize=16)
sns.heatmap(
    avg_salary_pivot.values[::-1],  # чтоб снизу были более низкие значения, изменим порядок строк
    xticklabels=[x[2] for x in avg_salary_pivot.columns],
    yticklabels=list(
        avg_salary_pivot.index[::-1]
    ),  # чтоб снизу были более низкие значения, изменим порядок строк
    annot=True,  # добавляем подписи
    ax=plt.gca(),
    fmt='',
)  # задаём исходный формат
plt.xlabel('Уровень безработицы, %', fontsize=16)
plt.ylabel('ВВП в ценах 2024 года, трлн руб', fontsize=16)
plt.show()
st.pyplot(fig)
st.markdown(
    '''
    Выводы:
- чем ниже уровень безработицы и выше ВВП, тем выше средняя заработная плата по стране.
    '''
)
