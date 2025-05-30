# Generated by Django 5.1.4 on 2025-05-27 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(choices=[('home_header', 'Home Page Header'), ('new_products', 'Best of new product'), ('shop_list', 'Catalog page banners')], default='home_header', help_text='Where this banner should appear on the site', max_length=20)),
                ('image', models.ImageField(help_text='Banner image file', upload_to='banners/%Y/%m/%d/')),
                ('title', models.CharField(blank=True, help_text='Optional title for the banner', max_length=100)),
                ('description', models.TextField(blank=True, help_text='Optional desc for the banner', max_length=500)),
                ('button_text', models.CharField(blank=True, help_text='name for the button', max_length=25)),
                ('link', models.URLField(blank=True, help_text='Optional URL to navigate to when clicked', max_length=300)),
                ('alt_text', models.CharField(blank=True, help_text='Alternative text for accessibility', max_length=150)),
                ('is_active', models.BooleanField(default=True, help_text='Toggle banner visibility without deleting it')),
                ('display_order', models.PositiveIntegerField(default=0, help_text='Lower numbers display first')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
                'ordering': ['display_order', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='E-posta')),
                ('isActive', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')),
            ],
        ),
    ]
