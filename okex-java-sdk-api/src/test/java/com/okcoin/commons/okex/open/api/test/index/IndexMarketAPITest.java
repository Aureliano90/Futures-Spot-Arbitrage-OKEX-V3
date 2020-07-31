package com.okcoin.commons.okex.open.api.test.index;

import com.okcoin.commons.okex.open.api.service.index.IndexMarketAPIService;
import com.okcoin.commons.okex.open.api.service.index.impl.IndexMarketAPIServiceImpl;
import org.junit.Before;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class IndexMarketAPITest extends IndexAPIBaseTest {

    private static final Logger LOG = LoggerFactory.getLogger(IndexMarketAPITest.class);
    private IndexMarketAPIService marketAPIService;

    @Before
    public void before() {
        config = config();
        marketAPIService = new IndexMarketAPIServiceImpl(config);
    }

    /**
     *公共-获取指数成分
     * 获取指数成分。此接口为公共接口，不需要身份验证。
     * 限速规则：20次/2s
     * GET /api/index/v3/<instrument_id>/constituents
     * **/

    @Test
    public void testGetIndex() {
        final String index = this.marketAPIService.getIndex("BTC-USD");
        this.toResultString(IndexMarketAPITest.LOG, "index", index);
    }

}
