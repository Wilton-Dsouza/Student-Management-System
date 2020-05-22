from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


from student_management_app.models import CustomUser, Staffs, Courses, Subjects, Students


def admin_home(request):
    return render(request,"hod_template/home_content.html")

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect("/add_staff")

def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed")
    else:
        course = request.POST.get("course")
        if(not course):
            messages.error(request, "Failed to Add Association")
            return HttpResponseRedirect("/add_course")
        else:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Successfully Added Association")
            return HttpResponseRedirect("/add_course")

def add_student(request):
    courses = Courses.objects.all()
    return render(request, "hod_template/add_student_template.html", {"courses": courses})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name,profile_pic)
        profile_pic_url = fs.url(filename)
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,last_name=last_name,first_name=first_name, user_type=3)
            user.students.address = address
            course_obj = Courses.objects.get(id=course_id)
            user.students.course_id = course_obj
            user.students.session_start_year = session_start
            user.students.session_end_year = session_end
            user.students.gender = sex
            user.students.profile_pic = profile_pic_url
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect("/add_student")
        except:
            messages.error(request, "Failed to Add Student")
            return HttpResponseRedirect("/add_student")

def add_subject(request):
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/add_subject_template.html",{"staffs":staffs})

def add_subject_save(request):
    if request.method!="POST":
        return render("<h2>Method not allowed</h2>")
    else:
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
        if(not subject_name):
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect("/add_subject")
        else:
            subject = Subjects(subject_name=subject_name, staff_id=staff)
            subject.save()
            messages.success(request, "Successfully Added Subject")
            return HttpResponseRedirect("/add_subject")
def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_student(request):
    students = Students.objects.all()
    return render(request, "hod_template/manage_student_template.html", {"students": students})

def manage_course(request):
    courses=Courses.objects.all()
    return render(request,"hod_template/manage_association_template.html",{"courses":courses})

def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, "hod_template/manage_subject_template.html", {"subjects": subjects})

def edit_staff(request,staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")
        user = CustomUser.objects.get(id=staff_id)
        if(not staff_id or not first_name or not last_name or not email or not username or not address):
            messages.error(request, "Failed to Edit Staff")
            return HttpResponseRedirect("/edit_staff/" + staff_id)
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, "Successfully Edited Staff")
            return HttpResponseRedirect("/edit_staff/" + staff_id)

def edit_student(request,student_id):
    courses = Courses.objects.all()
    student = Students.objects.get(admin=student_id)
    return render(request,"hod_template/edit_student_template.html",{"student":student,"courses":courses})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method not allowed</h2>")
    else:
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        session_start = request.POST.get("session_start")
        session_end = request.POST.get("session_end")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        if request.FILES['profile_pic']:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

        else:
            profile_pic_url = None
        if(not student_id or not first_name or not last_name or not username or not email or not address or not session_start or not session_end or not course_id or not sex ):
            messages.error(request, "Failed to Edit Student")
            return HttpResponseRedirect("/edit_student/"+student_id)
        else:
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            student = Students.objects.get(admin=student_id)
            student.address = address
            student.session_start_year = session_start
            student.session_end_year = session_end
            student.gender = sex
            course = Courses.objects.get(id=course_id)
            student.course_id = course
            if profile_pic_url!=None:
                student.profile_pic = profile_pic_url
            student.save()
            messages.success(request, "Successfully Edited Student")
            return HttpResponseRedirect("/edit_student/"+student_id)

def delete_staff(request,staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    user = CustomUser.objects.get(id=staff_id)
    staff.delete()
    user.delete()
    return HttpResponseRedirect("/manage_staff")

def delete_student(request,student_id):
    student = Students.objects.get(admin=student_id)
    user = CustomUser.objects.get(id=student_id)
    student.delete()
    user.delete()
    return HttpResponseRedirect("/manage_student")

def delete_course(request,course_id):
    course = Courses.objects.get(id=course_id)
    course.delete()
    return HttpResponseRedirect("/manage_course")

def delete_subject(request,subject_id):
    subject = Subjects.objects.get(id=subject_id)
    subject.delete()
    return HttpResponseRedirect("/manage_subject")

def edit_subject(request,subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request,"hod_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"courses":courses})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staff")
        course_id = request.POST.get("course")
        if(not subject_name or not subject_id or not course_id):
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect("/edit_subject/"+subject_id)
        else:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()
            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect("/edit_subject/"+subject_id)

def edit_course(request,course_id):
    course = Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")
        if(not course_name):
            messages.error(request, "Failed to Edit Association")
            return HttpResponseRedirect("/edit_course/" + course_id)

        else:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, "Successfully Edited Association")
            return HttpResponseRedirect("/edit_course/" + course_id)

