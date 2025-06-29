//+------------------------------------------------------------------+
//|                                                  JsonMessage.mqh |
//|                                  Copyright 2025, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#ifndef __MY_REQ_MESSAGE__
#define __MY_REQ_MESSAGE__

#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"

#include "PositionInfo.mqh"
#include "Utils.mqh"

class Request {
   public:
      int mToken;
      int mReqType;
      string ToJson()
      {
         string ret;
         ret = "{\"Token\":"           + mToken    + ",";
         ret =  "\"RequestType\":"     + mReqType  + "}";
         return ret;
      }
};

class RequestMessage
{
   public:
      double         mJsonVersion;
      int            mClientId;
      Request        mReq;
      PositionInfo   mPosition;
      
      void PrintAll()
      {
         Print("-> JsonVersion:", mJsonVersion, " ClientId: ", mClientId);
         mPosition.PrintInfo();
      }

      void ParseFromJSON(const string jsonStr)
      {
         mJsonVersion = StringToDouble(Utils::GetJsonValue(jsonStr, "JsonVersion"));
         mClientId    = StringToInteger(Utils::GetJsonValue(jsonStr, "ClientId"));
         
         string positionStr = Utils::GetJsonBlock(jsonStr, "Position");
         if (StringLen(positionStr) > 0)
         {
            mPosition.mTokenId = StringToInteger(Utils::GetJsonValue(positionStr, "TokenId"));
            mPosition.mPosType = StringToInteger(Utils::GetJsonValue(positionStr, "PosType"));
            mPosition.mCode    =                 Utils::GetJsonValue(positionStr, "Code");
            mPosition.mStatus  = StringToInteger(Utils::GetJsonValue(positionStr, "Status"));
            mPosition.mVolume  = StringToInteger(Utils::GetJsonValue(positionStr, "Volume"));
            mPosition.mPrice   = StringToDouble (Utils::GetJsonValue(positionStr, "Price"));
         }
      }
      
      string ToJson()
      {
         string ret;
         ret =   "{\"JsonVersion\":"   + mJsonVersion       + ",";
         ret +=   "\"ClientId\":"      + mClientId          + ",";
         ret +=   "\"Request\":"       + mReq.ToJson()      + ",";
         ret +=   "\"Position\":"      + mPosition.ToJson() + "}";
         return ret;
      }
};

#endif