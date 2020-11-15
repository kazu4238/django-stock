from django.shortcuts import render

# home関数の追加
# render関数は、第二引数に指定したテンプレートを読み込み、テンプレートに記述されている
# データを表示できるように変換する処理を行う。
# 第三引数に、辞書型を指定することで、テンプレートで{{}}という形で
# 値を埋め込めるようにできます。(今回は空)
def home(request):
    return render(request,'hoge.html',{})
