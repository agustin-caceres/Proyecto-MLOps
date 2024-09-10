from fastapi import FastAPI
import pandas as pd


app = FastAPI()


movies_df = pd.read_parquet('dataset_final.parquet')


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
    
    # Convertimos el mes a su número correspondiente
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
    
    # Convertimos el día a su número correspondiente
    dia_numero = dias_diccionario.get(dia.lower())
    
    if dia_numero is not None:
        # Filtramos las películas por el día de la semana del 'release_date'
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
    # Filtramos la película por el título
    film = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    
    if not film.empty:
        # Extraemos el año de estreno y el score
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
    # Filtramos la película por el título
    film = movies_df[movies_df['title'].str.lower() == titulo.lower()]
    
    if not film.empty:
        votos = film['vote_count'].values[0]
        promedio_votos = film['vote_average'].values[0]
        
        # Verificamos si la película tiene al menos 2000 votos
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
    # Filtramos por el nombre del actor
    actor_data = movies_df[movies_df['actor_name'].str.contains(nombre_actor, case=False, na=False)]
    
    # Verificamos si se encontraron resultados
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

