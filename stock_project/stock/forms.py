from django import forms

import requests
import json

Mytoken = "pk_be483a022b2f4e7699de538fc0131481"

class SymbolNameListForm(forms.Form):
    # requests.get()で全ての銘柄を取得するアドレスを用いて、全ての銘柄を取得する
    api_list_request = requests.get("https://cloud.iexapis.com/beta/ref-data/symbols?token=" + Mytoken)
    api_list = json.loads(api_list_request.content)

    # タプルの作成　formでプルダウンリストを作成するには、タプル型に変換する必要がある
    # api_listはjson型なのでまず for i in api_list で各銘柄にiを代入し、その銘柄
    # の辞書型のデータから、各キー(symbol、name)を利用して値を取得していく
    # （"取得したい値", "ウェブ上で表示したい値"）となるようにタプル型を作成する
    symbol_name_tuple = [(i["symbol"],i["name"]) for i in api_list]

    # sortでタプルの１番目を基準に昇順に、リストの順番を分かりやすくするために
    # 小文字化してから並べ替える(デフォルトでは大文字優先のため)
    symbol_name_tuple = sorted(symbol_name_tuple,key=lambda t:t[1].lower())
    target_stock = forms.ChoiceField(label="選択してください",choices=symbol_name_tuple,required=False)





