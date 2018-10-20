

from swaggertools import resolve

with open('/swagger.yml') as filehandler:
    app = resolve(filehandler)

print(app.to_yaml())


