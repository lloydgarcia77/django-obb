# Generated by Django 3.2.14 on 2022-11-21 23:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('obb_app', '0010_auto_20221121_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='datetime',
        ),
        migrations.AddField(
            model_name='booking',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='BookingSeats',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_booking_seats_booking', to='obb_app.booking')),
            ],
        ),
    ]
