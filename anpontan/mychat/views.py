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
    template_file = "mychat/adduser.html"

    # 空のリスト
    message = []
    error_message = []
    
    # 入力データを取得し、それぞれ代入
    name = request.POST.get("name", "")
    password = request.POST.get("password", "")
    group_id = request.POST.get("group", "")

    # ユーザ名が未記入か空文字の時エラーメッセージ
    if not name:
        error_message.append("ユーザ名が未記入です")

    # パスワードが未記入か空文字の時エラーメッセージ
    if not password:
        error_message.append("パスワードが未記入です")

    # グループ選択が未選択または無効な値の時エラーメッセージ
    if not group_id:
        error_message.append("グループを選択してください")
    else:
        try:
            group_id = int(group_id)
            if group_id not in [1, 2]:  # 有効なグループIDを指定
                error_message.append("無効なグループが選択されました")
        except ValueError:
            error_message.append("無効なグループが選択されました")

    # エラーメッセージが0件の時
    if not error_message:
        # データベースからユーザ名が完全一致するユーザ情報を取得する
        target = models.User.objects.filter(name__exact=name).first()
        if target is not None:
            error_message.append("すでにそのユーザは存在します")
        else:
            # 新しいユーザを登録
            newinstance = models.User.objects.create(
                name=name,
                password=password,
                group=group_id  # グループ情報を保存
            )
            newinstance.save()
            message.append(f"ユーザ {name} を登録しました (グループ: {'起業ユーザ' if group_id == 1 else '就活ユーザ'})")

    # 受け渡しデータ
    options = {
        'message': message,
        'error_message': error_message,
    }

    # テンプレートを表示する
    return render(request, template_file, options)
