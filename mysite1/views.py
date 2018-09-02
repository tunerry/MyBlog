from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mysite1 import models
import random
import json
import os
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
    #被注销的ajax借用
    if(request.method == 'POST'):
        method = request.POST.get('method')
        if(method == 'logout'):
            request.session['isLogin'] = 0
            request.session['user'] = '还没登录呢'
            return HttpResponse(json.dumps({
                'status': 1,
            }))

    isLogin = request.session.get('isLogin')
    if(not isLogin):
        request.session['isLogin'] = 0
        request.session['user'] = '还没登录呢'
        isLogin = 0
    user = request.session.get('user')
    return render(request, "index.html", {"user": user,"isLogin":isLogin})

def generic(request):
    return render(request, "elements.html", )

def toLogin(request):
    isLogin = request.session.get('isLogin')
    return render(request, "toLogin.html", {"isLogin": isLogin})

@csrf_exempt        #跳过csrf中间件保护
def login(request):
    isLogin = request.session.get('isLogin')
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
    return render(request, "login.html", {"isLogin": isLogin})

def articles(request):
    user = request.session.get('user')
    isLogin = request.session.get('isLogin')
    find = models.Article.objects.all().order_by('-time')   #加 - 表示降序

    paginator = Paginator(find, 4, 1)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)
    defaults = []
    for i in range(1,11):
        defaults.append('Covers/Default_pic/pic' + str(i) + '.jpg')
    return render(request, "Articles.html", {"user": user,"isLogin":isLogin,"articles":articles,"defaults":defaults})

@csrf_exempt
def write(request, id=-1):
    user = request.session.get('user')
    isLogin = request.session.get('isLogin')
    if(id != -1):
        e_article = models.Article.objects.get(articleid=id)
        texts = e_article.test.splitlines()
        return render(request, "write.html", {"user": user, "isLogin": isLogin, "article": e_article, "texts":texts, "edit": 1,})
    if(request.method == 'POST'):
        title = request.POST.get('title')
        image = request.FILES.get('img')
        article = request.POST.get('article')
        userid = request.POST.get('user')
        if (request.POST.get('method') == 'edit'):
            id = request.POST.get('id')
            e_a = models.Article.objects.get(articleid=id)
            e_a.title = title
            e_a.test = article
            e_a.save()
            return HttpResponse(json.dumps({
                'status': 2,
            }))
        if(request.POST.get('method') == 'dele'):
            id = request.POST.get('id')
            e_a = models.Article.objects.filter(articleid=id).delete()
            return HttpResponse(json.dumps({
                'status': 1,
            }))
        find = models.User.objects.filter(name=userid)
        models.Article.objects.create(title=title, cover=image, owner=find[0], test=article)
        return HttpResponse(json.dumps({
            'status': 1,
        }))

    return render(request, "write.html", {"user": user, "isLogin": isLogin, "edit": 0})

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

def center(request):
    user = request.session.get('user')
    isLogin = request.session.get('isLogin')
    find = models.User.objects.filter(name=user)
    return render(request, "center.html", {"user": user, "isLogin": isLogin, "User":find[0],})

#用Paginator分页
def anime(request):
    user = request.session.get('user')
    isLogin = request.session.get('isLogin')
    find = models.Anime.objects.all().order_by('animeid')

    paginator = Paginator(find, 5, 2)
    page = request.GET.get('page')
    try:
        animes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        animes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        animes = paginator.page(paginator.num_pages)

    return render(request, "Anime.html", {"user": user, "isLogin": isLogin, "animes": animes, })

def anime_play(request, a_id, e_id=-1):
    user = request.session.get('user')
    isLogin = request.session.get('isLogin')
    anime = models.Anime.objects.get(animeid=a_id)
    episodes = anime.episode_anime.all()
    if(e_id == -1):
        e = episodes[0]
    else:
        e = models.Episode.objects.get(episodeid=e_id)
    return render(request, "anime_play.html", {"user": user, "isLogin": isLogin, "episodes": episodes, "anime": anime, "e": e })
