# Generated by Django 3.2.25 on 2024-04-30 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_tester_last_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='tester',
            name='name',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
