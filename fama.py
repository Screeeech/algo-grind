import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm


def run_fama(ticker, months):
    ticker_df = pd.read_csv("monthly-data/" + ticker + "-m.csv", index_col="Date")
    ticker_df = ticker_df.drop(ticker_df.columns[0], axis=1)
    factors_df = pd.read_csv("month_factors.csv", index_col="Date")

    first_date = max(ticker_df.index[0], factors_df.index[0])
    last_date = min(ticker_df.index[-1], factors_df.index[-1])

    ticker_df = ticker_df[first_date:last_date]
    ticker_df = ticker_df[first_date:last_date]
    ticker_df["ER"] = np.nan

    if ticker_df.shape[0] >= 24:
        for i in range(months, ticker_df.shape[0]):
            X = factors_df[i - months:i][["Mkt-RF", "SMB", "HML"]]
            y = ticker_df[i - months:i]["roi"] - factors_df[i - months:i]["RF"]

            X = sm.add_constant(X)
            ff_model = sm.OLS(y, X, missing="drop").fit()
            intercept, b1, b2, b3 = ff_model.params

            rf = factors_df[i - months:i]['RF'].mean()
            market_premium = factors_df[i - months:i]['Mkt-RF'].mean()
            size_premium = factors_df[i - months:i]['SMB'].mean()
            value_premium = factors_df[i - months:i]['HML'].mean()

            ticker_df["ER"][i] = rf + b1 * market_premium + b2 * size_premium + b3 * value_premium

        rx = ticker_df["roi"]
        ry = ticker_df["ER"]
        rx = sm.add_constant(rx)
        rmodel = sm.OLS(ry, rx, missing="drop").fit()

        return ticker_df, rmodel.rsquared

    # intercept, b1, b2, b3 = ff_model.params


if __name__ == "__main__":
    """
    tickers = pd.read_csv("constituents.csv")
    analysis_df = pd.DataFrame(columns=["ticker", "r^2", "adj r^2"])
    analysis_df = analysis_df.set_index("ticker")

    for ticker in tickers["ticker"]:
        ticker_df = pd.read_csv("monthly-data/" + ticker + "-m.csv", index_col="Date")
        ticker_df = ticker_df.drop(ticker_df.columns[0], axis=1)
        factors_df = pd.read_csv("month_factors.csv", index_col="Date")

        first_date = max(ticker_df.index[0], factors_df.index[0])
        last_date = min(ticker_df.index[-1], factors_df.index[-1])

        ticker_df = ticker_df[first_date:last_date]
        ticker_df = ticker_df[first_date:last_date]

        if ticker_df.shape[0] >= 24:
            X = factors_df[["Mkt-RF", "SMB", "HML"]]
            y = ticker_df["roi"] - factors_df["RF"]

            X = sm.add_constant(X)
            ff_model = sm.OLS(y, X, missing="drop").fit()
            # intercept, b1, b2, b3 = ff_model.params

            analysis_df.loc[ticker] = [ff_model.rsquared, ff_model.rsquared_adj]
"""
    x = run_fama("AAPL", 12)[0]

    plt.subplot(211)
    plt.bar(x.index, x["ER"], label="ER", alpha=0.5)
    plt.bar(x.index, x["roi"], label="roi", alpha=0.5)
    plt.legend(loc="upper right")

    plt.subplot(212)
    plt.scatter(x["roi"], x["ER"])
    plt.show()