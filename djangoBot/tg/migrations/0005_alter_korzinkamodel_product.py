# Generated by Django 3.2.10 on 2021-12-26 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg', '0004_productmodel_zapas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='korzinkamodel',
            name='product',
            field=models.CharField(max_length=250),
        ),
    ]
