# Generated by Django 3.1.6 on 2021-02-13 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(choices=[('urgent', 'Urgent'), ('important', 'Important'), ('medium', 'Medium'), ('low', 'Low')], default='medium', max_length=20, verbose_name='Priority'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='progress',
            field=models.CharField(choices=[('not_started', 'Not started'), ('in_progress', 'In progress'), ('completed', 'Completed')], default='not_started', max_length=20, verbose_name='Progress'),
        ),
    ]