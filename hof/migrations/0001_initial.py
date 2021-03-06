# Generated by Django 3.0.5 on 2020-04-16 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(default=2020)),
                ('day_of_the_week', models.CharField(max_length=10)),
                ('lecturer', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TaskCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_blood_cells', models.IntegerField(default=1)),
                ('description', models.CharField(max_length=200)),
                ('task_collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hof.TaskCollection')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('nickname', models.CharField(max_length=20, unique=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hof.Group')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquired_blood_cells', models.IntegerField(default=0)),
                ('date', models.DateTimeField(verbose_name='due date')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hof.Student')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hof.Task')),
            ],
        ),
    ]
