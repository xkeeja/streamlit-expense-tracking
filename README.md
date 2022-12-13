# 💰📝 Expense Tracker (Japanese & English)

A simple expense tracker built entirely in Streamlit. <br>
Data saved & retrieved from Google Sheet through Google APIs. <br>
Primarily written in Japanese with English translations.

## Demo

https://expense-tracker.streamlit.app/

## Set up

### Google API credentials
- Authenticate gspread (https://docs.gspread.org/en/v5.7.0/oauth2.html)
- Add key to your local app secrets and copy your app secrets to streamlit cloud (https://docs.streamlit.io/knowledge-base/tutorials/databases/gcs)

### Install requirements
In terminal:
```
pip install -U pip
pip install -r requirements.txt
```

### Run locally
In terminal:
```
cd ~/{your_file_path}/streamlit-expense-tracking
make streamlit
```
In your browser go to this url: `localhost:8501`

### Streamlit deployment
- Main file path is `finance_app/Summary.py`
- Copy local app secrets to streamlit cloud

## Built With
- [Streamlit](https://streamlit.io/) - UI & deployment
- [GCP](https://cloud.google.com/) - API credentials & access

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License
