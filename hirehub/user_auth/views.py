from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile,Project,Language
from .forms import CreateUserForm
import pdfkit
from django.template import loader 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('cv_create')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('cv_create')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('cv_create')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@csrf_exempt
@login_required(login_url='login')
def cv_create(request):
    if request.method == 'POST':
        # Retrieve form data
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        summary = request.POST.get('summary')
        school = request.POST.get('school')
        school_gpa = request.POST.get('school_gpa')
        school_joined_year = request.POST.get('school_joined_year')
        school_left_year = request.POST.get('school_left_year')
        college = request.POST.get('college')
        college_gpa = request.POST.get('college_gpa')
        stream = request.POST.get('stream')
        college_joined_year = request.POST.get('college_joined_year')
        college_left_year = request.POST.get('college_left_year')
        university = request.POST.get('university')
        university_gpa = request.POST.get('university_gpa')
        university_faculty = request.POST.get('university_faculty')
        university_joined_year = request.POST.get('university_joined_year')
        university_left_year = request.POST.get('university_left_year')
        technical_skills = request.POST.get('technical_skills')
        nontechnical_skills = request.POST.get('nontechnical_skills')
        reference_name = request.POST.get('reference_name')
        reference_position = request.POST.get('reference_position')
        reference_organization = request.POST.get('reference_organization')
        reference_email = request.POST.get('reference_email')
        reference_phone = request.POST.get('reference_phone')

        # Create and save the Profile instance
        profile = Profile.objects.create(
            full_name=full_name,
            address=address,
            email=email,
            phone=phone,
            summary=summary,
            school=school,
            school_gpa=float(school_gpa) if school_gpa else None,
            school_joined_year=school_joined_year,
            school_left_year=school_left_year,
            college=college,
            college_gpa=float(college_gpa) if college_gpa else None,
            stream=stream,
            college_joined_year=college_joined_year,
            college_left_year=college_left_year,
            university=university,
            university_gpa=float(university_gpa) if university_gpa else None,
            university_faculty=university_faculty,
            university_joined_year=university_joined_year,
            university_left_year=university_left_year,
            technical_skills=technical_skills,
            nontechnical_skills=nontechnical_skills,
            reference_name=reference_name,
            reference_position=reference_position,
            reference_organization=reference_organization,
            reference_email=reference_email,
            reference_phone=reference_phone
        )

        # Handle multiple projects
        project_names = request.POST.getlist('project[]')
        project_descriptions = request.POST.getlist('project_description[]')
        project_links = request.POST.getlist('project_link[]')

        for name, description, link in zip(project_names, project_descriptions, project_links):
            if name:  # Only create a project if the name is not empty
                project = Project.objects.create(
                    name=name,
                    description=description,
                    link=link
                )
                profile.projects.add(project)

        # Handle multiple languages
        language_names = request.POST.getlist('language[]')
        for name in language_names:
            if name:  # Only create a language if the name is not empty
                language, created = Language.objects.get_or_create(name=name)
                profile.languages.add(language)

        profile.save()
        return redirect('cv_view', profile_id=profile.id)  # Redirect to a view page of submitted data

    return render(request, 'index.html')

def cv_download(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    template = loader.get_template('pdf.html')
    html = template.render({'profile': profile})
    
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")  
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'margin-top': '10mm',
        'margin-right': '10mm',
        'margin-bottom': '10mm',
        'margin-left': '10mm',
        'disable-smart-shrinking': '',  # Prevents automatic scaling
    }
    
    pdf = pdfkit.from_string(html, False, options=options, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    
    return response
def cv_view(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    return render(request, 'cv.html',{'profile': profile})


def list_view(request):
    profile= Profile.objects.all()
    return render(request, 'list.html', {'profile': profile})


def cv_update(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == 'POST':
        # Update profile fields
        profile.address = request.POST.get('address')
        profile.full_name = request.POST.get('full_name')
        profile.email = request.POST.get('email')
        profile.phone = request.POST.get('phone')
        profile.summary = request.POST.get('summary')
        profile.school = request.POST.get('school')
        profile.school_gpa = request.POST.get('school_gpa')
        profile.school_joined_year = request.POST.get('school_joined_year')
        profile.school_left_year = request.POST.get('school_left_year')
        profile.college = request.POST.get('college')
        profile.college_gpa = request.POST.get('college_gpa')
        profile.stream = request.POST.get('stream')
        profile.college_joined_year = request.POST.get('college_joined_year')
        profile.college_left_year = request.POST.get('college_left_year')
        profile.university = request.POST.get('university')
        profile.university_gpa = request.POST.get('university_gpa')
        profile.university_faculty = request.POST.get('university_faculty')
        profile.university_joined_year = request.POST.get('university_joined_year')
        profile.university_left_year = request.POST.get('university_left_year')
        profile.technical_skills = request.POST.get('technical_skills')
        profile.nontechnical_skills = request.POST.get('nontechnical_skills')
        profile.reference_name = request.POST.get('reference_name')
        profile.reference_position = request.POST.get('reference_position')
        profile.reference_organization = request.POST.get('reference_organization')
        profile.reference_email = request.POST.get('reference_email')
        profile.reference_phone = request.POST.get('reference_phone')

        # Handle multiple projects
        profile.projects.clear()  # Remove existing projects
        project_names = request.POST.getlist('project[]')
        project_descriptions = request.POST.getlist('project_description[]')
        project_links = request.POST.getlist('project_link[]')

        for name, description, link in zip(project_names, project_descriptions, project_links):
            if name:  # Only create a project if the name is not empty
                project = Project.objects.create(
                    name=name,
                    description=description,
                    link=link
                )
                profile.projects.add(project)

        # Handle multiple languages
        profile.languages.clear()  # Remove existing languages
        language_names = request.POST.getlist('language[]')
        for name in language_names:
            if name:  # Only create a language if the name is not empty
                language, created = Language.objects.get_or_create(name=name)
                profile.languages.add(language)

        profile.save()
        return redirect('cv_view', profile_id=profile.id)

    return render(request, 'updatecv.html', {'profile': profile})

def cv_delete(request, profile_id):
    profile= get_object_or_404(Profile,id=profile_id)
    if request.method=="POST":
        profile.delete()
        return redirect('list_view')  
    return render(request,'delete.html',{'profile':profile})
