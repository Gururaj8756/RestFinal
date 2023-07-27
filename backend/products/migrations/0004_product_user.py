# Generated by Django 4.2.3 on 2023-07-27 06:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(default=1, null=1, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
            preserve_default=1,
        ),
    ]
