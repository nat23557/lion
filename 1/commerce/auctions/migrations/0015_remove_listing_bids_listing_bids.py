# Generated by Django 4.2.2 on 2023-07-04 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_listing_highest_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bids',
        ),
        migrations.AddField(
            model_name='listing',
            name='bids',
            field=models.ManyToManyField(blank=True, related_name='listing_bids', to='auctions.bid'),
        ),
    ]
