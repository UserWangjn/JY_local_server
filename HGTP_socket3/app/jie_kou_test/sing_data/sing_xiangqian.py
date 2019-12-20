import base64
from Crypto.Cipher import AES
import json
import requests
class AESCipher:
    def __init__(self,key):
        # self.key = 'Jy_ApP_0!9i+90&#'[0:16] #只截取16位
        self.key = key[0:16].encode('utf-8') #只截取16位
        self.iv = "2015030120123456".encode('utf-8') # 16位字符，用来填充缺失内容，可固定值也可随机字符串，具体选择看需求。
    def __pad(self, text):
        """填充方式，加密内容必须为16字节的倍数，若不足则使用self.iv进行填充"""
        text_length = len(text)
        amount_to_pad = AES.block_size - (text_length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = chr(amount_to_pad)
        return (text + pad * amount_to_pad).encode('utf-8')
    def __unpad(self, text):
        pad = ord(text[-1])
        return text[:-pad]
    def encrypt(self, raw):
        """加密"""
        raw = self.__pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return base64.b64encode(cipher.encrypt(raw))
    def decrypt(self, enc):
        """解密"""
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv )
        return self.__unpad(cipher.decrypt(enc).decode("utf-8"))
class hengfeng_w_sing(object):
    #参数是请求中的reqData，字典格式，
    def __init__(self, data, xq_path='http://xq-app-server.jc1.jieyue.com/xqAppServer/api/APPBizRest/sign/v1/'):
        self.url_sing = xq_path
        self.crypt = AESCipher('Jy_ApP_0!9i+90&#')
        if type(data) not in [list, dict]:
            self.data=json.dumps(data)
        else:
            self.data=data
    #返回直接可以调用的json字符串
    def sign_return(self, key=None):
        self.header_data={"Content-Type": "application/json"}
        if key in self.data:
            self.header_data['reqJSON'] = self.data.get(key)
        self.header_data['reqJSON'] = json.dumps(self.data)
        k = requests.post(self.url_sing, data=json.dumps(self.data), headers=self.header_data)
        print(k.text)
#        print(self.crypt.decrypt(json.loads(k.text)['aesResponse']))
        return json.loads(k.text)['responseBody']['sign']


if __name__ == '__main__':
    e = AESCipher('abcdnnnnnn123456')
    enc_str = e.encrypt('123456')
    print(enc_str)
    dec_str = e.decrypt(enc_str)
    print(dec_str)
