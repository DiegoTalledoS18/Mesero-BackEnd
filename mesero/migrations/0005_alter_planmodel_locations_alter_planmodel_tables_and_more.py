# Generated by Django 5.1.1 on 2025-02-05 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mesero', '0004_rename_quantity_planmodel_locations_planmodel_tables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planmodel',
            name='locations',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='planmodel',
            name='tables',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterModelTable(
            name='planmodel',
            table=None,
        ),
    ]
