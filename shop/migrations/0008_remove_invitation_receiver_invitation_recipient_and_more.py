# Generated by Django 4.2.2 on 2023-06-14 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_notification'),
        ('shop', '0007_invitation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='receiver',
        ),
        migrations.AddField(
            model_name='invitation',
            name='recipient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='invitations_received', to='account.sellerprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invitation',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations_sent', to='account.sellerprofile'),
        ),
    ]
