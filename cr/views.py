import stripe
from django.conf import settings  # new
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic.base import TemplateView
from .models import login, profile, register, rooms, room_members, connections, chats, moderators, feedback, private
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY  # new


def log(request):
    auth.logout(request)
    return render(request, "login.html")


def logn(request):
    un = request.POST['uname']
    pwd = request.POST['pawd']
    try:
        res = login.objects.get(username=un, password=pwd)
        user = auth.authenticate(username='admin', password='admin')
        if user is not None:
            auth.login(request, user)
        if res.type == "admin":
            return redirect('/adminhome')
        elif res.type == "user":
            ob = register.objects.get(lid=res)
            request.session['lid'] = ob.id
            return redirect('/userhome')
        else:
            messages.info(request, "Invalid Credentials!")
            return redirect('/')
    except:
        messages.info(request, "Invalid Credentials!")
        return redirect('/')


@login_required(login_url='/')
def adminhome(request):
    return render(request, "adminhome.html")


@login_required(login_url='/')
def userhome(request):
    return render(request, "userhome.html")


def registre(request):
    return render(request, "regis.html")


def reg(request):
    name = request.POST['name']
    age = request.POST['age']
    add = request.POST['address']
    gender = request.POST['gender']
    email = request.POST['email']
    phone = request.POST['phone']
    un = request.POST['uname']
    pwd = request.POST['pasd']

    oblog = login()
    oblog.username = un
    oblog.password = pwd
    oblog.type = "user"
    oblog.save()

    obus = register()
    obus.name = name
    obus.age = age
    obus.address = add
    obus.gender = gender
    obus.email = email
    obus.phone = phone
    obus.lid = oblog
    obus.save()
    return render(request, "userhome.html")


@login_required(login_url='/')
def usnchk(request):
    user = request.GET['usid']
    data = {
        'is_taken': login.objects.filter(username__iexact=user).exists()
    }
    if data['is_taken']:
        data['error_message'] = "username already exists!"
    return JsonResponse(data)


@login_required(login_url='/')
def pwdchk(request):
    pawd = request.GET['pwd']
    if len(pawd) == 0:
        return HttpResponse("")
    elif len(pawd) < 5:
        return HttpResponse("weak password")
    elif len(pawd) < 9:
        return HttpResponse("medium password")
    else:
        return HttpResponse("strong password")


@login_required(login_url='/')
def viewusers(request):
    ob = register.objects.all().order_by("name")
    return render(request, "viewuser.html", {"res": ob})


@login_required(login_url='/')
def deluser(request, id):
    ob = register.objects.get(lid=id)
    ob.delete()
    obus = login.objects.get(id=id)
    obus.delete()
    return HttpResponse('''<script>alert('user deleted!');window.location='adminhome'</script>''')


@login_required(login_url='/')
def gotoprof(request):
    return render(request, "userprofile.html")


@login_required(login_url='/')
def prof(request):
    us = request.POST['usn']
    img = request.FILES['image']
    bio = request.POST['bio']
    status = request.POST['status']
    about = request.POST['about']
    fs = FileSystemStorage()
    fn = fs.save(img.name, img)
    ob = profile()
    ob.user = us
    ob.bio = bio
    ob.about = about
    ob.status = status
    ob.image = fn
    obr = register.objects.get(id=request.session['lid'])
    ob.pid = obr
    ob.save()
    return HttpResponse('''<script>alert('Saved successfully!');window.location='userhome'</script>''')


@login_required(login_url='/')
def usnachk(request):
    un = request.GET['usid']
    data = {
        'is_taken': profile.objects.filter(user__iexact=un).exists()
    }
    if data['is_taken']:
        data['error_message'] = "nickname already exists!"
    return JsonResponse(data)


@login_required(login_url='/')
def gotovp(request):
    obp = profile.objects.get(pid=request.session['lid'])
    request.session['pid'] = obp.id
    return render(request, "viewprofile.html", {"res": obp})


@login_required(login_url='/')
def ditprof(request):
    ob = profile.objects.get(pid=request.session['lid'])
    return render(request, "editprofile.html", {"res": ob})


