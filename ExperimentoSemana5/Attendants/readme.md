## Componente Attendants

Tiene como propósito simular el comportamiento de un servicio de creación de candidatos, guardando el candidato y aleatoriamente generando errores en las transacciones

Este servicio guarda en la una base de datos postgres los datos del candidato

Acepta un llamado `POST` a `/attendats`

A continuación un ejemplo de la solicitud
```
{
    "first_name": "Louisa",
    "last_name": "Yost",
    "age": 583,
    "phone": "650-211-6769",
    "email": "Pietro75@gmail.com",
    "country": "Sao Tome and Principe",
    "languages": [
        {
            "name": "neural"
        }
    ]
}
```

y de la respuesta

```
{
    "id": 1,
    "first_name": "Louisa",
    "last_name": "Yost",
    "age": 583,
    "phone": "650-211-6769",
    "email": "Pietro75@gmail.com",
    "country": "Sao Tome and Principe",
    "languages": [
        {
            "name": "neural"
        }
    ],
    "created_at": "2023-09-08T03:33:24.720352"
}
```

En caso de error la respuesta será un error aleatorio con la hora de registro del error, como se muestra a continuación:

```
{
    "error": "Main have officer soon across should within.",
    "current_timestamp": "2023-09-08T03:40:24.036367"
}
```