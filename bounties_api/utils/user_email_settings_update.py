from user.models import User

# WARNING - This will modify user settings in the database
# Use with caution and test on your local database first!

# Change these to fit what you need to update:

# recipient = 'issuer'
# notification = 'BountyCompleted'

for user in User.objects.all():
    user.settings.emails[recipient][notification] = True
    user.settings.save()