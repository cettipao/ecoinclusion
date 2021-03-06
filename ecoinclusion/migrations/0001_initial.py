# Generated by Django 2.2 on 2021-11-04 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKeyGoogleMaps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='LugarDeReciclado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('lat', models.DecimalField(blank=True, decimal_places=21, max_digits=23, null=True)),
                ('long', models.DecimalField(blank=True, decimal_places=21, max_digits=24, null=True)),
                ('direccion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TipoDeReciclado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CentroDeReciclaje',
            fields=[
                ('lugardereciclado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ecoinclusion.LugarDeReciclado')),
                ('telefono', models.CharField(blank=True, max_length=50, null=True)),
                ('horario_apertura', models.TimeField(blank=True, null=True)),
                ('horario_cierre', models.TimeField(blank=True, null=True)),
                ('verificado', models.BooleanField(default=False)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cooperativa', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('ecoinclusion.lugardereciclado',),
        ),
        migrations.AddField(
            model_name='lugardereciclado',
            name='tipo_de_reciclado',
            field=models.ManyToManyField(to='ecoinclusion.TipoDeReciclado'),
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(blank=True, null=True)),
                ('peso', models.DecimalField(blank=True, decimal_places=1, max_digits=9, null=True)),
                ('fecha', models.DateField()),
                ('fecha_deposito', models.DateField(blank=True, null=True)),
                ('verificado', models.BooleanField(default=False)),
                ('lugar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depositos', to='ecoinclusion.LugarDeReciclado')),
                ('tipo_de_reciclado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depositos', to='ecoinclusion.TipoDeReciclado')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depositos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PuntoDeAcopio',
            fields=[
                ('lugardereciclado_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ecoinclusion.LugarDeReciclado')),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puntos', to='ecoinclusion.CentroDeReciclaje')),
            ],
            bases=('ecoinclusion.lugardereciclado',),
        ),
        migrations.CreateModel(
            name='Intermediario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('telefono', models.CharField(blank=True, max_length=100, null=True)),
                ('dias_disponibles', models.ManyToManyField(max_length=7, to='ecoinclusion.Dia')),
                ('lugares', models.ManyToManyField(to='ecoinclusion.LugarDeReciclado')),
                ('centro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intermediarios', to='ecoinclusion.CentroDeReciclaje')),
            ],
        ),
    ]
