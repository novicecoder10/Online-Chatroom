from django.db import models


# Create your models here.

class login(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=50)


class register(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.CharField(max_length=200)
    gender = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.BigIntegerField()
    lid = models.ForeignKey(login, on_delete=models.CASCADE)


class profile(models.Model):
    user = models.CharField(max_length=50)
    image = models.ImageField(upload_to='uploads')
    bio = models.CharField(max_length=1000)
    status = models.CharField(max_length=50)
    about = models.CharField(max_length=300)
    pid = models.ForeignKey(register, on_delete=models.CASCADE)


class rooms(models.Model):
    room_creator = models.ForeignKey(profile, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)


class room_members(models.Model):
    rid = models.ForeignKey(rooms, on_delete=models.CASCADE)
    usid = models.ForeignKey(register, on_delete=models.CASCADE)


class chats(models.Model):
    chat = models.CharField(max_length=9999999)
    cid = models.ForeignKey(rooms, on_delete=models.CASCADE)
    tid = models.ForeignKey(profile, on_delete=models.CASCADE)


class moderators(models.Model):
    moderator = models.CharField(max_length=50)
    gid = models.ForeignKey(rooms, on_delete=models.CASCADE)


class connections(models.Model):
    userid = models.ForeignKey(profile, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    crid = models.ForeignKey(register, on_delete=models.CASCADE)


class feedback(models.Model):
    uid = models.ForeignKey(register, on_delete=models.CASCADE)
    feed = models.CharField(max_length=500)


class private(models.Model):
    chat = models.CharField(max_length=9999999)
    regid = models.ForeignKey(register, on_delete=models.CASCADE)
    pid = models.ForeignKey(profile, on_delete=models.CASCADE)


    