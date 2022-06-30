from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.urls import reverse



# Create your views here.
def towelcome(request):
    return redirect("/welcome")
def index(request):
    return render(request,"index.html")
def welcome(request):
    return render(request,"welcome.html")

def register(request):
    if request.method == "POST":
    #check for errors
        errors=Users.objects.validatorRe(request.POST)
        if len(errors) > 0:
            for key ,value in errors.items():
                messages.error(request,value)
            return redirect("/index") # idf ther is any error redirect me to the registeraion forms page
        
        else:
            First_Name=request.POST['First_Name']
            Last_Name=request.POST['Last_Name']
            Email=request.POST['Email']
            Password=request.POST['Password']
            #use "bcrypt" to hash password
            pwHash=bcrypt.hashpw(Password.encode(),bcrypt.gensalt()).decode()

            #create user 
            newUser =Users.objects.create(First_Name=First_Name,Last_Name=Last_Name,Email=Email,Password=pwHash)
            newUser.save()

            #(save user id in session to access to user ) 
            request.session['loginID']=newUser.id
        return redirect("/dashboard")
    else:
        return redirect('/index')


def login(request):
    if request.method == "POST":
        #check for errors 
        errors=Users.objects.validatorLo(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect("/index")
        #fetching for the id to redirect user to success page.
        request.session['loginID'] = Users.objects.get(Email=request.POST['Email']).id
        return redirect('/dashboard')


def dashboard(request):
    try:
        id = request.session['loginID']   
    except:
        messages.error(request, "Need to login first")
        return render(request,'dashboard.html')
    context={
    'loginUser':Users.objects.get(id=request.session['loginID']),
    'users':Users.objects.all(),
    'articles':Articles.objects.all().order_by('-createdAt'),
    'tags': Tags.objects.all()
    }
    return render(request,"dashboard.html",context)

def logout (request):
    del request.session['loginID']
    return redirect('/index')

def adding(request):
    return render(request,"create.html")
    
def add_article(request):
    if request.method == 'POST':
        errors =Articles.objects.validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/dashboard')
        else:
            user = Users.objects.get(id=request.session['loginID'])
            title = request.POST['title']
            body = request.POST['body']
            tags = request.POST["tags"]
            tags_list = tags.split(",")
            newArticle =Articles.objects.create(title=title,user=user,body=body)
            for tagName in tags_list:
                tag = Tags.objects.filter(tag_name=tagName)
                if tag.exists():
                    newArticle.tags.add(tag[0])
                else:
                    newTag = Tags.objects.create(tag_name=tagName)
                    newArticle.tags.add(newTag)
            #newArticle.users_wish.add(user) auto make each Article that user create in his/her wish list.
            # newArticle.save()
            messages.success(request,"the Article successfully added!")
            return redirect('/dashboard')
    return redirect('/dashboard')


def show_article(request,id):
    context = {
        "article": Articles.objects.get(id=id),
        "user": Users.objects.get(id=request.session['loginID']),
        'comment': Comment.objects.all(),
    }
    return render(request, 'article.html', context)
def comment(request):
    if request.method == 'POST':
        comment = Comment.objects.create(comment = request.POST['comment'], user_id = Users.objects.get(id = request.session['loginID']), message_id = Articles.objects.get(id = request.POST['msg_id']))
        comment.save()
    # return redirect("/dashboard")
    return redirect(f"/show_article/{comment.message_id.id}")

def edit(request,id):#for edit btn 
    article = Articles.objects.get(id=id)
    
    context={
        "article":article,
    }

    if request.method == "POST": #check for post method 
        errors = Articles.objects.validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect(f'/editarticle/{id}')
        else:
        #if one field changed| no need for change the old value
            article.title= request.POST.get('title') if request.POST.get('title')  else article.title
            article.body=request.POST.get('body') if request.POST.get('body') else article.body
            article.save()
        return redirect(f"/show_article/{article.id}")
    return render(request,'edit.html',context)



def delete(request,id):
    article= Articles.objects.get(id=id)
    article.delete()
    return redirect("/dashboard")

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        results = Articles.objects.filter(title__contains=searched)
        context={
            'searched' : searched,
            'results': results,
        }
        return render(request,'search.html',context)

def tag(request,id):
    
    context = {
        "tag": Tags.objects.get(id=id),
        "articles": Articles.objects.exclude(),
        
    }
    return render(request, "tags.html", context)

# def addtag(request,id):
#     if request.method == "POST":
#         tagId=request.post.get("tag")
#         tag=Tags.objects.get(id=int(tagId))
#         article= Articles.objects.get(id=id)
#         article.tags.add(tag)
#         return redirect(f'/article/{id}')

# def addtagspage(request):
#     return render(request,'tags.html')
#----------------likes-------------------------

def like_article(request):
    # user=request.user
    user_id=request.session['loginID']
    if request.method == "POST":
        article_id=request.POST.get('article_id')
        print(article_id)
        article_obj=Articles.objects.get(id=article_id)
        print(article_obj)
        
        user = Users.objects.get(id=user_id)
        print(user_id)
        if user in article_obj.liked.all():#means the user liked the article already then remove from many to many
            article_obj.liked.remove(user_id)
            print("liked")
        else:
            article_obj.liked.add(user_id)
            print("dislike")
        like,created=Like.objects.get_or_create(user=user ,article_id=article_id)

        print(like)
        print(created)
        if not created:
            if like.value =='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        like.save()
    return redirect(f"/show_article/{ article_obj.id}")
