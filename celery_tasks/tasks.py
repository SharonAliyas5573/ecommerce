from celery import shared_task

@shared_task
def send_order_confirmation_email(order_id, user_email):
    """
    Simulate sending an order confirmation email by printing the details.
    """
    print(f"Order Confirmation: Your order with ID {order_id} has been confirmed for {user_email}.")