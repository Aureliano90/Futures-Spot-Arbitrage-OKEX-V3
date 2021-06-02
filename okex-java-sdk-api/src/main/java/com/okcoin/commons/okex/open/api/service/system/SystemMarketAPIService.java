package com.okcoin.commons.okex.open.api.service.system;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

public interface SystemMarketAPIService {

    //获取系统升级状态
    JSONArray getMaintenance(String status);

    //获取系统升级状态
    JSONObject getStatus(String state);

}
