# Generated by Django 4.1.3 on 2022-12-06 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('page', '0016_alter_page_follow_requests_alter_page_followers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=180)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_post', to=settings.AUTH_USER_MODEL)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='page.page')),
            ],
        ),
    ]
