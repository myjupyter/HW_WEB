from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db import models

###################################### User #############################################################

class myuser_manager(models.Manager):
    def get_n_top_users(self,user_count):
        return self.order_by('-rating')[:user_count]
    
    def check_user(self, user_name, e_mail):
        return self.filter(username = user_name, email=e_mail).first()
    
    def create_a_user(self, username=None, first_name='', last_name='',email=None, password=None):
        if not (username and email and password):
            raise TypeError('User has no username or email or password!!!')
        if self.check_user(username, email):
            raise RuntimeError('User has alredy been created!')
        user = MyUser(username = username,
                      first_name = first_name,
                      last_name = last_name,
                      email = email,
                      password = password)
        user.save()
        return user

class MyUser(User):
    rating = models.IntegerField(default=0, verbose_name='rating')
    objects = myuser_manager()
    avatar = models.ImageField(upload_to='', blank = True, verbose_name='avatar')

    def __str__(self):
        return self.get_username()
    
###################################### Like #############################################################

class Like(models.Model):
    author = models.ForeignKey('MyUser',on_delete=models.CASCADE, verbose_name='Like author')
    value = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

class QuestionLike(Like):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='question of like')

class AnswerLike(Like):
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, verbose_name='answer of like')
    

###################################### Question #########################################################

class question_manager(models.Manager):
    def create_a_question(self, user=None, title=None, text='', tags=None):
        if(not(user and title)):
            raise TypeError('Question must have ref to user and title!!!')
        question = Question()
        question.author = user
        question.title = title
        question.text = text
        question.publish()
        question.save()
        for tag in tags:
            tag_obj = Tag.objects.create_tag(tag)
            tag_obj.post_count += 1
            tag_obj.save()
            question.tags.add(tag_obj)
        return question

    def get_q_ordered_by(self, order_by=None):
        if order_by is None:
            raise TypeError('Bad \'order_by\' argument!!!')
        else:
            order_by = order_by or ('-published_time', '-rating', '-count_of_answer')
            return self.order_by(order_by)

class Question(models.Model):
    author = models.ForeignKey('MyUser', on_delete=models.CASCADE, verbose_name = 'author of question')
    title = models.CharField(max_length=200, verbose_name = 'title of question')
    text = models.TextField(verbose_name = 'text of question')
    tags = models.ManyToManyField('Tag', verbose_name = 'tags of question')
    count_of_answers = models.IntegerField(default=0, verbose_name = 'count of answers')
    objects = question_manager()
    
    rating = models.IntegerField(default=0,verbose_name='rating of question')
    
    dislikes = models.IntegerField(default=0,verbose_name='dislike')
    likes = models.IntegerField(default=0,verbose_name='like')

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='published date of question')
    
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title

    def update_rating(self):
        self.rating = self.likes - self.dislikes
        self.save()

    def set_like(self, user, value):
        like = QuestionLike.objects.filter(question=self, author=user).first()
        if like is None:
            if value: 
                self.likes += 1 
            else:
                self.dislikes += 1
            like = QuestionLike(question=self, author=user, value=value, is_active=True)
        else:
            if(like.is_active):
                if(like.value == value):
                    if value:
                        self.likes -= 1
                    else:
                        self.dislikes -= 1
                    like.is_active = False
                else:
                    if value:
                        self.likes += 1
                        self.dislikes -= 1
                        like.value = True
                    else:
                        self.likes -= 1
                        self.dislikes += 1
                        like.value = False
            else:
                if value:
                    like.value = True
                    self.likes += 1
                else:
                    like.value = False
                    self.dislikes += 1
                like.is_active = True
        self.update_rating()
        like.save()

###################################### Answer ###########################################################

class answer_manager(models.Manager):
    def create_answer(self, user=None, question=None, text=None):
        if(not(user or question or text)):
            raise TypeError("Answer mush have user, question and answer!!!")
        answer = Answer(author=user,
                        question = question,
                        answer_text = text)
        answer.publish()
        question.count_of_answers += 1
        question.save()
        answer.save()
        return answer


class Answer(models.Model):
    author = models.ForeignKey('MyUser', on_delete=models.CASCADE, verbose_name='author of answer')
    question = models.ForeignKey('Question', default=0, on_delete=models.CASCADE, verbose_name='question of answer')
    answer_text = models.TextField()
    published_date = models.DateTimeField(blank=True, null=True)

    objects = answer_manager()
    rating = models.IntegerField(default=0, verbose_name='rating of answer')
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def set_like(self, user, value):
        like = AnswerLike.objects.filter(answer=self, author=user).first()
        if like is None:
            AnswerLike(author=user, question=self.question, value=value, is_active=True).save()
            if value:
                self.rating += 1
                like.author.raiting += 1
            else:
                self.rating -= 1
                like.author.rating -= 1
        else:
            if(like.value == value):
                if value:
                    self.rating -= 1
                    like.author.raiting -= 1
                else:
                    self.rating += 1
                    like.author.rating += 1
            else:
                if value:
                    self.rating += 2
                    like.author.raiting += 2
                else:
                    self.rating -= 2
                    like.author.rating -= 2
        self.save()
        like.author.save()

###################################### Tag ##############################################################
                    
class tag_manager(models.Manager):
    def create_tag(self, tag_name=None):
        if tag_name is None:
            raise ValueError('Tag must has name!!!')
        tag = self.filter(tag_name=tag_name).first()
        if tag is None:
            tag = Tag(tag_name = tag_name)
            tag.save()
        return tag

    def get_n_top_tags(self,tag_count):
        return self.order_by('-post_count')[:tag_count]

class Tag(models.Model):
    tag_name = models.CharField(max_length=20, unique = True, verbose_name = 'name of tag')
    post_count = models.IntegerField(default=0, verbose_name = 'count of posts')
    objects = tag_manager()

    def __str__(self):
        return '#' + self.tag_name


