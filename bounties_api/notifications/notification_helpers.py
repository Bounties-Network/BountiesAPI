from notifications.models import Notification, NotificationDashboard


def createDashboardNotification(notification_id, user, notification_created, string_data, email=True):
    notification = Notification.objects.create(
        notification_id=notification_id,
        user=user,
        notification_created=notification_created,
        email=email,
        dashboard=True
    )
    NotificationDashboard.objects.create(
        notification=notification,
        string_data=string_data
    )
