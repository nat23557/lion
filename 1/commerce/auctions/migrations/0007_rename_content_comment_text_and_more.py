# Generated by Django 4.2.2 on 2023-07-03 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_listing_bids'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='commenter',
            new_name='user',
        ),
    ]