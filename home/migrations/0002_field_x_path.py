# Generated by Django 3.2.8 on 2022-09-29 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='x_path',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]