@login_required(login_url='/')
def editprof(request):
    us = request.POST['usn']
    bio = request.POST['bio']
    status = request.POST['status']
    about = request.POST['about']
    ob = profile.objects.get(pid=request.session['lid'])
    ob.user = us
    ob.bio = bio
    ob.about = about
    ob.status = status
    ob.save()
    try:
        img = request.FILES['image']
        fs = FileSystemStorage()
        fn = fs.save(img.name, img)
        ob.image = fn

        ob.save()
    except:
        pass
    return HttpResponse('''<script>alert('Edited Successfully!');window.location='userhome'</script>''')


@login_required(login_url='/')
def gotocrrm(request):
    return render(request, "createroom.html")


@login_required(login_url='/')
def createroom(request):
    name = request.POST['rname']
    descrip = request.POST['descrip']
    ob = rooms()
    ob.room_name = name
    ob.description = descrip
    obp = profile.objects.get(pid=request.session['lid'])
    ob.room_creator = obp
    ob.save()
    return HttpResponse('''<script>alert('Room created successfully!');window.location='userhome'</script>''')


@login_required(login_url='/')
def roomcheck(request):
    name = request.GET['name']
    data = {
        'is_taken': rooms.objects.filter(room_name__iexact=name).exists()
    }
    if data['is_taken']:
        data['error_message'] = "room name already exists!"
    return JsonResponse(data)


@login_required(login_url='/')
def viewroom(request):
    obc = room_members.objects.get(usid=request.session['lid'])
    ob = rooms.objects.filter(id=obc.rid.id)
    return render(request, "viewroom.html", {"res": ob})


@login_required(login_url='/')
def gotoam(request, id):
    obc = rooms.objects.get(id=id)
    obj = room_members.objects.filter(rid=obc)
    obr = register.objects.all()
    lst = []
    for i in obj:
        lst.append(i.usid.id)
    lists = []
    for i in obr:
        if i.id not in lst:
            lists.append(i)
            print(lists)
    return render(request, "addmembers.html", {"res": lists, "ress": obc})


@login_required(login_url='/')
def addmembers(request):
    mem = request.POST.getlist('member')
    print(mem, '............................')
    id = request.POST['idd']
    print("-----------", id)
    obj = rooms.objects.get(id=id)
    # ob = room_members.objects.get(rid=obj)
    for i in mem:
        us = register.objects.get(id=i)
        me = room_members()
        me.rid = obj
        me.usid = us
        me.save()
    return HttpResponse('''<script>alert('Saved Successfully!');window.location='userhome'</script>''')


@login_required(login_url='/')
def gotorm(request, id):
    ob = rooms.objects.get(id=id)
    obj = room_members.objects.filter(rid=ob)
    return render(request, "viewmembers.html", {"res": obj, "ress": ob})


@login_required(login_url='/')
def delmembers(request):
    id = request.POST['idd']
    print(id)
    mem = request.POST.getlist('del')
    print("---------------", mem)
    ob = rooms.objects.get(id=id)
    for i in mem:
        us = register.objects.get(id=i)
        obj = room_members.objects.filter(usid=us, rid=ob)
        obj.delete()
    return HttpResponse('''<script>alert('Deleted Successfully!');window.location='userhome'</script>''')


@login_required(login_url='/')
def ditroom(request, id):
    ob = rooms.objects.get(id=id)
    return render(request, "editroom.html", {"res": ob})


@login_required(login_url='/')
def editroom(request):
    name = request.POST['rname']
    descrip = request.POST['descrip']
    obj = profile.objects.get(pid=request.session['lid'])
    ob = rooms.objects.get(room_creator=obj)
    ob.room_name = name
    ob.description = descrip
    ob.save()
    return HttpResponse('''<script>alert('Edited Successfully!');window.location='userhome'</script>''')


