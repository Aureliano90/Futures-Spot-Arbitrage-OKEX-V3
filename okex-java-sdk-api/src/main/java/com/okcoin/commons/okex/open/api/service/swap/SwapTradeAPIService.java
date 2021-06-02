package com.okcoin.commons.okex.open.api.service.swap;

import com.alibaba.fastjson.JSONObject;
import com.okcoin.commons.okex.open.api.bean.swap.param.*;
import com.okcoin.commons.okex.open.api.bean.swap.result.ApiOrderVO;
import retrofit2.http.Body;

import java.util.List;
import java.util.Map;

public interface SwapTradeAPIService {

    //下单
    Object order(PpOrder ppOrder);

    //批量下单
    Map<String, Object> orders(PpOrders ppOrders);

    //撤单(通过order_id)
    JSONObject cancelOrderByOrderId(String instrument_id, String order_id);

    //撤单(通过client_oid)
    JSONObject cancelOrderByClientOid(String instrument_id, String client_oid);

    //批量撤单(通过order_id)
    Map<String, Object> cancelOrdersByOrderIds(String instrument_id, PpCancelOrderVO ppCancelOrderVO);

    //批量撤单(通过client_oid)
    Map<String, Object> cancelOrdersByClientOids(String instrument_id, PpCancelOrderVO ppCancelOrderVO);

    //修改订单(通过order_id)
    JSONObject amendOrderByOrderId(String instrument_id,AmendOrder amendOrder);

    //修改订单(通过client_oid)
    JSONObject amendOrderByClientOid(String instrument_id,AmendOrder amendOrder);

    //批量修改订单(通过order_id)
    Map<String, Object> amendBatchOrderByOrderId(String instrument_id, AmendOrderParam amendOrder);

    //批量修改订单(通过client_oid)
    Map<String, Object> amendBatchOrderByClientOid(String instrument_id, AmendOrderParam amendOrder);

    //策略委托下单
    JSONObject swapOrderAlgo(SwapOrderParam swapOrderParam);

    //策略委托撤单
    JSONObject cancelOrderAlgo(CancelOrderAlgo cancelOrderAlgo);

    //获取委托单列表
    Map<String,Object> getSwapOrders(String instrument_id,
                         String order_type,
                         String status,
                         String algo_id,
                         String before,
                         String after,
                         String limit);

    //市价全平
    JSONObject closePosition(ClosePosition closePosition);

    //撤销所有平仓挂单
    JSONObject CancelAll(CancelAllParam cancelAllParam);
}
