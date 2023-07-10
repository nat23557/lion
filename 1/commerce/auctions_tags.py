from django import template

register = template.Library()

@register.filter
def last_bid_amount(bids):
    last_bid = bids.last()
    if last_bid:
        return last_bid.bid_amount
    return None
