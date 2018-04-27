from django_faker import Faker

from analytics.models import BountiesTimeline

populator = Faker.getPopulator()

populator.addEntity(BountiesTimeline, 150)

print(populator.execute())