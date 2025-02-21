# views.py
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from fuzzywuzzy import fuzz
import json
import google.generativeai as genai
import pandas as pd 
import joblib 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

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
    """
    if 'course ' in message.lower():
        return get_course_recommendations(message)
    elif 'job openings' in message.lower():
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
