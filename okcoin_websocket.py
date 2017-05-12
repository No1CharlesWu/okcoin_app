import websocket
import zlib
import json
import datetime
from data_filter import global_data_filter


def websocket_ticker(symbol='btc', event='addChannel', binary=True):
    channel = 'ok_sub_spotcny_' + symbol + '_ticker'
    return {'event': event, 'channel': channel, 'binary': str(binary)}


def websocket_incremental_depth(symbol='btc', event='addChannel', binary=True):
    channel = 'ok_sub_spot_' + symbol + '_depth'
    return {'event': event, 'channel': channel, 'binary': str(binary)}


def websocket_depth(symbol='btc', size=60, event='addChannel', binary=True):
    channel = 'ok_sub_spotcny_' + symbol + '_depth_' + str(size)
    return {'event': event, 'channel': channel, 'binary': str(binary)}


def websocket_trades(symbol='btc', event='addChannel', binary=True):
    channel = 'ok_sub_spotcny_' + symbol + '_trades'
    return {'event': event, 'channel': channel, 'binary': str(binary)}


def websocket_kline(symbol='btc', time='1min', event='addChannel', binary=True):
    channel = 'ok_sub_spotcny_' + symbol + '_kline_' + time
    return {'event': event, 'channel': channel, 'binary': str(binary)}


def on_open(self):
    l = list()
    l.append(websocket_ticker())
    l.append(websocket_depth())
    l.append(websocket_trades())
    l.append(websocket_kline())
    self.send(str(l))


def inflate(data):
    decompress = zlib.decompressobj(
        -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated


def on_message(self, evt):
    if type(evt) == bytes:
        evt = str(inflate(evt), 'utf-8')  # data decompress
    data = json.loads(evt)[0]
    # print(datetime.now(), data)
    global_data_filter.websocket_add_data(data)
    print('--------------------------------------------')
    # for i, d in enumerate(global_data_filter.get_kline_list()):
    #     print(i, datetime.datetime.fromtimestamp(d['timestamp']/1000), d)
    # for i, d in enumerate(global_data_filter.get_trades_list()):
    #     print(i, d)


def on_error(self, error):
    print(error)
    websocket_start()


def on_close(self):
    print('DISCONNECT')
    websocket_start()


def websocket_start():
    url = "wss://real.okcoin.cn:10440/websocket/okcoinapi"
    api_key = 'c3b622bc-8255-40f2-9585-138928ae376d'
    secret_key = '7C1DDC1745C93B87BE1643A689938459'
    websocket.enableTrace(True)
    host = url
    ws = websocket.WebSocketApp(host, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(ping_interval=20)


if __name__ == "__main__":
    websocket_start()
