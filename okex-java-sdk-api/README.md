OKCoin OKEX V3 Open Api使用说明
--------------
### 1.使用技术：okhttp3 + retrofit2

```
### 2.简单使用方式:
```
 public static void main(String[] args) {

        APIConfiguration config = new APIConfiguration();
        config.setEndpoint(" https://www.okex.com/");
        //secretKey,api注册成功后页面上有
        config.setApiKey("");
        config.setSecretKey("");
        //Passphrase忘记后无法找回
        config.setPassphrase("");
        config.setPrint(true);

        GeneralAPIService marketAPIService = new GeneralAPIServiceImpl(config);
        ServerTime time = marketAPIService.getServerTime();
        System.out.println(JSON.toJSONString(time));

        FuturesTradeAPIService tradeAPIService = new FuturesTradeAPIServiceImpl(config);

        Order order = new Order();
        order.setClient_oid("OkexTestFuturesOrder2020");
        order.setInstrument_id("BTC-USD-200626");
        order.setType("1");
        order.setPrice("7000");
        order.setSize("400");
        order.setMatch_price("0");
        order.setOrder_type("0");
        OrderResult orderResult = tradeAPIService.newOrder(order); 
        System.out.println(JSON.toJSONString(orderResult));
 }
```
### 3.Spring 或 Spring Boot使用方式:
```
@RestController
public class TestOKEXOpenApiV3 {

    @Autowired
    private GeneralAPIService generalAPIService;

    @GetMapping("/server-time")
    public ServerTime getServerTime() {
        return generalAPIService.getServerTime();
    }
    
    @Bean
    public APIConfiguration okexApiConfig() {
        APIConfiguration config = new APIConfiguration();
          config.setEndpoint(" https://www.okex.com/");
            //secretKey,api注册成功后页面上有
            config.setApiKey("");
            config.setSecretKey("");
            //Passphrase忘记后无法找回
            config.setPassphrase("");
            config.setPrint(true);
        return config;
    }

    @Bean
    public GeneralAPIService generalAPIService(APIConfiguration config) {
        return new GeneralAPIServiceImpl(config);
    }
}
