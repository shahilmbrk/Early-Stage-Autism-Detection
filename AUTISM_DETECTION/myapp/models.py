from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Expert_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    photo=models.CharField(max_length=200)
    phone=models.BigIntegerField()

class Parent_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    phone=models.BigIntegerField()

class Student_table(models.Model):
    PARENT=models.ForeignKey(Parent_table,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    age=models.CharField(max_length=100)
    photo=models.CharField(max_length=300)


class Feedback_table(models.Model):
    date=models.DateField()
    feedback=models.CharField(max_length=100)
    rating=models.FloatField()
    PARENT=models.ForeignKey(Parent_table,on_delete=models.CASCADE)


class Tips_table(models.Model):
    date=models.DateField()
    tips=models.CharField(max_length=100)
    details=models.CharField(max_length=200)
    EXPERT=models.ForeignKey(Expert_table,on_delete=models.CASCADE)



class Studymaterial_table(models.Model):
    date=models.DateField()
    title=models.CharField(max_length=100)
    file=models.CharField(max_length=200)
    EXPERT=models.ForeignKey(Expert_table,on_delete=models.CASCADE)




class Chat_table(models.Model):
    date=models.DateField()
    message=models.CharField(max_length=100)
    FROM=models.ForeignKey(User,on_delete=models.CASCADE,related_name='fuser')
    TO=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tuser')


class Test_table(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=100)
    details = models.CharField(max_length=200)
    level = models.CharField(max_length=100)
    EXPERT = models.ForeignKey(Expert_table, on_delete=models.CASCADE)

class Question_table(models.Model):
    date = models.DateField()
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    TEST = models.ForeignKey(Test_table, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    file = models.CharField(max_length=250)
    startime = models.CharField(max_length=100)
    endtime = models.CharField(max_length=100)


class Attend_table(models.Model):
    QUESTION = models.ForeignKey(Question_table, on_delete=models.CASCADE)
    STUDENT = models.ForeignKey(Student_table, on_delete=models.CASCADE)
    solution = models.CharField(max_length=100)
    mark = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    date = models.DateField()


class Medicalreport(models.Model):
    STUDENT = models.ForeignKey(Student_table, on_delete=models.CASCADE)
    file = models.CharField(max_length=200)
    details = models.CharField(max_length=200)
    date = models.DateField()



class Guidline(models.Model):
    MEDICALREPORT = models.ForeignKey(Medicalreport, on_delete=models.CASCADE)
    EXPERT = models.ForeignKey(Expert_table, on_delete=models.CASCADE)
    guidline = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    date = models.DateField()


class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

class Result(models.Model):
    ATTENDTABLE=models.ForeignKey(Attend_table,on_delete=models.CASCADE)
    similarity_percent = models.CharField(max_length=100)
    mark = models.CharField(max_length=100)
    solving_time = models.CharField(max_length=100)
    prediction = models.CharField(max_length=100)
    message = models.CharField(max_length=100)

class audio_table(models.Model):
    file=models.FileField()
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    result=models.CharField(max_length=100)
