from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.log_in, name='LogIn'),
    path('signup', views.sign_up, name='SignUp'),
    path('ask', views.ask, name='ask'), 
    path('settings', views.settings, name='settings'), 
    path('<int:question_id>', views.to_question, name='to_question'),
    path('by_tag/<int:tag_id>', views.question_by_tag, name='to_questions_by_tag'),
    path('by_time/', views.order_questions_by_time, name='order_questions_by_time'),
    path('by_rating/', views.order_questions_by_rating, name='order_questions_by_rating'),
    path('profile/', views.profile, name='profile'),
]
