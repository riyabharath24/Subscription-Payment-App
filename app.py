import os
from flask import Flask, redirect, jsonify, json, request, current_app

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51NbllzSHPUgNmFMxpQe6OabFmirbCu3bECbj3jiPIPFXsYcJesqkc2K2UvJZ01qI5qFO38ltIQ8fqcInrjwHniyO00juHmVRsk'

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'


@app.route('/', methods=['GET'])
def get_index():
    return current_app.send_static_file('new_checkout.html')


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        prices = stripe.Price.list(
            lookup_keys=[request.form['lookup_key']],
            expand=['data.product']
        )

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1NbxoMSHPUgNmFMxE9ml6Omh',
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN +
            '/success.html?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )

        # return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(e)
    # return "Server error", 500
    return redirect(checkout_session.url, code=303)


if __name__ == '__main__':
    app.run(port=4242)
