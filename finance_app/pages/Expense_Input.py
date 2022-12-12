import streamlit as st
import datetime
import pandas as pd
import gspread

st.set_page_config(
        page_title='Expense Input',
        layout='wide'
)

st.markdown(''' # 費用入力 ''')


with st.form("my_form", clear_on_submit=True):
   # set date as today
   d = st.date_input("日にち", datetime.date.today())
   
   # calculate day of the week
   dow_idx = d.weekday()
   dow_dict = {
           0: '月',
           1: '火',
           2: '水',
           3: '木',
           4: '金',
           5: '土',
           6: '日',
   }
   dow = dow_dict[dow_idx]
   
   # expense amount
   amt = st.number_input('金額', min_value=0)
   
   # payment method
   pay_method = st.radio('支払方法', (
           '現金',
           'ID',
           'クレカ',
           'ポイント利用',
           ))
   
#    pay_method = st.radio('支払方法', (
#            '現金',
#            'ID',
#            'クレカ：LINEカード',
#            'クレカ：エポスカード',
#            'クレカ：三井ショッピングパーク',
#            'クレカ：三井住友',
#            'クレカ：その他',
#            'ポイント利用',
#            ))
   
   # category of expense
   category = st.radio('カテゴリー', (
           '必需品',
           '外食費',
           '好きなもの',
           '交通費',
           '交際費',
           '医療費',
           '旅費',
           'ペット費',
           '雑費'
   ))
   
   # memo
   memo = st.text_input('備考 (任意)', '')


   # every form must have a submit button.
   submitted = st.form_submit_button("確認")
   if submitted:
        success = st.empty()
        with st.spinner('⏳ 書き込み中...'):
                # df for new expense entry
                columns = ['日にち', '曜日', '金額', '支払方法', 'カテゴリー', '備考']
                exp_input = [str(d), dow, amt, pay_method, category, memo]
                df = pd.DataFrame(dict(zip(columns, exp_input)), index=[0])
                st.dataframe(df, use_container_width=True)
        
                # load gsheet & write new entry
                gc = gspread.service_account_from_dict(st.secrets.service_account)
                sh = gc.open_by_key(st.secrets.sheet.sheet_key)
                worksheet = sh.sheet1
                index = len(worksheet.col_values(1)) + 1
                worksheet.update(f'A{index}', [exp_input])
        success.success('経費更新完成しました', icon='✅')