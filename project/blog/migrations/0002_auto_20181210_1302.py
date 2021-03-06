# Generated by Django 2.1.2 on 2018-12-10 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('rating', models.IntegerField(default=0, verbose_name='rating of answer')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=20, unique=True, verbose_name='name of tag')),
                ('post_count', models.IntegerField(default=0, verbose_name='count of posts')),
            ],
        ),
        migrations.AlterModelManagers(
            name='myuser',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='rating'),
        ),
        migrations.AddField(
            model_name='question',
            name='count_of_answers',
            field=models.IntegerField(default=0, verbose_name='count of answers'),
        ),
        migrations.AddField(
            model_name='question',
            name='dislikes',
            field=models.IntegerField(default=0, verbose_name='dislike'),
        ),
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='like'),
        ),
        migrations.AddField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='rating of question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.MyUser', verbose_name='author of question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='published date of question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.TextField(verbose_name='text of question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=200, verbose_name='title of question'),
        ),
        migrations.CreateModel(
            name='AnswerLike',
            fields=[
                ('like_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Like')),
            ],
            bases=('blog.like',),
        ),
        migrations.CreateModel(
            name='QuestionLike',
            fields=[
                ('like_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.Like')),
            ],
            bases=('blog.like',),
        ),
        migrations.AddField(
            model_name='like',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.MyUser', verbose_name='Like author'),
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.MyUser', verbose_name='author of answer'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='blog.Question', verbose_name='question of answer'),
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag', verbose_name='tags of question'),
        ),
        migrations.AddField(
            model_name='questionlike',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Question', verbose_name='question of like'),
        ),
        migrations.AddField(
            model_name='answerlike',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Answer', verbose_name='answer of like'),
        ),
    ]
