import pandas as pd
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




def label_sd_with_signals(df, column='Distance_From_Mean'):
    mean = df[column].mean()
    std = df[column].std()

    def categorize(x):
        if x >= mean + 3 * std:
            return 'ABOVE 3 SD', 3
        elif x <= mean - 3 * std:
            return 'BELOW 3 SD', -3
        elif x >= mean + 2 * std:
            return 'ABOVE 2 SD', 2
        elif x <= mean - 2 * std:
            return 'BELOW 2 SD', -2
        elif x >= mean + 1 * std:
            return 'ABOVE 1 SD', 1
        elif x <= mean - 1 * std:
            return 'BELOW 1 SD', -1
        else:
            return 'AT MEAN', 0

    labels_levels = df[column].apply(categorize)
    df[['Label', 'SD_Level']] = pd.DataFrame(labels_levels.tolist(), index=df.index)
    return df


def label_exit_signals(df):
    df = df.copy()
    df['Exit_Price'] = None
    df['Exit_For_Entry'] = None

    for i in range(len(df)):
        entry_label = df.iloc[i]['Label']
        entry_index = df.index[i]

        if entry_label == 'BELOW 3 SD':
            df.at[entry_index, 'Exit_Price'] = df.at[entry_index, 'UB']
            df.at[entry_index, 'Exit_For_Entry'] = entry_index

        elif entry_label == 'BELOW 2 SD':
            df.at[entry_index, 'Exit_Price'] = df.at[entry_index, 'MB']
            df.at[entry_index, 'Exit_For_Entry'] = entry_index

    return df




        