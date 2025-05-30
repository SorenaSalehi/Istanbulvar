# Generated by Django 5.1.4 on 2025-05-27 15:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('shop', '0003_alter_attribute_options_alter_attributevalue_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('discount_percent', models.PositiveSmallIntegerField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('groups', models.ManyToManyField(blank=True, related_name='group_offers', to='auth.group')),
                ('products', models.ManyToManyField(related_name='offers', to='shop.product')),
                ('users', models.ManyToManyField(blank=True, related_name='personal_offers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['start_date', 'end_date'], name='shop_specia_start_d_698f47_idx')],
            },
        ),
    ]
