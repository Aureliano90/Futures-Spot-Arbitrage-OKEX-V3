package com.okcoin.commons.okex.open.api.test.swap;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.okcoin.commons.okex.open.api.bean.swap.param.LevelRateParam;
import com.okcoin.commons.okex.open.api.bean.swap.result.*;
import com.okcoin.commons.okex.open.api.service.swap.SwapUserAPIServive;
import com.okcoin.commons.okex.open.api.service.swap.impl.SwapUserAPIServiceImpl;
import org.junit.Before;
import org.junit.Test;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

public class SwapUserTest extends SwapBaseTest {
    private SwapUserAPIServive swapUserAPIServive;
    private String jsonObject;

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
        String result = this.swapUserAPIServive.getPositions();
        System.out.println(result);
    }

    /**
     *单个合约持仓信息
     * GET /api/swap/v3/<instrument_id>/position
     */
    @Test
    public void getPosition() {
        String jsonObject = swapUserAPIServive.getPosition("XRP-USDT-SWAP");
        System.out.println(jsonObject);
}

    /**
     * 所有币种合约账户信息
     * GET /api/swap/v3/accounts
     */
    @Test
    public void getAccounts() {
        String jsonObject = swapUserAPIServive.getAccounts();
        System.out.println(jsonObject);
}

    /**
     * 单个币种合约账户信息
     * GET /api/swap/v3/<instrument_id>/accounts
     */
    @Test
    public void selectAccount() {
        String jsonObject = swapUserAPIServive.selectAccount("XRP-USDT-SWAP");
        System.out.println(jsonObject);

    }

    /**
     * 获取某个合约的用户配置
     * GET /api/swap/v3/accounts/<instrument_id>/settings
     */
    @Test
    public void selectContractSettings() {
        String jsonObject = swapUserAPIServive.selectContractSettings("BTC-USDT-SWAP");
        System.out.println(jsonObject);
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
        String jsonObject = swapUserAPIServive.updateLevelRate("BTC-USDT-SWAP", levelRateParam);
        System.out.println(jsonObject);

    }

    /**
     * 账单流水查询
     * GET /api/swap/v3/accounts/<instrument_id>/ledger
     */
    @Test
    public void getLedger() {
        String jsonArray = swapUserAPIServive.getLedger("XRP-USDT-SWAP", null, null, null,null);
        System.out.println(jsonArray);
    }



    /**
     * 获取所有订单列表
     * GET /api/swap/v3/orders/<instrument_id>
     */
    @Test
    public void selectOrders() {
        String jsonObject = swapUserAPIServive.selectOrders("XRP-USDT-SWAP", null, null, null, "0");
        System.out.println(jsonObject);
    }

    /**
     * 获取订单信息(通过order_id)
     * GET /api/swap/v3/orders/<instrument_id>/<order_id>
     */
    @Test
    public void selectOrderByOrderId() {
        String jsonObject = swapUserAPIServive.selectOrderByOrderId("XRP-USDT-SWAP", "771515013530292224");
        System.out.println(jsonObject);
    }

    /**
     * 获取订单信息(通过client_oid)
     * GET /api/swap/v3/orders/<instrument_id>/<order_id>
     */
    @Test
    public void selectOrderByClientOid() {
        String jsonObject = swapUserAPIServive.selectOrderByClientOid("XRP-USDT-SWAP", "testswap052501");
        System.out.println("success");
        System.out.println(jsonObject);
    }

    /**
     * 获取成交明细
     * GET /api/swap/v3/fills
     */
    @Test
    public void selectDealDetail(){
        String jsonArray = swapUserAPIServive.selectDealDetail("XRP-USDT-SWAP",null,null,null,"10");
        System.out.println(jsonArray);

    }

    /**
     * 获取合约挂单冻结数量
     * GET /api/swap/v3/accounts/<instrument_id>/holds
     */
    @Test
    public void getHolds() {
        String jsonObject = swapUserAPIServive.getHolds("XRP-USDT-SWAP");
        System.out.println(jsonObject);
    }

    /**
     * 获取手续费等级费率
     * GET/api/swap/v3/trade_fee
     */
    @Test
    public void TestGetTradeFee(){
        String result = swapUserAPIServive.getTradeFee("1","XRP-USDT-SWAP");
        System.out.println(result);
    }

}
