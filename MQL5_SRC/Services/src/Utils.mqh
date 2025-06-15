#ifndef __MY_UTILS__
#define __MY_UTILS__

#property copyright "Copyright 2025, MetaQuotes Ltd."
#property link      "https://www.mql5.com"

class Utils
{
   public:
   static string Trim(string str)
   {
      StringTrimRight(str);
      StringTrimLeft(str);
      return str;
   }
   static string GetJsonValue(const string json, const string key)
   {
      int key_pos = StringFind(json, "\"" + key + "\"");
      if(key_pos < 0)
         return "";
      
      int colon_pos = StringFind(json, ":", key_pos);
      if(colon_pos < 0)
         return "";
      
      int end_pos = StringFind(json, ",", colon_pos);
      if(end_pos < 0)
         end_pos = StringFind(json, "}", colon_pos);
      if(end_pos < 0)
         end_pos = StringLen(json);
      
      string subStr = StringSubstr(json, colon_pos + 1, end_pos - colon_pos - 1);
      string raw = Trim(subStr);
      StringReplace(raw, "\"", "");
      return raw;
   }
   static string GetJsonBlock(const string json, const string key)
   {
      int start = StringFind(json, "\"" + key + "\"");
      if(start < 0)
         return "";
      
      int open_brace = StringFind(json, "{", start);
      int brace_count = 1;
      int i = open_brace + 1;
      
      while(i < StringLen(json) && brace_count > 0)
      {
         if(StringGetCharacter(json, i) == '{') brace_count++;
         if(StringGetCharacter(json, i) == '}') brace_count--;
         i++;
      }
      return StringSubstr(json, open_brace, i - open_brace);
   }
};

#endif