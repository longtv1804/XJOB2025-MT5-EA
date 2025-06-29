//+------------------------------------------------------------------+
//|                                                   WebHandler.mqh |
//|                                  Copyright 2025, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"

#include "Utils.mqh"

class WebHandler
{
   private:
      string mSession;
      string mWebAddress;
   
   public:
      
      bool LoginToServer(const string username, const string password)
      {
         const string url = mWebAddress + "/login";
         const string contentType = "Content-Type: application/json\r\n";
      
         string jsonPayload;
         jsonPayload = "{\"username\":\"" + username + "\",\"password\":\"" + password + "\"}";
      
         char postData[];
         StringToCharArray(jsonPayload, postData);
      
         char result[];
         string headers;
         int timeout = 5000;
      
         ResetLastError();
         int res = WebRequest(
            "POST",
            url,
            contentType,
            timeout,
            postData,
            result,
            headers
         );

         if (res == -1)
         {
            Print("WebRequest error: ", GetLastError());
            return false;
         }

         string response = CharArrayToString(result);
         Print("Server response: ", response);

         mSession = Utils::GetJsonValue(response, "token");
         if (mSession != "") {
            Print("Login successed: ", mSession);
         } else {
            Print("Login failed");
         }
         return true;
      }
      
      // server -> client
      string RequestSyn()
      {
      }
      
      // client -> server
      void UpdateInformation()
      {
      }
};