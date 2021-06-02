package com.okcoin.commons.okex.open.api.service.system.impl;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;
import retrofit2.http.Query;

interface SystemMarketAPI {

    //获取系统升级状态
    @GET("/api/system/v3/status")
    Call<JSONArray> getMaintenance(@Query("status") String status);

    //获取系统升级状态V5
    @GET("/api/v5/system/status")
    Call<JSONObject> getStatus(@Query("state") String state);

}
