package com.okcoin.commons.okex.open.api.service.swap.impl;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.okcoin.commons.okex.open.api.client.APIClient;
import com.okcoin.commons.okex.open.api.config.APIConfiguration;
import com.okcoin.commons.okex.open.api.service.swap.SwapMarketAPIService;

public class SwapMarketAPIServiceImpl implements SwapMarketAPIService {
    private APIClient client;
    private SwapMarketAPI api;

    public SwapMarketAPIServiceImpl() {
    }

    public SwapMarketAPIServiceImpl(APIConfiguration config) {
        this.client = new APIClient(config);
        this.api = client.createService(SwapMarketAPI.class);
    }

    //公共-获取合约信息
    @Override
    public JSONArray getContractsApi() {
        return client.executeSync(api.getContractsApi());
    }

    //公共-获取深度数据
    @Override
    public JSONObject getDepthApi(String instrument_id, String depth, String size) {
        return client.executeSync(api.getDepthApi(instrument_id, depth, size));
    }

    //公共-获取全部ticker信息
    @Override
    public JSONArray getTickersApi() {
        return client.executeSync(api.getTickersApi());
    }

    //公共-获取某个ticker信息
    @Override
    public JSONObject getTickerApi(String instrument_id) {
        return client.executeSync(api.getTickerApi(instrument_id));
    }

    //公共-获取成交数据
    @Override
    public JSONArray getTradesApi(String instrument_id, String after, String before, String limit) {
        return client.executeSync(api.getTradesApi(instrument_id,  after, before, limit));
    }

    //公共-获取K线数据
    @Override
    public JSONArray getCandlesApi(String instrument_id, String start, String end, String granularity) {
        return client.executeSync(api.getCandlesApi(instrument_id, start, end, granularity));
    }

    //公共-获取指数信息
    @Override
    public JSONObject getIndexApi(String instrument_id) {
        return client.executeSync(api.getIndexApi(instrument_id));
    }

    //公共-获取法币汇率
    @Override
    public JSONObject getRateApi() {
        return client.executeSync(api.getRateApi());
    }

    //公共-获取平台总持仓量
    @Override
    public JSONObject getOpenInterestApi(String instrument_id) {
        return client.executeSync(api.getOpenInterestApi(instrument_id));
    }

    //公共-获取当前限价
    @Override
    public JSONObject getPriceLimitApi(String instrument_id) {
        return client.executeSync(api.getPriceLimitApi(instrument_id));
    }

    //公共-获取强平单
    @Override
    public JSONArray getLiquidationApi(String instrument_id, String status, String limit, String from, String to) {
        return client.executeSync(api.getLiquidationApi(instrument_id, status, limit, from, to));
    }

    //公共-获取合约资金费率
    @Override
    public JSONObject getFundingTimeApi(String instrument_id) {
        return client.executeSync(api.getFundingTimeApi(instrument_id));
    }

    //公共-获取合约标记价格
    @Override
    public JSONObject getMarkPriceApi(String instrument_id) {
        return client.executeSync(api.getMarkPriceApi(instrument_id));
    }

    //公共-获取合约历史资金费率
    @Override
    public JSONArray getHistoricalFundingRateApi(String instrument_id,String limit) {
        return client.executeSync(api.getHistoricalFundingRateApi(instrument_id,limit));
    }

    //公共-获取历史K线数据
    @Override
    public JSONArray getHistoryCandlesApi(String instrument_id, String start, String end, String granularity, String limit) {
        return client.executeSync(api.getHistoryCandlesApi(instrument_id, start, end, granularity,limit));
    }


}
