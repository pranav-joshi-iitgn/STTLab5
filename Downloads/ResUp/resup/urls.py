from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("company/<int:id>/",views.company,name="company"),
    path("job/<int:id>/",views.job,name="job"),
    path("student/<int:id>/<str:password>",views.student,name='student'),
    path("application/<int:id>/<str:password>",views.application,name="application"),
    path("register_company/",views.register_company),
    path("register_student/",views.register_student),
    path("register_job/",views.register_job),
    path("success/",views.success),
    path("delete/",views.delete),
]