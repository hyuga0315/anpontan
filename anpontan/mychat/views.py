from django.shortcuts import render, redirect
from urllib.parse import unquote
from . import models
import urllib.parse
from .models import Room
from django.core.files.storage import FileSystemStorage

def startView(request):
    template_file='mychat/start.html'
    
    # ここまでで処理が終わらなければ、メイン画面を表示
            
    return render(request, template_file)



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
    group_id = request.POST.get("group_id", "")

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
                group_id=group_id  # グループ情報を保存
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

def mainView(request):
    template_file_1 = "mychat/main_1.html"
    template_file_2 = "mychat/main_2.html"
    back_file = "mychat/start.html"
    error_message = []

    # [1] クッキーからユーザ名を取得
    cookie_value = request.COOKIES.get('USER')
    value = urllib.parse.unquote(cookie_value) if cookie_value else None

    # [2] ユーザ名が取得できた場合
    if value:
        user = models.User.objects.filter(name__exact=value).first()

        if user and user.islogin:
            # ルームリストを取得
            roomlist = Room.objects.all()  # すべてのルームを取得
            # グループIDに応じてメイン画面に遷移
            template_file = template_file_1 if user.group_id == "1" else template_file_2
            return render(request, template_file, {"user": user, "roomlist": roomlist})
        else:
            # ログイン状態でない場合、クッキーを削除してログイン画面に遷移
            response = render(request, back_file)
            response.delete_cookie('USER')
            return response
        
    # [3] フォームデータの処理
    name = request.POST.get("name", "").strip()
    password = request.POST.get("password", "").strip()
    login = request.POST.get("login", "off")

    if login != 'on':
        error_message.append("ログインフラグが有効ではありません")
        return render(request, back_file, {"error_message": error_message})

    if not name:
        error_message.append("ユーザー名が入力されていません")
    if not password:
        error_message.append("パスワードが入力されていません")
    if error_message:
        return render(request, back_file, {"error_message": error_message})

    # [4] ユーザ認証
    user_info = models.User.objects.filter(name__exact=name, password__exact=password).first()
    if not user_info:
        error_message.append("ユーザー名、パスワードが一致しません")
        return render(request, back_file, {"error_message": error_message})

    # [5] ログイン状態を更新
    user_info.islogin = True
    user_info.save()

    # [6] クッキー設定とメイン画面への遷移
    response = render(
        request, template_file_1 if user_info.group_id == "1" else template_file_2, {"user": user_info}
    )
    response.set_cookie('USER', urllib.parse.quote(name))
    return response

def logout(request):
    # クッキーからユーザ情報取得
    value = request.COOKIES.get('USER')

    if value:
        value_data = urllib.parse.unquote(value)
        user = models.User.objects.filter(name__exact=value_data).first()
        if user:
            user.islogin = False
            user.save()

    # クッキーを削除してスタート画面にリダイレクト
    response = redirect('/mychat')
    response.delete_cookie('USER')
    return response

def createRoom(request):
    template_file = "mychat/createroom.html"
    error_message = []

    if request.method == "POST":
        room_name = request.POST.get("name", "").strip()
        if not room_name:
            error_message.append("ルーム名を入力してください。")
        elif Room.objects.filter(name=room_name).exists():
            error_message.append("このルーム名は既に使用されています。")
        else:
            Room.objects.create(name=room_name)
            return redirect('mychat:main')  # 作成後にメイン画面にリダイレクト

    return render(request, template_file, {"error_message": error_message})

def addRoom(request):
    template_file="mychat/addroom.html"
    message=[]
    error_message=[]
    if "name" in request.POST:
        name=request.POST.get("name")
    #[2]
    if name is None or name == '':
        error_message.append("掲示板名が入力されていません")

    #[3]
    else:
        if models.Room.objects.filter(name__exact=name).exists():
            error_message.append("すでにその掲示板は存在します")
        else:
            room=models.Room.objects.create(
            name=name
            )
            room.save()
            message.append("掲示板"+name+"を作成しました")

    options = {
        'error_message':error_message,
        'message':message
        }
    return render(request, template_file, options)

def roomView(request,id=None):  

    template_file="mychat/room.html"
    room=None
    if id is not None:
        room = models.Room.objects.get(id=id)
    else:
        room = None

    if room is not None:
        options = {
            'room':room
        }        
    else:
        options = {
        }       

    return render(request,template_file,options)

def searchView(request):
    template_file = "mychat/serch.html"
    query = request.GET.get('q', '')

    try:
        if query:
            roomlist = models.Room.objects.filter(name__icontains=query)  # 検索キーワードが含まれている掲示板を取得
        else:
            roomlist = models.Room.objects.all()  # 検索クエリがない場合はすべての掲示板を表示
        # ログで確認
        print("Room list:", roomlist)
        options = {
            'roomlist': roomlist
        }
        return render(request, template_file)
    except Exception as e:
        print("Error in serchView:", e)  # エラーの詳細を出力
        raise
