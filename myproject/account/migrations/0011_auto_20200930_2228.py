# Generated by Django 3.0.8 on 2020-09-30 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20200930_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='line',
            field=models.CharField(choices=[(0, '취준생'), (1, '식품'), (2, '유통'), (3, '화학/건설/제조'), (4, '관광/서비스/금융')], max_length=1, verbose_name='계열'),
        ),
    ]
