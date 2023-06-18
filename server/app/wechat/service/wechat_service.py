import requests
from ..config import appId, appSecret


class WechatService:

    def __init__(self):
        pass

    def get_session(self, code: any) -> any:
        """
        https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
        :param code:
        :param db:
        :return:
        """
        url = 'https://api.weixin.qq.com/sns/jscode2session?grant_type=authorization_code' + '&appid=' + appId + '&secret=' + appSecret + '&js_code=' + code
        res = requests.get(url)
        res_data = res.json()
        session_key = res_data['session_key']
        unionid = res_data['unionid']
        openid = res_data['openid']
        errmsg = res_data['errmsg']
        print(res_data)
        return res_data

    def get_access_token(self) -> any:
        """
        https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/mp-access-token/getAccessToken.html
        :return:
        """
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential' + '&appid=' + appId + '&secret=' + appSecret
        res = requests.get(url)
        res_data = res.json()
        access_token = res_data['access_token']
        expires_in = res_data['expires_in']
        print(access_token)
        return access_token

    def get_user_phone(self, access_token: str, code: any) -> any:
        """
        https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-info/phone-number/getPhoneNumber.html
        :param access_token:
        :param code:
        :return:
        """
        url = 'https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token=' + access_token
        data = {
            'code': code
        }
        res = requests.post(url=url, json=data)
        res_data = res.json()
        phone_info = res_data['phone_info']
        phone = phone_info['phoneNumber']

        return phone


wechat_service = WechatService()
