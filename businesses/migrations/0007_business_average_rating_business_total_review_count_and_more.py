# Generated by Django 4.0.5 on 2022-07-08 02:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('businesses', '0006_rename_created_by_review_user_review_business_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='average_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='business',
            name='total_review_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='business',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='businesses', to=settings.AUTH_USER_MODEL),
        ),
    ]
