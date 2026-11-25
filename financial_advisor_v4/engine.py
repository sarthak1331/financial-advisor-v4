import numpy as np
import pandas as pd
import yfinance as yf

ASSETS = ['SPY','QQQ','BND','GLD']
WEIGHTS = {'Conservative':[25,10,50,15], 'Moderate':[40,20,25,15], 'Aggressive':[45,35,10,10]}

def plan(income, expenses, savings, goal, years, risk):
    surplus = income-expenses
    emergency = expenses*6
    investable = max(0,savings-emergency)
    monthly = max(0,surplus)
    rate = 0.06/12
    n = years*12
    projected = investable*(1+rate)**n + monthly*((1+rate)**n-1)/rate
    return {'monthly_surplus':surplus,'emergency_target':emergency,'emergency_shortfall':max(0,emergency-savings),'investable_savings':investable,'illustrative_goal_value':round(projected,2),'goal_gap':round(max(0,goal-projected),2),'assumed_annual_nominal_return':0.06,'allocation_pct':dict(zip(ASSETS,WEIGHTS[risk]))}

def market_data():
    raw = yf.download(ASSETS,period='1y',auto_adjust=True,progress=False,threads=False,timeout=10)
    if raw.empty: raise ValueError('No market data returned')
    prices=raw['Close'].reindex(columns=ASSETS).dropna()
    if len(prices)<30: raise ValueError('Insufficient market history')
    ret=prices.pct_change().dropna()
    metrics=pd.DataFrame({'Total return %':(prices.iloc[-1]/prices.iloc[0]-1)*100,'Annualized volatility %':ret.std()*np.sqrt(252)*100,'Max drawdown %':(prices/prices.cummax()-1).min()*100})
    return prices,metrics.round(2)
