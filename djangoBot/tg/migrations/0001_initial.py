# Generated by Django 3.2.10 on 2021-12-25 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('text', models.TextField()),
                ('rasm', models.ImageField(blank=True, upload_to='image/')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('is_chanal', models.BooleanField(default=False)),
                ('ctg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tg.categorymodel')),
            ],
        ),
        migrations.CreateModel(
            name='KorzinkaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('haridor', models.CharField(max_length=250)),
                ('is_deliver', models.BooleanField(default=True)),
                ('soni', models.ImageField(default=1, upload_to='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tg.productmodel')),
            ],
        ),
    ]
