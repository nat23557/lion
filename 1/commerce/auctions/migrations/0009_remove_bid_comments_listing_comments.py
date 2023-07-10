# Generated by Django 4.2.2 on 2023-07-03 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_comment_listing_bid_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='comments',
        ),
        migrations.AddField(
            model_name='listing',
            name='comments',
            field=models.ManyToManyField(related_name='listings', to='auctions.comment'),
        ),
    ]
