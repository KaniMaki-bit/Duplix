# URL base
http://localhost:5000

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

## GET /heatmap (por implementar)
Regresa los datos para la representación de un heatmap de similitud entre archivos.

El formato es un diccionario en donde la llave es la matricula del archivo en x, y su valor es un diccionario que contiene todas las demás matriculas (incluyendose a sí misma) como llaves y su porcentaje de similitud (0 - 100) como valor

## Ejemplo de la respuesta
```json
{
    "A01111111": {
        "A01111111": 100,
        "A02222222": 49,
        "A03333333": 69
    },
    "A02222222": {
        "A01111111": 49,
        "A02222222": 100,
        "A03333333": 10
    },
    "A03333333": {
        "A01111111": 69,
        "A02222222": 10,
        "A03333333": 100
    }
}
```

## GET /codigo (por implementar)
Regresa el código de ambas matriculas y señala que bloques son de plagio poniendo cada bloque plagiado entre tres `{}` seguido de un numero que representa el id del bloque, el cual es el mismo en ambos codigos (maybe mostrar cada bloque de plagio con el mismo id con un color). Por ejemplo {{{codigo}}}1
### Ejemplo de llamada
```http
GET {URL base}/codigo?matricula1=A01234567&matricula2=A00000000
```

### Ejemplo de respuesta
(realmente todo el código es un mismo bloque de plagio pero para poner el ejemplo mas claro supongamos que son 2 :) )
```json
{
    "codigo1": "{{{for i}}}1 in {{{range(10):\n\tprint(i)}}}2",
    "codigo2": "{{{for n}}}1 in {{{range(10):\n\tprint(n)}}}2"
}
```