from plyer import notification

def send_notification(title: str, message: str):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # seconds
    ) 