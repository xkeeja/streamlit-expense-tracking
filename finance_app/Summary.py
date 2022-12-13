import streamlit as st
import datetime
import pandas as pd
import gspread
import plotly.express as px

st.set_page_config(
        page_title='経費概要 / Expense Summary',
        layout='wide'
)

st.markdown('# 経費概要 / Expense Summary')

# insert line spacer
st.markdown('***')

# load dataframe from gsheet
def load_gsheet():
        gc = gspread.service_account_from_dict(st.secrets.service_account)
        sh = gc.open_by_key(st.secrets.sheet.sheet_key)
        worksheet = sh.sheet1
        df = pd.DataFrame(worksheet.get_all_records())
        df['日にち'] = pd.to_datetime(df['日にち'])
        return df

@st.cache(ttl=60*5)
def graph_year(df, cumulative=False):
        fig = px.histogram(x=df.日にち.dt.month, y=df.金額, color=df.カテゴリー, nbins=12, labels={'x': '月 / Month', 'y': '金額 / Amount', 'color': 'カテゴリー / Category'}, cumulative=cumulative)
        fig.update_layout(bargap =0.2, yaxis_title='金額 / Amount', )
        fig.update_xaxes(tickmode='linear')
        fig.update_yaxes(tickformat=',d')
        fig.update_traces(hovertemplate='%{y}')
        return fig


df = load_gsheet()

# current datetime
now = datetime.date.today()

# choose year
years = list(set(df.日にち.dt.year))
years.sort(reverse=True)
y = st.selectbox('年度を選択してください / Choose year', years, index=0)

# filter df to selected year & calculate sum
df_y = df[df.日にち.dt.year == y]
df_y_sum = df_y.金額.sum()
df_py = df[df.日にち.dt.year == y-1]
df_py_sum = df_py.金額.sum()

# current year vs. last year
a, b = st.columns(2)
a.metric(f'{y}総金額 / {y} Total', str('¥{:,}'.format(df_y_sum)), str('¥{:,}'.format(df_py_sum - df_y_sum)))
b.metric(f'{y-1}総金額 / {y-1} Total', str('¥{:,}'.format(df_py_sum)))

# graph current year
st.plotly_chart(graph_year(df_y, False))

# graph cumulative year
with st.expander('年間累積グラフ / Yearly Cumulative Graph'):
        st.plotly_chart(graph_year(df_y, True))

# insert line spacer
st.markdown('***')

# choose month
m = st.selectbox('月を選択してください / Choose month', list(range(1,13)), index=now.month-1)

# filter df to current month
df_m = df[(df.日にち.dt.month == m) & (df.日にち.dt.year == y)].sort_values(by=['日にち'])

# filter df to previous month
if m == 1:
        df_pm = df[(df.日にち.dt.month == 12) & (df.日にち.dt.year == y-1)]
        df_pm_str = f'{y-1}-{12}の総金額'
else:
        df_pm = df[(df.日にち.dt.month == m-1) & (df.日にち.dt.year == y)]
        df_pm_str = f'{y}-{m-1}の総金額'

# current month vs last month
a, b = st.columns(2)
df_m_sum = df_m.金額.sum()
df_pm_sum = df_pm.金額.sum()
a.metric(f'{y}-{m}の総金額', str('{:,}'.format(df_m_sum)), str('{:,}'.format(df_pm_sum - df_m_sum)))
b.metric(df_pm_str, str('{:,}'.format(df_pm_sum)))

# show expense entries of selected month
st.markdown(f'### {y}-{m}の経費 / {y}-{m} Expense Entries')
df_m = df[(df.日にち.dt.month == m) & (df.日にち.dt.year == y)].sort_values(by=['日にち'])
df_m['日にち'] = df_m['日にち'].dt.date
df_m.set_index('日にち', inplace=True)
st.dataframe(df_m.style.format({'金額': '{:,d}'}), use_container_width=True)
st.markdown('***')

# calculate expenses by category & payment method
a, b = st.columns(2)
with a:
        exp_cat = df_m.filter(items=['カテゴリー', '金額']).groupby('カテゴリー').sum().sort_values(by=['金額'], ascending=False)
        st.markdown('#### カテゴリーごと / By Category')
        for index, row in exp_cat.iterrows():
                st.write(index + ': '  + str('{:,}'.format(row['金額'])))

with b:
        exp_pay = df_m.filter(items=['支払方法', '金額']).groupby('支払方法').sum().sort_values(by=['金額'], ascending=False)
        st.markdown('#### 支払方法ごと / By Payment Method')
        for index, row in exp_pay.iterrows():
                st.write(index + ': ' + str('{:,}'.format(row['金額'])))
