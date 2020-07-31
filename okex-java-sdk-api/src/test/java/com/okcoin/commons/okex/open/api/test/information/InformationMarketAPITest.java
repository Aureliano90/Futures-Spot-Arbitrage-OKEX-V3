package com.okcoin.commons.okex.open.api.test.information;


import com.alibaba.fastjson.JSONArray;
import com.okcoin.commons.okex.open.api.service.information.InformationMarketAPIService;
import com.okcoin.commons.okex.open.api.service.information.impl.InformationMarketAPIServiceImpl;
import org.junit.Before;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class InformationMarketAPITest extends InformationAPIBaseTest{
    private static final Logger LOG = LoggerFactory.getLogger(InformationMarketAPITest.class);

    private InformationMarketAPIService marketAPIService;

    @Before
    public void before() {
        config = config();
        marketAPIService = new InformationMarketAPIServiceImpl(config);
    }

   /* 公共-多空持仓人数比*/
    @Test
    public void testGetLongShortRatio(){
        String start = "2020-07-06T00:00:00Z";
        String end = "2020-07-06T06:20:00Z";
//        String start = null;
//        String end = null;

        JSONArray result = marketAPIService.getLongShortRatio("BTC",start,end,"300");
        toResultString(LOG, "long-short-ratio", result);
    }

    /*公共-持仓总量及交易量*/
    @Test
    public void testGetVolume(){
        String start = "2020-07-06T00:00:00Z";
        String end = "2020-07-06T06:20:00Z";
//        String start = null;
//        String end = null;

        JSONArray result = marketAPIService.getVolume("BTC",start,end,"300");
        toResultString(LOG, "volume", result);
    }

    /*公共-主动买入卖出情况*/
    @Test
    public void testTaker(){
        String start = "2020-07-07T00:00:00Z";
        String end = "2020-07-07T06:20:00Z";
//        String start = null;
//        String end = null;

        JSONArray result = marketAPIService.getTaker("BTC",start,end,"300");
        toResultString(LOG, "taker", result);
    }

    /*公共-多空精英趋向指标*/
    @Test
    public void testSentiment(){
        String start = "2020-07-06T00:00:00Z";
        String end = "2020-07-06T06:20:00Z";
//        String start = null;
//        String end = null;

        JSONArray result = marketAPIService.getSentiment("BTC",start,end,"300");
        toResultString(LOG, "sentiment", result);
    }

    /*公共-多空精英平均持仓比例*/
    @Test
    public void testgetMargin(){
//        String start = "2020-07-06T00:00:00Z";
//        String end = "2020-07-06T06:20:00Z";
        String start = null;
        String end = null;

        JSONArray result = marketAPIService.getMargin("BTC",start,end,"300");
        toResultString(LOG, "margin", result);
    }

}
