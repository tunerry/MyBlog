from django.shortcuts import render
from django.shortcuts import HttpResponse
import json
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.views.decorators.csrf import csrf_exempt
from mysite1 import models
# Create your views here.

#user_list = [{"user":"flansk","pwd":"22002"},]


def test(request):
    #return HttpResponse("Hello World!")
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        #user = {"user":username,"pwd":password}
        models.User.objects.create(name=username, pwd=password)
        #user_list.append(user)

    user_list = models.User.objects.all()
    return render(request, "test.html",{"users":user_list})

@csrf_exempt
def index(request):
    #被注销的ajax使用
    if(request.method == 'POST'):
        method = request.POST.get('method')
        if(method == 'logout'):
            request.session['isLogin'] = 0
            request.session['user'] = '还没登录呢'
            return HttpResponse(json.dumps({
                'status': 1,
            }))

    isLogin = request.session.get('isLogin')
    if(isLogin == None):
        request.session['isLogin'] = 0
        request.session['user'] = '还没登录呢'
    user = request.session.get('user')
    return render(request, "index.html", {"user": user,"isLogin":isLogin})

def generic(request):
    return render(request, "generic.html", )

def toLogin(request):
    return render(request, "toLogin.html", )

@csrf_exempt        #跳过csrf中间件保护
def login(request):
    if(request.method == 'POST'):
        method = request.POST.get('method')
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        status = 0
        result = user
        #登录
        if(method == 'login'):
            #通过名字找到user对象，判断密码是否相同
            find = models.User.objects.filter(name=user)
            if( len(find) and pwd == find[0].pwd):
                status = 1
                request.session['isLogin'] = 1
                request.session['user'] = user
            elif(not len(find)):   #没找到user
                result = r"用户不存在！"
            else:
                result = r"密码错误了！"


            return HttpResponse(json.dumps({
                'status': status,
                'result': result,
            }))
        #注册
        elif(method == 'signup'):
            email = request.POST.get('email')
            find = models.User.objects.filter(name=user)
            if (len(find)):
                result = r'用户已经存在啦！'
            else:
                models.User.objects.create(name=user,pwd=pwd,email=email)
                status = 1
                result = user
                request.session['isLogin'] = 1
                request.session['user'] = user
            return HttpResponse(json.dumps({
                'status': status,
                'result': result,
            }))
    return render(request, "login.html",)

def articles(request):
    user = request.session.get('user')
    isLogin = request.session.get('isLogin')
    articles = reversed(models.Article.objects.all())
    return render(request, "Articles.html", {"user": user,"isLogin":isLogin,"articles":articles})

@csrf_exempt
def write(request):
    user = request.session.get('user')
    isLogin = request.session.get('isLogin')
    if(request.method == 'POST'):
        title = request.POST.get('title')
        image = request.FILES.get('img')
        article = request.POST.get('article')
        userid = request.POST.get('user')
        find = models.User.objects.filter(name=userid)
        models.Article.objects.create(title=title, cover=image, owner=find[0], test=article)
        return HttpResponse(json.dumps({
            'status': 1,
        }))

    return render(request, "write.html", {"user": user, "isLogin": isLogin})

def articleid(request, id):
    user = request.session.get('user')
    isLogin = request.session.get('isLogin')
    aid = models.Article.objects.filter(articleid=id)
    if (not len(aid)):
        print("id找不到")
    else:
        article = aid[0]
        #处理字符串得到html
        texts = article.test.splitlines()
        t = map(lambda x:'<p>'+x+'</p>', texts)
        article.test = ''.join(t)
    return render(request, "articleid.html", {"user":user, "isLogin":isLogin, "article":article,})