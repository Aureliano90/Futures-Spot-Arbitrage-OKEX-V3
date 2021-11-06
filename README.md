# Futures-Spot-Arbitrage-OKEx-V3
## Introduction
An object-oriented program for arbitrage between perpetual futures and spot on OKEx using V3 API. However OKEx V3 API 
keys may not be available anymore. Written in April for my personal use. Inherited and modified OKEx V3 API SDK. 
Functional and stable enough for me. Then the market crashed in May and the funding rates were not appealing anymore.
The development was halted ever since.

Printouts and annotations are in Chinese. May or may not translate to English.

## Features
* Sort and output historical funding rates over given period
* Analyze historical funding rates and volatility (taken as [NATR](https://www.macroption.com/normalized-atr/)) to find most profitable underlyings for arbitrage
* Monitor existing positions and adjust leverage accordingly, i.e. increase leverage when price drops and deleverage when price rises to avoid liquidation
* Store tickers, funding rates, operations and transactions in MongoDB
* Open a position by longing spot and shorting perpetual futures equally and simultaneously
  * Use historical tickers and statistics to open position when futures have max premium, on the basis that the premium over a period of time satisfies Gaussian distribution
  * Accelerate when a desired premium does not appear by given time
* Close a position by selling spot and buying to close perpetual futures
  * Use historical tickers and statistics to close position when futures have max discount
  * Accelerate when a desired discount does not appear by given time
  * Automatically close a position when the predicted funding rate is low enough such that it is better off to reopen later
* Calculate PnL, APR and APY

## Features nice to add
* Typical arbitrage of perpetual futures and spot is passively receiving funding fees while keeping the portfolio open. 
  However it is profitable to proactively close a portion of the portfolio when the futures premium surges and reopen later 
  when it subdues.
* If the program is interrupted when opening or closing positions, it will not resume. Could be improved.
* The current program uses REST API to fetch tickers which has significant delays. WebSocket API should give more 
  responsive tickers.

## Background
Futures spot arbitrage in crypto is profitable because there is a huge demand for long leverage in the crypto market.
Arbitrageurs act as the counterparty to buyers in the perpetual swap market. They effectively multiply and 
transfer the buying pressure in the perpetual swap market to the spot market. Leverage comes at a cost. Therefore 
arbitrageurs or market makers are entitled to charge interest on futures buyers, just like stock brokers charge interest 
for margin. As a result the APY depends on the market sentiment, ranging from 10% to 100%+.

## Reference
[1] [OKEx V3 API guide](https://www.okex.com/docs/en)

[2] [Cryptocurrency Spot-Futures Arbitrage Strategy Report](https://www.okex.com/academy/en/spot-futures-arbitrage-strategy-report-2)

[3] [Alternative Opportunities In Crypto Space: Spot-Futures Arbitrage](https://seekingalpha.com/article/4410256-alternative-opportunities-in-crypto-spot-futures-arbitrage)
