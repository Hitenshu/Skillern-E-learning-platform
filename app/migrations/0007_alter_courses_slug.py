# Generated by Django 5.1.7 on 2025-04-01 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_courses_slug_alter_courses_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
