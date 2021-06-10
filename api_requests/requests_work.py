import ast
import http
import json
import re
import time

import requests, os
from http.cookiejar import MozillaCookieJar


class OkjikeRequests:
    def __init__(self):
        self.session = requests.session()

        path = 'cookies.txt'  # 设置cookies文件保存路径
        s = MozillaCookieJar(path)
        os.path.isfile(path) and s.load(path, ignore_discard=True, ignore_expires=True)  # 存在文件则载入
        self.session.cookies = s  # 使用MozillaCookieJar进行会话管理

    def get_sms_code(self):
        url = 'https://web-api.okjike.com/api/graphql'
        data = {
            'operationName': 'GetSmsCode',
            'query': "mutation GetSmsCode($mobilePhoneNumber: String!, $areaCode: String!)"
                     "{getSmsCode(action: PHONE_MIX_LOGIN, mobilePhoneNumber: $mobilePhoneNumber, areaCode: $areaCode) "
                     "{action __typename}}",
            'variables': {'mobilePhoneNumber': '18380477311', 'areaCode': '+86'},
            'areaCode': '+86',
            'mobilePhoneNumber': '18380477311'
        }
        data2 = json.dumps(data)
        header = {'Content-Type': 'application/json'}
        print(data2)
        response = self.session.post(url=url, data=data2, headers=header, verify=False)
        self.session.cookies.save(ignore_discard=True, ignore_expires=True)
        # result = response.json()
        print(response.text)  # {"data":{"getSmsCode":{"action":"LOGIN","__typename":"GetSmsCodeResponse"}}}

    def mix_login_with_phone(self):
        url = 'https://web-api.okjike.com/api/graphql'
        data = {
            'operationName': 'MixLoginWithPhone',
            'query': "mutation MixLoginWithPhone($smsCode: String!, $mobilePhoneNumber: String!, $areaCode: String!) "
                     "{mixLoginWithPhone(smsCode: $smsCode, mobilePhoneNumber: $mobilePhoneNumber, areaCode: $areaCode) "
                     "{isRegister user {distinctId: id ...TinyUserFragment __typename}__typename}}"
                     "fragment TinyUserFragment on UserInfo {avatarImage {thumbnailUrl smallPicUrl picUrl __typename}"
                     "username screenName briefIntro __typename}",
            'variables': {'smsCode': '351147', 'mobilePhoneNumber': '18380477311', 'areaCode': '+86'},
            'areaCode': '+86',
            'mobilePhoneNumber': '18380477311',
            'smsCode': '960281'
        }
        data2 = json.dumps(data)
        header = {'Content-Type': 'application/json'}
        # print(data2)
        response = self.session.post(url=url, data=data2, headers=header, verify=False)
        self.session.cookies.save(ignore_discard=True, ignore_expires=True)
        # result = response.json()
        print(response.json())

    def topic_feeds(self):
        url = 'https://web-api.okjike.com/api/graphql'
        data = {
            'operationName': 'TopicHotFeeds',
            'query': 'query TopicHotFeeds($topicId: ID!, $loadMoreKey: JSON) {   topic(topicId: $topicId) {     id     selectedFeeds(loadMoreKey: $loadMoreKey) {       ...BasicFeedItem       __typename     }     __typename   } }  fragment BasicFeedItem on FeedsConnection {   pageInfo {     loadMoreKey     hasNextPage     __typename   }   nodes {     ... on ReadSplitBar {       id       type       text       __typename     }     ... on MessageEssential {       ...FeedMessageFragment       __typename     }     ... on UserAction {       id       type       action       actionTime       ... on UserFollowAction {         users {           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           __typename         }         allTargetUsers {           ...TinyUserFragment           following           statsCount {             followedCount             __typename           }           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           __typename         }         __typename       }       ... on UserRespectAction {         users {           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           __typename         }         targetUsers {           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           ...TinyUserFragment           __typename         }         content         __typename       }       __typename     }     __typename   }   __typename }  fragment FeedMessageFragment on MessageEssential {   ...EssentialFragment   ... on OriginalPost {     ...LikeableFragment     ...CommentableFragment     ...RootMessageFragment     ...UserPostFragment     ...MessageInfoFragment     pinned {       personalUpdate       __typename     }     __typename   }   ... on Repost {     ...LikeableFragment     ...CommentableFragment     ...UserPostFragment     ...RepostFragment     pinned {       personalUpdate       __typename     }     __typename   }   ... on Question {     ...UserPostFragment     __typename   }   ... on OfficialMessage {     ...LikeableFragment     ...CommentableFragment     ...MessageInfoFragment     ...RootMessageFragment     __typename   }   __typename }  fragment EssentialFragment on MessageEssential {   id   type   content   shareCount   repostCount   createdAt   collected   pictures {     format     watermarkPicUrl     picUrl     thumbnailUrl     smallPicUrl     width     height     __typename   }   urlsInText {     url     originalUrl     title     __typename   }   __typename }  fragment LikeableFragment on LikeableMessage {   liked   likeCount   __typename }  fragment CommentableFragment on CommentableMessage {   commentCount   __typename }  fragment RootMessageFragment on RootMessage {   topic {     id     content     __typename   }   __typename }  fragment UserPostFragment on MessageUserPost {   readTrackInfo   user {     ...TinyUserFragment     __typename   }   __typename }  fragment TinyUserFragment on UserInfo {   avatarImage {     thumbnailUrl     smallPicUrl     picUrl     __typename   }   username   screenName   briefIntro   __typename }  fragment MessageInfoFragment on MessageInfo {   video {     title     type     image {       picUrl       __typename     }     __typename   }   linkInfo {     originalLinkUrl     linkUrl     title     pictureUrl     linkIcon     audio {       title       type       image {         thumbnailUrl         picUrl         __typename       }       author       __typename     }     video {       title       type       image {         picUrl         __typename       }       __typename     }     __typename   }   __typename }  fragment RepostFragment on Repost {   target {     ...RepostTargetFragment     __typename   }   targetType   __typename }  fragment RepostTargetFragment on RepostTarget {   ... on OriginalPost {     id     type     content     pictures {       thumbnailUrl       __typename     }     topic {       id       content       __typename     }     user {       ...TinyUserFragment       __typename     }     __typename   }   ... on Repost {     id     type     content     pictures {       thumbnailUrl       __typename     }     user {       ...TinyUserFragment       __typename     }     __typename   }   ... on Question {     id     type     content     pictures {       thumbnailUrl       __typename     }     user {       ...TinyUserFragment       __typename     }     __typename   }   ... on Answer {     id     type     content     pictures {       thumbnailUrl       __typename     }     user {       ...TinyUserFragment       __typename     }     __typename   }   ... on OfficialMessage {     id     type     content     pictures {       thumbnailUrl       __typename     }     __typename   }   ... on DeletedRepostTarget {     status     __typename   }   __typename } ',
            'variables': {'topicId': '557ed045e4b0a573eb66b751'}
        }
        data2 = json.dumps(data)
        header = {'Content-Type': 'application/json'}
        response = self.session.post(url=url, data=data2, headers=header, verify=False)
        self.session.cookies.save(ignore_discard=True, ignore_expires=True)
        # result = response.json()
        # print(response.json())
        nodes = response.json()['data']['topic']['selectedFeeds']['nodes']
        # for i in range(len(nodes)):
        #     content = nodes[i]['content']
        #     print(f'第{i + 1}条：\n', content)
        #     if nodes[i]['pictures'] == []:
        #         print('=' * 50, '\n')
        #     else:
        #         pictures = nodes[i]['pictures']
        #         for n in range(len(pictures)):
        #             pictures_url = pictures[n]['picUrl']
        #             print(n, pictures_url)
        #         print('=' * 50, '\n')
        time = self.get_date()
        num = int(time[-1])
        # print(num)
        content = nodes[num]['content']
        pic_lis = []
        pictures = nodes[num]['pictures']
        for n in range(len(pictures)):
            pictures_url = pictures[n]['picUrl']
            pic_lis.append(pictures_url)
        return content, pic_lis

    def news(self):
        url = 'https://web-api.okjike.com/api/graphql'
        data = {
            'operationName': 'TopicFeeds',
            'query': "query TopicFeeds($topicId: ID!, $loadMoreKey: JSON) {\n  topic(topicId: $topicId) {\n    id\n    feeds(loadMoreKey: $loadMoreKey) {\n      ...BasicFeedItem\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment BasicFeedItem on FeedsConnection {\n  pageInfo {\n    loadMoreKey\n    hasNextPage\n    __typename\n  }\n  nodes {\n    ... on ReadSplitBar {\n      id\n      type\n      text\n      __typename\n    }\n    ... on MessageEssential {\n      ...FeedMessageFragment\n      __typename\n    }\n    ... on UserAction {\n      id\n      type\n      action\n      actionTime\n      ... on UserFollowAction {\n        users {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        allTargetUsers {\n          ...TinyUserFragment\n          following\n          statsCount {\n            followedCount\n            __typename\n          }\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        __typename\n      }\n      ... on UserRespectAction {\n        users {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        targetUsers {\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          ...TinyUserFragment\n          __typename\n        }\n        content\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment FeedMessageFragment on MessageEssential {\n  ...EssentialFragment\n  ... on OriginalPost {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...RootMessageFragment\n    ...UserPostFragment\n    ...MessageInfoFragment\n    pinned {\n      personalUpdate\n      __typename\n    }\n    __typename\n  }\n  ... on Repost {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...UserPostFragment\n    ...RepostFragment\n    pinned {\n      personalUpdate\n      __typename\n    }\n    __typename\n  }\n  ... on Question {\n    ...UserPostFragment\n    __typename\n  }\n  ... on OfficialMessage {\n    ...LikeableFragment\n    ...CommentableFragment\n    ...MessageInfoFragment\n    ...RootMessageFragment\n    __typename\n  }\n  __typename\n}\n\nfragment EssentialFragment on MessageEssential {\n  id\n  type\n  content\n  shareCount\n  repostCount\n  createdAt\n  collected\n  pictures {\n    format\n    watermarkPicUrl\n    picUrl\n    thumbnailUrl\n    smallPicUrl\n    width\n    height\n    __typename\n  }\n  urlsInText {\n    url\n    originalUrl\n    title\n    __typename\n  }\n  __typename\n}\n\nfragment LikeableFragment on LikeableMessage {\n  liked\n  likeCount\n  __typename\n}\n\nfragment CommentableFragment on CommentableMessage {\n  commentCount\n  __typename\n}\n\nfragment RootMessageFragment on RootMessage {\n  topic {\n    id\n    content\n    __typename\n  }\n  __typename\n}\n\nfragment UserPostFragment on MessageUserPost {\n  readTrackInfo\n  user {\n    ...TinyUserFragment\n    __typename\n  }\n  __typename\n}\n\nfragment TinyUserFragment on UserInfo {\n  avatarImage {\n    thumbnailUrl\n    smallPicUrl\n    picUrl\n    __typename\n  }\n  username\n  screenName\n  briefIntro\n  __typename\n}\n\nfragment MessageInfoFragment on MessageInfo {\n  video {\n    title\n    type\n    image {\n      picUrl\n      __typename\n    }\n    __typename\n  }\n  linkInfo {\n    originalLinkUrl\n    linkUrl\n    title\n    pictureUrl\n    linkIcon\n    audio {\n      title\n      type\n      image {\n        thumbnailUrl\n        picUrl\n        __typename\n      }\n      author\n      __typename\n    }\n    video {\n      title\n      type\n      image {\n        picUrl\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment RepostFragment on Repost {\n  target {\n    ...RepostTargetFragment\n    __typename\n  }\n  targetType\n  __typename\n}\n\nfragment RepostTargetFragment on RepostTarget {\n  ... on OriginalPost {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    topic {\n      id\n      content\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Repost {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Question {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on Answer {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    user {\n      ...TinyUserFragment\n      __typename\n    }\n    __typename\n  }\n  ... on OfficialMessage {\n    id\n    type\n    content\n    pictures {\n      thumbnailUrl\n      __typename\n    }\n    __typename\n  }\n  ... on DeletedRepostTarget {\n    status\n    __typename\n  }\n  __typename\n}\n",
            'variables': {'topicId': '553870e8e4b0cafb0a1bef68'}
        }
        data2 = json.dumps(data)
        header = {'Content-Type': 'application/json'}
        response = self.session.post(url=url, data=data2, headers=header, verify=False)
        self.session.cookies.save(ignore_discard=True, ignore_expires=True)
        # result = response.json()
        # print(response.json())
        nodes = response.json()['data']['topic']['feeds']['nodes']
        concent = nodes[0]['content']
        url = nodes[0]['urlsInText'][0]['url']
        return concent, url

    def get_date(self):
        date = time.strftime("%Y-%m-%d", time.localtime())  # 格式： 年-月-日
        return date
# if __name__ == '__main__':
#     test = OkjikeRequests()
#     # test.get_sms_code()
#     # test.mix_login_with_phone()
#     repones = test.topic_feeds()
#     # repones = test.news()
#     print(round(time.time()))


