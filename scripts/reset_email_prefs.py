from user.models import User
from user.serializers import SettingsSerializer
from notifications.constants import default_email_options

users = User.objects.all()

for user in users:
    serializer = SettingsSerializer(data={'emails': default_email_options})
    serializer.is_valid(raise_exception=True)
    settings = serializer.save()
    user.settings = settings
    user.save()