@login_required(login_url='/')
def delroom(request, id):
    ob = rooms.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert('Deleted Successfully!');window.location='/userhome'</script>''')


@login_required(login_url='/')
def goto(request):
    ob = profile.objects.exclude(pid=request.session['lid'])
    return render(request, "createconn.html", {"res": ob})


@login_required(login_url='/')
def createcon(request):
    con = request.POST.getlist('conn')
    print(con)
    abc = request.POST.getlist('connect')
    print(abc)
    uid = request.session['lid']
    obc = register.objects.get(id=uid)
    for i in range(0, len(con)):
        typ = con[i]
        id = abc[i]
        pob = profile.objects.get(id=id)
        obj = connections.objects.filter(userid=pob, crid=obc)
        if len(obj) == 0:
            obj = connections()
            obj.type = typ
            obj.userid = pob
            obj.crid = obc
            obj.save()
        else:
            obj[0].type = typ
            obj[0].save()
    return redirect('/userhome')


@login_required(login_url='/')
def gotoconn(request, id):
    ob = profile.objects.get(id=id)


@login_required(login_url='/')
def viewconn(request):
    ob = connections.objects.filter(crid=request.session['lid'])
    return render(request, "viewconnections.html", {"res": ob})


@login_required(login_url='/')
def gotocm(request, id):
    ob = rooms.objects.get(id=id)
    obc = chats.objects.filter(cid=id)
    request.session['rid'] = id
    pid = profile.objects.get(pid=request.session['lid'])
    return render(request, "gotoroom.html", {"res": ob, "ress": obc, "pid": pid.id})


@login_required(login_url='/')
def sendchat(request):
    id = request.POST['idd']
    chat = request.POST['chat']
    ob = chats()
    ob.chat = chat
    obr = rooms.objects.get(id=id)
    ob.cid = obr
    obp = profile.objects.get(pid=request.session['lid'])
    ob.tid = obp
    ob.save()
    rid = str(request.session['rid'])
    return redirect('/gotocm/' + rid)


@login_required(login_url='/')
def createmod(request):
    ob = rooms.objects.all()
    return render(request, "createmoderator.html", {"res": ob})


@login_required(login_url='/')
def moder(request):
    name = request.POST['name']
    lst = request.POST.getlist('check')
    for i in range(0, len(lst)):
        obj = moderators()
        obj.moderator = name
        ob = rooms.objects.get(id=lst[i])
        obj.gid = ob
        obj.save()
    return redirect('/userhome')


@login_required(login_url='/')
def viewmod(request):
    ob = moderators.objects.all()
    return render(request, "viewmoderator.html", {"res": ob})


@login_required(login_url='/')
def insta(request, id):
    request.session['sid'] = id
    topob = profile.objects.get(id=id)
    torob = register.objects.get(id=topob.pid.id)
    frrob = register.objects.get(id=request.session['lid'])
    frpob = profile.objects.get(pid=frrob)
    # obj = private.objects.filter(regid=frrob, pid=frpob)
    # print(obj)
    print(request.session['lid'], "==========================")
    #  obj = private.objects.filter(regid=torob, pid=topob)
    obj = private.objects.filter(Q(regid=torob, pid=frpob) | Q(regid=frrob, pid=topob))
    print(obj)
    return render(request, "instantchat.html", {"res": topob, "ress": obj})


@login_required(login_url='/')
def instachat(request):
    id = request.POST['idd']
    chat = request.POST['chat']
    ob = private()
    obj = profile.objects.get(id=id)
    ob.pid = obj
    ob.chat = chat
    obp = register.objects.get(id=request.session['lid'])
    ob.regid = obp
    ob.save()
    ids = str(request.session['sid'])
    return redirect('/insta/' + ids)


@login_required(login_url='/')
def gotofeedbk(request):
    return render(request, "feedback.html")


@login_required(login_url='/')
def feed(request):
    feedbck = request.POST['feed']
    ob = feedback()
    ob.feed = feedbck
    obj = register.objects.get(id=request.session['lid'])
    ob.uid = obj
    ob.save()
    return HttpResponse('''<script>alert('Thank you for the feedback!');window.location='userhome'</script>''')


@login_required(login_url='/')
def viewfeed(request):
    ob = feedback.objects.all()
    return render(request, "viewfeedback.html", {"res": ob})


@login_required(login_url='/')
def pay(request):
    return render(request, "home.html")


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request): # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'charge.html')