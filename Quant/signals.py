# Strategy 1 
def stratgey1_mean_reversion(row):
    if(
    (row['Z_Score'] <= -1.90) and                                  # Strong reversion signal
    (row['RSI'] < 30) or                                         # Momentum confirmation
    (row['Close'] < row['LB'])     or                       # Below lower BB — stretched
    (row['Close'] < row['VWAP'])                           # Mispricing under fair value
    # ((row['High'] - row['Low']) < 1.2 * row['ATR'])          # Not a breakout candle
    # (row['Close'] > row['Low'] + 0.4 * (row['High'] - row['Low'])) # Bullish intraday structure
    ):
        return 1  # Buy signal
    elif (row['RSI'] > 85 and
          row['Close'] > row['UB']):
        return -1  # Sell
    else:
        return 0  # Hold

# Strategy 2
def stratgey2_momentum(row):
    if (row['RSI'] > 50 and
        row['Close'] > row['VWAP'] and
        (row['High'] - row['Low']) > (1.5 * row['ATR']) and
        row['Close'] > row['UB']):
        return 1  # Buy
    elif (row['RSI'] > 85 and
          row['Close'] > row['UB']):
        return -1  # Sell
    else:
        return 0  # Hold
