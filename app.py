from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    ticker = request.form['ticker'].upper()  # Converti il ticker in maiuscolo
    investment_amount = float(request.form['amount'])
    years = int(request.form['years'])

    # Ottieni i dati storici
    stock_data = yf.download(ticker, start='2010-01-01', end='2024-01-01')
    
    if stock_data.empty:
        return "Nessun dato trovato", 404

    # Calcola il rendimento
    stock_data['Cumulative Return'] = (1 + stock_data['Adj Close'].pct_change()).cumprod()
    final_value = stock_data['Cumulative Return'].iloc[-1] * investment_amount

    # Visualizza il grafico
    plt.figure(figsize=(10, 5))
    stock_data['Cumulative Return'].plot()
    plt.title(f'Andamento dell\'investimento in {ticker}')
    plt.xlabel('Data')
    plt.ylabel('Rendimento Cumulativo')
    plt.grid()
    plt.savefig(os.path.join('static', 'plot.png'))
    plt.close()

    return f"Valore finale dell'investimento: €{final_value:.2f}"

if __name__ == '__main__':
    app.run(debug=True)
