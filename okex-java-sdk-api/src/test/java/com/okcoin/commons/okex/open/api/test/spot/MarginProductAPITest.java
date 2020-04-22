package com.okcoin.commons.okex.open.api.test.spot;

import com.okcoin.commons.okex.open.api.service.spot.MarginProductAPIService;
import com.okcoin.commons.okex.open.api.service.spot.impl.MarginProductAPIServiceImpl;
import org.junit.Before;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class MarginProductAPITest extends SpotAPIBaseTests{
    private static final Logger LOG = LoggerFactory.getLogger(MarginOrderAPITest.class);
    private MarginProductAPIService marginOrderAPIService;

    @Before
    public void before() {
        this.config = this.config();
        this.marginOrderAPIService = new MarginProductAPIServiceImpl(this.config);
    }

    /**
     *公共-获取标记价格
     * 获取现货杠杆标记价格。此接口为公共接口，不需要身份验证。
     * 限速规则：20次/2s
     * GET/api/margin/v3/instruments/<instrument_id>/mark_price
     *
     * **/
    @Test
    public void testGetMarginMarkPrice(){
        final String markPrice = this.marginOrderAPIService.getMarginMarkPrice("BTC-USDT");
        this.toResultString(MarginProductAPITest.LOG, "markPrice", markPrice);
    }


}
