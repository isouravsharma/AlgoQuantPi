from getData import get_data
from technical_indicator import calculate_LR, calculate_rsi
from Returns import cummulative_returns

data=get_data('RELIANCE.NS', '2022-01-01')

print(data)
type(data)

calculate_LR(data)
calculate_rsi(data)


cummulative_returns(data)
#data['pct']= data['Close'].pct_change()