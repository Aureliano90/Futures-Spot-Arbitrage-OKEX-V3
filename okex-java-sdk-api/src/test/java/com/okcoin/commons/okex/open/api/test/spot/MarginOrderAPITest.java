package com.okcoin.commons.okex.open.api.test.spot;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.okcoin.commons.okex.open.api.bean.spot.param.MarginAmendOrder;
import com.okcoin.commons.okex.open.api.bean.spot.param.OrderParamDto;
import com.okcoin.commons.okex.open.api.bean.spot.param.PlaceOrderParam;
import com.okcoin.commons.okex.open.api.bean.spot.result.*;
import com.okcoin.commons.okex.open.api.service.spot.MarginOrderAPIService;
import com.okcoin.commons.okex.open.api.service.spot.impl.MarginOrderAPIServiceImpl;
import org.junit.Before;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class MarginOrderAPITest extends SpotAPIBaseTests {

    private static final Logger LOG = LoggerFactory.getLogger(MarginOrderAPITest.class);
    private MarginOrderAPIService marginOrderAPIService;

    @Before
    public void before() {
        this.config = this.config();
        this.marginOrderAPIService = new MarginOrderAPIServiceImpl(this.config);
    }

    /**
     * 下单
     * POST /api/margin/v3/orders
     */
    @Test
    public void addOrder() {
        final PlaceOrderParam order = new PlaceOrderParam();

        //公共参数
        order.setClient_oid("testmargin5281");
        order.setType("limit");
        order.setSide("buy");
        order.setInstrument_id("XRP-USDT");
        order.setOrder_type("0");
        order.setMargin_trading("2");

        //限价单特殊参数
        order.setPrice("0.4");
        order.setSize("1");

        //市价单特殊参数(买入必填notional<买入金额> 卖出必填size<卖出数量>)
        /*order.setNotional("1");
        order.setSize("1");*/

        final OrderResult orderResult = this.marginOrderAPIService.addOrder(order);
        this.toResultString(MarginOrderAPITest.LOG, "orders", orderResult);
    }

    /**
     * 批量下单
     * POST /api/margin/v3/batch_orders
     */
    @Test
    public void batchOrders() {
        final PlaceOrderParam order = new PlaceOrderParam();
        //公共参数
        order.setClient_oid("test052803");
        order.setType("limit");
        order.setSide("buy");
        order.setInstrument_id("XRP-USDT");
        order.setOrder_type("0");
        order.setMargin_trading("2");

        //限价单特殊参数
        order.setPrice("0.6");
        order.setSize("1");

        //市价单特殊参数(买入必填notional<买入金额> 卖出必填size<卖出数量>)
        /*order.setNotional("");
        order.setSize("");*/


        final PlaceOrderParam order1 = new PlaceOrderParam();
        //公共参数
        order1.setClient_oid("test052804");
        order1.setType("limit");
        order1.setSide("buy");
        order1.setInstrument_id("XRP-USDT");
        order.setOrder_type("0");
        order1.setMargin_trading("2");

        //普通限价单参数
        order1.setPrice("0.55");
        order1.setSize("1");

        //市价单(买入必填notional<买入金额> 卖出必填size<卖出数量>)
        //order.setNotional("");
        //order.setSize("");

        final List<PlaceOrderParam> list = new ArrayList<>();
        list.add(order);
        list.add(order1);

        final Map<String, List<OrderResult>> orderResult = this.marginOrderAPIService.batchOrders(list);
        this.toResultString(MarginOrderAPITest.LOG, "orders", orderResult);
    }

    /**
     * 修改订单(通过order_id)
     * POST/api/margin/v3/amend_order/<instrument_id>
     */
    @Test
    public void amendOrderByOrderId(){
        MarginAmendOrder marginAmendOrder = new MarginAmendOrder();
        marginAmendOrder.setCancel_on_fail("0");
        marginAmendOrder.setOrder_id("7041846456631296");
//        marginAmendOrder.setRequest_id("");
        marginAmendOrder.setNew_price("0.6");
        marginAmendOrder.setNew_size("2");

        final OrderResult orderResult = this.marginOrderAPIService.amendOder("XRP-USDT",marginAmendOrder);
        this.toResultString(MarginOrderAPITest.LOG, "cancleOrder", orderResult);

    }

    /**
     * 修改订单(通过client_oid)
     * POST/api/margin/v3/amend_order/<instrument_id>
     */
    @Test
    public void amendOrderByClientOid(){
        MarginAmendOrder marginAmendOrder = new MarginAmendOrder();
//        marginAmendOrder.setInstrument_id("XRP-USDT");
        marginAmendOrder.setCancel_on_fail("0");
        marginAmendOrder.setClient_oid("testmargin5201");
//        marginAmendOrder.setRequest_id("");
        marginAmendOrder.setNew_price("0.5");
        marginAmendOrder.setNew_size("1");

        final OrderResult orderResult = this.marginOrderAPIService.amendOder("XRP-USDT",marginAmendOrder);
        this.toResultString(MarginOrderAPITest.LOG, "cancleOrder", orderResult);

    }
    /**
     * 批量修改订单(通过order_id)
     * POST/api/margin/v3/amend_order/<instrument_id>
     */
    @Test
    public void batchAmendOrderByOrderid(){
        List<MarginAmendOrder> list = new ArrayList<>();

        MarginAmendOrder marginAmendOrder = new MarginAmendOrder();
        marginAmendOrder.setInstrument_id("XRP-USDT");
//        marginAmendOrder.setCancel_on_fail("0");
        marginAmendOrder.setOrder_id("7042708973436928");
//        marginAmendOrder.setRequest_id("");
        marginAmendOrder.setNew_price("0.5");
        marginAmendOrder.setNew_size("2");

        MarginAmendOrder marginAmendOrder1 = new MarginAmendOrder();
        marginAmendOrder1.setInstrument_id("XRP-USDT");
//        marginAmendOrder1.setCancel_on_fail("0");
        marginAmendOrder1.setOrder_id("7042708973502464");
//        marginAmendOrder1.setRequest_id("");
        marginAmendOrder1.setNew_price("0.4");
        marginAmendOrder1.setNew_size("2");

        list.add(marginAmendOrder);
        list.add(marginAmendOrder1);

        Map<String, List<OrderResult>> result = this.marginOrderAPIService.batchAmendOder(list);
        this.toResultString(MarginOrderAPITest.LOG, "result", result);


    }


    /**
     * 批量修改订单(通过order_id)
     * POST/api/margin/v3/amend_order/<instrument_id>
     */
    @Test
    public void batchAmendOrderByClientOid(){
        List<MarginAmendOrder> list = new ArrayList<>();

        MarginAmendOrder marginAmendOrder = new MarginAmendOrder();
        marginAmendOrder.setInstrument_id("XRP-USDT");
//        marginAmendOrder.setCancel_on_fail("0");
        marginAmendOrder.setClient_oid("test052803");
//        marginAmendOrder.setRequest_id("");
        marginAmendOrder.setNew_price("0.4");
        marginAmendOrder.setNew_size("1");

        MarginAmendOrder marginAmendOrder1 = new MarginAmendOrder();
        marginAmendOrder1.setInstrument_id("XRP-USDT");
//        marginAmendOrder1.setCancel_on_fail("0");
        marginAmendOrder1.setClient_oid("test052803");
//        marginAmendOrder1.setRequest_id("");
        marginAmendOrder1.setNew_price("0.3");
        marginAmendOrder1.setNew_size("1");

        list.add(marginAmendOrder);
        list.add(marginAmendOrder1);

        Map<String, List<OrderResult>> result = this.marginOrderAPIService.batchAmendOder(list);
        this.toResultString(MarginOrderAPITest.LOG, "result", result);


    }




    /**
     * 撤销指定订单(通过order_id)
     * POST /api/margin/v3/cancel_orders/<order_id>
     */
    @Test
    public void cancleOrdersByOrderId() {
        PlaceOrderParam orderParam = new PlaceOrderParam();
        orderParam.setInstrument_id("MNBTC-MNUSDT");
        final OrderResult orderResult = this.marginOrderAPIService.cancleOrdersByOrderId(orderParam,"5915531078819840" );
        this.toResultString(MarginOrderAPITest.LOG, "cancleOrder", orderResult);
    }

    /**
     * 撤销指定订单(通过client_oid)
     * POST /api/margin/v3/cancel_orders/<client_oid>
     */
    @Test
    public void cancleOrdersByClientOid() {
        PlaceOrderParam orderParam = new PlaceOrderParam();
        orderParam.setInstrument_id("OKB-USDT");
        final OrderResult orderResult = this.marginOrderAPIService.cancleOrdersByClientOid(orderParam, "1022testmargin02");
        this.toResultString(MarginOrderAPITest.LOG, "cancleOrder", orderResult);
    }

    /**
     * 批量撤单(通过order_id)
     * POST /api/margin/v3/cancel_batch_orders
     */
    @Test
    public void batchCancleOrdersByOrderId() {
        final List<OrderParamDto> cancleOrders = new ArrayList<>();

        final OrderParamDto dto = new OrderParamDto();
        dto.setInstrument_id("MNBTC-MNUSDT");
        final List<String> order_ids = new ArrayList<>();
        order_ids.add("5915541774950400");
        order_ids.add("5915541775015936");
//        order_ids.add("5807450915300352");

        dto.setOrder_ids(order_ids);
        cancleOrders.add(dto);

       /* final OrderParamDto dto1 = new OrderParamDto();
        dto1.setInstrument_id("XRP-USDT");
        final List<String> order_ids1 = new ArrayList<>();
        order_ids1.add("5326387405613056");
        order_ids1.add("5326404345413632");
        dto1.setOrder_ids(order_ids1);
        cancleOrders.add(dto1);*/

        final Map<String, Object> orderResult = this.marginOrderAPIService.batchCancleOrdersByOrderId(cancleOrders);
        this.toResultString(MarginOrderAPITest.LOG, "cancleOrders", orderResult);
    }

    /**
     * 批量撤单(通过client_oid)
     * POST /api/margin/v3/cancel_batch_orders
     */
    @Test
    public void batchCancleOrdersByClientOid() {
        final List<OrderParamDto> cancleOrders = new ArrayList<>();

        final OrderParamDto dto = new OrderParamDto();
        dto.setInstrument_id("OKB-USDT");
        final List<String> client_oids = new ArrayList<>();
        client_oids.add("1022testmargin06");
        client_oids.add("1022testmargin07");
        dto.setClient_oids(client_oids);
        cancleOrders.add(dto);

        /*final OrderParamDto dto1 = new OrderParamDto();
        dto1.setInstrument_id("XRP-USDT");
        final List<String> client_oids1 = new ArrayList<>();
        client_oids1.add("");
        client_oids1.add("");
        dto1.setClient_oids(client_oids1);
        cancleOrders.add(dto1);*/

        final Map<String, Object> orderResult = this.marginOrderAPIService.batchCancleOrdersByClientOid(cancleOrders);
        this.toResultString(MarginOrderAPITest.LOG, "cancleOrders", orderResult);
    }

    /**
     * 获取订单列表
     * GET /api/margin/v3/orders
     */
    @Test
    public void getOrders() {
        final List<OrderInfo> orderInfoList = this.marginOrderAPIService.getOrders("XRP-USDT", "0", null, null, null);
        this.toResultString(MarginOrderAPITest.LOG, "orderInfoList", orderInfoList);
    }

    /**
     * 获取订单信息（通过order_id）
     * GET /api/margin/v3/orders/<order_id>
     */
    @Test
    public void getOrderByOrderId() {
        final OrderInfo orderInfo = this.marginOrderAPIService.getOrderByOrderId("OKB-USDT", "5807457240567808");
        this.toResultString(MarginOrderAPITest.LOG, "orderInfo", orderInfo);
    }

    /**
     * 获取订单信息（通过client_oid）
     * GET /api/margin/v3/orders/<client_oid>
     */
    @Test
    public void getOrderByClientOid() {
        final OrderInfo orderInfo = this.marginOrderAPIService.getOrderByClientOid("1022testmargin07","OKB-USDT");
        this.toResultString(MarginOrderAPITest.LOG, "orderInfo", orderInfo);
    }

    /**
     * 获取所有未成交订单
     * GET /api/margin/v3/orders_pending
     */
    @Test
    public void getPendingOrders() {
        final List<PendingOrdersInfo> orderInfoList = this.marginOrderAPIService.getPendingOrders("OKB-USDT", null, null, "10");
        this.toResultString(MarginOrderAPITest.LOG, "orderInfoList", orderInfoList);
    }

    /**
     * 获取成交明细
     * GET /api/margin/v3/fills
     */
    @Test
    public void getFills() {
        final List<MarginFills> fills = this.marginOrderAPIService.getFills(null, "OKB-USDT", null, null, "10");
        this.toResultString(MarginOrderAPITest.LOG, "fills", fills);
    }

}
