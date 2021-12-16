from zeep import Client

client = Client(
    wsdl='http://localhost:8000/?wsdl')

print(dir(client.service))
print(client.service.say_hello("Alvin", 123))