# Generated by Django 4.0.5 on 2022-06-16 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='login_method',
            field=models.CharField(choices=[('kakao', 'Kakao'), ('google', 'Google'), ('email', 'Email')], default='email', max_length=10),
        ),
    ]
