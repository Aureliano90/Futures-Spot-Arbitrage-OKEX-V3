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
     * API交易提供限价单下单模式，只有当您的账户有足够的资金才能下单。
     * 一旦下单，您的账户资金将在订单生命周期内被冻结，被冻结的资金以及数量取决于订单指定的类型和参数。目前api下单只支持以美元为计价单位
     * POST /api/swap/v3/order
     * 限速规则：40次/2s
     * {"match_price":"0","size":"1","price":"55","client_oid":"2016TestOrder2","type":"2","instrument_id":"LTC-USD-SWAP","order_type":"0"}
     */
    @Test
    public void order() {
        PpOrder ppOrder = new PpOrder("testswap1", "1", "1", "0","0.17", "XRP-USDT-SWAP","0");
        final  Object apiOrderVO = tradeAPIService.order(ppOrder);
        this.toResultString(SwapTradeTest.LOG, "orders", apiOrderVO);
        System.out.println("jsonObject:"+apiOrderVO);

    }


    /**
     * 批量下单
     * 批量进行下单请求，每个合约可批量下10个单。
     * POST /api/swap/v3/orders
     * 限速规则：20次/2s
     */
    @Test
    public void batchOrder() {

        List<PpBatchOrder> list = new LinkedList<>();
        list.add(new PpBatchOrder("0422testswap3", "1", "1", "0", "0.17","0"));
        list.add(new PpBatchOrder("0422testswap4", "1", "1", "0", "0.165","0"));

        PpOrders ppOrders = new PpOrders();
        ppOrders.setInstrument_id("XRP-USDT-SWAP");
        ppOrders.setOrder_data(list);
        String jsonObject = tradeAPIService.orders(ppOrders);
        //ApiOrderResultVO apiOrderResultVO = JSONObject.parseObject(jsonObject, ApiOrderResultVO.class);
        System.out.println("success");
        System.out.println(jsonObject);


    }

    /**
     * 撤单
     * 撤销之前下的未完成订单。
     * POST /api/swap/v3/cancel_order/<instrument_id>/<order_id> or <client_oid>
     * 限速规则：40次/2s
     */
    @Test
    public void cancelOrderByOrderId() {
        String jsonObject = tradeAPIService.cancelOrderByOrderId("XRP-USDT-SWAP", "483146185764421632");
        ApiCancelOrderVO apiCancelOrderVO = JSONObject.parseObject(jsonObject, ApiCancelOrderVO.class);
        System.out.println("success");
        System.out.println(apiCancelOrderVO.getOrder_id());
    }

    @Test
    public void cancelOrderByClientOid() {
        String jsonObject = tradeAPIService.cancelOrderByClientOid("XRP-USDT-SWAP", "testswap2");
        ApiCancelOrderVO apiCancelOrderVO = JSONObject.parseObject(jsonObject, ApiCancelOrderVO.class);
        System.out.println("success");
        System.out.println(apiCancelOrderVO.getOrder_id());
    }

    /**
     * 批量撤单
     * 撤销之前下的未完成订单，每个币对可批量撤10个单。
     * POST /api/swap/v3/cancel_batch_orders/<instrument_id>
     * 限速规则：20次/2s
     */
    @Test
    public void batchCancelOrderByOrderId() {
        //生成一个PpCancelOrderVO对象
        PpCancelOrderVO ppCancelOrderVO = new PpCancelOrderVO();

        ppCancelOrderVO.getIds().add("483148167046414336");
        ppCancelOrderVO.getIds().add("483148167054802944");

        System.out.println(JSONObject.toJSONString(ppCancelOrderVO));
        String jsonObject = tradeAPIService.cancelOrders("XRP-USDT-SWAP", ppCancelOrderVO);
        OrderCancelResult orderCancelResult = JSONObject.parseObject(jsonObject, OrderCancelResult.class);
        System.out.println("success");
        System.out.println(orderCancelResult.getInstrument_id());
    }
    @Test
    public void batchCancelOrderByClientOid() {
        PpCancelOrderVO ppCancelOrderVO = new PpCancelOrderVO();
        List<String> oidlist = new ArrayList<String>();

        oidlist.add("0422testswap3");
        oidlist.add("0422testswap4");
        ppCancelOrderVO.setClientOids(oidlist);

        System.out.println(JSONObject.toJSONString(ppCancelOrderVO));
        String jsonObject = tradeAPIService.cancelOrders("XRP-USDT-SWAP", ppCancelOrderVO);
        OrderCancelResult orderCancelResult = JSONObject.parseObject(jsonObject, OrderCancelResult.class);
        System.out.println("success");
        System.out.println(orderCancelResult.getInstrument_id());
    }

    /**
     * 委托策略下单
     * 提供止盈止损、跟踪委托、冰山委托和时间加权委托策略
     * POST /api/swap/v3/order_algo
     * 限速规则：40次/2s
     */
    @Test
    public void testSwapOrderAlgo(){
        SwapOrderParam swapOrderParam=new SwapOrderParam();
        //公共参数
        swapOrderParam.setInstrument_id("XRP-USDT-SWAP");
        swapOrderParam.setType("1");
        swapOrderParam.setOrder_type("1");
        swapOrderParam.setSize("1");
        //止盈止损
        swapOrderParam.setTrigger_price("0.17");
        swapOrderParam.setAlgo_price("0.165");
        swapOrderParam.setAlgo_type("");
        //跟踪委托
       /* swapOrderParam.setCallback_rate("");
        swapOrderParam.setTrigger_price("");*/

        //冰山委托
        /*swapOrderParam.setAlgo_variance("");
        swapOrderParam.setAvg_amount("");
        swapOrderParam.setPrice_limit("");*/

        //时间加权
        /*swapOrderParam.setSweep_range("");
        swapOrderParam.setSweep_ratio("");
        swapOrderParam.setSingle_limit("");
        swapOrderParam.setPrice_limit("");
        swapOrderParam.setTime_interval("");*/

        String jsonObject = tradeAPIService.swapOrderAlgo(swapOrderParam);
        System.out.println("---------success--------");
        System.out.println(jsonObject);
    }

    /**
     * 委托策略撤单
     * 根据指定的algo_id撤销某个合约的未完成订单，每次最多可撤6（冰山/时间）/10（计划/跟踪）个。
     * POST /api/swap/v3/cancel_algos
     * 限速规则：20 次/2s
     */
    @Test
    public void testCancelOrderAlgo(){
        CancelOrderAlgo cancelOrderAlgo=new CancelOrderAlgo();
        List<String>  list = new ArrayList<>();
        list.add("482967665054498816");
       // list.add("");

        cancelOrderAlgo.setAlgo_ids(list);
        cancelOrderAlgo.setInstrument_id("XRP-USDT-SWAP");
        cancelOrderAlgo.setOrder_type("1");

        String jsonObject = tradeAPIService.cancelOrderAlgo(cancelOrderAlgo);
        System.out.println("---------success--------");
        System.out.println(jsonObject);
    }

    /**
     * 获取委托单列表
     * 列出您当前所有的订单信息。
     * GET /api/swap/v3/order_algo/<instrument_id>
     * 限速规则：20次/2s
     */
    @Test
    public void testGetSwapAlgOrders(){
        System.out.println("begin to show the swapAlgpOrders");
        String jsonObject = tradeAPIService.getSwapOrders("XRP-USDT-SWAP",
                                                            "1",
                                                            "","482967665054498816","","","");
        System.out.println(jsonObject);
    }

    /**
     * 市价全平
     * 市价全平接口，其中BTC合约持仓小于或等于999张时才能调用，否则报错；类似的，其他币种合约的持仓应该小于或等于9999张
     * POST/api/swap/v3/close_position
     * 限速规则：2次/2s
     */
    @Test
    public void testClosePosition(){
        ClosePosition closePosition = new ClosePosition();
        closePosition.setInstrument_id("XRP-USDT-SWAP");
        closePosition.setDirection("short");
        String result = tradeAPIService.closePosition(closePosition);
        System.out.println(result);

    }

    /**
     * 撤销所有平仓挂单
     * 此接口，仅支持撤销平仓的所有挂单。不包括开仓的挂单。
     * POST /api/swap/v3/cancel_all
     * 限速规则：5次/2s （根据underlying，分别限速）
     */
    @Test
    public void testCancelAll(){
        CancelAllParam cancelAllParam = new CancelAllParam();
        cancelAllParam.setInstrument_id("XRP-USDT-SWAP");
        cancelAllParam.setDirection("short");
        String result = tradeAPIService.CancelAll(cancelAllParam);
        System.out.println(result);

    }



}
