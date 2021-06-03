package com.okcoin.commons.okex.open.api.test.swap;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.okcoin.commons.okex.open.api.bean.swap.param.LevelRateParam;
import com.okcoin.commons.okex.open.api.bean.swap.result.*;
import com.okcoin.commons.okex.open.api.service.swap.SwapUserAPIServive;
import com.okcoin.commons.okex.open.api.service.swap.impl.SwapUserAPIServiceImpl;
import org.junit.Before;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class SwapUserTest extends SwapBaseTest {
    private SwapUserAPIServive swapUserAPIServive;
    private static final Logger LOG = LoggerFactory.getLogger(SwapUserTest.class);

    @Before
    public void before() {
        config = config();
        swapUserAPIServive = new SwapUserAPIServiceImpl(config);
    }

    /**
     *所有合约持仓信息
     * GET /api/swap/v3/position
     */
    @Test
    public void testGetPositions(){
        JSONArray result = this.swapUserAPIServive.getPositions();
        this.toResultString(SwapUserTest.LOG, "orders", result);
    }

    /**
     *单个合约持仓信息
     * GET /api/swap/v3/<instrument_id>/position
     */
    @Test
    public void getPosition() {
        Map<String,Object> result = swapUserAPIServive.getPosition("BTC-USDT-SWAP");
        this.toResultString(SwapUserTest.LOG, "orders", result);
}

    /**
     * 所有币种合约账户信息
     * GET /api/swap/v3/accounts
     */
    @Test
    public void getAccounts() {
        Map<String,Object> result = swapUserAPIServive.getAccounts();
        this.toResultString(SwapUserTest.LOG, "orders", result);
}

    /**
     * 单个币种合约账户信息
     * GET /api/swap/v3/<instrument_id>/accounts
     */
    @Test
    public void selectAccount() {
        JSONObject result = swapUserAPIServive.selectAccount("XRP-USDT-SWAP");
        this.toResultString(SwapUserTest.LOG, "orders", result);
    }

    /**
     * 获取某个合约的用户配置
     * GET /api/swap/v3/accounts/<instrument_id>/settings
     */
    @Test
    public void selectContractSettings() {
        JSONObject result = swapUserAPIServive.selectContractSettings("BTC-USDT-SWAP");
        this.toResultString(SwapUserTest.LOG, "orders", result);
    }

    /**
     * 设定某个合约的杠杆
     * POST /api/swap/v3/accounts/<instrument_id>/leverage
     */
    @Test
    public void updateLevelRate() {
        LevelRateParam levelRateParam = new LevelRateParam();
        levelRateParam.setLeverage("5");
        levelRateParam.setSide("1");
        JSONObject result = swapUserAPIServive.updateLevelRate("BTC-USDT-SWAP", levelRateParam);
        this.toResultString(SwapUserTest.LOG, "orders", result);

    }

    /**
     * 账单流水查询
     * GET /api/swap/v3/accounts/<instrument_id>/ledger
     */
    @Test
    public void getLedger() {
        JSONArray result = swapUserAPIServive.getLedger("XRP-USDT-SWAP", null, null, null,null);
        this.toResultString(SwapUserTest.LOG, "orders", result);
    }

    /**
     * 获取所有订单列表
     * GET /api/swap/v3/orders/<instrument_id>
     */
    @Test
    public void selectOrders() {
        Map<String,Object> result = swapUserAPIServive.selectOrders("XRP-USDT-SWAP", null, null, null, "0");
        this.toResultString(SwapUserTest.LOG, "orders", result);
    }

    /**
     * 获取订单信息(通过order_id)
     * GET /api/swap/v3/orders/<instrument_id>/<order_id>
     */
    @Test
    public void selectOrderByOrderId() {
        JSONObject result = swapUserAPIServive.selectOrderByOrderId("XRP-USDT-SWAP", "771515013530292224");
        this.toResultString(SwapUserTest.LOG, "orders", result);
    }

    /**
     * 获取订单信息(通过client_oid)
     * GET /api/swap/v3/orders/<instrument_id>/<order_id>
     */
    @Test
    public void selectOrderByClientOid() {
        JSONObject result = swapUserAPIServive.selectOrderByClientOid("XRP-USDT-SWAP", "testswap052501");
        this.toResultString(SwapUserTest.LOG, "orders", result);
    }

    /**
     * 获取成交明细
     * GET /api/swap/v3/fills
     */
    @Test
    public void selectDealDetail(){
        JSONArray result = swapUserAPIServive.selectDealDetail("XRP-USDT-SWAP",null,null,null,"10");
        this.toResultString(SwapUserTest.LOG, "orders", result);

    }

    /**
     * 获取合约挂单冻结数量
     * GET /api/swap/v3/accounts/<instrument_id>/holds
     */
    @Test
    public void getHolds() {
        JSONObject result = swapUserAPIServive.getHolds("XRP-USDT-SWAP");
        this.toResultString(SwapUserTest.LOG, "orders", result);
    }

    /**
     * 获取手续费等级费率
     * GET/api/swap/v3/trade_fee
     */
    @Test
    public void TestGetTradeFee(){
        JSONObject result = swapUserAPIServive.getTradeFee("1","XRP-USDT-SWAP");
        this.toResultString(SwapUserTest.LOG, "orders", result);
    }

}
