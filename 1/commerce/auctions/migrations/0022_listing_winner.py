# Generated by Django 4.2.2 on 2023-07-04 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_listing_bids_listing_comments_alter_bid_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
