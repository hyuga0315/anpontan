from django.shortcuts import render
from . import models
import urllib

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
def mainView(request):
    template_file="mychat/main_1.html"
    back_file="mychat/start.html"
    error_message=[]

    #[1] クッキー情報(後述)からユーザ名(USERをキー名とする)を取得する。 
    cookie_value = request.COOKIES.get('USER') 
    if cookie_value is not None:
        value = urllib.parse.unquote(cookie_value)
    else:
        value=None
    options={}
    #[2] ユーザ名を取得できた場合は、以下を行う。 
    if value is not None:
    #[2](1) データベースからそのユーザ名と完全一致するユーザ情報を取得する。 
        user = models.User.objects.filter(name__exact=value).first()
    #[2](2)ユーザ情報のログイン状態がログイン中(True)ならば認証処理は行わずにメイン画 
    #面に遷移する。（遷移パターンA） 
        if user is not None and user.islogin:
            roomlist=models.Room.objects.all()
            options={
                'roomlist':roomlist
            }
            return render(request,template_file,options)
    #[2](3)ユーザ情報のログイン状態がログイン中でない(False)場合、クッキーからユーザ名 
    #を削除(後述)してから、ログイン画面に遷移する（遷移パターンB） 
        else:
            response = render(request, back_file, options) 
            response.delete_cookie('USER')   # key は削除したいキー名が入る 
            return response 
    #[3] フォームのデータとしてユーザ名、パスワード、ログインフラグを取得し、内部変数user、 
    #password、login にそれぞれ代入する。ログインフラグが取得できなかった場合はNoneでは 
    #なく"off"を値として代入する。 
    if "name" in request.POST:
        name=request.POST.get("name")
    else:
        name = None
    if "password" in request.POST:
        password=request.POST.get("password")
    else:
        password = None
    if "login" in request.POST:
        login=request.POST.get("login")
    else:
        login = 'off' 

    #[4] ログインフラグが "on"ではない 時は、ログイン画面に遷移する。（遷移パターンC） 
    if login != 'on':
        #error_message.append("ここ")
        options = {"error_message":error_message}
        return render(request,back_file,options)

    #[5] ユーザ名が取得できない場合は「ユーザ名が入力されていません」というエラーメッセージ 
    #を用意する。 
    if name is None or name=='':
        error_message.append("ユーザー名が入力されていません")
    #[6] パスワードが取得できない場合は「パスワードが入力されていません」というエラーメッセージを用意する。
    if password is None or password=='':
        error_message.append("パスワードが入力されていません")
    #[7] [5][6]で入力エラーのメッセージが１つでも用意されたならば、それをテンプレートに渡す 
    #（遷移パターンD） 
    if len(error_message) > 0:
        errors = {'error_message':error_message}
        return render(request,back_file,errors)

    #[8] データベースから「ユーザ名」と「パスワード」の両方が完全一致するユーザ情報を取得する。
    user_info=models.User.objects.filter(name__exact=name,password__exact=password).first()
    #[9] 一致するユーザ情報が取得できなかった場合は、「ユーザ名、パスワードが一致しません」と#
    #いうエラーメッセージを用意し、ログイン画面に遷移し、それをメッセージ表示エリアに赤 
    #字で表示する。（遷移パターンE） 
    if user_info is None:
        error_message.append("ユーザー名、パスワードが一致しません")
        errors={'error_message':error_message}
        return render(request,back_file,errors)
    #[10] 一致するユーザ情報が取得できた場合には、そのユーザ情報のログイン状態をTrueにして、データベースを更新する。 
    user_info.islogin = True
    user_info.save()

    roomlist=models.Room.objects.all()
    options={
        'roomlist':roomlist
    }
    #[11] 更新後、ユーザ名(USERをキー名とする)をクッキー情報として設定しつつメイン画面に遷移する。（遷移パターンF） 
    response = render(request, template_file, options) 
    response.set_cookie('USER', urllib.parse.quote(str(name)))  # key, value は保存したいキー名と値 
    return response 
def logout(request):
    value = request.COOKIES.get('USER')
    if value is not None:
        user = models.User.objects.filter(name=value).first()
        if user is not None:
            user.islogin=False
            user.save()
    return redirect('/mychat')

def createRoom(request):
    template_file="mychat/createroom.html"
    options={

    }
    return render(request,template_file,options)

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
    query = request.GET.get('q', '')
    if query:
        roomlist = models.Room.objects.filter(name__icontains=query)  # 検索キーワードが含まれている掲示板を取得
    else:
        roomlist = models.Room.objects.all()  # 検索クエリがない場合はすべての掲示板を表示
    options={
        'roomlist': roomlist
    }
    return render(request, 'mychat/search.html', options)
