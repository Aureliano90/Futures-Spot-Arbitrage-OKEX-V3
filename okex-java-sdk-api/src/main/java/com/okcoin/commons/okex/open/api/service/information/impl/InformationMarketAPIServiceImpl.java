package com.okcoin.commons.okex.open.api.service.information.impl;

import com.alibaba.fastjson.JSONArray;
import com.okcoin.commons.okex.open.api.client.APIClient;
import com.okcoin.commons.okex.open.api.config.APIConfiguration;
import com.okcoin.commons.okex.open.api.service.information.InformationMarketAPIService;

public class InformationMarketAPIServiceImpl implements InformationMarketAPIService {
    private APIClient client;
    private InformationMarketAPI api;

    public InformationMarketAPIServiceImpl(APIConfiguration config) {
        this.client = new APIClient(config);
        this.api = client.createService(InformationMarketAPI.class);
    }


    @Override
    public JSONArray getLongShortRatio(String currency, String start, String end, String granularity) {
        return this.client.executeSync(this.api.getLongShortRatio(currency,start,end,granularity));
    }

    @Override
    public JSONArray getVolume(String currency, String start, String end, String granularity) {
        return this.client.executeSync(this.api.getVolume(currency,start,end,granularity));
    }

    @Override
    public JSONArray getTaker(String currency, String start, String end, String granularity) {
        return this.client.executeSync(this.api.getTaker(currency,start,end,granularity));
    }

    @Override
    public JSONArray getSentiment(String currency, String start, String end, String granularity) {
        return this.client.executeSync(this.api.getSentiment(currency, start, end, granularity));
    }

    @Override
    public JSONArray getMargin(String currency, String start, String end, String granularity) {
        return this.client.executeSync(this.api.getMargin(currency, start, end, granularity));
    }
}
