# Generated by Django 5.1.1 on 2025-02-06 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mesero', '0008_alter_planmodel_plan_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planmodel',
            name='plan_type',
            field=models.CharField(choices=[('free', 'free'), ('pay', 'pay')], max_length=10),
        ),
    ]
