from django.db import models

# Create your models here.
class Staffs(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    gender = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    profile_picture = models.FileField(upload_to='profile_picture')
    attachment = models.FileField(upload_to='attachments')
    status = models.BooleanField(default=True)
    access = models.BooleanField(default=True)
    shift = models.CharField(max_length=20)

    class Meta:
        db_table = 'staffs'


class Expences(models.Model):
    Purchase = models.CharField(max_length=100)
    Remark = models.CharField(max_length=250)
    Amount = models.CharField(max_length=10)
    Date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'expenses'


class Returns(models.Model):
    Date = models.DateField(auto_now_add=True)
    Staff  = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    Description = models.TextField()

    class Meta:
        db_table = 'Returns'
