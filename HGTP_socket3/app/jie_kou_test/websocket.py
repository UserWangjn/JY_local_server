# -*- encoding:utf-8 -*-
from app. import websocket
ws = websocket.WebSocket()
ws.connect("ws://127.0.0.1:5000/testnamespace", http_proxy_host="testnamespace", http_proxy_port=5000)


