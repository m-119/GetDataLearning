import scrapy
import re
import json
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
from urllib.parse import urlencode
from copy import deepcopy


class InstagramcomSpider(scrapy.Spider):

    name = 'instagramcom'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    inst_login = 'ne_nulls'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:9:1624645851:AVdQAMeQ4qH7XbrBOcXQKKUhJ6pAq3dW/3CvbTdkFGtILB80NANlEpKO3mgozn6P6M5/UKHDjW9LQuM+rfLdntf/IWMrRVI80nzkFr9tx2xiVk/2Yldq071/Z485RdJEfk/VDn97LdME8nmVAFRwixHlYA=='
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'

    graphql_url = 'https://www.instagram.com/graphql/query/?'

    subscribers = 'HnJp4H2YIWTkwFSK8BYAIHST45kM65fJ'
    subscriptions = 'HnJp4H2YIWTkwFSK8BYAIHST45kM65fJ'

    def __init__(self, users_list):
        self.parse_users = users_list

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for user in self.parse_users:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_data_parse,
                    cb_kwargs={'username': user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables={'id': user_id,
                   'username': username,
                   'first': 12}

        url_subscribers = f'{self.graphql_url}query_hash={self.subscribers}&{urlencode(variables)}'
        yield response.follow(
            url_subscribers,
            callback=self.subscribers_parse,
            cb_kwargs={'user_id': user_id,
                       'username': username,
                       'variables': deepcopy(variables)
                       }
        )

        url_subscriptions = f'{self.graphql_url}query_hash={self.subscriptions}&{urlencode(variables)}'
        yield response.follow(
            url_subscriptions,
            callback=self.subscriptions_parse,
            cb_kwargs={'user_id': user_id,
                       'username': username,
                       'variables': deepcopy(variables)
                       }

        )

    def subscribers_parse(self, response, user_id, username, variables):
        j_body = json.loads(response.text)
        page_info = j_body.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']

            url_subscribers = f'{self.graphql_url}query_hash={self.subscribers_hash}&{urlencode(variables)}'

            yield response.follow(
                url_subscribers,
                callback=self.subscribers_parse,
                cb_kwargs={'user_id': user_id,
                           'username': username,
                           'variables': deepcopy(variables)}
            )

        subscribers = j_body.get('data').get('user').get('edge_followed_by').get('edges')
        for subscriber in subscribers:
            item = InstaparserItem(
                source_id=user_id,
                source_name=username,
                user_id=subscriber['node']['id'],
                user_name=subscriber['node']['username'],
                user_fullname=subscriber['node']['full_name'],
                photo=subscriber['node']['profile_pic_url'],
                subs_type='subscriber'
            )

            yield item

    def subscriptions_parse(self, response, user_id, username, variables):
        j_body = json.loads(response.text)
        page_info = j_body.get('data').get('user').get('edge_follow').get('page_info')
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']

            url_subscriptions = f'{self.graphql_url}query_hash={self.subscriptions_hash}&{urlencode(variables)}'

            yield response.follow(
                url_subscriptions,
                callback=self.subscriptions_parse,
                cb_kwargs={'user_id': user_id,
                           'username': username,
                           'variables': deepcopy(variables)}
            )

        subscriptions = j_body.get('data').get('user').get('edge_follow').get('edges')
        for subscription in subscriptions:
            item = InstaparserItem(
                source_id=user_id,
                source_name=username,
                user_id=subscription['node']['id'],
                user_name=subscription['node']['username'],
                user_fullname=subscription['node']['full_name'],
                photo=subscription['node']['profile_pic_url'],
                subs_type='subscription'
            )

            yield item

    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')