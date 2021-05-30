# Generated by Django 3.1.7 on 2021-05-30 06:54

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20210530_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='picture',
            field=models.ImageField(default='products/no_pic.jpg', upload_to='products', validators=[account.models.validate_image]),
        ),
    ]
