from flask import Flask, jsonify
from bit import PrivateKeyTestnet
from bit import PrivateKey

# cTcUTVZg83NxsLceNGbwm1vweucqyyNeSvLuFoYuwxdFp6kkMD44
# 1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g

# muZWv4sxadbPpQcXbuS4owxo2qNp6d3hWt
# cUHB1WA5Ap7uMhmHq8SHEX1FukTQop76kqMGBQhoZSBvxnDihjdW

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'God is light'


@app.route('/create/<network>', methods=['GET'])
def create(network):

    if network == 'mainnet':
        key = PrivateKey()
    else:
        key = PrivateKeyTestnet()

    return jsonify({
        "version": key.version,
        "address": key.address,
        "wif": key.to_wif(),
    })


@app.route('/info/<network>/<wif>', methods=['GET'])
def info(wif, network):

    if network == 'mainnet':
        key = PrivateKey(wif)
    else:
        key = PrivateKeyTestnet(wif)

    return jsonify({
        "version": key.version,
        "address": key.address,
        "wif": key.to_wif(),
        "balance": key.get_balance('btc'),
        "trnx": key.get_transactions(),
    })


@app.route('/send/<network>/<wif>/<to>/<value>', methods=['POST'])
def send(wif, to, value, network):

    if network == 'mainnet':
        key = PrivateKey(wif)
    else:
        key = PrivateKeyTestnet(wif)

    outputs = [(to, value, 'btc')]

    tx_hash = key.send(outputs)

    return jsonify({
        "hash": tx_hash,
    })


if __name__ == "__main__":
    app.run(debug=True)
