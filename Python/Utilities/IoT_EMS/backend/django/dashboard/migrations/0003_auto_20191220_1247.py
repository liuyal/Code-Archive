# Generated by Django 3.0 on 2019-12-20 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20191218_1917'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Node',
            new_name='Nodes',
        ),
        migrations.DeleteModel(
            name='Current_status',
        ),
    ]