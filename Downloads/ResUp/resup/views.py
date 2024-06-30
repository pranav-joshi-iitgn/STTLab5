from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Company, Job, Student, Application
from .Scoring import score
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def file_upload(file):
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    uploaded_file_url = fs.url(filename)
    return "/home/PranavJoshiIitgn/ResUp" + uploaded_file_url , "https://pranavjoshiiitgn.pythonanywhere.com" + uploaded_file_url
    #save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file)
    #path = default_storage.save(save_path, file)
    #return default_storage.path(path)

all_possible_branches = "CSE,Mechanical,Electrical,Civil,AI,MSE"
all_possible_levels = "BTech,Btech,Btech 1st year,Btech 2nd year,Btech 3rd year,Mtech,MS,PhD"

def give_score_and_suggest(A,path,url):
    global all_possible_branches,all_possible_levels
    J = A.job
    S = A.student
    jd = J.description
    technologies = [t.strip() for t in J.stack.split(",")]
    skills = [s.strip() for s in J.skills.split(",")]
    CGPA_Req = J.cpi
    Working_exp = J.exp
    Branch_req = J.branch
    if Branch_req in ["","all"]:Branch_req = all_possible_branches
    Branch_req = [b.strip() for b in Branch_req.split(",")]
    education_req = J.level
    if education_req in ["","all"]:education_req = all_possible_levels
    education_req = [e.strip() for e in education_req.split(",")]
    #Candidate_resume_path = A.resume.path
    Candidate_resume_path = path
    candidate_CGPA = S.cpi
    candidate_Working_exp = A.exp
    candidate_Branch = S.branch
    candidate_education = S.level
    L =  score(
        Candidate_resume_path,
        candidate_CGPA, candidate_Working_exp,
        candidate_Branch, candidate_education,
        jd,
        skills,
        technologies,
        CGPA_Req,
        Working_exp,
        Branch_req,
        education_req
    )
    if isinstance(L,str):
        return L
    final_score, absent_skills, absent_tech, skillscore, techscore, sim_score = L
    A.resume = url
    A.score = final_score
    A.absent_skills = ",".join([s[0] for s in absent_skills])
    A.absent_stack = ",".join([t[0] for t in absent_tech])
    A.skillscore = skillscore
    A.techscore = techscore
    A.simscore = sim_score
    return "Done"

# Create your views here.

def index(request):
    Companies = Company.objects.all()
    Students = Student.objects.all()
    Jobs = Job.objects.all()
    return render(request,"resup/index.html",{"Companies":Companies,"Students":Students,"Jobs":Jobs})

def company(request,id):
    C = get_object_or_404(Company,pk=id)
    return render(request,"resup/company.html",{"C":C})

def job(request,id):
    J = get_object_or_404(Job,pk=id)
    applicants = len(J.application_set.all())
    return render(request,"resup/job.html",{"J":J,"applicants":applicants})

def student(request,id,password):
    S = get_object_or_404(Student,pk=id)
    if S.password != password : show=False
    else : show=True
    return render(request,"resup/student.html",{"S":S,"show":show})

def application(request,id,password):
    A = get_object_or_404(Application,pk=id)
    show = (A.student.password == password)
    return render(request,"resup/application.html",{"A":A,"show":show})

def register_company(request):
    return render(request,"resup/register_company.html")

def register_student(request):
    return render(request,"resup/register_student.html")

def register_job(request):
    return render(request,"resup/register_job.html")

def success(request):
    global all_possible_branches,all_possible_levels
    type = request.POST['type']
    if type == "company":
        name = request.POST['name']
        description = request.POST['description']
        password = request.POST["password"]
        if len(Company.objects.filter(name=name)) > 0 :
            return HttpResponse(name+ " is already registered")
        C = Company(name=name,description=description,password=password)
        C.save()
        return HttpResponseRedirect(f"/resup/company/{C.id}")
    elif type == "application":
        Jid = int(request.POST["Jid"])
        Sid = int(request.POST["id"])
        resume = request.FILES["resume"]
        password = request.POST["password"]
        exp = int(request.POST["exp"])
        J = Job.objects.get(pk=Jid)
        S = Student.objects.get(pk=Sid)
        if password != S.password:
            return HttpResponse("incorrect password")
        if J.cpi > S.cpi:
            return HttpResponse("CPI requirement not met")

        path,url = file_upload(resume)

        A = Application(student=S,job=J,resume=resume,exp=exp)
        status = give_score_and_suggest(A,path,url)
        if status != "Done":
            return HttpResponse(status)
        else:
            A.save()
            return HttpResponseRedirect(f"/resup/application/{A.id}/{S.password}")
    elif type=="student":
        name = request.POST['name']
        password = request.POST['password']
        skills = request.POST['skills']
        stack = request.POST['stack']
        branch = request.POST["branch"]
        projects = request.POST['projects']
        description = request.POST['description']
        level = request.POST['level']
        cpi = request.POST['cpi']
        S = Student(
            name=name,skills=skills,cpi=cpi,
            projects=projects,description=description,
            stack=stack,level=level,branch=branch,
            password=password
        )
        S.save()
        return HttpResponseRedirect(f"/resup/student/{S.id}/{password}")
    elif type=="job":
        position = request.POST["position"]
        skills = request.POST["skills"]
        stack = request.POST["stack"]
        description = request.POST["description"]
        password = request.POST["password"]
        cpi = request.POST["cpi"]
        branch = request.POST["branch"]
        if branch in ["all",""]:branch=all_possible_branches
        exp = request.POST["exp"]
        level = request.POST['level']
        if level in ["all",""]:level=all_possible_levels
        Cid = request.POST["Cid"]
        C = Company.objects.filter(id=Cid)
        if len(C) == 0:
            return HttpResponse(f"No company with id {Cid}")
        assert len(C) == 1
        C = C[0]
        if C.password != password:
            return HttpResponse("incorrect password")
        J = Job(
            company=C,
            position=position,
            skills=skills,
            description=description,
            cpi=cpi,
            branch=branch,
            stack=stack,
            exp=exp,
            level=level
        )
        J.save()
        return HttpResponseRedirect(f"/resup/job/{J.id}")
    elif type=="student_login":
        id = request.POST["id"]
        password = request.POST["password"]
        return HttpResponseRedirect(f"/resup/student/{id}/{password}")
    return HttpResponse(f"successfuly registered {name}.")

def delete(request):
    type = request.POST['type']
    id = request.POST['id']
    password = request.POST["password"]
    D = {"student":Student,"company":Company,"job":Job,"application":Application}
    L = D[type]
    O = L.objects.get(pk=id)
    if type == "application":real_password = O.student.password
    elif type == "job":real_password = O.company.password
    else:real_password = O.password
    if real_password != password:return HttpResponse("incorrect password")
    O.delete()
    return HttpResponse(f"deleted {type} with id {id}")


