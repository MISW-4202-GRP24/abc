import unittest
import requests

class TestApp(unittest.TestCase):
    def test_post_request_to_other_service(self):
        other_service_url = 'URL'
        
        data = {
            'nombre': 'Ejemplo',
            'apellido': 'Apellido',
            'edad': 30,
            'telefono': '1234567890',
            'correo': 'ejemplo@example.com',
            'país': 1,
            'idiomas': 'es, en'
        }

        # Realizar la solicitud POST
        response = requests.post(other_service_url, json=data)

        # Verificar que la solicitud se haya realizado correctamente (código de estado 200)
        self.assertEqual(response.status_code, 200)

