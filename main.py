from fastapi import FastAPI
from scipy import sparse
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD


app = FastAPI(
    title= "Sistema de Recomendación de Películas",
    description= " La API proporciona recomendaciones de películas basadas en la similitud de contenido. Utiliza TF-IDF y la similitud del coseno para calcular las películas más similares."
)


# Dataset y modelos
movies_df = pd.read_parquet('Dataset/dataset_final.parquet', engine='fastparquet')
model_df = pd.read_parquet('ModelML/model_ml.parquet')
tfidf_matrix = sparse.load_npz('ModelML/tfidf_matrix.npz')

# Se reduce la dimensionalidad de la matriz TF-IDF
svd = TruncatedSVD(n_components=500) 
reduced_tfidf_matrix = svd.fit_transform(tfidf_matrix)

# Vectorizador
with open('ModelML/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf_vectorizer = pickle.load(f)
 
# Se calcula la similitud del coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)




@app.get("/")
def read_root():
    return {"message": "¡Bienvenido al sistema de recomendación de películas!. Inserte /docs en la URL"}




@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str, num_recomendaciones: int = 5):
    """
    Devuelve una lista de películas similares a la película proporcionada basadas en la similitud del coseno.
    
    Parámetros:
    - titulo (str): El título de la película para la cual se quieren obtener recomendaciones.
    - num_recomendaciones (int, opcional): Número de películas a recomendar (por defecto 5).

    Retorna:
    - dict: Diccionario con la lista de títulos de películas recomendadas o un mensaje de error si el título no se encuentra.

    Descripción:
    La función utiliza una matriz TF-IDF reducida en dimensionalidad mediante TruncatedSVD para calcular la similitud
    del coseno de manera eficiente en términos de memoria. El objetivo es reducir el uso de memoria mientras se mantiene 
    una alta precisión en las recomendaciones.
    """
    # Verificación del título proporcionado en el dataset
    if titulo not in model_df['title'].values:
        return {"error": "El título no está en el dataset."}
    
    # Obtención del índice de la película solicitada
    idx = model_df[model_df['title'] == titulo].index[0]
    
    # Calculo de la similitud del coseno con reducción de dimensionalidad de la matriz TF-IDF
    sim_scores = cosine_similarity(reduced_tfidf_matrix[idx], reduced_tfidf_matrix).flatten()
    
    # Enumera y ordena las similitudes de mayor a menor
    sim_scores = list(enumerate(sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Selección de películas similares
    sim_scores = sim_scores[1:num_recomendaciones + 1]
    
    # Obtención del índice de las películas recomendadas
    movie_indices = [i[0] for i in sim_scores]
    
    # Obtención de títulos de las películas recomendadas
    recomendaciones = model_df['title'].iloc[movie_indices].tolist()
    
    return {"recomendaciones": recomendaciones}




@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str) -> dict:
    """
    Devuelve la cantidad de películas que fueron estrenadas en el mes consultado.
    
    Parámetros:
    mes (str): Nombre del mes en español.
    
    Retorno:
    dict: Mensaje con la cantidad de películas estrenadas en el mes.
    """
    # Diccionario de meses en español a números
    meses_diccionario = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    # Conversión de mes a su número correspondiente
    mes_numero = meses_diccionario.get(mes.lower())
    
    if mes_numero:
        # Filtramos las películas del mes del 'release_date'
        cantidad = movies_df[movies_df['release_date'].dt.month == mes_numero].shape[0]
        return {"mensaje": f"{cantidad} películas fueron estrenadas en el mes de {mes.capitalize()}"}
    else:
        return {"error": "Mes no válido. Por favor, ingrese en español un mes válido."}




@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str) -> dict:
    """
    Devuelve la cantidad de películas que fueron estrenadas en el día de la semana consultado.
    
    Parámetros:
    - dia (str): Nombre del día en español.
    
    Retorno:
    - dict: Mensaje con la cantidad de películas estrenadas en el día.
    """
    # Diccionario de días de la semana en español a su número correspondiente (lunes=0, domingo=6)
    dias_diccionario = {
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3, 
        'viernes': 4, 'sábado': 5, 'domingo': 6
    }
    
    # Conversión de día a su número correspondiente
    dia_numero = dias_diccionario.get(dia.lower())
    
    if dia_numero is not None:
        # Filtro de películas por el día de la semana del 'release_date'
        cantidad = movies_df[movies_df['release_date'].dt.dayofweek == dia_numero].shape[0]
        return {"mensaje": f"{cantidad} películas fueron estrenadas el {dia.capitalize()}"}
    else:
        return {"error": "Por favor, ingrese en español un día válido."}




@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str) -> dict:
    """
    Devuelve el título, año de estreno y score de una filmación.

    Parámetros:
    - titulo (str): Título de la filmación.

    Retorno:
    - dict: Mensaje con el título, año de estreno y el score de la película.
    """
    # Filtro de película por el título
    film = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    
    if not film.empty:
        # Extracción del año de estreno y el score
        titulo_film = film['title'].values[0]
        año_estreno = film['release_year'].values[0]
        popularity = film['popularity'].values[0]
        
        return {
            "mensaje": f"La película '{titulo_film}' fue estrenada en el año {año_estreno} con un score de {popularity}"
        }
    else:
        return {"error": f"No se encontró la película con el título '{titulo}'."}
    



@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str) -> dict:
    """
    Devuelve la cantidad de votos y el promedio de votaciones de una película.
    
    Parámetros:
    - titulo (str): Título de la película.

    Retorno:
    - dict: Mensaje con la cantidad de votos y el promedio, o un mensaje si no cumple el mínimo de votos.
    """
    # Filtro de película por el título
    film = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    
    if not film.empty:
        votos = film['vote_count'].values[0]
        promedio_votos = film['vote_average'].values[0]
        
        # Verificación de película con al menos 2000 votos
        if votos >= 2000:
            return {
                "mensaje": f"La película '{titulo}' tiene {votos} valoraciones, con un promedio de {promedio_votos}"
            }
        else:
            return {
                "mensaje": f"La película '{titulo}' no cumple con el mínimo de 2000 votos. Solo tiene {votos} votos."
            }
    else:
        return {"error": f"No se encontró la película con el título '{titulo}'."}
    



@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str) -> dict:
    """
    Devuelve el éxito de un actor medido a través del retorno total y promedio,
    así como la cantidad de películas en las que ha participado.

    Parámetros:
    - nombre_actor (str): Nombre del actor a consultar.

    Retorno:
    - dict: Diccionario con la cantidad de películas en las que ha participado,
            el retorno total y el retorno promedio por filmación.
            Si no se encuentra el actor, devuelve un mensaje de error.
    """
    # Filtro por el nombre del actor
    actor_data = movies_df[movies_df['actor_name'].str.contains(nombre_actor, case=False, na=False)]
    
    # Verificación de resultados
    if not actor_data.empty:
        cantidad_filmaciones = actor_data.shape[0]
        total_retorno = actor_data['return'].sum()
        promedio_retorno = total_retorno / cantidad_filmaciones
        
        # Retorno exitoso con los datos del actor
        return {
            "actor": nombre_actor,
            "cantidad_filmaciones": cantidad_filmaciones,
            "total_retorno": total_retorno,
            "promedio_retorno": promedio_retorno
        }
    else:
        # Retorno en caso de no encontrar al actor
        return {"error": f"No se encontraron películas para el actor {nombre_actor}"}