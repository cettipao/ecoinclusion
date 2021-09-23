# Generated by Django 2.2 on 2021-09-19 00:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ecoinclusion', '0033_auto_20210919_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='cantidadreciclado',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cantidades', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cantidadreciclado',
            name='tipo_de_reciclado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cantidades', to='ecoinclusion.TipoDeReciclado'),
        ),
    ]