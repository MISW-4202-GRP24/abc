from faker import Faker
import random
import json

fake = Faker()

candidates = []

# Genera 1000 registros
for _ in range(1000):
    candidate = {
        'nombre': fake.first_name(),
        'apellido': fake.last_name(),
        'edad': random.randint(18, 99),
        'telefono': fake.phone_number(),
        'correo': fake.email(),
        'pais': random.randint(1, 100),
        'idiomas': [fake.language_code() for _ in range(random.randint(1, 3))]
    }
    candidates.append(candidate)

# Guarda los registros en un archivo JSON estático
with open('candidates.json', 'w') as file:
    json.dump(candidates, file, indent=4)
