# Generated by Django 2.2 on 2021-09-19 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecoinclusion', '0036_auto_20210919_0040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cantidadreciclado',
            name='user',
        ),
        migrations.RemoveField(
            model_name='deposito',
            name='cantidades',
        ),
        migrations.AddField(
            model_name='cantidadreciclado',
            name='deposito',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cantidades', to='ecoinclusion.Deposito'),
            preserve_default=False,
        ),
    ]
