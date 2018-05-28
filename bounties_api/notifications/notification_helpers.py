from notifications.models import Notification, DashboardNotification


def create_dashboard_notification(notification_name, user, notification_created, string_data, is_activity=True, email=False):
    notification = Notification.objects.create(
        notification_name=notification_name,
        user=user,
        notification_created=notification_created,
        email=email,
        dashboard=True
    )
    DashboardNotification.objects.create(
        notification=notification,
        string_data=string_data,
        is_activity=is_activity,
    )
