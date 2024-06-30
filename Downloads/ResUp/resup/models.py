from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default="")
    password = models.CharField(max_length=50, default="")

class Job(models.Model):
    position = models.CharField(max_length=200,default="unknown position")
    company = models.ForeignKey(Company,on_delete = models.CASCADE)
    skills = models.TextField(default = "")
    cpi = models.FloatField(default=3)
    branch = models.CharField(default="",max_length=200)
    description = models.TextField(default="")
    exp = models.IntegerField(default=0)
    level = models.CharField(default="",max_length=100)
    stack = models.TextField(default="")

class Student(models.Model):
    name = models.CharField(max_length=200)
    skills = models.TextField(default = "")
    stack = models.TextField(default="")
    projects = models.TextField(default = "")
    cpi = models.FloatField(default=9)
    branch = models.CharField(default="",max_length=200)
    description = models.TextField(default="")
    level = models.CharField(default="",max_length=100)
    password = models.TextField(default="")

class Application(models.Model):
    job = models.ForeignKey(Job,on_delete = models.CASCADE)
    student = models.ForeignKey(Student,on_delete = models.CASCADE)
    score = models.FloatField(default = 0)
    resume = models.FileField(default="example.pdf")
    suggestions = models.TextField(default="None.")
    exp = models.IntegerField(default=0)
    absent_skills = models.TextField(default="")
    absent_stack = models.TextField(default="")
    skillscore = models.FloatField(default=0)
    techscore = models.FloatField(default=0)
    simscore = models.FloatField(default=0)


