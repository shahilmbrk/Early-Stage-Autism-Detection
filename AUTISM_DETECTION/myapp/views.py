import base64
import os
import random
from datetime import datetime
import librosa
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password,check_password
from django.core.files.storage import FileSystemStorage
from imblearn.tensorflow.tests.test_generator import tf
from myapp.classify import check
from myapp.models import *
# Create your views here.


def login_get(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.groups.filter(name="Admin").exists():
                login(request,user)
                return redirect('/myapp/adminhome/')
            elif user.groups.filter(name="Expert").exists():
                login(request,user)
                return redirect('/myapp/experthome/')
            elif user.groups.filter(name="Parent").exists():
                login(request,user)
                return redirect('/myapp/parenthome/')
            else:
                messages.warning(request,"Invalid")
                return redirect('/myapp/login_get/')
        else:
                messages.warning(request,"Invalid  username and password")
                return redirect('/myapp/login_get/')
    return render(request,'login.html')

@login_required(login_url='/myapp/login_get/')
def adminhome(request):
    return render(request,'admin/homeindex.html')

def forgotpassword(request):
    return render(request,'forgot.html')

def forgotPassword_otp(request):
    email=request.POST['email']
    try:
        user=User.objects.get(email=email)
    except User.DoesNotExist:
        messages.warning(request,'Email doesnt match')
        return redirect('/myapp/')
    otp=random.randint(100000,999999)
    request.session['otp']=str(otp)
    request.session['email'] = email

    from AUTISM_DETECTION import settings
    send_mail('Your Verification Code',
    f'Your verification code is {otp}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False)
    messages.success(request,'OTP sent To your Mail')
    return redirect('/myapp/verifyOtp/')

def verifyOtp(request):
    return render(request,'otpverification.html')

def verifyOtpPost(request):
    entered_otp=request.POST['entered_otp']
    if request.session.get('otp') == entered_otp:
        messages.success(request,'otp verified')
        return redirect('/myapp/new_password/')
    else:
        messages.warning(request,'Invalid OTP!!')
        return redirect('/myapp/verifyOtp/')

def new_password(request):
    return render(request,'otpverification.html')

def changePassword(request):
    newpassword=request.POST['newPassword']
    confirmPassword=request.POST['confirmPassword']
    if newpassword == confirmPassword:
        email=request.session.get('email')
        user = User.objects.get(email=email)
        user.set_password(confirmPassword)
        user.save()
        messages.success(request, 'Password Updated Successfully')
        return redirect('/myapp/login_get/')
    else:
        messages.warning(request, 'The password doesnt match!!')
        return redirect('/myapp/new_password/')


@login_required(login_url='/myapp/login_get/')
def addexpert(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        place = request.POST['place']
        qualification = request.POST['qualification']
        district = request.POST['district']
        photo = request.FILES['photo']
        username = request.POST['username']
        password = request.POST['password']

        fs=FileSystemStorage()
        path=fs.save(photo.name,photo)

        plogin = User.objects.create(username=username, password=make_password(password))
        plogin.save()
        plogin.groups.add(Group.objects.get(name="Expert"))

        pobj = Expert_table()
        pobj.name = name
        pobj.email = email
        pobj.place = place
        pobj.qualification = qualification
        pobj.district = district
        pobj.photo = path
        pobj.phone = phone
        pobj.LOGIN = plogin
        pobj.save()
        return redirect('/myapp/viewexpert/')
    else:
        return render(request, 'admin/view expert.html')

@login_required(login_url='/myapp/login_get/')
def viewexpert(request):
    res = Expert_table.objects.all()
    return render(request, 'admin/view expert.html', {'data': res})

@login_required(login_url='/myapp/login_get/')
def deleteexpert(request, id):
    res = Expert_table.objects.get(LOGIN=id).delete()
    var = User.objects.get(id=id).delete()
    return redirect('/myapp/viewexpert/')

@login_required(login_url='/myapp/login_get/')
def editexpert(request, id):
    res = Expert_table.objects.get(id=id)
    return render(request, 'admin/edit expert.html', {'data': res})

@login_required(login_url='/myapp/login_get/')
def editexpert_post(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    qualification = request.POST['qualification']
    district = request.POST['district']
    id = request.POST['id']
    hobj = Expert_table.objects.get(id=id)
    if 'photo' in request.FILES:
        fs = FileSystemStorage()
        photo = request.FILES['photo']
        path = fs.save(photo.name, photo)
        hobj.photo=path
        hobj.save()

    hobj.name = name
    hobj.email = email
    hobj.place = place
    hobj.qualification = qualification
    hobj.district = district

    hobj.phone = phone
    hobj.save()
    return redirect('/myapp/viewexpert/')

@login_required(login_url='/myapp/login_get/')
def changepassword(request):
    if request.method == "POST":
        oldpasspwrd= request.POST["cpassword"]
        newpassword= request.POST["npassword"]


        print(request.user)
        f=check_password(oldpasspwrd,request.user.password)
        if f:
            user=request.user
            user.set_password(newpassword)
            user.save()

            #update_session_auth_hash(request,user)
            messages.success(request, 'Password changed successfully')
            return redirect('/myapp/login/')
        else:
            messages.success(request, 'Password updated successfully. Please lgin try again')
            return redirect('/myapp/login_get/')


    return render(request,"admin/change password.html")

@login_required(login_url='/myapp/login_get/')
def logout_func(request):
     logout(request)
     return redirect('/myapp/login_get/')

@login_required(login_url='/myapp/login_get/')
def viewfeedback(request):
     res=Feedback_table.objects.all()
     return render(request,'admin/view feedback.html',{'data':res})


@login_required(login_url='/myapp/login_get/')
def viewstudent(request):
     res=Student_table.objects.all()
     return render(request,'admin/view students.html',{'data':res})


########################################


@login_required(login_url='/myapp/login_get/')
def expertchangepassword(request):
    if request.method == "POST":
        oldpasspwrd= request.POST["cpassword"]
        newpassword= request.POST["npassword"]
        print(request.user)
        f=check_password(oldpasspwrd,request.user.password)
        if f:
            user=request.user
            user.set_password(newpassword)
            user.save()

            #update_session_auth_hash(request,user)
            messages.success(request, 'Password changed successfully')
            return redirect('/myapp/login/')
        else:
            messages.success(request, 'Password updated successfully. Please lgin try again')
            return redirect('/myapp/login_get/')
    return render(request,"expert/change password.html")


@login_required(login_url='/myapp/login_get/')
def addtips(request):
    if request.method == 'POST':
        tips=request.POST['tips']
        details=request.POST['details']
        obj=Tips_table()
        obj.date=datetime.datetime.now().today()
        obj.tips=tips
        obj.details=details
        obj.EXPERT=Expert_table.objects.get(LOGIN=request.user.id)
        obj.save()
        return redirect('/myapp/viewtips/')
    return render(request,'expert/view tips.html')


@login_required(login_url='/myapp/login_get/')
def viewtips(request):
    res=Tips_table.objects.filter(EXPERT__LOGIN_id=request.user.id)
    return render(request,'expert/view tips.html',{'data':res})


@login_required(login_url='/myapp/login_get/')
def deletetips(request,id):
    Tips_table.objects.get(id=id).delete()
    return redirect('/myapp/viewtips/')



@login_required(login_url='/myapp/login_get/')
def edittips(request,id):
    res=Tips_table.objects.get(id=id)
    request.session['tid']=id
    return render(request,'expert/edit tips.html',{'data':res})

@login_required(login_url='/myapp/login_get/')
def edittips_post(request):
    tips = request.POST['tips']
    details = request.POST['details']

    obj = Tips_table.objects.get(id=request.session['tid'])
    obj.date = datetime.datetime.now().today()
    obj.tips = tips
    obj.details = details
    obj.EXPERT = Expert_table.objects.get(LOGIN=request.user.id)
    obj.save()
    return redirect('/myapp/viewtips/')

@login_required(login_url='/myapp/login_get/')
def experthome(request):
    return render(request,'expert/homeindex.html')



@login_required(login_url='/myapp/login_get/')
def addstudymaterials(request):
    if request.method == 'POST':
        tips=request.POST['title']
        file=request.FILES['file']

        fs = FileSystemStorage()
        path = fs.save(file.name, file)

        obj=Studymaterial_table()
        obj.date=datetime.datetime.now().today()
        obj.title=tips
        obj.file=path
        obj.EXPERT=Expert_table.objects.get(LOGIN=request.user.id)
        obj.save()
        return redirect('/myapp/viewstudymaterilas/')
    return render(request,'expert/view studymaterials.html')

@login_required(login_url='/myapp/login_get/')
def viewstudymaterilas(request):
    res=Studymaterial_table.objects.filter(EXPERT__LOGIN_id=request.user.id)
    return render(request,'expert/view studymaterials.html',{'data':res})


@login_required(login_url='/myapp/login_get/')
def deletestudymaterials(request,id):
    Studymaterial_table.objects.get(id=id).delete()
    return redirect('/myapp/viewstudymaterilas/')





@login_required(login_url='/myapp/login_get/')
def addtest(request):
    if request.method == 'POST':
        tips=request.POST['title']
        details=request.POST['details']
        level=request.POST['level']
        obj=Test_table()
        obj.date=datetime.datetime.now().today()
        obj.title=tips
        obj.details=details
        obj.level=level
        obj.EXPERT=Expert_table.objects.get(LOGIN=request.user.id)
        obj.save()
        return redirect('/myapp/viewtest/')
    return render(request,'expert/view test.html')


@login_required(login_url='/myapp/login_get/')
def viewtest(request):
    res=Test_table.objects.filter(EXPERT__LOGIN_id=request.user.id)
    return render(request,'expert/view test.html',{'data':res})


@login_required(login_url='/myapp/login_get/')
def deletetest(request,id):
    Test_table.objects.get(id=id).delete()
    return redirect('/myapp/viewtest/')

@login_required(login_url='/myapp/login_get/')
def edittest(request,id):
    res=Test_table.objects.get(id=id)
    request.session['tid']=id
    return render(request,'expert/edit test.html',{'data':res})

@login_required(login_url='/myapp/login_get/')
def edittest_post(request):
    title = request.POST['title']
    details = request.POST['details']
    level = request.POST['level']

    obj = Test_table.objects.get(id=request.session['tid'])
    obj.date = datetime.datetime.now().today()
    obj.title = title
    obj.details = details
    obj.level = level
    obj.EXPERT = Expert_table.objects.get(LOGIN=request.user.id)
    obj.save()
    return redirect('/myapp/viewtest/')

@login_required(login_url='/myapp/login_get/')
def addquestion(request,id):
    return render(request,'expert/add question.html',{'id':id})


@login_required(login_url='/myapp/login_get/')
def addquestion_post(request):
    question=request.POST['question']
    answer=request.POST['answer']
    type=request.POST['type']
    file=request.FILES['file']
    tid=request.POST['tid']
    start=request.POST['stime']
    stop=request.POST['etime']

    fs = FileSystemStorage()
    path = fs.save(file.name, file)

    obj=Question_table()
    obj.date=datetime.datetime.now().today()
    obj.question=question
    obj.file=path
    obj.answer=answer
    obj.type=type
    obj.startime=start
    obj.endtime=stop
    obj.TEST_id=tid
    obj.EXPERT=Expert_table.objects.get(LOGIN=request.user.id)
    obj.save()
    return redirect(f'/myapp/viewquestion/{tid}')


@login_required(login_url='/myapp/login_get/')
def viewquestion(request,id):
    res=Question_table.objects.filter(TEST_id=id)
    return render(request,'expert/view question.html',{'data':res})


@login_required(login_url='/myapp/login_get/')
def deletequestion(request,id):
    Question_table.objects.get(id=id).delete()
    # return redirect('/myapp/viewquestion/')
    return redirect(f'/myapp/viewquestion/{id}')



@login_required(login_url='/myapp/login_get/')
def editquestion(request,id):
    request.session['qid']=id
    res=Question_table.objects.get(id=id)
    return render(request,'expert/edit question.html',{'id':id,'data':res})


@login_required(login_url='/myapp/login_get/')
def editquestion_post(request):
    question=request.POST['question']
    answer=request.POST['answer']
    type=request.POST['type']
    tid=request.POST['tid']
    start = request.POST['stime']
    stop = request.POST['etime']

    obj=Question_table.objects.get(id=request.session['qid'])

    if 'file' in request.FILES:
        file = request.FILES['file']

        fs = FileSystemStorage()
        path = fs.save(file.name, file)
        obj.file = path
        obj.save()

    obj.date=datetime.datetime.now().today()
    obj.question=question

    obj.answer=answer
    obj.type=type
    obj.startime = start
    obj.endtime = stop
    obj.TEST_id=tid
    obj.EXPERT=Expert_table.objects.get(LOGIN=request.user.id)
    obj.save()
    return redirect(f'/myapp/viewquestion/{tid}')


@login_required(login_url='/myapp/login_get/')
def viewparent(request):
    res=Parent_table.objects.all()
    return render(request,'expert/view parent.html',{'data':res})

@login_required(login_url='/myapp/login_get/')
def viewreport(request,id):
    res=Medicalreport.objects.filter(STUDENT__PARENT_id=id)
    return render(request,'expert/view medical report.html',{'data':res})

@login_required(login_url='/myapp/login_get/')
def addguidline(request,id):
    return render(request,'expert/add guidline.html',{'id':id})


@login_required(login_url='/myapp/login_get/')
def addguidline_post(request):
    desc=request.POST['details']
    title=request.POST['title']

    tid=request.POST['tid']

    obj=Guidline()
    obj.date=datetime.datetime.now().today()
    obj.title=title
    obj.guidline=desc
    obj.MEDICALREPORT_id=tid
    obj.EXPERT=Expert_table.objects.get(LOGIN=request.user.id)
    obj.save()
    return redirect(f'/myapp/viewguidline/{tid}')


@login_required(login_url='/myapp/login_get/')
def viewguidline(request,id):
    request.session['gid']=id
    res=Guidline.objects.filter(MEDICALREPORT_id=id)
    return render(request,'expert/view quidline.html',{'data':res})



@login_required(login_url='/myapp/login_get/')
def deleteguidline(request,id):
    Guidline.objects.get(id=id).delete()
    b=request.session['gid']
    return redirect(f'/myapp/viewguidline/{b}')

@login_required(login_url='/myapp/login_get/')
def expert_view_result(request):
    res=Attend_table.objects.filter(QUESTION__TEST__EXPERT__LOGIN_id=request.user.id)
    return render(request,'expert/view result.html',{'data':res})



########################################


def chat(request,id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = Parent_table.objects.get(LOGIN=cid)

    return render(request, "expert/Chat.html", {'photo': '/static/user.png', 'name': qry.name, 'toid': cid})

def chat_view(request):
    fromid = request.user.id
    toid = request.session["userid"]
    qry = Parent_table.objects.get(LOGIN=request.session["userid"])
    from django.db.models import Q

    res = Chat_table.objects.filter(Q(FROM_id=fromid,TO_id=toid) | Q(FROM_id=toid, TO_id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TO_id, "date": i.date, "from": i.FROM_id})

    return JsonResponse({'photo':'/static/user.png', "data": l, 'name': qry.name, 'toid': request.session["userid"]})

def chat_send(request, msg):
    lid = request.user.id
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat_table()
    chatobt.message = message
    chatobt.TO_id = toid
    chatobt.FROM_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})


####




def chat2(request,id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    request.session["new"] = cid
    qry = Expert_table.objects.get(LOGIN=cid)

    return render(request, "parent/Chat.html", {'photo': '/static/user.png', 'name': qry.name, 'toid': cid})

def chat_view2(request):
    fromid = request.user.id
    toid = request.session["userid"]
    qry = Expert_table.objects.get(LOGIN=request.session["userid"])
    from django.db.models import Q

    res = Chat_table.objects.filter(Q(FROM_id=fromid,TO_id=toid) | Q(FROM_id=toid, TO_id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.message, "to": i.TO_id, "date": i.date, "from": i.FROM_id})

    return JsonResponse({'photo':'/static/user.png', "data": l, 'name': qry.name, 'toid': request.session["userid"]})

def chat_send2(request, msg):
    lid = request.user.id
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat_table()
    chatobt.message = message
    chatobt.TO_id = toid
    chatobt.FROM_id = lid
    chatobt.date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})



def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat_table()
    c.FROM_id=FROM_id
    c.TO_id=TOID_id
    c.message=msg
    c.date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def User_viewchat(request):
    fromid = request.POST["from_id"]
    toid = request.POST["to_id"]
    from django.db.models import Q

    res = Chat_table.objects.filter(Q(FROM_id=fromid, TO_id=toid) | Q(FROM_id=toid, TO_id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.message, "from": i.FROM_id, "date": i.date, "to": i.TO_id})

    return JsonResponse({"status":"ok",'data':l})



#######################parent




@login_required(login_url='/myapp/login_get/')
def parenthome(request):
    return render(request,'parent/parenthomeindex.html')


def register_get(request):
    return render(request,'parent/register.html')

def register(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    district = request.POST['district']
    username = request.POST['username']
    password = request.POST['password']

    plogin = User.objects.create(username=username, password=make_password(password))
    plogin.save()
    plogin.groups.add(Group.objects.get(name="Parent"))

    obj = Parent_table()
    obj.LOGIN = plogin
    obj.name = name
    obj.email = email
    obj.place = place
    obj.district = district
    obj.phone = phone
    obj.save()
    return redirect('/myapp/login_get/')

@login_required(login_url='/myapp/login_get/')
def add_children_get(request):
    return render(request,'parent/add children.html')


@login_required(login_url='/myapp/login_get/')
def add_children(request):
    name = request.POST['name']
    age = request.POST['age']
    photo = request.FILES['photo']
    lid = request.user.id
    fs = FileSystemStorage()
    path = fs.save(photo.name, photo)
    print(request.user.id, 'kk')
    obj = Student_table()
    obj.name = name
    obj.age = age
    obj.photo = path
    obj.PARENT = Parent_table.objects.get(LOGIN_id=lid)
    obj.save()
    return redirect('/myapp/view_student/')


@login_required(login_url='/myapp/login_get/')
def view_children(request):
    res = Student_table.objects.filter(PARENT__LOGIN_id=request.user.id)
    return render(request,'parent/view child.html',{'data':res})


@login_required(login_url='/myapp/login_get/')
def edit_children(request):
    name = request.POST['name']
    age = request.POST['age']
    sid = request.session['sid']
    obj = Student_table.objects.get(id=sid)
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        path = fs.save(photo.name, photo)
        obj.photo = path
        obj.save()

    obj.name = name
    obj.age = age

    obj.PARENT = Parent_table.objects.get(LOGIN=request.user.id)
    obj.save()
    return redirect('/myapp/view_student/')


@login_required(login_url='/myapp/login_get/')
def edit_child(request,id):
    request.session['sid']=id
    s = Student_table.objects.get(id=id)
    return render(request,'parent/edit children.html',{'data':s})


@login_required(login_url='/myapp/login_get/')
def delete_student(request,id):
    Student_table.objects.get(id=id).delete()
    return redirect('/myapp/view_student/')


@login_required(login_url='/myapp/login_get/')
def view_experts(request):
    res = Expert_table.objects.all()
    return render(request,'parent/view expert.html',{'data':res})


@login_required(login_url='/myapp/login_get/')
def add_medical_report_get(request,id):
    request.session['sid']=id
    return render(request,'parent/add medical report.html')


@login_required(login_url='/myapp/login_get/')
def add_medical_report(request):
    details = request.POST['details']
    sid = request.session['sid']
    file = request.FILES['file']
    fs = FileSystemStorage()
    path = fs.save(file.name, file)
    obj = Medicalreport()
    obj.file = path
    obj.details = details
    obj.STUDENT = Student_table.objects.get(id=sid)
    obj.date = datetime.datetime.now().today()
    obj.save()
    # id=request.session['sid']
    return redirect(f'/myapp/view_medical_report/{sid}')


@login_required(login_url='/myapp/login_get/')
def view_medical_report(request,id):
    res = Medicalreport.objects.filter(STUDENT_id=id)
    request.session['mid']=id
    return render(request,'parent/view medical report.html',{'data':res})


@login_required(login_url='/myapp/login_get/')
def delete_medical_report(request,id):
    Medicalreport.objects.get(id=id).delete()
    id=request.session['mid']
    return redirect('/myapp/view_medical_report/{id}')


@login_required(login_url='/myapp/login_get/')
def parent_view_guidline(request,id):
    request.session['gid']=id
    res = Guidline.objects.filter(MEDICALREPORT_id=id)
    return render(request,'parent/view quidline.html',{'data':res})


@login_required(login_url='/myapp/login_get/')
def view_test(request):
    res = Test_table.objects.all()
    return render(request, 'parent/view test.html', {'data': res})


@login_required(login_url='/myapp/login_get/')
def view_questions(request,id):
    data = Question_table.objects.filter(TEST_id=id)

    current_date = datetime.datetime.now().date()
    current_time = datetime.datetime.now().time()

    # Convert string time (e.g., "01:04 PM") into real time object
    for d in data:
        try:
            d.startime_obj = datetime.datetime.strptime(d.startime.strip(), "%I:%M %p").time()
            d.endtime_obj = datetime.datetime.strptime(d.endtime.strip(), "%I:%M %p").time()
        except:
            d.startime_obj = None
            d.endtime_obj = None

    return render(request, "parent/view question.html", {
        "data": data,
        "current_date": current_date,
        "current_time": current_time,
    })


@login_required(login_url='/myapp/login_get/')
def view_study_material(request):
    res = Studymaterial_table.objects.all()
    return render(request, 'parent/view studymaterials.html', {'data': res})


@login_required(login_url='/myapp/login_get/')
def view_tips(request):
    res = Tips_table.objects.all()
    return render(request, 'parent/view tips.html', {'data': res})


@login_required(login_url='/myapp/login_get/')
def send_feedback_get(request):
    return render(request,'parent/send feedback.html')


@login_required(login_url='/myapp/login_get/')
def send_feedback(request):
    feedback = request.POST['feedback']
    rating = request.POST['rating']
    lid = request.user.id
    obj = Feedback_table()
    obj.PARENT = Parent_table.objects.get(LOGIN_id=lid)
    obj.date = datetime.datetime.now().today()
    obj.feedback = feedback
    obj.rating = rating
    obj.save()
    return redirect('/myapp/parenthome/')


@login_required(login_url='/myapp/login_get/')
def view_results(request):
    res = Result.objects.filter(ATTENDTABLE__STUDENT__PARENT__LOGIN_id=request.user.id)
    return render(request, 'parent/view result.html', {'data': res})


@login_required(login_url='/myapp/login_get/')
def attend_exam_get(request, id):
    request.session['qid'] = id
    q = Question_table.objects.get(id=id)
    return render(request, 'parent/attend exam.html', {'q': q})

@login_required(login_url='/myapp/login_get/')
def attend_exam(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    try:
        eid = request.session['qid']
        solution = request.POST['solution']
        lid = request.user.id

        student = Student_table.objects.get(PARENT__LOGIN_id=lid)
        question = Question_table.objects.get(id=eid)

        # Clean answers
        solution_clean = solution.strip().lower()
        correct_clean = question.answer.strip().lower()

        # Word Overlap Similarity
        solution_words = set(solution_clean.split())
        correct_words = set(correct_clean.split())

        similarity_percent = 0
        if correct_words:
            similarity_percent = round((len(solution_words & correct_words) / len(correct_words)) * 100, 2)

        # Current time
        now = datetime.datetime.now()
        now_time = now.time()

        # Convert end time
        end_time_obj = datetime.datetime.strptime(question.endtime, "%I:%M %p").time()

        # Calculate mark
        if similarity_percent >= 50:
            mark = 1 if now_time <= end_time_obj else 0.5
        else:
            mark = 0

        # Prevent duplicates
        if Attend_table.objects.filter(STUDENT=student, QUESTION=question).exists():
            return JsonResponse({'status': 'already_submitted', 'message': 'Already submitted'})

        # Solving time
        start_time_obj = datetime.datetime.strptime(question.startime, "%I:%M %p").time()
        solving_seconds = (datetime.datetime.combine(now.date(), now_time) -
                           datetime.datetime.combine(now.date(), start_time_obj)).total_seconds()

        # Save Attend Table
        obj = Attend_table(
            QUESTION=question,
            STUDENT=student,
            date=now.date(),
            time=now_time,
            mark=mark,
            solution=solution
        )
        obj.save()

        # Autism prediction logic
        if solving_seconds > 120 and mark == 0:
            prediction = "High risk"
        elif solving_seconds > 60 and mark <= 0.5:
            prediction = "Moderate risk"
        else:
            prediction = "Low risk"

        # Save Result
        result = Result(
            similarity_percent=similarity_percent,
            mark=mark,
            solving_time=solving_seconds,
            prediction=prediction,
            message=f"Similarity: {similarity_percent}%, Mark: {mark}, Prediction: {prediction}",
            ATTENDTABLE=obj
        )
        result.save()

        return render(request, 'parent/attend exam.html', {
            'q': question,
            'similarity_percent': similarity_percent,
            'mark': mark,
            'solving_time': solving_seconds,
            'prediction': prediction,
            'message': f"Similarity: {similarity_percent}%, Mark: {mark}, Prediction: {prediction}"
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})




@login_required(login_url='/myapp/login_get/')
def parent_changepassword(request):
    if request.method == "POST":
        oldpasspwrd= request.POST["cpassword"]
        newpassword= request.POST["npassword"]


        print(request.user)
        f=check_password(oldpasspwrd,request.user.password)
        if f:
            user=request.user
            user.set_password(newpassword)
            user.save()

            #update_session_auth_hash(request,user)
            messages.success(request, 'Password changed successfully')
            return redirect('/myapp/login_get/')
        else:
            messages.success(request, 'Password updated successfully. Please lgin try again')
            return redirect('/myapp/login_get/')


    return render(request,"parent/change password.html")


########################check
from .checking_img import check_type
@login_required(login_url='/myapp/login_get/')
def user_check(request):
    if request.method == "POST":
        photo = request.FILES['photo']

        fs = FileSystemStorage()
        filename = fs.save(photo.name, photo)

        save_path = os.path.join(
            r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\media", filename
        )

        result,p = check_type(save_path)
        if result!="invalid":
            if result == 'autistic':
                print(result)
                print( round(p * 100, 2))
                return render(request, 'parent/upload image.html', {
                    "label": "YES",
                    "accuracy": round(p * 100, 2),            "autism": "YES",
                    'msg':result
                })
            else:
                print(result)
                print(round(p * 100, 2))
                return render(request, 'parent/upload image.html', {
                    "label": "NO",
                    "accuracy": round(p * 100, 2), "autism": "NO",
                    'msg': result
                })
        else:
            return render(request, 'parent/upload image.html', {
                "label": "Invalid",
                "accuracy": "90", "autism": "Invalid",
                'msg': "Invalid"
            })

    return render(request, 'parent/upload image.html')



def forgotpasswordflutter(request):
    email = request.POST['email']
    print(email, 'eeeee')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found'})

    otp = random.randint(100000, 999999)
    PasswordResetOTP.objects.create(email=email, otp=otp)

    from AUTISM_DETECTION import settings
    send_mail('Your Verification Code',
              f'Your verification code is {otp}',
              settings.EMAIL_HOST_USER,
              [email],
              fail_silently=False)
    return JsonResponse({'status': 'ok', 'message': 'OTP sent'})

def verifyOtpflutterPost(request):
    email = request.POST['email']
    entered_otp = request.POST['entered_otp']
    otp_obj = PasswordResetOTP.objects.filter(email=email).latest('created_at')
    if otp_obj.otp == entered_otp:
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'error'})

def changePasswordflutter(request):
    email = request.POST['email']
    newpassword = request.POST['newPassword']
    confirmPassword = request.POST['confirmPassword']
    if newpassword == confirmPassword:
        try:
            user = User.objects.get(email=email)
            user.set_password(confirmPassword)
            user.save()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})

