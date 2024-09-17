# **👩‍💻** MLops - SISTEMA DE RECOMENDACIÓN DE PELÍCULAS 👩‍💻

## 📌 Descripción

Este proyecto consiste en el desarrollo de un sistema de recomendación de películas utilizando **Técnicas de Machine Learning (K-Nearest Neighbors - Cosine Similarity)** , implementado en una **API** desarrollada con **FastAPI** . El proyecto abarca desde la transformación de los datos originales hasta el despliegue de la API en **Render** , donde los usuarios pueden consultar información sobre películas y obtener recomendaciones basadas en similitudes de contenido.

## ⚙️ Funcionalidades

* **Transformación de Datos** : Procesamiento y limpieza de un dataset de películas, incluyendo el desanidado de diversas columnas y el manejo de valores nulos.
* **API con FastAPI** : Desarrollada para ofrecer varios endpoints que permiten consultas sobre películas.
* **Sistema de Recomendación** : Utiliza K-Vecinos basado en la similitud de descripciones para recomendar películas.
* **Despliegue** : El proyecto está deployado en **Render** y se puede consumir a través de endpoints.

## 🧬Estructura del Proyecto

* **📁 Dataset/** : Contiene el archivo `dataset_final.parquet` con los datos procesados de las películas.
* **📁 ModelML/** : Incluye los archivos necesarios para el sistema de recomendación (matriz TF-IDF, modelo KNN, etc.).
* **📁 Notebooks/** : Jupyter Notebooks que documentan el proceso de:
  * Extracción, Transformación y Carga de los Datos (ETL) - [Notebook](https://github.com/agustin-caceres/Proyecto-MLOps/blob/main/Notebooks/ETL_movies.ipynb)
  * Análisis exploratorio de datos (EDA) - [Notebook](https://github.com/agustin-caceres/Proyecto-MLOps/blob/main/Notebooks/EDA_movies.ipynb)
  * Entrenamiento del modelo - [Notebook](https://github.com/agustin-caceres/Proyecto-MLOps/blob/main/Notebooks/Model_training.ipynb)
  * Testeo de endpoints - [Notebook](https://github.com/agustin-caceres/Proyecto-MLOps/blob/main/Notebooks/API_testing.ipynb)
* **📝 main.py** : Archivo principal que define la API con FastAPI.
* **📄 requirements.txt** : Lista de las dependencias necesarias para correr el proyecto.

## 🛠️ Tecnologías Utilizadas

* **🐍 Python** : Lenguaje principal del proyecto.
* **🚀 FastAPI** : Framework para el desarrollo de la API.
* **🔧 scikit-learn** : Para el procesamiento de datos y la implementación del modelo.
* **🐼 pandas** : Para la manipulación y transformación de los datos.
* **🌐 Render** : Plataforma de despliegue para la API.

## 💻 Instalación y Ejecución Local

### 🧰 Requisitos

* Python 3.10 o superior.
* Instalar las dependencias listadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

### ⚡Ejecución Local

1. Clonar el repositorio:

```bash
git clone https://github.com/agustin-caceres/Proyecto-MLOps.git
```

2. Navegar al directorio del proyecto:

```bash
cd Proyecto-MLOps
```

3. Ejecutar la API localmente usando  **uvicorn** :

```bash
uvicorn main:app --reload
```

4. La API estará disponible en:

```bash
http://127.0.0.1:8000
```

### 🌐 Endpoints

1️⃣ **GET** `/recomendacion/{titulo}`
Devuelve una lista de películas similares a la película proporcionada, utilizando K-Vecinos.

**Ejemplo de consulta:**

```bash
GET /recomendacion/Toy Story
```

2️⃣ **GET** `/cantidad_filmaciones_mes/{Mes``
Devuelve la cantidad de filmaciones realizadas en un mes específico (independientemente del año).

**Ejemplo de consulta:**

```bash
GET /cantidad_filmaciones_mes/Enero
```

3️⃣ **GET** `/cantidad_filmaciones_dia/{Dia}`
Devuelve la cantidad de filmaciones realizadas en un día específico de la semana.

**Ejemplo de consulta:**

```bash
GET /cantidad_filmaciones_dia/Lunes
```

4️⃣ **GET** `/score_titulo/{titulo_de_la_filmacion}`
Devuelve el título, fecha de estreno y puntaje de una película específica.

**Ejemplo de consulta:**

```bash
GET /score_titulo/Toy Story
```

5️⃣ **GET** `/votos_titulo/{titulo_de_la_filmacion}`
Devuelve el título, cantidad de votos y el promedio de votos de una película específica.

**Ejemplo de consulta**

```bash
GET /votos_titulo/Spider-Man
```

6️⃣ **GET** `/get_actor/{nombre_actor}`
Devuelve el éxito de un actor medido a través del retorno total y promedio, así como la cantidad de películas en las que ha participado.

**Ejemplo de consulta**

```bash
GET /get_actor/Tom Cruise
```

## 🚀 Despliegue en Render

El proyecto ha sido desplegado en **Render** , y puedes acceder a la API a través del siguiente enlace:

- [API deployed](https://proyecto-mlops-dp3e.onrender.com)

## 📞 Contacto

Si tienes alguna pregunta sobre este proyecto o deseas contactarte conmigo, puedes encontrarme en LinkedIn:

- [LinkedIn](https://www.linkedin.com/in/agustincaceres9/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base%3BZXoBeymUQzCjeF5HzAKDAA%3D%3D)

## 🎥 Video

Video de presentación del proyecto:

- [Video](https://youtu.be/FHPJ-z_-9II?si=w3CALnuhOBqB-n07)

## 📜 Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Para más información, consulta el archivo

- [LICENSE](https://github.com/agustin-caceres/Proyecto-MLOps/blob/main/LICENSE)
