from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db import models

class myuser_manager(models.Manager):
    def get_n_top_users(self,user_count):
        return self.objects.order_by('-rating')[:user_count]
    
    def create_a_user(self, username=None, first_name='', last_name='',email=None, password=None):
        if not (username and email and password):
            raise ValueError('User has no username or email or password!!!')
        user = MyUser()
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.password = password
        user.save()
        return user

class MyUser(User):
    #avatar = models.ImageField(upload_to='img/', verbose_name='avatar')
    rating = models.IntegerField(default=0, verbose_name='rating')
    objects = myuser_manager()

    def __str__(self):
        return self.get_username()
    




class Like(models.Model):
    author = models.ForeignKey('MyUser',on_delete=models.CASCADE, verbose_name='Like author')
    value = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

class QuestionLike(Like):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='question of like')

class AnswerLike(Like):
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name='answer of like')
    





class question_manager(models.Manager):
    def create_a_question(self, user=None, title=None, text='', *tags):
        if(not(user and title)):
            raise ValueError('Question must have ref to user and title!!!')
        question = Question()
        question.author = user
        question.title = title
        question.text = text
        for tag in tags:
            question.tags.add(Tag.tag_manager.create_tag(tag))
        question.publish()
        question.save()
        return question

    def get_q_ordered_by(self, order_by=None):
        if(order_by):
            raise ValueError('Bad \'order_by\' argument!!!')
        else:
            order_by = order_by or ('-published_time', '-rating', '-count_of_answer')
            return self.order_by(order_by)

class Question(models.Model):
    author = models.ForeignKey('MyUser', on_delete=models.CASCADE, verbose_name = 'author of question')
    title = models.CharField(max_length=200, verbose_name = 'title of question')
    text = models.TextField(verbose_name = 'text of question')
    tags = models.ManyToManyField('Tag', verbose_name = 'tags of question')
    count_of_anwers = models.IntegerField(default=0, verbose_name = 'count of answers')
    
    rating = models.IntegerField(default=0,verbose_name='rating of question')

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True, 'published date of question')
    
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title

    def set_like(self, user, value):
        like = QuestionLike.objects.filter(question=self, author=user).first()
        if like is None:
            value if self.rating += 1 else self.rating -= 1
            QuestionLike(question=self, author=user, value=value, is_active=True).save()
            self.save()
        else:
            if(like.value == value):
                value if self.rating -= 1 else self.rating += 1
                like.is_active = False
            else:
                value if self.rating += 2 else self.rating -= 2
                like.is_active = True
            self.save()
            like.save()


class answer_manager(models.Manager):
    pass

class Answer(models.Model):
    author = models.ForeignKey('MyUser', on_delete=models.CASCADE, verbose_name='author of answer')
    question = models.ForeignKey('Question', default=0, on_delete=models.CASCADE, verbose_name='question of answer')
    answer_text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)

    rating = models.IntegerField(default=0, verbose_name='rating of answer')
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def set_like(self, user, value):
        like = AnswerLike.objects.filter(answer=self, author=user).first()
        if like is None:
            value if like.author.raiting += else like.author.rating -= 1
            


class tag_manager(models.Manager):
    def create_tag(self, tag_name=None):
        if not tag_name:
            raise ValueError('Tag must has name!!!')
        tag = self.filter(tag_name=tag_name).first()
        if not tag:
            tag = Tag()
            tag.tag_name = tag_name
            tag.save()
        tag.post_count += 1
        return tag

    def get_n_top_tags(self,tag_count):
        return self.order_by('-post_count')[:tag_count]

class Tag(models.Model):
    tag_name = models.CharField(max_length=20, unique = True, verbose_name = 'name of tag')
    post_count = models.IntegerField(default=0, verbose_name = 'count of posts')
    objects = tag_manager()

    def __str__(self):
        return '#' + self.tag_name


