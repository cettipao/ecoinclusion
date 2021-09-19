# Generated by Django 2.2 on 2021-09-18 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecoinclusion', '0031_auto_20210918_1759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposito',
            name='tipo_de_reciclado',
        ),
        migrations.CreateModel(
            name='CantidadReciclado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(blank=True, default=1, null=True)),
                ('peso', models.DecimalField(blank=True, decimal_places=1, max_digits=9, null=True)),
                ('tipo_de_reciclado', models.ManyToManyField(related_name='cantidad', to='ecoinclusion.TipoDeReciclado')),
            ],
        ),
        migrations.AddField(
            model_name='deposito',
            name='cantidades',
            field=models.ManyToManyField(to='ecoinclusion.CantidadReciclado'),
        ),
    ]
