from django.shortcuts import render

def startView(request):
    template_file='mychat/start.html'
    
    options={
        
    }
    
    return render(request, template_file, options)


def createUser(request):
    template_file='mychat/createuser.html'
    
    options={
        
    }
    
    return render(request, template_file, options)

# ユーザ登録結果画面処理
def addUser(request):
    # テンプレートファイル
    template_file="mychat/adduser.html"

    #空のリスト
    message=[]
    error_message=[]
    
    #入力データを取得し、それぞれ代入
    if "name" in request.POST:
        name=request.POST.get("name")
    if "password" in request.POST: 
        password=request.POST.get("password")

    # ユーザ名が未記入か空文字の時エラーメッセージ
    if name is None or name == '':
        error_message.append("ユーザ名が未記入です") 

    # パスワードが未記入か空文字の時エラーメッセージ
    if password is None or password == '':
        error_message.append("パスワードが未記入です")


    #エラーメッセージが0件の時
    if len(error_message) == 0  :
        # データベースからユーザ名が完全一致するユーザ情報を取得する
        target=models.User.objects.filter(name__exact=name).first()
        # データを取得できた際、エラーメッセージの出力
        if target is not None:
            error_message.append("すでにそのユーザは存在します")
        # データが取得できないとき、新たに追加する
        if target is None:
            newinstance=models.User.objects.create(
                name=name,
                password=password
            )
            newinstance.save()
            message.append("ユーザ"+str(name)+"を登録しました")
    #受け渡しデータ
    options={
        'message':message,
        'error_message':error_message,
    }
    #テンプレートを表示する
    return render(request, template_file, options)
