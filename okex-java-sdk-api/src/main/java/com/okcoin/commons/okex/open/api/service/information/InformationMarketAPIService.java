package com.okcoin.commons.okex.open.api.service.information;

import com.alibaba.fastjson.JSONArray;
import retrofit2.Call;

public interface InformationMarketAPIService {
    //获取多空持仓比
    JSONArray getLongShortRatio(String currency, String start, String end, String granularity);

    //公共-获取持仓总量
    JSONArray getVolume(String currency, String start, String end, String granularity);

    JSONArray getTaker(String currency, String start, String end, String granularity);

    JSONArray getSentiment(String currency, String start, String end, String granularity);

    JSONArray getMargin(String currency, String start, String end, String granularity);

}
