# Generated by Django 3.0.3 on 2020-05-21 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projektit', '0005_projekti_app_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projekti',
            options={'ordering': ('shortdescription',)},
        ),
        migrations.AddField(
            model_name='projekti',
            name='projtype',
            field=models.CharField(blank=True, max_length=1),
        ),
    ]
