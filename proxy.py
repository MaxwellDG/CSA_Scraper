# from browsermobproxy import Server
# 
# class ProxyManager:
# 
#     __BMP = "C:/Users/Max/Documents/BrowserMob/browsermob-proxy-2.1.4/bin/browsermob-proxy.bat"
# 
#     def __init__(self):
#         self.__server = Server(ProxyManager.__BMP)
#         self.__client = None
# 
#     def start_server(self):
#         self.__server.start()
#         return self.__server
# 
#     def start_client(self):
#         self.__client = self.__server.create_proxy(
#             params={"trustAllServers": True, 'captureHeaders': True, 'captureContent':True}) #remove params and test without
#         return self.__client
# 
#     @property
#     def client(self):
#         return self.client
# 
#     @property
#     def server(self):
#         return self.__server

