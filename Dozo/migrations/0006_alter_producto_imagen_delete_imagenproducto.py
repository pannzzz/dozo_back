# Generated by Django 5.1.3 on 2024-11-15 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dozo', '0005_alter_producto_talla'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(default='entrevista_cambot_trabajo_remoto.png', null=True, upload_to='images/'),
        ),
        migrations.DeleteModel(
            name='ImagenProducto',
        ),
    ]