# Generated by Django 4.2.2 on 2023-06-24 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EShop', '0007_delete_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='importance',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]
