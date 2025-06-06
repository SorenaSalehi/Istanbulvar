# Generated by Django 5.1.4 on 2025-05-17 09:16

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Attribute Name')),
                ('attribute_type', models.CharField(choices=[('attributes', 'Özellikler'), ('variants', 'Bağlantılı Ürünler')], default='attributes', max_length=10, verbose_name='Attribute Type')),
            ],
            options={
                'verbose_name': 'Attribute',
                'verbose_name_plural': 'Attributes',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Brand Name')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True, verbose_name='Description')),
                ('img', models.ImageField(blank=True, default='brands/defaults/default_banner.webp', upload_to='brands/banner', verbose_name='img')),
                ('logo', models.ImageField(blank=True, default='brands/defaults/default_logo.webp', upload_to='brands/logo', verbose_name='logo')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Quantity')),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Category Name')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('is_active', models.BooleanField(default=False, verbose_name='Active')),
                ('rating', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='rating (0–5 stars)')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='CommentMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='comment_media/', verbose_name='image')),
            ],
            options={
                'verbose_name': 'Comment Media',
                'verbose_name_plural': 'Comment Media',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('status', models.CharField(choices=[('pending', 'Sipariş Alındı'), ('paid', 'Ödeme Yapıldı'), ('payment_failed', 'Ödeme Hatalı'), ('preparing', 'Hzırlanıyor'), ('shipped', 'Kargoya Verildi'), ('delivered', 'Teslim Edildi'), ('canceled', 'İptal Edildi')], default='pending', max_length=15, verbose_name='Order Status')),
                ('tracking_number', models.CharField(blank=True, max_length=100, verbose_name='Tracking Number')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('estimated_delivery', models.DateField(blank=True, null=True, verbose_name='Estimated Delivery')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total Amount')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Unit Price')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Product Name')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Discount Price')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Price')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock')),
                ('sku', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='SKU')),
                ('rating', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='rating (0–5 stars)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Product Detail',
                'verbose_name_plural': 'Product Detail',
            },
        ),
        migrations.CreateModel(
            name='ProductDetailMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], default='image', max_length=5, verbose_name='Media Type')),
                ('media_position', models.CharField(choices=[('center', 'Center'), ('left', 'Left'), ('right', 'Right')], default='center', max_length=10, verbose_name='Media Position')),
                ('file', models.FileField(blank=True, null=True, upload_to='product_detail_media/', verbose_name='Media File')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
            ],
            options={
                'verbose_name': 'Product Detail Media',
                'verbose_name_plural': 'Product Detail Media',
            },
        ),
        migrations.CreateModel(
            name='ProductMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], default='image', max_length=5, verbose_name='Media Type')),
                ('file', models.FileField(upload_to='product_media/', verbose_name='Media File')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='product_media/', verbose_name='Thumbnail')),
                ('normal_size', models.ImageField(blank=True, null=True, upload_to='product_media/', verbose_name='Normal Size')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
            ],
            options={
                'verbose_name': 'Product Media',
                'verbose_name_plural': 'Product Media',
            },
        ),
        migrations.CreateModel(
            name='RelatedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_type', models.CharField(choices=[('similarity', 'Similarity'), ('buy-together', 'Buy Together')], default='image', max_length=20, verbose_name='Media Type')),
            ],
            options={
                'verbose_name': 'Related Product',
                'verbose_name_plural': 'Related Products',
            },
        ),
        migrations.CreateModel(
            name='ShippingCarrier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Carrier Name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('logo', models.ImageField(blank=True, help_text='Optional carrier logo for display in frontend', null=True, upload_to='shipping_carriers/', verbose_name='Logo')),
                ('tracking_url', models.CharField(blank=True, max_length=255, verbose_name='Tracking URL Template')),
            ],
            options={
                'verbose_name': 'Shipping Carrier',
                'verbose_name_plural': 'Shipping Carriers',
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
            ],
            options={
                'verbose_name': 'Wishlist',
                'verbose_name_plural': 'Wishlists',
            },
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, verbose_name='Attribute Key')),
                ('value', models.CharField(max_length=100, verbose_name='Attribute Value')),
                ('desc', models.CharField(blank=True, max_length=100, null=True, verbose_name='Attribute Description')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.attribute', verbose_name='Attribute')),
            ],
            options={
                'verbose_name': 'Attribute Value',
                'verbose_name_plural': 'Attribute Values',
            },
        ),
    ]
