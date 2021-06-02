package com.okcoin.commons.okex.open.api.service.swap.impl;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface SwapMarketAPI {

    //公共-获取合约信息
    @GET("/api/swap/v3/instruments")
    Call<JSONArray> getContractsApi();

    //公共-获取深度数据
    @GET("/api/swap/v3/instruments/{instrument_id}/depth")
    Call<JSONObject> getDepthApi(@Path("instrument_id") String instrument_id, @Query("depth")  String depth, @Query("size") String size);

    //公共-获取全部ticker信息
    @GET("/api/swap/v3/instruments/ticker")
    Call<JSONArray> getTickersApi();

    //公共-获取某个ticker信息
    @GET("/api/swap/v3/instruments/{instrument_id}/ticker")
    Call<JSONObject> getTickerApi(@Path("instrument_id") String instrument_id);

    //公共-获取成交数据
    @GET("/api/swap/v3/instruments/{instrument_id}/trades")
    Call<JSONArray> getTradesApi(@Path("instrument_id") String instrument_id, @Query("after") String after, @Query("before") String before,  @Query("limit") String limit);

    //公共-获取K线数据
    @GET("/api/swap/v3/instruments/{instrument_id}/candles")
    Call<JSONArray> getCandlesApi(@Path("instrument_id") String instrument_id, @Query("start") String start, @Query("end") String end, @Query("granularity") String granularity);

    //公共-获取指数信息
    @GET("/api/swap/v3/instruments/{instrument_id}/index")
    Call<JSONObject> getIndexApi(@Path("instrument_id") String instrument_id);

    //公共-获取法币汇率
    @GET("/api/swap/v3/rate")
    Call<JSONObject> getRateApi();

    //公共-获取平台总持仓量
    @GET("/api/swap/v3/instruments/{instrument_id}/open_interest")
    Call<JSONObject> getOpenInterestApi(@Path("instrument_id") String instrument_id);

    //公共-获取当前限价
    @GET("/api/swap/v3/instruments/{instrument_id}/price_limit")
    Call<JSONObject> getPriceLimitApi(@Path("instrument_id") String instrument_id);

    //公共-获取强平单
    @GET("/api/swap/v3/instruments/{instrument_id}/liquidation")
    Call<JSONArray> getLiquidationApi(@Path("instrument_id") String instrument_id, @Query("status") String status,  @Query("limit") String limit, @Query("from") String from, @Query("to") String to);

    //公共-获取合约资金费率
    @GET("/api/swap/v3/instruments/{instrument_id}/funding_time")
    Call<JSONObject> getFundingTimeApi(@Path("instrument_id") String instrument_id);

    //公共-获取合约标记价格
    @GET("/api/swap/v3/instruments/{instrument_id}/mark_price")
    Call<JSONObject> getMarkPriceApi(@Path("instrument_id") String instrument_id);

    //公共-获取合约历史资金费率
    @GET("/api/swap/v3/instruments/{instrument_id}/historical_funding_rate")
    Call<JSONArray> getHistoricalFundingRateApi(@Path("instrument_id") String instrument_id, @Query("limit") String limit);

    //公共-获取历史K线数据
    @GET("/api/swap/v3/instruments/{instrument_id}/history/candles")
    Call<JSONArray> getHistoryCandlesApi(@Path("instrument_id") String instrument_id, @Query("start") String start, @Query("end") String end, @Query("granularity") String granularity, @Query("limit") String limit);

}
