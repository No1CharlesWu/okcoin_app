import websocket
import zlib


def websocket_ticker(symbol='btc', event='addChannel', binary=True):
    channel = 'ok_sub_spotcny_' + symbol + '_ticker'
    return str({'event': event, 'channel': channel, 'binary': str(binary)})


def websocket_incremental_depth(symbol='btc', event='addChannel', binary=True):
    channel = 'ok_sub_spot_' + symbol + '_depth'
    return str({'event': event, 'channel': channel, 'binary': str(binary)})


def websocket_depth(symbol='btc', size=20, event='addChannel', binary=True):
    channel = 'ok_sub_spotcny_' + symbol + '_depth_' + str(size)
    return str({'event': event, 'channel': channel, 'binary': str(binary)})


def websocket_trades(symbol='btc', event='addChannel', binary=True):
    channel = 'ok_sub_spotcny_' + symbol + '_trades'
    return str({'event': event, 'channel': channel, 'binary': str(binary)})


def websocket_kline(symbol='btc', time='1min', event='addChannel', binary=True):
    channel = 'ok_sub_spotcny_' + symbol + '_kline_' + time
    return str({'event': event, 'channel': channel, 'binary': str(binary)})


def on_open(self):
    # self.send(websocket_ticker())
    # self.send(websocket_incremental_depth())
    # self.send(websocket_depth('btc', 20))
    # self.send(websocket_trades())
    self.send(websocket_kline('btc', 'week'))


def inflate(data):
    decompress = zlib.decompressobj(
        -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated


def on_message(self, evt):
    if type(evt) == bytes:
        evt = inflate(evt)  # data decompress

    print(evt)


def on_error(self, evt):
    print(evt)


def on_close(self, evt):
    print('DISCONNECT')


if __name__ == "__main__":
    url = "wss://real.okcoin.cn:10440/websocket/okcoinapi"
    api_key = 'c3b622bc-8255-40f2-9585-138928ae376d'
    secret_key = '7C1DDC1745C93B87BE1643A689938459'

    websocket.enableTrace(False)
    host = url
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
