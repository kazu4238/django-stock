from django.shortcuts import render

Mytoken = "pk_be483a022b2f4e7699de538fc0131481"

# home関数の追加
# render関数は、第二引数に指定したテンプレートを読み込み、テンプレートに記述されている
# データを表示できるように変換する処理を行う。
# 第三引数に、辞書型を指定することで、テンプレートで{{}}という形で
# 値を埋め込めるようにできます。(今回は空)
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
        return render(request,'home.html',{'api':api,'SymbolNameListForm':SymbolNameListForm})
    else:
        return render(request,'home.html',{'SymbolNameListForm':SymbolNameListForm})
