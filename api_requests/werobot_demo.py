import os
import re

import werobot, requests, time
from urllib3 import encode_multipart_formdata
from werobot.client import Client
import requests_work, pic_dowload


class WerobotWork:
    def __init__(self):
        robot = werobot.WeRoBot(token='martin001')  # 微信公众平台配置设置的Token
        robot.config["APP_ID"] = "wxea71666b8d83f748"  # 微信公众平台的APP_ID
        robot.config["ENCODING_AES_KEY"] = "YMsC7mHdYuHgOTYvodslwwK8jvHeT7tlOSjHFAx05RE"
        robot.config["APP_SECRET"] = "f70f01d1ef613d5de795644b58d71872"

        self.client = werobot.client.Client(config=robot.config)  # 连接平台

    def weather(self):
        # 获取天气
        respones = requests.get(
            'https://api.seniverse.com/v3/weather/daily.json?key=ShbpOM8E7jVmKEr31&location=chengdu&language=zh-Hans&unit=c'
            '&start=-1&days=5')

        daily = respones.json()['results'][0]['daily']
        info = daily[0]
        text_day = info['text_day']
        text_night = info['text_night']
        high = info['high']
        low = info['low']
        weather_str = f'白天：【{text_day}】' + f'    夜间：【{text_night}】' + f'    气温：【{low}-{high}℃】'
        return weather_str

    def get_date(self):
        date = time.strftime("%Y-%m-%d", time.localtime())  # 格式： 年-月-日
        return date

    def get_pic_url(self, filename):
        """
        将本地图片上传至微信平台，并获取其URL地址
        :param filename:
        :return: 含有url地址的数组
        """
        token_result = self.client.token
        # print(token_result)

        filepath = f'./pic/{filename}'
        data = {'file': (f'{filename}', open(filepath, 'rb').read())}
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        header = {'Content-Type': encode_data[1]}
        pic_url = requests.post(url=f'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token_result}',
                                data=data, headers=header).json()
        return pic_url['url']

    def pic_dowload(self, url):
        """
        下载url对应的图片至本地
        :param url: 含有图片下载连接的列表
        :return: 含有下载完毕的本地文件名的列表
        """
        pic_dow = pic_dowload.down_pic
        file_name_lis = []
        for url in url:
            picname = round(time.time())
            # print('第%s个文件长在下载' % picname)
            pic_dow(url, picname)
            file_name = f'{picname}' + '.jpeg'
            file_name_lis.append(file_name)
            time.sleep(1)
        return file_name_lis

    def content(self):
        okjike = requests_work.OkjikeRequests()
        jike_data = okjike.topic_feeds()

        hot_word = re.sub('\n', '</br>', jike_data[0])  # 无用但有趣的冷知识文字处理

        wxpicurl_lis = []
        if jike_data[1]:
            file_name_lis = self.pic_dowload(jike_data[1])
            for i in range(len(file_name_lis)):
                wxpicurl = self.get_pic_url(file_name_lis[i])
                wxpicurl_lis.append(wxpicurl)

        pic_tab = ''
        for n in range(len(wxpicurl_lis)):
            str_url = f'<p><img src="{wxpicurl_lis[n]}"></p>'
            pic_tab += str_url

        self.new_get = okjike.news()
        new_str = re.findall(r"2(.+)\（", self.new_get[0], re.S)
        new_out = re.sub('\n', '</br>', new_str[0])
        # print(new_out)
        content = f'<p>【今日天气】</p>' \
                  f'<p>{self.weather()}</p>' \
                  f'<hr />' \
                  f'<p></p></br>' \
                  f'<p>【一觉醒来世界发生了什么】</p>' \
                  f'<p>2{new_out}</p>' \
                  '<p>点击下方【阅读全文】获取详细内容</p>' \
                  f'<hr />' \
                  f'<p></p></br>' \
                  f'<p>【无用但有趣的冷知识】</p>' \
                  f'<p>{hot_word}</p>' \
                  f'<p></p>' \
                  f'{pic_tab}'
        return content

    def send_mpnews(self):
        date = self.get_date()

        articles = [{
            "thumb_media_id": "zQ0Y8Z3Tf4AFQK2ItHrd18aLy1drvOiNmvD_MHKs62BP5SwtzR0fjMBRBV7RPkpM",
            "author": "柚子",
            "title": f'Happy Day【{date}】',
            "content": f'{self.content()}',
            "content_source_url": f'{self.new_get[1]}',
            "digest": "柚子的每日冒泡~",
            "show_cover_pic": 1,
            "need_open_comment": 1,
            "only_fans_can_comment": 1
        }]
        news_response = self.client.upload_news(articles)
        self.client.send_mass_preview_to_user(msg_type='mpnews', content=news_response['media_id'], user='koko1216',
                                              user_type='wxname')
        # self.client.send_mass_preview_to_user(msg_type='mpnews', content=news_response['media_id'],
        #                                       user='zhang-xiaopengyou',
        #                                       user_type='wxname')
        # self.client.send_mass_preview_to_user(msg_type='mpnews', content=news_response['media_id'],
        #                                       user='dddys_hh',
        #                                       user_type='wxname')

        # print(i)


if __name__ == '__main__':
    new_send_mpnews = WerobotWork()
    new_send_mpnews.send_mpnews()
