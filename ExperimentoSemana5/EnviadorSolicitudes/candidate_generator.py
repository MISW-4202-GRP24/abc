from faker import Faker
import random
import json

fake = Faker()

candidates = []

# Genera 1000 registros
for _ in range(1000):
    candidate = {
        'name': fake.first_name(),
        'last_name': fake.last_name(),
        'age': random.randint(18, 99),
        'phone_number': fake.phone_number(),
        'email': fake.email(),
        'country': random.randint(1, 100),
        'languages': [fake.language_code() for _ in range(random.randint(1, 3))]
    }
    candidates.append(candidate)

# Guarda los registros en un archivo JSON estático
with open('candidates.json', 'w') as file:
    json.dump(candidates, file, indent=4)
