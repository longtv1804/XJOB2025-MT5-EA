//+------------------------------------------------------------------+
//|                                                  CommandInfo.mqh |
//|                                  Copyright 2025, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
//+------------------------------------------------------------------+
//| defines                                                          |
//+------------------------------------------------------------------+
// #define MacrosHello   "Hello, world!"
// #define MacrosYear    2010
//+------------------------------------------------------------------+
//| DLL imports                                                      |
//+------------------------------------------------------------------+
// #import "user32.dll"
//   int      SendMessageA(int hWnd,int Msg,int wParam,int lParam);
// #import "my_expert.dll"
//   int      ExpertRecalculate(int wParam,int lParam);
// #import
//+------------------------------------------------------------------+
//| EX5 imports                                                      |
//+------------------------------------------------------------------+
// #import "stdlib.ex5"
//   string ErrorDescription(int error_code);
// #import
//+------------------------------------------------------------------+

class PositionInfo
{
public:
   int      mTokenId;
   int      mPosType;
   string   mCode;
   int      mStatus;
   int      mVolume;
   double   mPrice;
   
   void PrintInfo()
   {
      Print("-> PositionInfo[PosType: ", mPosType, " TokenId: ", mTokenId, " Code:", mCode, " Status: ", mStatus, " Volume: ", mVolume, " Price: ", mPrice, "]");
   }
   
   string ToJson ()
   {
      string ret;
      ret   =    "{\"TokenId\":"    + mTokenId   + ",";
      ret   +=    "\"PosType\":"    + mPosType   + ",";
      ret   +=    "\"Code\":\""     + mCode      + "\",";
      ret   +=    "\"Status\":"     + mStatus    + ",";
      ret   +=    "\"Volume\":"     + mVolume    + ",";
      ret   +=    "\"Price\":"      + mPrice     + "}";
      return ret;
   }
};
