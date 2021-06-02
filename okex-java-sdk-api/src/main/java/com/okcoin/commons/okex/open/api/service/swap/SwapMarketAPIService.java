package com.okcoin.commons.okex.open.api.service.swap;


import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

public interface SwapMarketAPIService {

    //公共-获取合约信息
    JSONArray getContractsApi();

    //公共-获取深度数据
    JSONObject getDepthApi(String instrument_id, String depth, String size);

    //公共-获取全部ticker信息
    JSONArray getTickersApi();

    //公共-获取某个ticker信息
    JSONObject getTickerApi(String instrument_id);

    //公共-获取成交数据
    JSONArray getTradesApi(String instrument_id, String after, String before, String limit);

    //公共-获取K线数据
    JSONArray getCandlesApi(String instrument_id, String start, String end, String granularity);

    //公共-获取指数信息
    JSONObject getIndexApi(String instrument_id);

    //公共-获取法币汇率
    JSONObject getRateApi();

    //公共-获取平台总持仓量
    JSONObject getOpenInterestApi(String instrument_id);

    //公共-获取当前限价
    JSONObject getPriceLimitApi(String instrument_id);

    //公共-获取强平单
    JSONArray getLiquidationApi(String instrument_id, String status, String limit, String from, String to);

    //公共-获取合约资金费率
    JSONObject getFundingTimeApi(String instrument_id);

    //公共-获取合约标记价格
    JSONObject getMarkPriceApi(String instrument_id);

    //公共-获取合约历史资金费率
    JSONArray getHistoricalFundingRateApi(String instrument_id,String limit);

    //公共-获取历史K线数据
    JSONArray getHistoryCandlesApi(String instrument_id, String start, String end, String granularity, String limit);

}
