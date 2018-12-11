from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Question, MyUser, Answer, Like, Tag

def pagination(question_list, request):
    paginator = Paginator(question_list, 10)
    page = request.GET.get('page')
    return paginator.get_page(page)

def get_users_tags(users_count, tags_count):
    users = MyUser.objects.get_n_top_users(users_count)
    tags = Tag.objects.get_n_top_tags(tags_count)
    return users, tags


