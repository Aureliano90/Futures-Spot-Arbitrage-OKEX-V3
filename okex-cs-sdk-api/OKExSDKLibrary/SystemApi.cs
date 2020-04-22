using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace OKExSDK
{
    public class SystemApi:SdkApi
    {
        private string SYSTEM_SEGMENT = "api/system/v3";
        public SystemApi(string apiKey, string secret, string passPhrase) : base(apiKey, secret, passPhrase) { }
        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public async Task<string> status()
        {
            var url = $"{this.BASEURL}{this.SYSTEM_SEGMENT}/status";
            using (var client = new HttpClient(new HttpInterceptor(this._apiKey, this._secret, this._passPhrase, null)))
            {
                var res = await client.GetAsync(url);
                var contentStr = await res.Content.ReadAsStringAsync();
                return contentStr;
            }
        }
    }
}
