import pickle

import yfinance as yf
import pandas as pd
import os
if os.path.exists("sp500_AAPL.csv"):
    sp500 = pd.read_csv("sp500.csv", index_col=0)
else:
    sp500 = yf.Ticker("AAPL")
    sp500 = sp500.history(period="max")
    sp500.to_csv("sp500_AAPL.csv")

sp500.index = pd.to_datetime(sp500.index)
print(sp500)
sp500.plot.line(y="Close", use_index=True)
del sp500["Dividends"]
del sp500["Stock Splits"]
sp500["Tomorrow"] = sp500["Close"].shift(-1)
sp500["Target"] = (sp500["Tomorrow"] > sp500["Close"]).astype(int)
sp500 = sp500[150:].copy()
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, min_samples_split=100, random_state=1)

train = sp500.iloc[:-100]
test = sp500.iloc[-100:]

predictors = ["Close", "Volume", "Open", "High", "Low"]
model.fit(train[predictors], train["Target"])
from sklearn.metrics import precision_score
print(type(test[predictors]))
filename = 'paper_trading/prediction/models/AAPL.sav'
pickle.dump(model, open(filename, 'wb'))

loaded_model = pickle.load(open(filename, 'rb'))
preds = loaded_model.predict(test[predictors])
preds = pd.Series(preds, index=test.index)
print(precision_score(test["Target"], preds))
combined = pd.concat([test["Target"], preds], axis=1)
combined.plot()
data = [[3951.570068359375, 5347140000,3917.469970703125,3956.6201171875,3916.889892578125]]
df = pd.DataFrame(data, columns=predictors)

# predict
print(loaded_model.predict(df))
# 2023-03-20 00:00:00-04:00,3917.469970703125,3956.6201171875,3916.889892578125,3951.570068359375,5347140000,0.0,0.0
# Date,Open,High,Low,Close,Volume,Dividends,Stock Splits

# def predict(train, test, predictors, model):
#     model.fit(train[predictors], train["Target"])
#     preds = model.predict(test[predictors])
#     preds = pd.Series(preds, index=test.index, name="Predictions")
#     combined = pd.concat([test["Target"], preds], axis=1)
#     return combined
#
#
# def backtest(data, model, predictors, start=2500, step=250):
#     all_predictions = []
#
#     for i in range(start, data.shape[0], step):
#         train = data.iloc[0:i].copy()
#         test = data.iloc[i:(i + step)].copy()
#         predictions = predict(train, test, predictors, model)
#         all_predictions.append(predictions)
#
#     return pd.concat(all_predictions)
#
#
# predictions = backtest(sp500, model, predictors)
# predictions["Predictions"].value_counts()
#
# precision_score(predictions["Target"], predictions["Predictions"])
# predictions["Target"].value_counts() / predictions.shape[0]
# horizons = [2, 5, 60, 250, 1000]
# new_predictors = []
#
# for horizon in horizons:
#     rolling_averages = sp500.rolling(horizon).mean()
#
#     ratio_column = f"Close_Ratio_{horizon}"
#     sp500[ratio_column] = sp500["Close"] / rolling_averages["Close"]
#
#     trend_column = f"Trend_{horizon}"
#     sp500[trend_column] = sp500.shift(1).rolling(horizon).sum()["Target"]
#
#     new_predictors += [ratio_column, trend_column]
#
# sp500 = sp500.dropna(subset=sp500.columns[sp500.columns != "Tomorrow"])
# model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)
# def predict(train, test, predictors, model):
#     model.fit(train[predictors], train["Target"])
#     preds = model.predict_proba(test[predictors])[:,1]
#     preds[preds >=.6] = 1
#     preds[preds <.6] = 0
#     preds = pd.Series(preds, index=test.index, name="Predictions")
#     combined = pd.concat([test["Target"], preds], axis=1)
#     return combined
# predictions = backtest(sp500, model, new_predictors)
