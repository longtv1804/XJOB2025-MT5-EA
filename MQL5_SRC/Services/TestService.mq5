//+------------------------------------------------------------------+
//|                                                  TestService.mq5 |
//|                                  Copyright 2025, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property service
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"

//#include <WinUser32.mqh>
#include "src/RequestMessage.mqh"
#include "src/Utils.mqh"
//+------------------------------------------------------------------+
//| Service program start function                                   |
//+------------------------------------------------------------------+
void OnStart()
{
   Print("Service started!");
   string url = "http://127.0.0.1:5000/data"; // Ví dụ URL trả về JSON
   int interval_seconds = 5;
   int loopCount = 10;
   
   while(!IsStopped() && loopCount > 0)
   {
      loopCount--;
      string json = GetJSONFromURL(url);
      json = Utils::Trim(json);
      if(json != "")
      {
         Print("fetched JSON: ", json);
         RequestMessage reqMsg;
         reqMsg.ParseFromJSON(json);
         reqMsg.PrintAll();
      }
      else
      {
         Print("Can not fetch the JSON.");
      }
      Sleep(interval_seconds * 1000);
   }
   
   Print("Service stopped.");
}
//+------------------------------------------------------------------+

//===================================================================
//           my logic
//===================================================================
string GetJSONFromURL(string url)
{
   char         post[];
   char         result[];
   string       headers = "";
   int          timeout = 5000; // 5s
   string       cookie = NULL;
   
   // Gửi yêu cầu HTTP GET
   int res = WebRequest(
               "GET",
               url,
               cookie,
               NULL,       // referer
               timeout,
               post,
               0,
               result,
               headers
            );

   if(res == -1)
   {
      Print("WebRequest ERR: ", GetLastError());
      ResetLastError();
      return "";
   }
   
   string json = CharArrayToString(result);
   return json;
}
