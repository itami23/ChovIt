# Generated by Django 4.1.4 on 2022-12-26 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0002_alter_community_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='community',
            options={'ordering': ['name']},
        ),
    ]
