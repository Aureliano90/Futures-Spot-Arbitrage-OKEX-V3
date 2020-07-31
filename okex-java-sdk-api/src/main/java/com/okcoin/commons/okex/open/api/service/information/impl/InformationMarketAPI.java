package com.okcoin.commons.okex.open.api.service.information.impl;

import com.alibaba.fastjson.JSONArray;
import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Path;
import retrofit2.http.Query;

public interface InformationMarketAPI {
    @GET("/api/information/v3/{currency}/long_short_ratio")
    Call<JSONArray> getLongShortRatio(@Path("currency") String currency,
                                      @Query("start") String start,
                                      @Query("end") String end,
                                      @Query("granularity") String granularity);


    @GET("/api/information/v3/{currency}/volume")
    Call<JSONArray> getVolume(@Path("currency") String currency,
                              @Query("start") String start,
                              @Query("end") String end,
                              @Query("granularity") String granularity);



    @GET("/api/information/v3/{currency}/taker")
    Call<JSONArray> getTaker(@Path("currency") String currency,
                              @Query("start") String start,
                              @Query("end") String end,
                              @Query("granularity") String granularity);

    @GET("/api/information/v3/{currency}/sentiment")
    Call<JSONArray> getSentiment(@Path("currency") String currency,
                             @Query("start") String start,
                             @Query("end") String end,
                             @Query("granularity") String granularity);

    @GET("/api/information/v3/{currency}/margin")
    Call<JSONArray> getMargin(@Path("currency") String currency,
                                 @Query("start") String start,
                                 @Query("end") String end,
                                 @Query("granularity") String granularity);

}
