# Generated by Django 4.2.2 on 2023-06-12 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_notification'),
        ('shop', '0002_product_seller'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerFollow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='account.buyerprofile')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='account.sellerprofile')),
            ],
            options={
                'unique_together': {('follower', 'seller')},
            },
        ),
    ]
