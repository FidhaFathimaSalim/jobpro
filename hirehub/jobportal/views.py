# views.py
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#doing joblib
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

def hirebot(request):
    return render(request, 'hirebot.html')