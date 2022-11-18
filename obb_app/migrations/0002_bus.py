# Generated by Django 3.2.14 on 2022-11-16 05:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('obb_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('driver_name', models.CharField(max_length=255)),
                ('conductor_name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('ordinary', 'ordinary'), ('aircon', 'aircon')], default='aircon', max_length=255)),
                ('plate_no', models.CharField(max_length=255, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]