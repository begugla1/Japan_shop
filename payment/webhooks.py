from django.shortcuts import get_object_or_404
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from order.models import Order


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, 
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET)
    except ValueError or stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            order = get_object_or_404(Order, id=session.client_reference_id)
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
    
    return HttpResponse(status=200)