from .models import Question, MyUser, Answer, Like, Tag 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from .handler import pagination, get_users_tags

def home(request):
    users, tags = get_users_tags(10, 10)
    questions = pagination(Question.objects.all(), request)
    return render(request, 'blog/home.html', {'questions': questions , 'users' : users, 'tags' : tags})

def log_in(request):
    return render(request, 'blog/login.html')

def sign_up(request):
    return render(request, 'blog/signup.html')

def ask(request):
    return render(request, 'blog/ask.html')

def settings(request):
    return render(request, 'blog/settings.html')

def to_question(request, question_id):
    users, tags = get_users_tags(10, 10)
    _question = Question.objects.get(pk=question_id)
    answers = Answer.objects.filter(question = _question)
    return render(request, 'blog/question.html', {'question': _question, 'answers' : answers, 'users' : users, 'tags' : tags})

def order_questions_by_rating(request):
    users, tags = get_users_tags(10, 10)
    questions = pagination(Question.objects.get_q_ordered_by('-rating'), request)
    return render(request, 'blog/home.html', {'questions': questions , 'users' : users, 'tags' : tags})

def order_questions_by_time(request):
    users, tags = get_users_tags(10, 10)
    questions = pagination(Question.objects.get_q_ordered_by('-published_date'), request)
    return render(request, 'blog/home.html', {'questions': questions , 'users' : users, 'tags' : tags})

def question_by_tag(request, tag_id):
    users, tags = get_users_tags(10, 10)
    questions = pagination(Question.objects.filter(tags = tag_id), request)
    return render(request, 'blog/home.html', {'questions': questions , 'users' : users, 'tags' : tags})

def profile(request):
    users, tags = get_users_tags(10, 10)
    questions = pagination(Question.objects.all(), request)
    return render(request, 'blog/profile.html', {'questions': questions , 'users' : users, 'tags' : tags})


