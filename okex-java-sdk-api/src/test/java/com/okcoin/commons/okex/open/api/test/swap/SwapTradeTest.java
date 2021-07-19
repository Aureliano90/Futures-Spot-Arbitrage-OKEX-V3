package com.okcoin.commons.okex.open.api.test.swap;

import com.alibaba.fastjson.JSONObject;
import com.okcoin.commons.okex.open.api.bean.futures.param.CancelAll;
import com.okcoin.commons.okex.open.api.bean.swap.param.*;
import com.okcoin.commons.okex.open.api.bean.swap.result.ApiCancelOrderVO;
import com.okcoin.commons.okex.open.api.bean.swap.result.ApiOrderResultVO;
import com.okcoin.commons.okex.open.api.bean.swap.result.ApiOrderVO;
import com.okcoin.commons.okex.open.api.bean.swap.result.OrderCancelResult;
import com.okcoin.commons.okex.open.api.service.swap.SwapTradeAPIService;
import com.okcoin.commons.okex.open.api.service.swap.impl.SwapTradeAPIServiceImpl;
import com.okcoin.commons.okex.open.api.test.spot.SpotOrderAPITest;
import org.junit.Before;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

public class SwapTradeTest extends SwapBaseTest {

    private SwapTradeAPIService tradeAPIService;
    private static final Logger LOG = LoggerFactory.getLogger(SwapTradeTest.class);


    @Before
    public void before() {
        config = config();
        tradeAPIService = new SwapTradeAPIServiceImpl(config);
    }

    /**
     * 下单
     * POST /api/swap/v3/order
     */
    @Test
    public void order() {
        PpOrder ppOrder = new PpOrder("0602testswap07", "1", "1", "0","0.5", "XRP-USDT-SWAP","0");
        final  Object apiOrderVO = tradeAPIService.order(ppOrder);
        this.toResultString(SwapTradeTest.LOG, "orders", apiOrderVO);

    }

    /**
     * 批量下单
     * POST /api/swap/v3/orders
     */
    @Test
    public void batchOrder() {

        List<PpBatchOrder> list = new LinkedList<>();
        list.add(new PpBatchOrder("testswap06027", "1", "1", "0", "0.5","0"));
        list.add(new PpBatchOrder("testswap06028", "1", "1", "0", "0.4","0"));

        PpOrders ppOrders = new PpOrders();
        ppOrders.setInstrument_id("XRP-USDT-SWAP");
        ppOrders.setOrder_data(list);
        Map<String, Object> jsonObject = tradeAPIService.orders(ppOrders);
        this.toResultString(SwapTradeTest.LOG, "orders", jsonObject);

    }

    /**
     * 撤单
     * POST /api/swap/v3/cancel_order/<instrument_id>/<order_id>
     */
    @Test
    public void cancelOrderByOrderId() {
        JSONObject jsonObject = tradeAPIService.cancelOrderByOrderId("XRP-USDT-SWAP", "777291060863471617");
        this.toResultString(SwapTradeTest.LOG, "cancelOrders", jsonObject);
    }

    /**
     * 撤单
     * POST /api/swap/v3/cancel_order/<instrument_id>/<client_oid>
     */
    @Test
    public void cancelOrderByClientOid() {
        JSONObject jsonObject = tradeAPIService.cancelOrderByClientOid("XRP-USDT-SWAP", "testswap06023");
        this.toResultString(SwapTradeTest.LOG, "cancelOrders", jsonObject);
    }

    /**
     * 批量撤单
     * POST /api/swap/v3/cancel_batch_orders/<instrument_id>
     */
    @Test
    public void batchCancelOrderByOrderId() {
        //生成一个PpCancelOrderVO对象
        PpCancelOrderVO ppCancelOrderVO = new PpCancelOrderVO();

        ppCancelOrderVO.getIds().add("777295696223703040");
        ppCancelOrderVO.getIds().add("777295696232091648");

        Map<String, Object> jsonObject = tradeAPIService.cancelOrdersByOrderIds("XRP-USDT-SWAP", ppCancelOrderVO);
        this.toResultString(SwapTradeTest.LOG, "cancelOrders", jsonObject);
    }

    /**
     * 批量撤单
     * POST /api/swap/v3/cancel_batch_orders/<instrument_id>
     */
    @Test
    public void batchCancelOrderByClientOid() {
        PpCancelOrderVO ppCancelOrderVO = new PpCancelOrderVO();
        List<String> oidlist = new ArrayList<String>();

        oidlist.add("testswap06027");
        oidlist.add("testswap06028");
        ppCancelOrderVO.setClientOids(oidlist);

        Map<String, Object> jsonObject = tradeAPIService.cancelOrdersByClientOids("XRP-USDT-SWAP", ppCancelOrderVO);
        this.toResultString(SwapTradeTest.LOG, "cancelOrders", jsonObject);

    }

    /**
     * 修改订单(通过order_id)
     * POST /api/swap/v3/amend_order/<instrument_id>
     */
    @Test
    public void testAmendOrderByOrderId(){
        AmendOrder amendOrder = new AmendOrder();
        amendOrder.setCancel_on_fail("0");
        amendOrder.setOrder_id("777297331087904769");
        amendOrder.setRequest_id(null);
        amendOrder.setNew_price("2.2");
        amendOrder.setNew_size("1");

        JSONObject result = tradeAPIService.amendOrderByOrderId("XRP-USDT-SWAP",amendOrder);
        this.toResultString(SwapTradeTest.LOG, "amendOrder", result);


    }

    /**
     * 修改订单(通过client_oid)
     * POST /api/swap/v3/amend_order/<instrument_id>
     */
    @Test
    public void testAmentOrderByClientOid(){
        AmendOrder amendOrder = new AmendOrder();
        amendOrder.setCancel_on_fail("0");
        amendOrder.setClient_oid("0602testswap06");
        amendOrder.setRequest_id(null);
        amendOrder.setNew_price("1.9");
        amendOrder.setNew_size("1");

        JSONObject result = tradeAPIService.amendOrderByClientOid("XRP-USDT-SWAP",amendOrder);
        this.toResultString(SwapTradeTest.LOG, "amendOrder", result);

    }

    /**
     * 批量修改订单(通过order_id)
     * POST /api/swap/v3/amend_batch_orders/<instrument_id>
     */
    @Test
    public void testAmentBatchOrderByOrderId(){
        AmendOrderParam amendOrderParam = new AmendOrderParam();
        List<AmendOrder> list = new ArrayList<>();

        AmendOrder amendOrder = new AmendOrder();
        amendOrder.setCancel_on_fail("0");
        amendOrder.setOrder_id("777297331087904769");
        amendOrder.setRequest_id(null);
        amendOrder.setNew_price("2.3");
        amendOrder.setNew_size("1");

        AmendOrder amendOrder1 = new AmendOrder();
        amendOrder1.setCancel_on_fail("0");
        amendOrder1.setOrder_id("777301594337873921");
        amendOrder1.setRequest_id(null);
        amendOrder1.setNew_price("0.7");
        amendOrder1.setNew_size("1");

        list.add(amendOrder);
        list.add(amendOrder1);
        amendOrderParam.setAmend_data(list);

        Map<String, Object> result = tradeAPIService.amendBatchOrderByOrderId("XRP-USDT-SWAP",amendOrderParam);
        this.toResultString(SwapTradeTest.LOG, "amendOrder", result);

    }

    /**
     * 批量修改订单(通过client_oid)
     * POST /api/swap/v3/amend_batch_orders/<instrument_id>
     */
    @Test
    public void testAmentBatchOrderByClientOid(){
        AmendOrderParam amendOrderParam = new AmendOrderParam();
        List<AmendOrder> list = new ArrayList<>();

        AmendOrder amendOrder = new AmendOrder();
        amendOrder.setCancel_on_fail("0");
        amendOrder.setClient_oid("0602testswap06");
        amendOrder.setRequest_id(null);
        amendOrder.setNew_price("4");
        amendOrder.setNew_size("1");

        AmendOrder amendOrder1 = new AmendOrder();
        amendOrder1.setCancel_on_fail("0");
        amendOrder1.setClient_oid("0602testswap07");
        amendOrder1.setRequest_id(null);
        amendOrder1.setNew_price("0.45");
        amendOrder1.setNew_size("1");


        list.add(amendOrder);
        list.add(amendOrder1);

        amendOrderParam.setAmend_data(list);

        Map<String, Object> result = tradeAPIService.amendBatchOrderByClientOid("XRP-USDT-SWAP",amendOrderParam);
        this.toResultString(SwapTradeTest.LOG, "amendOrder", result);
    }

