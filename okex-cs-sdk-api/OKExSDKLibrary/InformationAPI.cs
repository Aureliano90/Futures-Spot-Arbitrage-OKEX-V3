using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace OKExSDK
{
    public class InformationAPI : SdkApi
    {
        private string INFORMATION_SEGMENT = "api/information/v3/";

        public InformationAPI(string apiKey, string secret, string passPhrase) : base(apiKey, secret, passPhrase) { }

        /// <summary>
        /// 公共-获取多空人数比
        /// 此接口为公共接口，不需要身份验证。
        /// 限速规则：20次/2s （根据underlying，分别限速）
        /// </summary>
        /// <returns></returns>
        public async Task<string> long_short_radio(string currency, string granularity = "", string start = "", string end = "")
        {
            var url = $"{this.BASEURL}{this.INFORMATION_SEGMENT}{currency}/long_short_ratio";
            var queryParams = new Dictionary<string, string>();
            if (!string.IsNullOrWhiteSpace(granularity))
            {
                queryParams.Add("granularity", granularity);
            }
            if (!string.IsNullOrWhiteSpace(start))
            {
                queryParams.Add("start", start);
            }
            if (!string.IsNullOrWhiteSpace(end))
            {
                queryParams.Add("end", end);
            }

            var encodedContent = new FormUrlEncodedContent(queryParams);
            var paramsStr = await encodedContent.ReadAsStringAsync();


            using (HttpClient client = new HttpClient(new HttpInterceptor(this._apiKey, this._secret, this._passPhrase, null)))
            {

                var res = await client.GetAsync($"{url}?{paramsStr}");
                var contentStr = await res.Content.ReadAsStringAsync();
                return contentStr;
            }
        }
        /// <summary>
        /// 公共-获取持仓总量
        /// 此接口为公共接口，不需要身份验证。
        /// 限速规则：20次/2s （根据underlying，分别限速）
        /// </summary>
        /// <param name="currency"></param>
        /// <returns></returns>
        public async Task<string> volume(string currency, string granularity = "", string start = "", string end = "")
        {
            var url = $"{this.BASEURL}{this.INFORMATION_SEGMENT}{currency}/volume";
            var queryParams = new Dictionary<string, string>();
            if (!string.IsNullOrWhiteSpace(granularity))
            {
                queryParams.Add("granularity", granularity);
            }
            if (!string.IsNullOrWhiteSpace(start))
            {
                queryParams.Add("start", start);
            }
            if (!string.IsNullOrWhiteSpace(end))
            {
                queryParams.Add("end", end);
            }

            var encodedContent = new FormUrlEncodedContent(queryParams);
            var paramsStr = await encodedContent.ReadAsStringAsync();


            using (HttpClient client = new HttpClient(new HttpInterceptor(this._apiKey, this._secret, this._passPhrase, null)))
            {

                var res = await client.GetAsync($"{url}?{paramsStr}");
                var contentStr = await res.Content.ReadAsStringAsync();
                return contentStr;
            }
        }
        /// <summary>
        /// 公共-主动买入卖出
        /// </summary>
        /// <param name="currency"></param>
        /// <returns></returns>
        public async Task<string> taker(string currency, string granularity = "", string start = "", string end = "")
        {
            var url = $"{this.BASEURL}{this.INFORMATION_SEGMENT}{currency}/taker";
            var queryParams = new Dictionary<string, string>();
            if (!string.IsNullOrWhiteSpace(granularity))
            {
                queryParams.Add("granularity", granularity);
            }
            if (!string.IsNullOrWhiteSpace(start))
            {
                queryParams.Add("start", start);
            }
            if (!string.IsNullOrWhiteSpace(end))
            {
                queryParams.Add("end", end);
            }

            var encodedContent = new FormUrlEncodedContent(queryParams);
            var paramsStr = await encodedContent.ReadAsStringAsync();


            using (HttpClient client = new HttpClient(new HttpInterceptor(this._apiKey, this._secret, this._passPhrase, null)))
            {

                var res = await client.GetAsync($"{url}?{paramsStr}");
                var contentStr = await res.Content.ReadAsStringAsync();
                return contentStr;
            }
        }
        /// <summary>
        /// 公共-多空精英趋向指标
        /// </summary>
        /// <param name="currency"></param>
        /// <returns></returns>
        public async Task<string> sentiment(string currency)
        {
            var url = $"{this.BASEURL}{this.INFORMATION_SEGMENT}{currency}/sentiment";


            using (HttpClient client = new HttpClient(new HttpInterceptor(this._apiKey, this._secret, this._passPhrase, null)))
            {
                var res = await client.GetAsync(url);
                var contentStr = await res.Content.ReadAsStringAsync();
                return contentStr;
            }
        }
        /// <summary>
        /// 公共-精英多空平均持仓比例
        /// </summary>
        /// <param name="currency"></param>
        /// <returns></returns>
        public async Task<string> margin(string currency)
        {
            var url = $"{this.BASEURL}{this.INFORMATION_SEGMENT}{currency}/margin";


            using (HttpClient client = new HttpClient(new HttpInterceptor(this._apiKey, this._secret, this._passPhrase, null)))
            {
                var res = await client.GetAsync(url);
                var contentStr = await res.Content.ReadAsStringAsync();
                return contentStr;
            }
        }
    }
}
