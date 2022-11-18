# Generated by Django 3.2.14 on 2022-11-17 13:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('obb_app', '0004_auto_20221116_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField()),
                ('is_paid', models.BooleanField(default=False)),
                ('total_cost', models.FloatField()),
                ('seat_person', models.JSONField()),
                ('status', models.CharField(choices=[('pending', 'pending'), ('approved', 'approved')], default='pending', max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_booking_bus', to='obb_app.bus')),
                ('scheduled_route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_booking_route', to='obb_app.dailyschedule')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('route', models.CharField(max_length=200)),
                ('total_cost', models.FloatField()),
                ('date', models.DateField()),
                ('seat_person', models.JSONField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fk_receipt_booking', to='obb_app.booking')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
    ]
