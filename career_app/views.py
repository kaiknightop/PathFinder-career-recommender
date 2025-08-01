from django.shortcuts import render, redirect
from .models import CareerPath
from .forms import CareerSearchForm
import requests
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
import os
from .forms import LoginForm
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from dotenv import load_dotenv
from django.shortcuts import render, get_object_or_404


@csrf_exempt  # optional depending on frontend config (can use @require_http_methods instead)
def generate_roadmap(request):
    roadmap = ""
    if request.method == "POST":
        career_goal = request.POST.get("career_goal", "").strip()
        skills = request.POST.get("skills", "").strip()

        # Placeholder: Fake AI response — replace this later with OpenRouter/LLM logic
        roadmap = f"""
        🛤️ Career Roadmap for: {career_goal.title()}

        👩‍💻 Current Skills:
        {skills if skills else 'None provided'}

        📚 Suggested Learning Path:
        1. Complete an introductory course on {career_goal.lower()} (e.g., Coursera, edX, Udemy)
        2. Build 3 mini-projects related to {career_goal.lower()} using your current skills
        3. Learn and master these next tools:
           - Python
           - SQL
           - Git & GitHub
           - Data Visualization
        4. Take an intermediate certification (Google, Meta, IBM, etc.)
        5. Contribute to open-source or build a portfolio
        6. Start applying to internships or junior roles

        📅 Estimated Timeline:
        - Month 1–2: Fundamentals + Projects
        - Month 3–4: Intermediate topics + Portfolio
        - Month 5–6: Certifications + Job hunting
        """

    return render(request, "career_recommender/roadmap_generator.html", {
        "roadmap": roadmap
    })



def career_paths_list(request):
    roadmap = ""
    if request.method == "POST":
        career_goal = request.POST.get("career_goal", "").strip()
        skills = request.POST.get("skills", "").strip()

        # Placeholder: Fake AI response — replace this later with OpenRouter/LLM logic
        roadmap = f"""
        🛤️ Career Roadmap for: {career_goal.title()}

        👩‍💻 Current Skills:
        {skills if skills else 'None provided'}

        📚 Suggested Learning Path:
        1. Complete an introductory course on {career_goal.lower()} (e.g., Coursera, edX, Udemy)
        2. Build 3 mini-projects related to {career_goal.lower()} using your current skills
        3. Learn and master these next tools:
           - Python
           - SQL
           - Git & GitHub
           - Data Visualization
        4. Take an intermediate certification (Google, Meta, IBM, etc.)
        5. Contribute to open-source or build a portfolio
        6. Start applying to internships or junior roles

        📅 Estimated Timeline:
        - Month 1–2: Fundamentals + Projects
        - Month 3–4: Intermediate topics + Portfolio
        - Month 5–6: Certifications + Job hunting
        """

    return render(request, "career_recommender/career_paths_list.html", {
        "roadmap": roadmap
    })


def career_detail(request, career_id):
    career = CareerPath.objects.get(id=career_id)
    return render(request, 'career_recommender/career_detail.html', {'career': career})

def fetch_jobs(request):
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {"query":"Software Engineer","page":"1","num_pages":"1"}

    headers = {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    jobs = data.get('data', [])  # Safely get job list

    return render(request, 'career_recommender/job_results.html', {'jobs': jobs})

def job_search(request):
    query = request.GET.get('query', 'software developer')

    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {"query": query, "num_pages": 1}

    response = requests.get(url, headers=headers, params=params)
    jobs = response.json().get('data', [])

    # Pagination setup
    paginator = Paginator(jobs, 5)  # Show 5 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'career_recommender/job_results.html', {
        'page_obj': page_obj,
        'query': query
    })


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Optional: fallback dictionary for career summaries
career_summaries = {
    'Data Analyst': 'Analyze and interpret complex data to help companies make decisions.',
    'Web Developer': 'Design and build websites and web apps using modern technologies.',
    'UI/UX Designer': 'Design user-friendly and visually appealing digital interfaces.',
    # Add more as needed...
}
def about_view(request):
    return render(request, 'career_recommender/about.html')


def career_paths_view(request):
    careers = []
    if request.method == 'POST':
        form = CareerSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            url = "https://jsearch.p.rapidapi.com/search"
            headers = {
                "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
                "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
            }
            params = {"query": query}

            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            # You customize this part based on your API's structure
            for item in data.get('jobs', [])[:6]:  # Limit to 6 paths
                title = item.get('title')
                desc = career_summaries.get(title, "Explore exciting opportunities in this field.")
                careers.append({
                    'title': title,
                    'description': desc,
                    'icon_class': 'fas fa-briefcase',  # Placeholder
                    'id': 1  # You’ll probably change this to real IDs later
                })
    else:
        form = CareerSearchForm()

    return render(request, 'career_app/career_paths_list.html', {
        'form': form,
        'careers': careers
    })
    


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Log in the user automatically
            return redirect('home')  # Redirect to home page
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after login
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout