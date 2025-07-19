#ifndef _CRT_SECURE_NO_WARNINGS
#define _CRT_SECURE_NO_WARNINGS
#endif // !_CRT_SECURE_NO_WARNINGS

//build with msbuild
// msbuild .\WebSocket.sln /p:Configuration=Release /p:Platform=x64

// socket_client_dll.cpp
// use https://www.zaphoyd.com/projects/websocketpp/
// or https://github.com/socketio/socket.io-client-cpp      build sang lib
#include <windows.h>
#include <string>
#include "socket.io-client-cpp/src/sio_client.h"
#include "socket.io-client-cpp/src/sio_socket.h"
#include "socket.io-client-cpp/src/sio_message.h"

#define DLL_API extern "C" __declspec(dllexport)

/*******************************************************************************
    global variable and User info management
********************************************************************************/
sio::client g_SocketClient;
struct UserInfo
{
    char userAccount[100];
    char token[100];
} g_loginInfo;

UserInfo* gp_loginInfo = NULL;
bool g_bIsSocketConnected = false;

/*******************************************************************************
    Callback and Register callback fucntion
********************************************************************************/
//typedef std::function<void(const std::string&)> ClientCallback;
typedef void (*ClientCallback)(const std::string&);
ClientCallback g_callback = NULL;

DLL_API
void RegisterCallback(ClientCallback cb)
{
    printf("RegisterCallback()");
    g_callback = cb;
    g_callback("welcome");
    printf("RegisterCallback() done");
}


/*******************************************************************************
    connection, disconectio

********************************************************************************/
void OnOpened();
void OnOpenFailed();
void OnReconnecting();
void OnReconnected(unsigned, unsigned);
void OnClosed(sio::client::close_reason const& reason);

void OnSocketOpened(std::string const& nsp);
void OnSocketClosed(std::string const& nsp);

DLL_API
void DoConnect(const std::string url) 
{
    printf("DoConnect()");
    if (g_bIsSocketConnected == true || gp_loginInfo != NULL)
    {
        return;
    }

    g_SocketClient.set_open_listener(OnOpened);
    g_SocketClient.set_fail_listener(OnOpenFailed);
    g_SocketClient.set_reconnecting_listener(OnReconnecting);
    g_SocketClient.set_reconnect_listener(OnReconnected);
    g_SocketClient.set_close_listener(OnClosed);

    g_SocketClient.set_socket_open_listener(OnSocketOpened);
    g_SocketClient.set_socket_close_listener(OnSocketClosed);

    g_SocketClient.set_reconnect_attempts(3);
    g_SocketClient.set_reconnect_delay(2000);

    g_SocketClient.connect(url);
    printf("DoConnect() Done!");
}

DLL_API
void DoDisconnect()
{
    g_SocketClient.close();
}

void OnOpened()
{
    printf("OnOpened()");

    DoDisconnect();
}

void OnOpenFailed()
{
    printf("OnOpened()");
}
void OnReconnecting()
{
    printf("OnOpened()");
}
void OnReconnected(unsigned, unsigned)
{
    printf("OnOpened()");
}
void OnClosed(sio::client::close_reason const& reason)
{
    printf("OnOpened() %d", reason);
}

void OnSocketOpened(std::string const& nsp)
{
    printf("OnSocketOpened() (%s)", nsp.c_str());
}
void OnSocketClosed(std::string const& nsp)
{
    printf("OnSocketClosed() (%s)", nsp.c_str());
}

/*******************************************************************************
    login function and callback
********************************************************************************/
DLL_API
void DoLogin(const std::string account, const std::string password)
{
    // {'client_acc':'xxx', 'password':'abc'}
    char message_json[1000];
    memset(message_json, 0x00, 1000);
    sprintf(message_json, "{'client_acc':%s, 'password':%s}", account.c_str(), password.c_str());
    g_SocketClient.socket()->emit("CLIENT_LOGIN", sio::string_message::create(message_json));
}

/*******************************************************************************
    send the messsage to server including user and session
********************************************************************************/
//DLL_API
//void SendMessage(const char* message_json)
//{
//    g_SocketClient.socket()->emit("CLIENT_LOGIN", sio::string_message::create(message_json));
//
//}