# utils/charts.py
import streamlit as st
import streamlit_shadcn_ui as ui
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

def overview_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close Price', mode='lines'))
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name='Volume', yaxis='y2', opacity=0.3))
    fig.update_layout(
        title="Stock Price & Volume Overview",
        yaxis=dict(title="Price"),
        yaxis2=dict(overlaying='y', side='right', title='Volume', showgrid=False),
        xaxis_title="Date",
        legend=dict(x=0, y=1.1, orientation='h')
    )
    return fig

def analysis_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name='RSI', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], name='MACD', line=dict(color='blue')))
    fig.update_layout(title="Technical Indicators: RSI & MACD", xaxis_title="Date", yaxis_title="Value")
    return fig

def reports_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close Price'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Bollinger_Upper'], name='Upper Band', line=dict(dash='dot')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Bollinger_Lower'], name='Lower Band', line=dict(dash='dot')))
    fig.update_layout(title="Price with Bollinger Bands", xaxis_title="Date", yaxis_title="Price")
    return fig

def notifications_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Sentiment_Score'], name='Sentiment Score', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Inflation_Rate'], name='Inflation Rate', yaxis='y2'))
    fig.update_layout(
        title="Sentiment vs Inflation",
        yaxis=dict(title='Sentiment'),
        yaxis2=dict(overlaying='y', side='right', title='Inflation Rate'),
        xaxis_title='Date'
    )
    return fig

def _not_enough_data_fig(message):
    fig = go.Figure()
    fig.add_annotation(text=message, xref="paper", yref="paper", showarrow=False, font=dict(size=16))
    fig.update_layout(height=300)
    return fig

def price_macro_overlay_chart(df, macro_col='CPI'):
    if 'Close' not in df.columns or macro_col not in df.columns or df['Close'].dropna().empty or df[macro_col].dropna().empty:
        return _not_enough_data_fig(f"Not enough data for Price + {macro_col} Overlay visualization.")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close Price', yaxis='y1', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df[macro_col], name=macro_col, yaxis='y2', line=dict(color='red')))
    fig.update_layout(
        title=f'Stock Price and {macro_col} Over Time',
        xaxis_title='Date',
        yaxis=dict(title='Close Price', side='left'),
        yaxis2=dict(title=macro_col, overlaying='y', side='right', showgrid=False),
        legend=dict(x=0.01, y=0.99),
        hovermode='x unified'
    )
    return fig

def moving_average_crossover_chart(df):
    required_cols = ['Close', 'MA_5', 'MA_20', 'Buy_Sell_Signal']
    if not all(col in df.columns for col in required_cols) or df['MA_5'].dropna().empty or df['MA_20'].dropna().empty:
        return _not_enough_data_fig("Not enough data for Moving Average Crossover visualization.")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_5'], name='MA 5', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_20'], name='MA 20', line=dict(color='green')))
    buy_signals = df[df['Buy_Sell_Signal'] == 'Buy']
    sell_signals = df[df['Buy_Sell_Signal'] == 'Sell']
    fig.add_trace(go.Scatter(
        x=buy_signals['Date'], y=buy_signals['Close'],
        mode='markers', name='Buy', marker=dict(symbol='triangle-up', color='lime', size=10)))
    fig.add_trace(go.Scatter(
        x=sell_signals['Date'], y=sell_signals['Close'],
        mode='markers', name='Sell', marker=dict(symbol='triangle-down', color='red', size=10)))
    fig.update_layout(
        title='Moving Average Crossover with Buy/Sell Signals',
        xaxis_title='Date', yaxis_title='Price',
        hovermode='x unified')
    return fig

def bollinger_bands_volume_chart(df):
    required_cols = ['Close', 'BB_Upper', 'BB_Lower', 'Volume']
    if not all(col in df.columns for col in required_cols) or df['BB_Upper'].dropna().empty or df['BB_Lower'].dropna().empty:
        return _not_enough_data_fig("Not enough data for Bollinger Bands + Volume visualization.")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['BB_Upper'], name='BB Upper', line=dict(color='orange', dash='dash')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['BB_Lower'], name='BB Lower', line=dict(color='orange', dash='dash')))
    fig.add_trace(go.Bar(x=df['Date'], y=df['Volume'], name='Volume', yaxis='y2', marker=dict(color='rgba(100,100,255,0.3)')))
    fig.update_layout(
        title='Bollinger Bands and Volume',
        xaxis_title='Date',
        yaxis=dict(title='Price'),
        yaxis2=dict(title='Volume', overlaying='y', side='right', showgrid=False),
        barmode='overlay',
        hovermode='x unified')
    return fig

def rsi_chart(df):
    if 'RSI' not in df.columns or df['RSI'].dropna().empty:
        return _not_enough_data_fig("Not enough data for RSI visualization.")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name='RSI', line=dict(color='purple')))
    fig.add_hrect(y0=70, y1=100, fillcolor='red', opacity=0.2, line_width=0)
    fig.add_hrect(y0=0, y1=30, fillcolor='green', opacity=0.2, line_width=0)
    fig.update_layout(
        title='RSI with Overbought/Oversold Zones',
        xaxis_title='Date', yaxis_title='RSI',
        yaxis=dict(range=[0, 100]),
        hovermode='x unified')
    return fig

def correlation_matrix_chart(df):
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] < 2:
        return _not_enough_data_fig("Not enough numeric data for Correlation Matrix visualization.")
    corr = numeric_df.corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu', aspect='auto',
                    title='Correlation Matrix')
    fig.update_layout(hovermode='closest')
    return fig

def returns_histogram_chart(df):
    if 'Daily_Return' not in df.columns or df['Daily_Return'].dropna().empty:
        return _not_enough_data_fig("Not enough data for Histogram of Returns visualization.")
    fig = px.histogram(df, x='Daily_Return', nbins=50, title='Histogram of Daily Returns',
                       color_discrete_sequence=['#636EFA'])
    fig.update_layout(xaxis_title='Daily Return', yaxis_title='Count', bargap=0.05)
    return fig

def scatter_return_vs_macro_chart(df, macro_col='CPI'):
    if 'Daily_Return' not in df.columns or macro_col not in df.columns or df['Daily_Return'].dropna().empty or df[macro_col].dropna().empty:
        return _not_enough_data_fig(f"Not enough data for Daily Return vs {macro_col} visualization.")
    fig = px.scatter(df, x=macro_col, y='Daily_Return',
                     title=f'Daily Return vs. {macro_col}',
                     labels={macro_col: macro_col, 'Daily_Return': 'Daily Return'},
                     hover_data=['Date', 'Close'])
    return fig
