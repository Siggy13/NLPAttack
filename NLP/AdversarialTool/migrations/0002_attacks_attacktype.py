# Generated by Django 3.1.2 on 2021-12-15 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdversarialTool', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attacks',
            name='attackType',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
