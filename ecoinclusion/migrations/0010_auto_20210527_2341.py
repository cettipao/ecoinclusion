# Generated by Django 2.2 on 2021-05-27 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecoinclusion', '0009_auto_20210527_2339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='centrodereciclaje',
            old_name='final_atencion',
            new_name='horarioFinal',
        ),
        migrations.RenameField(
            model_name='centrodereciclaje',
            old_name='inicio_atencion',
            new_name='horarioInicio',
        ),
    ]
