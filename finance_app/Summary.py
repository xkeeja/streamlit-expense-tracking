import streamlit as st
import datetime
import pandas as pd
import gspread
import plotly.express as px

st.set_page_config(
        page_title='経費概要',
        layout='wide'
)

st.markdown(''' # 経費概要 ''')


# load dataframe from gsheet
def load_gsheet():
        gc = gspread.service_account_from_dict(st.secrets.service_account)
        sh = gc.open_by_key(st.secrets.sheet.sheet_key)
        worksheet = sh.sheet1
        df = pd.DataFrame(worksheet.get_all_records())
        df['日にち'] = pd.to_datetime(df['日にち'])
        return df

df = load_gsheet()

# current datetime
now = datetime.date.today()

# choose year & month
a, b = st.columns(2)
with a:
        y = st.selectbox('年度を選択してください', set(df.日にち.dt.year))
with b:
        m = st.selectbox('月を選択してください', list(range(1,13)), index=now.month-1)

# graph current year
df_y = df[df.日にち.dt.year == y]
fig = px.histogram(x=df_y.日にち.dt.month, y=df_y.金額, color=df_y.カテゴリー, nbins=12, labels={'x': '月', 'y': '金額', 'color': 'カテゴリー'})
fig.update_layout(bargap =0.2, yaxis_title='金額', )
fig.update_xaxes(tickmode='linear')
fig.update_yaxes(tickformat=',d')
fig.update_traces(hovertemplate='%{y}')
st.plotly_chart(fig)


# show expense entries of selected month
st.markdown('''### 選択した月の経費 ''')
df_m = df[(df.日にち.dt.month == m) & (df.日にち.dt.year == y)].sort_values(by=['日にち'])
df_m['日にち'] = df_m['日にち'].dt.date
df_m.set_index('日にち', inplace=True)
st.dataframe(df_m.style.format({'金額': '{:,d}'}), use_container_width=True)
st.markdown('***')

# sum expenses by category & payment method
a, b = st.columns(2)

with a:
        exp_cat = df_m.filter(items=['カテゴリー', '金額']).groupby('カテゴリー').sum().sort_values(by=['金額'], ascending=False)
        st.markdown('''#### カテゴリーごと''')
        st.markdown('##### 総金額: ' + str('{:,}'.format(df_m.金額.sum())))
        for index, row in exp_cat.iterrows():
                st.write(index + ': '  + str('{:,}'.format(row['金額'])))

with b:
        exp_pay = df_m.filter(items=['支払方法', '金額']).groupby('支払方法').sum().sort_values(by=['金額'], ascending=False)
        st.markdown('''#### 支払方法ごと''')
        st.markdown('##### 総金額: ' + str('{:,}'.format(df_m.金額.sum())))
        for index, row in exp_pay.iterrows():
                st.write(index + ': ' + str('{:,}'.format(row['金額'])))
