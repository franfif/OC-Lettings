# Generated by Django 3.0 on 2023-10-06 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oc_lettings_site', '0002_auto_20231005_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letting',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='Letting',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
