using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace OKExSDK
{
    public class IndexApi:SdkApi
    {
        private string INDEX_SEGMENT  = "api/index/v3";
        public IndexApi(string apiKey, string secret, string passPhrase) : base(apiKey, secret, passPhrase) { }
        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public async Task<string> constituents(string instrument_id)
        {
            var url = $"{this.BASEURL}{this.INDEX_SEGMENT}/{instrument_id}/constituents";
            using (var client = new HttpClient(new HttpInterceptor(this._apiKey, this._secret, this._passPhrase, null)))
            {
                var res = await client.GetAsync(url);
                var contentStr = await res.Content.ReadAsStringAsync();
                return contentStr;
            }
        }
    }
}