###########################





from datetime import datetime
import os
from myapp.models import audio_table

@login_required(login_url='/myapp/login_get/')
def audioupload(request):
    return render(request, 'parent/upload_audio.html')

@login_required(login_url='/myapp/login_get/')
def view_audioresult(request):
    if request.method == 'POST':
        audio_results = audio_table.objects.all().values('id', 'result', 'date', 'confidence_level', 'file')

        data = {
            'status': 'ok',
            'data': list(audio_results)
        }
        return JsonResponse(data)
    else:
        data = {
            'status': 'error',
            'message': 'Method not allowed'
        }
        return JsonResponse(data, status=405)








###################################################predictions
from django.http import JsonResponse

def user_check2(path):
    result = check(path)
    return result[0]



from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import tensorflow as tf

# -------------------------------
# IMAGE CHECK FUNCTION
# -------------------------------
def check_image(path):
    image_data = tf.io.gfile.GFile(path, 'rb').read()
    label_lines = [line.rstrip() for line
                   in tf.io.gfile.GFile(
            r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\static\output_labels.txt")]

    with tf.compat.v1.gfile.FastGFile(
            r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\static\output_graph.pb", 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.compat.v1.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        nid = top_k[0]
        return label_lines[nid], predictions[0][nid]

import cv2
import os
import uuid


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return "Video Error"

    results = []
    frame_interval = 30   # sample every 30 frames
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # sample every N frames
        if frame_index % frame_interval == 0:

            # generate UNIQUE filename
            temp_img_path = f"temp_frame_{uuid.uuid4().hex}.png"

            ok = cv2.imwrite(temp_img_path, frame)
            if not ok:
                frame_index += 1
                continue

            label, _ = check_image(temp_img_path)

            # cleanup file
            if os.path.exists(temp_img_path):
                os.remove(temp_img_path)

            results.append(label.lower())
            if len(results)>=20:
                break

        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()

    # classification mapping
    positive = ["inattentive", "combined", "hyperactive"]
    negative = ["others", "typically developing"]

    pos_count = sum([r in positive for r in results])
    neg_count = sum([r in negative for r in results])

    if pos_count > neg_count:
        return "Autism is Positive"
    elif neg_count > pos_count:
        return "Autism is Negative"
    else:
        return "Unknown result"



# from joblib import load
# import numpy as np
# import librosa
# import os
# import datetime
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
#
# audio_model = load(r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\audio_detector2.h5")
#
# def extract_features(audio_path):
#     y, sr = librosa.load(audio_path, sr=16000)
#     mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=14)
#     return np.mean(mfcc.T, axis=0)
#
# def check_audio(audio_path):
#     features = extract_features(audio_path).reshape(1, -1)
#     prediction = audio_model.predict(features)[0]
#     return "Autism is Positive" if prediction == 1 else "Autism is Negative"
#
# @csrf_exempt
# def check_autism(request):
#     if request.method == "POST":
#         file = request.FILES.get('file')
#         if not file:
#             return render(request, 'parent/upload_audio.html', {"msg": "No file uploaded"})
#
#         ext = os.path.splitext(file.name)[1].lower()
#         save_dir = "media/uploads"
#         os.makedirs(save_dir, exist_ok=True)
#
#         filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ext
#         path = os.path.join(save_dir, filename)
#
#         with open(path, 'wb+') as f:
#             for chunk in file.chunks():
#                 f.write(chunk)
#
#         if ext in ['.wav', '.mp3', '.ogg']:
#             msg = check_audio(path)
#         else:
#             msg = "Unsupported format"
#
#         return render(request, 'parent/upload_audio.html', {"msg": msg})
#
#     return render(request, 'parent/upload_audio.html')

# import os
# import datetime
# import numpy as np
# import librosa
# import tensorflow as tf
#
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from tensorflow.keras.models import load_model
#
# # --------------------------------
# # LOAD MODEL (CORRECT WAY)
# # --------------------------------
# MODEL_PATH = r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\audio_detector2.h5"
# audio_model = load_model(MODEL_PATH)
#
# # --------------------------------
# # FEATURE EXTRACTION (MATCH TRAINING)
# # --------------------------------
# def extract_features(audio_path):
#     y, sr = librosa.load(audio_path, sr=22050)
#
#     mfcc = librosa.feature.mfcc(
#         y=y,
#         sr=sr,
#         n_mfcc=60
#     )
#
#     # Ensure fixed shape (13, 60)
#     mfcc = mfcc[:, :13]
#     mfcc = mfcc.T  # (13, 60)
#
#     return mfcc
#
# # --------------------------------
# # PREDICTION FUNCTION
# # --------------------------------
# def check_audio(audio_path):
#     features = extract_features(audio_path)
#     features = np.expand_dims(features, axis=0)  # (1, 13, 60)
#
#     prediction = audio_model.predict(features)[0][0]
#
#     return "Autism is Positive" if prediction >= 0.5 else "Autism is Negative"
#
# # --------------------------------
# # DJANGO VIEW
# # --------------------------------
# @csrf_exempt
# def check_autism(request):
#     if request.method == "POST":
#         file = request.FILES.get('file')
#
#         if not file:
#             return render(request, 'parent/upload_audio.html', {"msg": "No file uploaded"})
#
#         ext = os.path.splitext(file.name)[1].lower()
#         save_dir = "media/uploads"
#         os.makedirs(save_dir, exist_ok=True)
#
#         filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ext
#         path = os.path.join(save_dir, filename)
#
#         with open(path, 'wb+') as f:
#             for chunk in file.chunks():
#                 f.write(chunk)
#
#         if ext in ['.wav', '.mp3', '.ogg']:
#             msg = check_audio(path)
#         else:
#             msg = "Unsupported audio format"
#
#         return render(request, 'parent/upload_audio.html', {"msg": msg,"accuracy": msg["confidence"]})
#
#     return render(request, 'parent/upload_audio.html')


#################################Audio detection

#
# import os
# import datetime
# import numpy as np
# import librosa
# import tensorflow as tf
#
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from tensorflow.keras.models import load_model
#
# # --------------------------------
# # LOAD AUDIO MODEL (LOAD ONCE)
# # --------------------------------
# MODEL_PATH = r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\audio_detector2.h5"
# audio_model = load_model(MODEL_PATH)
#
# # --------------------------------
# # FEATURE EXTRACTION
# # (MUST MATCH TRAINING)
# # --------------------------------
# def extract_features(audio_path):
#     # Load audio
#     y, sr = librosa.load(audio_path, sr=22050)
#
#     # Extract MFCCs
#     mfcc = librosa.feature.mfcc(
#         y=y,
#         sr=sr,
#         n_mfcc=60
#     )
#
#     # Fix length (13 frames)
#     mfcc = mfcc[:, :13]
#
#     # Transpose → (13, 60)
#     mfcc = mfcc.T
#
#     return mfcc
#
#
# # --------------------------------
# # AUDIO PREDICTION FUNCTION
# # --------------------------------
# def check_audio(audio_path):
#     features = extract_features(audio_path)
#
#     # Add batch dimension → (1, 13, 60)
#     features = np.expand_dims(features, axis=0)
#
#     # Model prediction (probability)
#     prediction = audio_model.predict(features, verbose=0)[0][0]
#
#     confidence = round(float(prediction) * 100, 2)
#
#     label = "Autism is Positive" if prediction >= 0.5 else "Autism is Negative"
#
#     return {
#         "label": label,
#         "confidence": confidence
#     }
#
#
# # --------------------------------
# # DJANGO VIEW
# # --------------------------------
# @csrf_exempt
# def check_autism(request):
#     if request.method == "POST":
#         file = request.FILES.get("file")
#
#         if not file:
#             return render(request, "parent/upload_audio.html", {
#                 "msg": "No file uploaded"
#             })
#
#         ext = os.path.splitext(file.name)[1].lower()
#
#         if ext not in [".wav", ".mp3", ".ogg"]:
#             return render(request, "parent/upload_audio.html", {
#                 "msg": "Unsupported audio format"
#             })
#
#         # Save uploaded file
#         save_dir = "media/uploads"
#         os.makedirs(save_dir, exist_ok=True)
#
#         filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ext
#         path = os.path.join(save_dir, filename)
#
#         with open(path, "wb+") as f:
#             for chunk in file.chunks():
#                 f.write(chunk)
#
#         # Predict
#         result = check_audio(path)
#
#         return render(request, "parent/upload_audio.html", {
#             "msg": result["label"],
#             "accuracy": result["confidence"]
#         })
#
#     return render(request, "parent/upload_audio.html")

# import os
# import datetime
# import numpy as np
# import librosa
# import tensorflow as tf
#
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
# from tensorflow.keras.models import load_model
#
# # ==================================================
# # LOAD MODEL (LOAD ONLY ONCE)
# # ==================================================
# MODEL_PATH = r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\audio_detector.h5"
# audio_model = load_model(MODEL_PATH)
#
# # ==================================================
# # FEATURE EXTRACTION (MATCH TRAINING)
# # ==================================================
# def extract_features(audio_path):
#     try:
#         # Load audio
#         y, sr = librosa.load(audio_path, sr=22050)
#
#         # Reject silent audio
#         if np.max(np.abs(y)) < 0.01:
#             return None
#
#         # MFCC extraction
#         mfcc = librosa.feature.mfcc(
#             y=y,
#             sr=sr,
#             n_mfcc=60
#         )
#
#         # Fix frame length to 13
#         if mfcc.shape[1] < 13:
#             pad_width = 13 - mfcc.shape[1]
#             mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant')
#         else:
#             mfcc = mfcc[:, :13]
#
#         # Transpose → (13, 60)
#         mfcc = mfcc.T
#
#         # Normalize (VERY IMPORTANT)
#         mfcc = (mfcc - np.mean(mfcc)) / np.std(mfcc)
#
#         return mfcc
#
#     except Exception as e:
#         print("Feature extraction error:", e)
#         return None
#
#
# # ==================================================
# # AUDIO PREDICTION
# # ==================================================
# def check_audio(audio_path):
#     features = extract_features(audio_path)
#
#     if features is None:
#         return {
#             "label": "Invalid or Silent Audio",
#             "confidence": 0.0
#         }
#
#     features = np.expand_dims(features, axis=0)
#
#     prediction = audio_model.predict(features, verbose=0)[0][0]
#
#     print("RAW PREDICTION:", prediction)
#
#     confidence = round(float(prediction) * 100, 2)
#
#     # 🔥 INVERTED LOGIC (FIX)
#     if prediction >= 0.75:
#         label = "Autism is Negative"
#     else:
#         label = "Autism is Positive"
#
#     return {
#         "label": label,
#         "confidence": confidence
#     }
#
#
# # ==================================================
# # AUDIO UPLOAD PAGE
# # ==================================================
# @login_required(login_url='/myapp/login_get/')
# def audioupload(request):
#     return render(request, 'parent/upload_audio.html')
#
#
# # ==================================================
# # AUDIO PREDICTION VIEW
# # ==================================================
# @csrf_exempt
# @login_required(login_url='/myapp/login_get/')
# def check_autism(request):
#     if request.method == "POST":
#         file = request.FILES.get("file")
#
#         if not file:
#             return render(request, "parent/upload_audio.html", {
#                 "msg": "No audio file uploaded"
#             })
#
#         ext = os.path.splitext(file.name)[1].lower()
#         if ext not in [".wav", ".mp3", ".ogg"]:
#             return render(request, "parent/upload_audio.html", {
#                 "msg": "Unsupported audio format"
#             })
#
#         # Save audio
#         save_dir = "media/uploads"
#         os.makedirs(save_dir, exist_ok=True)
#
#         filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ext
#         path = os.path.join(save_dir, filename)
#
#         with open(path, "wb+") as f:
#             for chunk in file.chunks():
#                 f.write(chunk)
#
#         # Predict
#         result = check_audio(path)
#
#         return render(request, "parent/upload_audio.html", {
#             "msg": result["label"],
#             "accuracy": result["confidence"]
#         })
#
#     return render(request, "parent/upload_audio.html")
#



import os
import datetime
import numpy as np
import librosa

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from tensorflow.keras.models import load_model


# ==================================================
# LOAD MODEL (LOAD ONLY ONCE)
# ==================================================
MODEL_PATH = r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\audio_detector.h5"
audio_model = load_model(MODEL_PATH)

print("✅ Audio model loaded successfully")
audio_model.summary()


# ==================================================
# CONFIG
# ==================================================
SAMPLE_RATE = 22050
N_MFCC = 60
FIXED_FRAMES = 13
AUTISM_THRESHOLD = 0.70     # 🔥 IMPORTANT
MIN_RMS_ENERGY = 0.01       # 🔥 SPEECH FILTER


# ==================================================
# FEATURE EXTRACTION
# ==================================================
def extract_features(audio_path):
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=SAMPLE_RATE)

        # Reject silent / non-speech audio
        rms = np.mean(librosa.feature.rms(y=y))
        if rms < MIN_RMS_ENERGY:
            print("❌ Non-speech or silent audio rejected")
            return None

        # Extract MFCC
        mfcc = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=N_MFCC
        )

        # Fix frame length
        if mfcc.shape[1] < FIXED_FRAMES:
            pad = FIXED_FRAMES - mfcc.shape[1]
            mfcc = np.pad(mfcc, ((0, 0), (0, pad)), mode="constant")
        else:
            mfcc = mfcc[:, :FIXED_FRAMES]

        # Shape → (13, 60)
        mfcc = mfcc.T

        return mfcc

    except Exception as e:
        print("❌ Feature extraction error:", e)
        return None


# ==================================================
# AUDIO PREDICTION
# ==================================================
def check_audio(audio_path):
    features = extract_features(audio_path)

    if features is None:
        return {
            "label": "Invalid / Non-speech Audio",
            "confidence": 0.0
        }

    # Expand dims → (1, 13, 60)
    features = np.expand_dims(features, axis=0)

    print("🧠 Input shape:", features.shape)

    # Predict
    prediction = audio_model.predict(features, verbose=0)[0][0]

    # 🔥 MODEL OUTPUT = NORMAL PROBABILITY
    autism_prob = 1 - prediction
    confidence = round(float(autism_prob) * 100, 2)

    print("🔍 Autism probability:", autism_prob)

    if autism_prob >= AUTISM_THRESHOLD:
        label = "Autism is Positive"
    else:
        label = "Autism is Negative"

    return {
        "label": label,
        "confidence": confidence
    }


# ==================================================
# AUDIO UPLOAD PAGE
# ==================================================
@login_required(login_url='/myapp/login_get/')
def audioupload(request):
    return render(request, "parent/upload_audio.html")


# ==================================================
# AUDIO PREDICTION VIEW
# ==================================================
@csrf_exempt
@login_required(login_url='/myapp/login_get/')
def check_autism(request):
    if request.method == "POST":
        file = request.FILES.get("file")

        if not file:
            return render(request, "parent/upload_audio.html", {
                "msg": "❌ No audio file uploaded"
            })

        ext = os.path.splitext(file.name)[1].lower()
        if ext not in [".wav", ".mp3", ".ogg"]:
            return render(request, "parent/upload_audio.html", {
                "msg": "❌ Unsupported audio format"
            })

        # Save audio
        save_dir = "media/uploads"
        os.makedirs(save_dir, exist_ok=True)

        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ext
        path = os.path.join(save_dir, filename)

        with open(path, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Predict
        result = check_audio(path)

        return render(request, "parent/upload_audio.html", {
            "msg": result["label"],
            "accuracy": f"{result['confidence']} %"
        })

    return render(request, "parent/upload_audio.html")







###########Questionaries

#
# import numpy as np
# from django.shortcuts import render
# from joblib import load
#
# MODEL_Q = load(r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\AutismDecisionTree.joblib")
# #
# # QUESTIONS = [
# #     "I prefer to do things with others rather than on my own",
# #     "I prefer to do things the same way over and over again",
# #     "If I try to imagine something, I find it very easy to create a picture in my mind",
# #     "I frequently get so strongly absorbed in one thing that I lose sight of other things",
# #     "I often notice small sounds when others do not",
# #     "I usually notice car number plates or similar strings of information",
# #     "Other people frequently tell me that what I’ve said is impolite, even though I think it is polite",
# #     "When I’m reading a story, I can easily imagine what the characters might look like",
# #     "I am fascinated by dates",
# #     "In a social group, I can easily keep track of several different people’s conversations",
# #     "I find social situations easy",
# #     "I tend to notice details that others do not",
# #     "I would rather go to a library than a party",
# #     "I find making up stories easy",
# #     "I find myself drawn more strongly to people than to things",
# #     "I tend to have very strong interests, which I get upset about if I can’t pursue",
# #     "I enjoy social chit-chat",
# #     "When I talk, it isn’t always easy for others to get a word in edgeways",
# #     "I am fascinated by numbers",
# #     "When I’m reading a story, I find it difficult to work out the characters’ intentions",
# #     "I don’t particularly enjoy reading fiction",
# #     "I find it hard to make new friends",
# #     "I notice patterns in things all the time",
# #     "I would rather go to the theatre than a museum",
# #     "It does not upset me if my daily routine is disturbed",
# #     "I frequently find that I don’t know how to keep a conversation going",
# #     "I find it easy to “read between the lines” when someone is talking to me",
# #     "I usually concentrate more on the whole picture, rather than the small details",
# #     "I am not very good at remembering phone numbers",
# #     "I don’t usually notice small changes in a situation, or a person’s appearance",
# #     "I know how to tell if someone listening to me is getting bored",
# #     "I find it easy to do more than one thing at once",
# #     "When I talk on the phone, I’m not sure when it’s my turn to speak",
# #     "I enjoy doing things spontaneously",
# #     "I am often the last to understand the point of a joke",
# #     "I find it easy to work out what someone is thinking or feeling just by looking at their face",
# #     "If there is an interruption, I can switch back to what I was doing very quickly",
# #     "I am good at social chit-chat",
# #     "People often tell me that I keep going on and on about the same thing",
# #     "When I was young, I used to enjoy playing games involving pretending with other children",
# #     "I like to collect information about categories of things",
# #     "I find it difficult to imagine what it would be like to be someone else",
# #     "I like to plan any activities I participate in carefully",
# #     "I enjoy social occasions",
# #     "I find it difficult to work out people’s intentions",
# #     "New situations make me anxious",
# #     "I enjoy meeting new people",
# #     "I am a good diplomat",
# #     "I am not very good at remembering people’s date of birth",
# #     "I find it very easy to play games with children that involve pretending"
# # ]
#
# QUESTIONS = [
#
#   "Does your child respond when their name is called?",
#   "Does your child smile back when someone smiles at them?",
#   "Does your child enjoy playing with other children?",
#   "Does your child make eye contact during play or interaction?",
#   "Does your child try to get your attention to show something?",
#   "Does your child look at you when you point to an object?",
#   "Does your child enjoy being hugged or held?",
#   "Does your child copy actions like clapping or waving?",
#   "Does your child show interest in people around them?",
#   "Does your child try to join group play activities?",
#   "Does your child use words or sounds to express needs?",
#   "Does your child point to objects they want?",
#   "Does your child try to imitate words spoken by others?",
#   "Does your child respond to simple verbal instructions?",
#   "Does your child use gestures like waving or nodding?",
#   "Does your child repeat the same words or sounds frequently?",
#   "Does your child talk more when excited or happy?",
#   "Does your child combine two or more words meaningfully?",
#   "Does your child communicate using facial expressions?",
#   "Does your child attempt to start communication on their own?",
#   "Does your child get upset when daily routines change?",
#   "Does your child insist on doing things in a specific order?",
#   "Does your child repeat the same actions again and again?",
#   "Does your child line up toys instead of playing with them?",
#   "Does your child focus on one toy for a long time?",
#   "Does your child get distressed if a favorite activity stops?",
#   "Does your child repeat the same game or activity daily?",
#   "Does your child show unusual attachment to certain objects?",
#   "Does your child become upset by small changes?",
#   "Does your child prefer familiar activities over new ones?",
#   "Does your child react strongly to loud noises?",
#   "Does your child avoid certain textures or fabrics?",
#   "Does your child notice small sounds that others ignore?",
#   "Does your child dislike bright lights or crowded places?",
#   "Does your child cover their ears in noisy environments?",
#   "Does your child enjoy spinning or watching moving objects?",
#   "Does your child react unusually to smells or tastes?",
#   "Does your child resist haircuts or nail trimming?",
#   "Does your child seek sensory stimulation like touching objects repeatedly?",
#   "Does your child show unusual reactions to temperature changes?",
#   "Does your child engage in pretend play such as feeding dolls?",
#   "Does your child play imaginatively with toys?",
#   "Does your child prefer playing alone rather than with others?",
#   "Does your child understand simple emotions like happy or sad?",
#   "Does your child seek comfort from parents when upset?",
#   "Does your child show frustration easily?",
#   "Does your child maintain attention during play?",
#   "Does your child switch between activities easily?",
#   "Does your child show interest in new toys or games?",
#   "Does your child respond appropriately to others’ emotions?"
# ]
#
# def predict_autism_question(request):
#
#     # ---------- GET REQUEST ----------
#     if request.method == "GET":
#         return render(request, "predict_question.html", {
#             "questions": QUESTIONS
#         })
#
#     # ---------- POST REQUEST ----------
#     if request.method == "POST":
#
#         age = int(request.POST["age"])
#         sex = request.POST["sex"]
#         jaundice = request.POST["jaundice"]
#         family_asd = request.POST["family_asd"]
#
#         agree_questions = {
#             1,2,4,5,6,7,9,12,13,16,18,19,20,21,22,
#             23,26,33,35,39,41,42,43,45,46
#         }
#
#         aq = []
#         for i in range(1, 51):
#             val = int(request.POST[f"ans{i}"])
#
#             if i in agree_questions:
#                 aq.append(1 if val in [1, 2] else 0)
#             else:
#                 aq.append(1 if val in [3, 4] else 0)
#
#         # Group into 10 features
#         grouped = [sum(aq[i*5:(i+1)*5]) for i in range(10)]
#
#         # Encode categorical values
#         sex = 0 if sex == "m" else 1
#         jaundice = 1 if jaundice == "yes" else 0
#         family_asd = 1 if family_asd == "yes" else 0
#
#         X = np.array(grouped + [age, sex, jaundice, family_asd]).reshape(1, -1)
#
#         pred = MODEL_Q.predict(X)[0]
#         result = "AUTISM YES" if pred == 1 else "AUTISM NO"
#
#         request.session["qna_result"] = result
#
#         return render(request, "final_result.html", {
#             "qna": result
#         })
#







#####################


#
#
# import numpy as np
# from joblib import load
#
# MODEL_Q = load(r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\AutismDecisionTree.joblib")
#
# QUESTIONS = [
#
#   "Does your child respond when their name is called?",
#   "Does your child smile back when someone smiles at them?",
#   "Does your child enjoy playing with other children?",
#   "Does your child make eye contact during play or interaction?",
#   "Does your child try to get your attention to show something?",
#   "Does your child look at you when you point to an object?",
#   "Does your child enjoy being hugged or held?",
#   "Does your child copy actions like clapping or waving?",
#   "Does your child show interest in people around them?",
#   "Does your child try to join group play activities?",
#   "Does your child use words or sounds to express needs?",
#   "Does your child point to objects they want?",
#   "Does your child try to imitate words spoken by others?",
#   "Does your child respond to simple verbal instructions?",
#   "Does your child use gestures like waving or nodding?",
#   "Does your child repeat the same words or sounds frequently?",
#   "Does your child talk more when excited or happy?",
#   "Does your child combine two or more words meaningfully?",
#   "Does your child communicate using facial expressions?",
#   "Does your child attempt to start communication on their own?",
#   "Does your child get upset when daily routines change?",
#   "Does your child insist on doing things in a specific order?",
#   "Does your child repeat the same actions again and again?",
#   "Does your child line up toys instead of playing with them?",
#   "Does your child focus on one toy for a long time?",
#   "Does your child get distressed if a favorite activity stops?",
#   "Does your child repeat the same game or activity daily?",
#   "Does your child show unusual attachment to certain objects?",
#   "Does your child become upset by small changes?",
#   "Does your child prefer familiar activities over new ones?",
#   "Does your child react strongly to loud noises?",
#   "Does your child avoid certain textures or fabrics?",
#   "Does your child notice small sounds that others ignore?",
#   "Does your child dislike bright lights or crowded places?",
#   "Does your child cover their ears in noisy environments?",
#   "Does your child enjoy spinning or watching moving objects?",
#   "Does your child react unusually to smells or tastes?",
#   "Does your child resist haircuts or nail trimming?",
#   "Does your child seek sensory stimulation like touching objects repeatedly?",
#   "Does your child show unusual reactions to temperature changes?",
#   "Does your child engage in pretend play such as feeding dolls?",
#   "Does your child play imaginatively with toys?",
#   "Does your child prefer playing alone rather than with others?",
#   "Does your child understand simple emotions like happy or sad?",
#   "Does your child seek comfort from parents when upset?",
#   "Does your child show frustration easily?",
#   "Does your child maintain attention during play?",
#   "Does your child switch between activities easily?",
#   "Does your child show interest in new toys or games?",
#   "Does your child respond appropriately to others’ emotions?"
# ]
#
# def predict_autism_question(request):
#
#     # ---------- GET REQUEST ----------
#     if request.method == "GET":
#         return render(request, "predict_question.html", {
#             "questions": QUESTIONS
#         })
#
#     # ---------- POST REQUEST ----------
#     if request.method == "POST":
#
#         age = int(request.POST["age"])
#         sex = request.POST["sex"]
#         jaundice = request.POST["jaundice"]
#         family_asd = request.POST["family_asd"]
#
#         agree_questions = {
#             1,2,4,5,6,7,9,12,13,16,18,19,20,21,22,
#             23,26,33,35,39,41,42,43,45,46
#         }
#
#         aq = []
#         for i in range(1, 51):
#             val = int(request.POST[f"ans{i}"])
#
#             if i in agree_questions:
#                 aq.append(1 if val in [1, 2] else 0)
#             else:
#                 aq.append(1 if val in [3, 4] else 0)
#
#         # Group into 10 features
#         grouped = [sum(aq[i*5:(i+1)*5]) for i in range(10)]
#
#         # Encode categorical values
#         sex = 0 if sex == "m" else 1
#         jaundice = 1 if jaundice == "yes" else 0
#         family_asd = 1 if family_asd == "yes" else 0
#
#         X = np.array(grouped + [age, sex, jaundice, family_asd]).reshape(1, -1)
#
#         pred = MODEL_Q.predict(X)[0]
#         result = "AUTISM YES" if pred == 1 else "AUTISM NO"
#
#         request.session["qna_result"] = result
#
#         return render(request, "final_result.html", {
#             "qna": result
#         })



import numpy as np
from joblib import load
from django.shortcuts import render

MODEL_Q = load(
    r"C:\Users\USER\Desktop\project\AUTISM_DETECTION\AUTISM_DETECTION\myapp\AutismDecisionTree.joblib"
)

QUESTIONS = [
    "Does your child respond when their name is called?",
    "Does your child smile back when someone smiles at them?",
    "Does your child enjoy playing with other children?",
    "Does your child make eye contact during play or interaction?",
    "Does your child try to get your attention to show something?",
    "Does your child look at you when you point to an object?",
    "Does your child enjoy being hugged or held?",
    "Does your child copy actions like clapping or waving?",
    "Does your child show interest in people around them?",
    "Does your child try to join group play activities?",
    "Does your child use words or sounds to express needs?",
    "Does your child point to objects they want?",
    "Does your child try to imitate words spoken by others?",
    "Does your child respond to simple verbal instructions?",
    "Does your child use gestures like waving or nodding?",
    "Does your child repeat the same words or sounds frequently?",
    "Does your child talk more when excited or happy?",
    "Does your child combine two or more words meaningfully?",
    "Does your child communicate using facial expressions?",
    "Does your child attempt to start communication on their own?",
    "Does your child get upset when daily routines change?",
    "Does your child insist on doing things in a specific order?",
    "Does your child repeat the same actions again and again?",
    "Does your child line up toys instead of playing with them?",
    "Does your child focus on one toy for a long time?",
    "Does your child get distressed if a favorite activity stops?",
    "Does your child repeat the same game or activity daily?",
    "Does your child show unusual attachment to certain objects?",
    "Does your child become upset by small changes?",
    "Does your child prefer familiar activities over new ones?",
    "Does your child react strongly to loud noises?",
    "Does your child avoid certain textures or fabrics?",
    "Does your child notice small sounds that others ignore?",
    "Does your child dislike bright lights or crowded places?",
    "Does your child cover their ears in noisy environments?",
    "Does your child enjoy spinning or watching moving objects?",
    "Does your child react unusually to smells or tastes?",
    "Does your child resist haircuts or nail trimming?",
    "Does your child seek sensory stimulation like touching objects repeatedly?",
    "Does your child show unusual reactions to temperature changes?",
    "Does your child engage in pretend play such as feeding dolls?",
    "Does your child play imaginatively with toys?",
    "Does your child prefer playing alone rather than with others?",
    "Does your child understand simple emotions like happy or sad?",
    "Does your child seek comfort from parents when upset?",
    "Does your child show frustration easily?",
    "Does your child maintain attention during play?",
    "Does your child switch between activities easily?",
    "Does your child show interest in new toys or games?",
    "Does your child respond appropriately to others’ emotions?"
]

def predict_autism_question(request):

    if request.method == "GET":
        return render(request, "predict_question.html", {
            "questions": QUESTIONS
        })

    if request.method == "POST":

        # ---------- DEMOGRAPHICS ----------
        age = int(request.POST["age"])
        sex = 0 if request.POST["sex"] == "m" else 1
        jaundice = 1 if request.POST["jaundice"] == "yes" else 0
        family_asd = 1 if request.POST["family_asd"] == "yes" else 0

        # ---------- AQ SCORING ----------
        aq = []
        for i in range(1, 51):
            val = int(request.POST[f"ans{i}"])
            aq.append(1 if val in [1, 2] else 0)

        # ---------- GROUP INTO 10 FEATURES ----------
        grouped_aq = [
            sum(aq[i*5:(i+1)*5]) for i in range(10)
        ]  # each range: 0–5

        # ---------- FINAL FEATURE VECTOR (14) ----------
        X = np.array(
            grouped_aq + [age, sex, jaundice, family_asd]
        ).reshape(1, -1)

        # ---------- PREDICTION ----------
        pred = MODEL_Q.predict(X)[0]

        result = "AUTISM YES" if pred == 1 else "AUTISM NO"

        return render(request, "final_result.html", {
            "qna": result,
            "aq_groups": grouped_aq
        })





#################################

import cv2
import os
import uuid

def process_video2(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {
            "label": "Video Error",
            "confidence": 0
        }

    results = []
    frame_interval = 30
    frame_index = 0
    max_samples = 20

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % frame_interval == 0:
            temp_img_path = f"temp_{uuid.uuid4().hex}.png"

            if cv2.imwrite(temp_img_path, frame):
                label, _ = check_image(temp_img_path)

                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)

                results.append(label.lower())

                if len(results) >= max_samples:
                    break

        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()

    # classification mapping
    positive = ["inattentive", "combined", "hyperactive"]
    negative = ["others", "typically developing"]

    pos_count = sum(r in positive for r in results)
    neg_count = sum(r in negative for r in results)
    total = pos_count + neg_count

    if total == 0:
        return {
            "label": "Unknown result",
            "confidence": 0
        }

    confidence = round((max(pos_count, neg_count) / total) * 100, 2)

    if pos_count > neg_count:
        label = "Autism is Positive"
    elif neg_count > pos_count:
        label = "Autism is Negative"
    else:
        label = "Unknown result"

    return {
        "label": label,
        "confidence": confidence
    }

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

def predict_autism_video(request):

    if request.method == "GET":
        return render(request, "predict_video.html")

    video = request.FILES.get("video")
    if not video:
        return render(request, "predict_video.html", {
            "error": "Upload video"
        })

    fs = FileSystemStorage(location="media/videos")
    name = fs.save(video.name, video)
    path = fs.path(name)

    # process video
    result = process_video2(path)

    # store in session
    request.session["video_result"] = result["label"]
    request.session["video_confidence"] = result["confidence"]

    return redirect("/myapp/final_autism_result2/")


def final_autism_result2(request):
    return render(request, "video_final_result.html", {
        "video": request.session.get("video_result"),
        "accuracy": request.session.get("video_confidence")
    })

# from django.core.files.storage import FileSystemStorage
#
# def predict_autism_video(request):
#
#     if request.method == "GET":
#         return render(request, "predict_video.html")
#
#     video = request.FILES.get("video")
#     if not video:
#         return render(request, "predict_video.html", {"error": "Upload video"})
#
#     fs = FileSystemStorage()
#     name = fs.save(video.name, video)
#     path = fs.path(name)
#
#     video_result = process_video2(path)
#
#     request.session["video_result"] = video_result
#     request.session["video_confidence"] = video_result['confidence']
#     return redirect("/myapp/final_autism_result2/")

# def final_autism_result2(request):
#     return render(request, "video_final_result.html", {
#         "video": request.session.get("video_result"),
#
#             "accuracy": request.session.get("video_confidence")
#     })



def final_autism_result(request):
    return render(request, "final_result.html", {
        "qna": request.session.get("qna_result"),
    })

