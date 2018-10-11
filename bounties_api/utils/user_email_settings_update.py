from user.models import User

# WARNING - This will modify user settings in the database
# Use with caution and test on your local database first!

for user in User.objects.all():
    print('Updating settings for user {}'.format(user.id))
    user.settings.emails['issuer']['BountyCompleted'] = True
    # user.settings.save() # Comment out when ready
