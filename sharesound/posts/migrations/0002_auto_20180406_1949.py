# Generated by Django 2.0.3 on 2018-04-06 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='track',
            options={'ordering': ['-created_at']},
        ),
    ]
