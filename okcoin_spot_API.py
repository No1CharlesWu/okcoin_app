#!/usr/bin/python
# -*- coding: utf-8 -*-
# 用于访问OKCOIN 现货REST API
from http_MD5_util import build_sign, http_get, http_post


class OKCoinSpot:
    def __init__(self, url, api_key, secret_key):
        self.__url = url
        self.__api_key = api_key
        self.__secret_key = secret_key

    # 获取OKCOIN现货行情信息
    def ticker(self, symbol=''):
        ticker_resource = "/api/v1/ticker.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return http_get(self.__url, ticker_resource, params)

    # 获取OKCOIN现货市场深度信息
    def depth(self, **kwargs):
        depth_resource = "/api/v1/depth.do"
        params = '&'.join([k + '=' + str(v) for k, v in kwargs.items()])
        return http_get(self.__url, depth_resource, params)

    # 获取OKCOIN现货历史交易信息
    def trades(self, symbol=''):
        trades_resource = "/api/v1/trades.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return http_get(self.__url, trades_resource, params)

    def kline(self, symbol=''):
        kline_resource = "/api/v1/kline.do"
        params = ''
        if symbol:
            params = 'symbol=%(symbol)s' % {'symbol': symbol}
        return http_get(self.__url, kline_resource, params)

    # 获取用户现货账户信息
    def user_info(self):
        userinfo_resource = "/api/v1/userinfo.do"
        params = dict()
        params['api_key'] = self.__api_key
        params['sign'] = build_sign(params, self.__secret_key)
        return http_post(self.__url, userinfo_resource, params)

    # 现货交易
    def trade(self, symbol, trade_type, price='', amount=''):
        trade_resource = "/api/v1/trade.do"
        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'type': trade_type
        }
        if price:
            params['price'] = price
        if amount:
            params['amount'] = amount

        params['sign'] = build_sign(params, self.__secret_key)
        return http_post(self.__url, trade_resource, params)

    # 现货批量下单
    def batch_trade(self, symbol, trade_type, orders_data):
        batch_trade_resource = "/api/v1/batch_trade.do"
        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'type': trade_type,
            'orders_data': orders_data
        }
        params['sign'] = build_sign(params, self.__secret_key)
        return http_post(self.__url, batch_trade_resource, params)

    # 现货取消订单
    def cancel_order(self, symbol, order_id):
        cancel_order_resource = "/api/v1/cancel_order.do"
        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'order_id': order_id
        }
        params['sign'] = build_sign(params, self.__secret_key)
        return http_post(self.__url, cancel_order_resource, params)

    # 现货订单信息查询
    def order_info(self, symbol, order_id):
        order_info_resource = "/api/v1/order_info.do"
        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'order_id': order_id
        }
        params['sign'] = build_sign(params, self.__secret_key)
        return http_post(self.__url, order_info_resource, params)

    # 现货批量订单信息查询
    def orders_info(self, symbol, order_id, trade_type):
        orders_info_resource = "/api/v1/orders_info.do"
        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'order_id': order_id,
            'type': trade_type
        }
        params['sign'] = build_sign(params, self.__secret_key)
        return http_post(self.__url, orders_info_resource, params)

    # 现货获得历史订单信息
    def order_history(self, symbol, status, current_page, page_length):
        order_history_resource = "/api/v1/order_history.do"
        params = {
            'api_key': self.__api_key,
            'symbol': symbol,
            'status': status,
            'current_page': current_page,
            'page_length': page_length
        }
        params['sign'] = build_sign(params, self.__secret_key)
        return http_post(self.__url, order_history_resource, params)
