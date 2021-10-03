using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

using Amazon.Lambda.Core;
using Amazon.Lambda.APIGatewayEvents;
using System.Runtime.Serialization;


// Assembly attribute to enable the Lambda function's JSON input to be converted into a .NET class.
[assembly: LambdaSerializer(typeof(Amazon.Lambda.Serialization.SystemTextJson.DefaultLambdaJsonSerializer))]

namespace SolarEnergyRecommendationLambdaFunction
{
    public class Function
    {
        
        /// <summary>
        /// A simple function that takes a string and does a ToUpper
        /// </summary>
        /// <param name="input"></param>
        /// <param name="context"></param>
        /// <returns></returns>
        public APIGatewayProxyResponse FunctionHandler(Parameter input, ILambdaContext context)
        {
            var result = new List<MonthObject>
            {
                new MonthObject
                {
                    month = "JAN",
                    angle = "19.0",
                    energy = "5.04",
                    orientation = "S",
                    saving = "$100"
                },
                new MonthObject
                {
                    month = "FEB",
                    angle = "19.0",
                    energy = "5.04",
                    orientation = "S",
                    saving = "$150"
                },
                new MonthObject
                {
                    month = "MAR",
                    angle = "19.0",
                    energy = "5.04",
                    orientation = "S",
                    saving = "$120"

                },
                new MonthObject
                {
                    month = "APR",
                    angle = "19.0",
                    energy = "5.04",
                    orientation = "S",
                    saving = "$110"
                },
                new MonthObject
                {
                    month = "MAY",
                    angle = "19.0",
                    energy = "5.04",
                    orientation = "S",
                    saving = "$120"
                },
                new MonthObject
                {
                    month = "JUN",
                    angle = "19.0",
                    energy = "5.04",
                    orientation = "S",
                    saving = "$120"
                },
                new MonthObject
                {
                    month = "JUL",
                    angle = "19.0",
                    energy = "5.04",
                    orientation = "S",
                    saving = "$120"
                },
                new MonthObject
                {
                    month = "AUG",
                    angle = "7.5",
                    energy = "4.6",
                    orientation =  "S",
                    saving = "$120"
                },
            };

            var response = new APIGatewayProxyResponse
            {
                IsBase64Encoded = false,
                StatusCode = (int)System.Net.HttpStatusCode.OK,
                Body = Newtonsoft.Json.JsonConvert.SerializeObject(result),
                Headers = new Dictionary<string, string> { { "Content-Type", "application/json" } },
            };

            return response;
            //return Newtonsoft.Json.JsonConvert.SerializeObject(response);
        }
    }

    public class Parameter
    {
        public string lat { get; set; }
        public string lng { get; set; }
        public string provider { get; set; }
        public string monthlybill { get; set; }
    }

    public class MonthObject
    {
        public string month { get; set; }
        public string angle { get; set; }
        public string energy { get; set; }
        public string orientation { get; set; }
        public string saving { get; set; }
    }
}
