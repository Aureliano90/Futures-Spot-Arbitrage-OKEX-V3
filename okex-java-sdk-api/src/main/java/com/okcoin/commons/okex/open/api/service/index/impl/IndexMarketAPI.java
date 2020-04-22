package com.okcoin.commons.okex.open.api.service.index.impl;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;

interface IndexMarketAPI {
    @GET("/api/index/v3/{instrument_id}/constituents")
    Call<String> getIndex(@Path("instrument_id") String instrument_id);
}
