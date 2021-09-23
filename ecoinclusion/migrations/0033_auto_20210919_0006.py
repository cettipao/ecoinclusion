# Generated by Django 2.2 on 2021-09-19 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecoinclusion', '0032_auto_20210918_2356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cantidadreciclado',
            name='tipo_de_reciclado',
        ),
        migrations.AddField(
            model_name='cantidadreciclado',
            name='tipo_de_reciclado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cantidad', to='ecoinclusion.TipoDeReciclado'),
            preserve_default=False,
        ),
    ]