# Generated by Django 3.2.1 on 2021-05-06 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_picture_original_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='picture_blurred',
            field=models.ImageField(blank=True, null=True, upload_to='blurred_pictures'),
        ),
    ]