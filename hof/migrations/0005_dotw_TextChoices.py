# Generated by Django 3.0.5 on 2020-04-30 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hof', '0004_auto_20200430_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='day_of_the_week',
            field=models.CharField(choices=[('MON', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday')], max_length=3),
        ),
    ]
