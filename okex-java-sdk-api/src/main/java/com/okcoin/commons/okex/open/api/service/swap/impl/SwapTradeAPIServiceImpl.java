package com.okcoin.commons.okex.open.api.service.swap.impl;

import com.alibaba.fastjson.JSONObject;
import com.okcoin.commons.okex.open.api.bean.swap.param.*;
import com.okcoin.commons.okex.open.api.bean.swap.result.ApiOrderVO;
import com.okcoin.commons.okex.open.api.client.APIClient;
import com.okcoin.commons.okex.open.api.config.APIConfiguration;
import com.okcoin.commons.okex.open.api.service.swap.SwapTradeAPIService;
import com.okcoin.commons.okex.open.api.utils.JsonUtils;

import java.util.List;
import java.util.Map;

public class SwapTradeAPIServiceImpl implements SwapTradeAPIService {
    private APIClient client;
    private SwapTradeAPI api;
    private SwapTradeAPI swapTradeAPI;

    public SwapTradeAPIServiceImpl() {
    }

    public SwapTradeAPIServiceImpl(APIConfiguration config) {
        this.client = new APIClient(config);
        this.api = client.createService(SwapTradeAPI.class);
    }

    //下单
    @Override
    public Object order(PpOrder ppOrder) {
        System.out.println(JsonUtils.convertObject(ppOrder, PpOrder.class));
        //return this.client.executeSync(this.api.order(JsonUtils.convertObject(ppOrder, PpOrder.class)));
        return this.client.executeSync(this.api.order(ppOrder));
    }

    //批量下单
    @Override
    public Map<String, Object> orders(PpOrders ppOrders) {
        return this.client.executeSync(this.api.orders(JsonUtils.convertObject(ppOrders, PpOrders.class)));
    }

    //撤单(通过order_id)
    @Override
    public JSONObject cancelOrderByOrderId(String instrument_id, String order_id) {
        return this.client.executeSync(this.api.cancelOrderByOrderId(instrument_id,order_id));
    }

    //撤单(通过client_oid)
    @Override
    public JSONObject cancelOrderByClientOid(String instrument_id, String client_oid) {
        return this.client.executeSync(this.api.cancelOrderByClientOid(instrument_id,client_oid));
    }

    //批量撤单(通过order_id)
    @Override
    public Map<String, Object> cancelOrdersByOrderIds(String instrumentId, PpCancelOrderVO ppCancelOrderVO) {
        return this.client.executeSync(this.api.cancelOrdersByOrderIds(instrumentId,JsonUtils.convertObject(ppCancelOrderVO, PpCancelOrderVO.class)));
    }

    //批量撤单(通过client_oid)
    @Override
    public Map<String, Object> cancelOrdersByClientOids(String instrumentId, PpCancelOrderVO ppCancelOrderVO) {
        return this.client.executeSync(this.api.cancelOrdersByClientOids(instrumentId,JsonUtils.convertObject(ppCancelOrderVO, PpCancelOrderVO.class)));
    }

    //修改订单(通过order_id)
    @Override
    public JSONObject amendOrderByOrderId(String instrumentId, AmendOrder amendOrder) {
        return this.client.executeSync(this.api.amendOrderByOrderId(instrumentId, amendOrder));
    }

    //修改订单(通过client_oid)
    @Override
    public JSONObject amendOrderByClientOid(String instrument_id, AmendOrder amendOrder) {
        return this.client.executeSync(this.api.amendOrderByClientOid(instrument_id, amendOrder));
    }

    //批量修改订单(通过order_id)
    @Override
    public Map<String, Object> amendBatchOrderByOrderId(String instrument_id, AmendOrderParam amendOrder) {
        return this.client.executeSync(this.api.amendBatchOrderByOrderId(instrument_id,amendOrder));
    }

    //批量修改订单(通过client_oid)
    @Override
    public Map<String, Object> amendBatchOrderByClientOid(String instrument_id, AmendOrderParam amendOrder) {
        return this.client.executeSync(this.api.amendBatchOrderByClientOid(instrument_id, amendOrder));
    }

    //委托策略下单
    @Override
    public JSONObject swapOrderAlgo(SwapOrderParam swapOrderParam) {
        System.out.println("begin swapOrder-----");
        return this.client.executeSync(this.api.swapOrderAlgo(swapOrderParam));
    }

    //委托策略撤单
    @Override
    public JSONObject cancelOrderAlgo(CancelOrderAlgo cancelOrderAlgo) {
        System.out.println("canceling the algo order");
        return this.client.executeSync(this.api.cancelOrderAlgo(cancelOrderAlgo));
    }

    //获取委托单列表
    @Override
    public Map<String,Object> getSwapOrders(String instrument_id, String order_type, String status, String algo_id, String before, String after, String limit ) {
        return this.client.executeSync(this.api.getSwapOrders(instrument_id,order_type,status,algo_id,before,after,limit));
    }

    //市价全平
    @Override
    public JSONObject closePosition(ClosePosition closePosition) {
        return this.client.executeSync(this.api.closePosition(closePosition));
    }

    //撤销所有平仓挂单
    @Override
    public JSONObject CancelAll(CancelAllParam cancelAllParam) {
        return this.client.executeSync(this.api.CancelAll(cancelAllParam));
    }
}
