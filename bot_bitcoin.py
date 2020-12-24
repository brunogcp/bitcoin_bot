import ssl
import json

import websocket
import bitstamp.client

import credenciais


def cliente():
    return bitstamp.client.Trading(username=credenciais.USERNAME,
                                   key=credenciais.KEY,
                                   secret=credenciais.SECRET)


def vender(quantidade):
    trading_client = cliente()
    trading_client.buy_market_order(quantidade)


def comprar(quantidade):
    trading_client = cliente()
    trading_client.sell_market_order(quantidade)


def on_open(ws):
    print('Abriu a conexão')

    json_subiscribe = """
    {
        "event": "bts:subscribe",
        "data": {
            "channel": "live_trades_btcusd"
        }
    }
    """

    ws.send(json_subiscribe)


def on_close(ws):
    print('Fechou a conexão')


def on_error(ws, erro):
    print('Deu erro')
    print(erro)


def on_message(ws, mensagem):
    mensagem = json.loads(mensagem)
    price = mensagem['data']['price']
    print(price)

    if price > 22890:
        vender()
    elif price <22810:
        comprar()
    else:
        print('Aguardar')


if __name__ == '__main__':
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('wss://ws.bitstamp.net.',
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close
                                )
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
