# Generated by Django 4.2.3 on 2023-07-06 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_remove_blogcomment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcomment',
            name='post',
        ),
    ]