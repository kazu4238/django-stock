from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

import matplotlib.pyplot as plt
import io
from django.http import HttpResponse

import pandas as pd

Mytoken = "pk_be483a022b2f4e7699de538fc0131481"


# home関数の追加
# render関数は、第二引数に指定したテンプレートを読み込み、テンプレートに記述されている
# データを表示できるように変換する処理を行う。
# 第三引数に、辞書型を指定することで、テンプレートで{{}}という形で
# 値を埋め込めるようにできる。(今回は空にする)
def home(request):
    from .forms import SymbolNameListForm
    import requests
    import json

    # formをインスタンス化
    SymbolNameListForm = SymbolNameListForm()

    if request.method == 'POST':
        # target_symbolに選択した銘柄記号が入ることでその銘柄記号のAPIが取得できるようにする
        target_symbol = request.POST['target_stock']
        # request.get(APIアドレス)でAPIデータをResponseオブジェクトとして取得している
        api_request = requests.get(
            "https://cloud.iexapis.com/stable/stock/" + target_symbol + "/quote?token=" + Mytoken)
        try:
            # 取得したAPIデータをjSON形式に変換して読み込み、変数apiに格納する
            api = json.loads(api_request.content)
        except Exception as e:
            api = "エラー"

        # form自体をhtmlに橋渡しできるようにする
        return render(request, 'home.html', {'api': api, 'SymbolNameListForm': SymbolNameListForm})
    else:
        return render(request, 'home.html', {'SymbolNameListForm': SymbolNameListForm})


# list_editがurlに入力された際に呼ばれる関数
def add_stock(request):
    import requests
    import json

    from .forms import SymbolNameListForm
    SymbolNameListForm = SymbolNameListForm()
    api = ""
    # このページ内で情報が送信された場合の処理（ブラウザで普通にアクセスした場合を除くため）
    if request.method == 'POST':

        # StockFormのインスタンス作成　引数にrequest.POSTを取ることによって、
        # POST送信されたフォームの情報が入る形になる
        form = StockForm(request.POST or None)
        # バルデーション処理
        if form.is_valid():
            # 新レコードが保存される
            form.save()
            # ユーザのアクションが成功した時にメッセージを通知する
            messages.success(request, "追加されました")
        return redirect('list_edit')

    else:
        # Stockモデルにある全てのレコードをモデルのインスタンスにしてそれを一つのセットとして取り出している
        stock_saved = Stock.objects.all()
        stock_list = []

        for target_symbol in stock_saved:
            print(target_symbol)
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" +
                                       str(target_symbol) + "/quote?token=" + Mytoken)
            try:
                api = json.loads(api_request.content)
                # 取得したapiに新しくidを割り振ることで、DB操作をしやすくする
                api["id"] = target_symbol.id
                # stock_listのリストにapiを追加する
                stock_list.append(api)

            except Exception as e:
                api = "error"
            print('api', api)

        return render(request, 'list_edit.html', {'stock_saved': stock_saved, 'stock_list': stock_list,
                                                  'api': api, 'SymbolNameListForm': SymbolNameListForm})


def delete(request, stock_id):
    # モデルから対象idの内容を取得
    item = Stock.objects.get(pk=stock_id)
    # 削除する
    item.delete()
    # ユーザのアクションが成功した時にメッセージを通知する
    messages.success(request, "削除されました")
    return redirect('list_edit')


def pandas_dr(request):
    import pandas_datareader as pdr
    pdr = pdr.stooq.StooqDailyReader(symbols='6701.jp', start='JAN-01-2010', end="JUN-26-2020").read().sort_values(
        by='Date', ascending=True)
    return redirect(request,'list_edit.html')



#グラフ作成 ローソク足で表示させるための一連の関数
def setPlt():
    import matplotlib
    # バックエンドを指定
    matplotlib.use('Agg')

    import pandas_datareader as pdr
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    from mpl_finance import candlestick_ohlc
    df = pdr.get_data_yahoo('AAPL', '2020-08-16', '2020-11-17')
    ax = plt.subplot()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    # ここでローソク足作成？
    candlestick_ohlc(ax, zip(mdates.date2num(df.index), df['Open'], df['High'], df['Low'], df['Close']), width=0.4)
    plt.title('apple')
    plt.savefig('stock.png')

# SVG化
def plt2svg():
    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    s = buf.getvalue()
    buf.close()
    return s

# 実行するビュー関数
def get_svg(request):
    setPlt()
    svg = plt2svg()  #SVG化
    plt.cla()  # グラフをリセット
    response = HttpResponse(svg, content_type='image/svg+xml')
    return response