    /**
     * 委托策略下单
     * POST /api/swap/v3/order_algo
     */
    @Test
    public void testSwapOrderAlgo(){
        SwapOrderParam swapOrderParam=new SwapOrderParam();
        //公共参数
        swapOrderParam.setInstrument_id("XRP-USDT-SWAP");
        swapOrderParam.setType("3");
        swapOrderParam.setOrder_type("1");
        swapOrderParam.setSize("1");

//        //计划委托
        swapOrderParam.setTrigger_price("2");
        swapOrderParam.setAlgo_price("2.1");
        swapOrderParam.setAlgo_type("1");

        //跟踪委托
       /* swapOrderParam.setCallback_rate("");
        swapOrderParam.setTrigger_price("");*/

        //冰山委托
        /*swapOrderParam.setAlgo_variance("0.0015");
        swapOrderParam.setAvg_amount("1");
        swapOrderParam.setPrice_limit("0.2009");*/

        //时间加权
        /*swapOrderParam.setSweep_range("");
        swapOrderParam.setSweep_ratio("");
        swapOrderParam.setSingle_limit("");
        swapOrderParam.setPrice_limit("");
        swapOrderParam.setTime_interval("");*/

        //止盈止损
//        swapOrderParam.setTp_trigger_price("23100");
//        swapOrderParam.setTp_price("0.255");
//        swapOrderParam.setTp_trigger_type("2");
//        swapOrderParam.setSl_trigger_price("26500");
//        swapOrderParam.setSl_price("11750.3");
//        swapOrderParam.setSl_trigger_type("2");

        JSONObject jsonObject = tradeAPIService.swapOrderAlgo(swapOrderParam);
        this.toResultString(SwapTradeTest.LOG, "algoOrder", jsonObject);

    }

    /**
     * 委托策略撤单
     * POST /api/swap/v3/cancel_algos
     */
    @Test
    public void testCancelOrderAlgo(){
        CancelOrderAlgo cancelOrderAlgo=new CancelOrderAlgo();
        List<String>  list = new ArrayList<>();
        list.add("777305120682184704");

        cancelOrderAlgo.setAlgo_ids(list);
        cancelOrderAlgo.setInstrument_id("XRP-USDT-SWAP");
        cancelOrderAlgo.setOrder_type("1");

        JSONObject jsonObject = tradeAPIService.cancelOrderAlgo(cancelOrderAlgo);
        this.toResultString(SwapTradeTest.LOG, "algoOrder", jsonObject);

    }

    /**
     * 获取委托单列表
     * GET /api/swap/v3/order_algo/<instrument_id>
     */

    @Test
    public void testGetSwapAlgOrders(){
        Map<String,Object> jsonObject = tradeAPIService.getSwapOrders("XRP-USDT-SWAP", "1", "3",null,null,null,"10");
        this.toResultString(SwapTradeTest.LOG, "algoOrders", jsonObject);
    }

    /**
     * 市价全平
     * POST/api/swap/v3/close_position
     */
    @Test
    public void testClosePosition(){
        ClosePosition closePosition = new ClosePosition();
        closePosition.setInstrument_id("XRP-USDT-SWAP");
        closePosition.setDirection("long");
        JSONObject result = tradeAPIService.closePosition(closePosition);
        this.toResultString(SwapTradeTest.LOG, "closePosition", result);

    }

    /**
     * 撤销所有平仓挂单
     * POST /api/swap/v3/cancel_all
     */
    @Test
    public void testCancelAll(){
        CancelAllParam cancelAllParam = new CancelAllParam();
        cancelAllParam.setInstrument_id("XRP-USDT-SWAP");
        cancelAllParam.setDirection("long");
        JSONObject result = tradeAPIService.CancelAll(cancelAllParam);
        this.toResultString(SwapTradeTest.LOG, "cancelAllParam", result);
    }

}
