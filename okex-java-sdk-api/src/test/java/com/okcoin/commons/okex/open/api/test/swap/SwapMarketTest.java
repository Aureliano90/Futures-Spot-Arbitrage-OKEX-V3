package com.okcoin.commons.okex.open.api.test.swap;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.okcoin.commons.okex.open.api.bean.swap.result.*;
import com.okcoin.commons.okex.open.api.service.swap.SwapMarketAPIService;
import com.okcoin.commons.okex.open.api.service.swap.impl.SwapMarketAPIServiceImpl;
import org.junit.Before;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class SwapMarketTest extends SwapBaseTest {
    private SwapMarketAPIService swapMarketAPIService;
    private static final Logger LOG = LoggerFactory.getLogger(SwapMarketTest.class);

    @Before
    public void before() {
        config = config();
        swapMarketAPIService = new SwapMarketAPIServiceImpl(config);
    }

    /**
     * 公共-获取合约信息
     * GET /api/swap/v3/instruments
     */
    @Test
    public void getContractsApi() {
        JSONArray contractsApi = swapMarketAPIService.getContractsApi();
        this.toResultString(SwapMarketTest.LOG, "contractsApi", contractsApi);
    }

    /**
     * 公共-获取深度数据
     * GET /api/swap/v3/instruments/<instrument_id>/depth
     */
    @Test
    public void getDepthApi() {
        JSONObject depthApi = swapMarketAPIService.getDepthApi("BTC-USDT-SWAP", "1","1");
        this.toResultString(SwapMarketTest.LOG, "depthApi", depthApi);
    }

    /**
     * 公共-获取全部ticker信息
     * GET /api/swap/v3/instruments/ticker
     */
    @Test
    public void getTickersApi() {
        JSONArray tickersApi = swapMarketAPIService.getTickersApi();
        this.toResultString(SwapMarketTest.LOG, "tickersApi", tickersApi);
    }

    /**
     * 公共-获取某个ticker信息
     * GET /api/swap/v3/instruments/<instrument_id>/ticker
     */
    @Test
    public void getTickerApi() {
        JSONObject tickerApi = swapMarketAPIService.getTickerApi("BTC-USD-SWAP");
        this.toResultString(SwapMarketTest.LOG, "tickersApi", tickerApi);
    }

    /**
     * 公共-获取成交数据
     * GET /api/swap/v3/instruments/<instrument_id>/trades
     */
    @Test
    public void getTradesApi() {
        JSONArray tradesApi = swapMarketAPIService.getTradesApi("BTC-USDT-SWAP", "", "", null);
        this.toResultString(SwapMarketTest.LOG, "tickersApi", tradesApi);

    }

    /**
     * 公共-获取K线数据
     * GET /api/swap/v3/instruments/<instrument_id>/candles
     */
    @Test
    public void getCandlesApi() {


//            String start = "2021-04-05T08:00:00.000Z";
//            String end = "2021-04-06T08:30:00.000Z";
        String start = null;
        String end = null;
        JSONArray candlesApi = swapMarketAPIService.getCandlesApi("ETH-USD-SWAP", start, end, "900");
        this.toResultString(SwapMarketTest.LOG, "tickersApi", candlesApi);
    }


    /**
     * 公共-获取指数信息
     * GET /api/swap/v3/instruments/<instrument_id>/index
     */
    @Test
    public void getIndexApi() {
        JSONObject indexApi = swapMarketAPIService.getIndexApi("XRP-USDT-SWAP");
        this.toResultString(SwapMarketTest.LOG, "tickersApi", indexApi);
    }

    /**
     * 公共-获取法币汇率
     * GET /api/swap/v3/rate
     */
    @Test
    public void getRateApi() {
        JSONObject rateApi = swapMarketAPIService.getRateApi();
        this.toResultString(SwapMarketTest.LOG, "rateApi", rateApi);
    }

    /**
     * 公共-获取平台总持仓量
     * GET /api/swap/v3/instruments/<instrument_id>/open_interest
     */
    @Test
    public void getOpenInterestApi() {
        JSONObject openInterestApi = swapMarketAPIService.getOpenInterestApi("XRP-USDT-SWAP");
        this.toResultString(SwapMarketTest.LOG, "openInterestApi", openInterestApi);
    }

    /**
     * 公共-获取当前限价
     * GET /api/swap/v3/instruments/<instrument_id>/price_limit
     */
    @Test
    public void getPriceLimitApi() {
        JSONObject priceLimitApi = swapMarketAPIService.getPriceLimitApi("XRP-USDT-SWAP");
        this.toResultString(SwapMarketTest.LOG, "priceLimitApi", priceLimitApi);
    }

    /**
     * 公共-获取强平单
     * GET /api/swap/v3/instruments/<instrument_id>/liquidation
     */
    @Test
    public void getLiquidationApi() {
        JSONArray liquidationApi = swapMarketAPIService.getLiquidationApi("BTC-USD-SWAP", "1", null, null, null);
        this.toResultString(SwapMarketTest.LOG, "liquidationApi", liquidationApi);
    }

    /**
     * 公共-获取合约资金费率
     * GET /api/swap/v3/instruments/<instrument_id>/funding_time
     */
    @Test
    public void getFundingTimeApi() {
        JSONObject fundingTimeApi = swapMarketAPIService.getFundingTimeApi("BTC-USD-SWAP");
        this.toResultString(SwapMarketTest.LOG, "fundingTimeApi", fundingTimeApi);
    }

    /**
     * 公共-获取合约标记价格
     * GET /api/swap/v3/instruments/<instrument_id>/mark_price
     */
    @Test
    public void getMarkPriceApi() {
        JSONObject markPriceApi = swapMarketAPIService.getMarkPriceApi("BTC-USD-SWAP");
        this.toResultString(SwapMarketTest.LOG, "markPriceApi", markPriceApi);
    }

    /**
     * 公共-获取合约历史资金费率
     * GET /api/swap/v3/instruments/<instrument_id>/historical_funding_rate
     */
    @Test
    public void getHistoricalFundingRateApi() throws InterruptedException {
        JSONArray historicalFundingRateApi = swapMarketAPIService.getHistoricalFundingRateApi("ALGO-USD-SWAP", "2");
        this.toResultString(SwapMarketTest.LOG, "historicalFundingRateApi", historicalFundingRateApi);


    }

    /**
     * 公共-获取历史K线数据
     * GET /api/swap/v3/instruments/<instrument_id>/history/candles
     */
    @Test
    public void getHistoryCandlesApi() {
//        String start = "2021-03-08T02:31:00.000Z";
//        String end = "2021-03-08T01:55:00.000Z";
        String start = null;
        String end = null;
        JSONArray candlesApi = swapMarketAPIService.getHistoryCandlesApi("BTC-USDT-SWAP", start, end, "60",null);

//        System.out.println("数据量："+candleSize.length);
        this.toResultString(SwapMarketTest.LOG, "candlesApi", candlesApi);
    }

}
