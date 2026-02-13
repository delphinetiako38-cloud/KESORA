import stripe
stripe.api_key="sk_test_xxxxxxxxxxxxxxxxxxxx"

def create_payment(amount,currency="USD",
                   description="paiement produit",email=None):
    payement_intent=stripe.PaymentIntent.create(amount=int(amount*100),
                                                currency=currency.lower(),
                                                description=description,
                                                receipt_email=email
    )
    return {"client_secret":payement_intent.client_secret,"id":payement_intent.id}
def capture_payement(payement_intent_id):
    stripe.PaymentIntent.capture(payement_intent_id)
    return True