# Generated by Django 3.2.25 on 2024-04-12 10:43

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20240407_1932'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('day', models.CharField(max_length=16)),
            ],
            options={
                'verbose_name': 'Дата',
                'verbose_name_plural': 'Даты',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('value', models.PositiveSmallIntegerField()),
                ('audio', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='marks', to='core.audiofiles')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='marks', to='core.day')),
                ('tester', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='marks', to='core.tester')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
                'ordering': ['-created'],
            },
        ),
    ]
