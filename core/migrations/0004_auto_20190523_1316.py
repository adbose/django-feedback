# Generated by Django 2.2.1 on 2019-05-23 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190523_1307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='response',
            old_name='question_id',
            new_name='question',
        ),
    ]