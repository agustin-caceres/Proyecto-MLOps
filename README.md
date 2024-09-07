PROYECTO INDIVIDUAL N°1: Machine Learning Operations (MLOps)

Este proyecto consiste en la realización de un pipeline completo de MLOps, que abarca diversas fases del ciclo de vida de un proyecto de ciencia de datos. 

Inicia con el procesamiento y transformación de un dataset de películas, desempeñando el rol de Data Engineer, para luego implementar una serie de endpoints mediante una API. Finalmente, se desarrolla un modelo de Machine Learning, específicamente un sistema de recomendación de películas, que será desplegado a través de la API para consultas y recomendaciones en tiempo real.

# Desanidado y limpieza de columnas anidadas en formato JSON

Se procedió con el desanidado de varias columnas de un dataset de películas que contenían listas de diccionarios en formato JSON. El objetivo fue convertir estas listas de diccionarios en nuevas columnas de fácil acceso, permitiendo un análisis más claro y estructurado.

Se realizó el desanidado de las siguientes columnas:
- `belongs_to_collection`
- `genres`
- `production_companies`
- `production_countries`
- `spoken_languages`

Cada columna fue procesada individualmente para desanidar la información de los diccionarios y convertirlos en nuevas columnas en el DataFrame.

