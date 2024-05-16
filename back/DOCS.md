# Endpoints

## POST /archivos
Carga los archivos a analizar que representan una entrega

Cada archivo está representado con la matricula como llave y el código de este como valor.

### Ejemplo del body en llamada
```json
{
    "A01234567": "print('hello world')",
    "A0XXXXXXX": "print('hola mundo')"
    ...
}
```

## GET /estudiantes
Regresa en forma de array las matriculas asociadas a los archivos cargados con `POST /archivos`

### Ejemplo de la respuesta
```json
[
    "A01234567",
    "A00000000"
]
```