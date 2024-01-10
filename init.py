import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('./xau-data/EURUSD.csv')


# Ensure the 'Date' column is in datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Calculate short-term (fast) and long-term (slow) moving averages
df['Short_MA'] = df['Close'].rolling(window=10).mean()
df['Long_MA'] = df['Close'].rolling(window=50).mean()

# Calculate RSI
window = 14
delta = df['Close'].diff(1)
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(window=window).mean()
avg_loss = loss.rolling(window=window).mean()

rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

# Combine Strategies
df['Signal_MA'] = 0  # 0 for no signal
df['Signal_MA'][df['Short_MA'] > df['Long_MA']] = 1  # 1 for buy signal
df['Signal_MA'][df['Short_MA'] < df['Long_MA']] = -1  # -1 for sell signal

df['Signal_RSI'] = 0  # 0 for no signal
df['Signal_RSI'][rsi > 70] = -1  # -1 for sell signal (overbought)
df['Signal_RSI'][rsi < 30] = 1   # 1 for buy signal (oversold)

# Combine Signals
df['Combined_Signal'] = df['Signal_MA'] + df['Signal_RSI']

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Close'], label='XAU Price')
plt.plot(df['Date'], df['Short_MA'], label='Short MA')
plt.plot(df['Date'], df['Long_MA'], label='Long MA')

# Plot Buy and Sell signals from MA strategy
buy_signals_MA = df[df['Signal_MA'] == 1]
sell_signals_MA = df[df['Signal_MA'] == -1]
plt.scatter(buy_signals_MA['Date'], buy_signals_MA['Close'], marker='^', color='g', label='Buy Signal (MA)')
plt.scatter(sell_signals_MA['Date'], sell_signals_MA['Close'], marker='v', color='r', label='Sell Signal (MA)')

# Plot Buy and Sell signals from RSI strategy
buy_signals_RSI = df[df['Signal_RSI'] == 1]
sell_signals_RSI = df[df['Signal_RSI'] == -1]
plt.scatter(buy_signals_RSI['Date'], buy_signals_RSI['Close'], marker='o', color='b', label='Buy Signal (RSI)')
plt.scatter(sell_signals_RSI['Date'], sell_signals_RSI['Close'], marker='x', color='m', label='Sell Signal (RSI)')

# Plot Combined Signals
buy_signals_combined = df[df['Combined_Signal'] == 2]
sell_signals_combined = df[df['Combined_Signal'] == -2]
plt.scatter(buy_signals_combined['Date'], buy_signals_combined['Close'], marker='*', color='y', label='Buy Signal (Combined)')
plt.scatter(sell_signals_combined['Date'], sell_signals_combined['Close'], marker='D', color='c', label='Sell Signal (Combined)')

plt.title('Combined Trading Strategies')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()