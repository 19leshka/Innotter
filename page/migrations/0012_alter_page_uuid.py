# Generated by Django 4.1.3 on 2022-12-04 14:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0011_alter_page_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=36, unique=True),
        ),
    ]
