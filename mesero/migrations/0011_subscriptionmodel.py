# Generated by Django 5.1.1 on 2025-02-07 06:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mesero', '0010_alter_planmodel_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('price_at_subscription', models.DecimalField(decimal_places=2, max_digits=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='mesero.ownermodel')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mesero.planmodel')),
            ],
            options={
                'db_table': 'subscriptions',
            },
        ),
    ]
