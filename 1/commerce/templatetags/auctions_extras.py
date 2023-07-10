from django import template

register = template.Library()

@register.filter
def get_highest_bid(bids):
    highest_bid = bids.order_by('-bid_amount').first()
    if highest_bid:
        return highest_bid.bid_amount
    else:
        return None
