import streamlit as st
import datetime
import pandas as pd
import gspread
import time

st.set_page_config(
        page_title="Expense Input",
)

st.markdown(''' # 費用入力 ''')

with st.form("my_form"):
   d = st.date_input("日にち", datetime.date.today())
   
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
   
   amt = st.number_input('金額', min_value=0)
   
   pay_method = st.radio('支払方法', (
           '現金',
           'ID',
           'クレカ：LINEカード',
           'クレカ：エポスカード',
           'クレカ：三井ショッピングパーク',
           'クレカ：三井住友',
           'クレカ：その他',
           'ポイント利用',
           ))
   
   category = st.radio('カテゴリー', (
           '必需品',
           '外食費',
           '好きなもの',
           '交通費',
           '交際費',
           '医療費',
           '旅費',
           'フゥ費',
           '雑費'
   ))
   
   memo = st.text_input('備考 (任意)', '')


   # Every form must have a submit button.
   submitted = st.form_submit_button("確認")
   if submitted:
        st.write('📝 Expense Submitted')
        
        columns = ['日にち', '曜日', '金額', '支払方法', 'カテゴリー', '備考']
        exp_input = [d, dow, amt, pay_method, category, memo]
        df = pd.DataFrame(dict(zip(columns, exp_input)), index=[0])
        st.write(df)
        
        start_time = time.time()
        gc = gspread.service_account_from_dict(st.secrets.service_account)
        sh = gc.open_by_key(st.secrets.sheet.sheet_key)
        worksheet = sh.sheet1
        st.write("--- %s seconds ---" % (time.time() - start_time))
        
        start_time = time.time()
        gdf = pd.DataFrame(worksheet.get_all_records())
        st.write("--- %s seconds ---" % (time.time() - start_time))
        
        st.write(gdf)