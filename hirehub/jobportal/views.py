# views.py
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponse, JsonResponse
from fuzzywuzzy import fuzz
import json
import google.generativeai as genai
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Profile,Project,Language
import pdfkit
from django.template import loader 

class JobRecommender:
    def __init__(self, job_data):
        self.job_data = job_data
        self.job_data['Required_Skills'] = self.job_data['Required_Skills'].fillna('')  # Replace NaN with empty string
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.job_data['Title'])

    def recommend_jobs(self, user_skills, required_skills, top_n=5):
        if not user_skills.strip() or not required_skills.strip():
            return pd.DataFrame()  # Return empty DataFrame if inputs are invalid

        # Combine both user skills and required skills to form a query
        query = f"{user_skills} {required_skills}"

        # Vectorize the input query
        query_vec = self.vectorizer.transform([query])

        # Compute the cosine similarity between the query and the job titles
        cosine_sim = cosine_similarity(query_vec, self.tfidf_matrix)

        # Get the top N most similar job indices
        top_indices = cosine_sim[0].argsort()[-top_n:][::-1]

        # Fetch the recommended jobs
        recommended_jobs = self.job_data.iloc[top_indices]
        return recommended_jobs[['Title',  'URL']]

    @staticmethod
    def load_data(file_path):
        try:
            job_data = pd.read_csv(file_path)
            return job_data
        except FileNotFoundError:
            print(f"Error: The file at {file_path} was not found.")
            exit(1)
        except pd.errors.EmptyDataError:
            print("Error: The provided CSV file is empty.")
            exit(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            exit(1)

# Load the data
file_path = 'C:\\Users\\huawei\\Desktop\\jobpro\\hirehub\\jobportal\\job_dataset.csv'  # Replace with your actual file path
job_data = JobRecommender.load_data(file_path)

# Create an instance of the recommender
recommender = JobRecommender(job_data)

def work(request):
    return render(request, 'jobportal/work.html')

def recommend_jobs(request):
    if request.method == 'POST':
        user_skills = request.POST.get('user_skills', '')
        required_skills = request.POST.get('required_skills', '')
        
        # Call the recommendation function
        recommended_jobs = recommender.recommend_jobs(user_skills, required_skills)

        return render(request, 'recommend_jobs.html', {'recommended_jobs': recommended_jobs.to_dict(orient='records')})
    
    return render(request, 'recommend_jobs.html')

# Load your dataset (make sure the path is correct in your local environment)
dataset = pd.read_csv('C:\\Users\\huawei\\Desktop\\jobpro\\hirehub\\jobportal\\job_dataset.csv')

# Configure the generative AI model
genai.configure(api_key="AIzaSyBdVNTdrfjHvb-IKMBACdlkJzvd_r4SETE")
instruction = "You are a chatbot which provides job openings, resume building, skill requirements. It also provides course recommendations using the below dataset."
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruction
)

# Function to get course recommendations based on user input
def get_course_recommendations(keywords):
    """
    Function to get course recommendations based on keywords.
    """
    keywords = keywords.lower().split()
    relevant_courses = []

    for _, row in dataset.iterrows():
        course_name = row['Title'].lower()
        course_url = row['URL'].lower()

        # Calculate the score based on the keywords in Title and URL
        title_score = max(fuzz.partial_ratio(keyword, course_name) for keyword in keywords)
        url_score = max(fuzz.partial_ratio(keyword, course_url) for keyword in keywords)

        # Combine scores to get a final score
        total_score = title_score + url_score

        # Check if the total score exceeds the threshold
        if total_score > 120:  # Adjust this threshold as needed
            relevant_courses.append((row['Title'], row['URL'], total_score))

    # Sort the relevant courses by score in descending order
    relevant_courses.sort(key=lambda x: x[2], reverse=True)
    top_courses = relevant_courses[:5]  # Get the top 5 courses

    # Prepare the result for output
    if top_courses:
        result = "Recommended courses based on your query:\n"
        for course, url, score in top_courses:
            result += f"- {course}\n  URL: {url}\n  Relevance Score: {score}\n"
        return result
    return "I couldn't find any relevant courses. Please try with different keywords."

# Function to get job openings based on a query
def get_job_openings(query):
    """
    Function to get job openings based on a query.
    """
    openings = dataset[dataset['job_title'].str.contains(query, case=False)]
    if not openings.empty:
        return openings.to_string(index=False)
    return "I couldn't find any job openings matching your query."

# Function to handle general chatbot responses
def chatbot_response(message):
    """
    Function to handle chatbot responses.
    Prioritizes dataset-based responses before falling back to generative AI.
    """
    # Check if the message is related to courses
    if any(keyword in message.lower() for keyword in ["course"]):
        print("The corse recommended are")
        return get_course_recommendations(message)
    
    # Check if the message is related to job openings
    elif any(keyword in message.lower() for keyword in ["job openings"]):
        print("The job openings are")
        return get_job_openings(message)
    else:
        # If message doesn't match, call the generative AI model for general conversation
        response = model.start_chat().send_message(message)
        return response.text

# Hirebot view to handle chat interactions
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Exempt CSRF check for the sake of development (use proper CSRF token in production)
def hirebot(request):
    """
    View function to handle chat interactions.
    """
    if request.method == 'POST':
        # Extract the message from the request body
        data = json.loads(request.body)
        user_message = data.get('message', '')

        # If the user types "bye", end the chat
        if user_message.lower() == 'bye':
            return JsonResponse({'response': 'goodbye!'})

        # Get the chatbot response for the message
        response = chatbot_response(user_message)

        # Return the response to the frontend
        return JsonResponse({'response': response})

    return render(request, 'hirebot.html')


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