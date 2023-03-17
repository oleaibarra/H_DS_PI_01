import pandas as pd

def get_max_duration(platform=None, duration_type=None, year=None):
    
    """ 
        Dados los parámetros opcionales año, plataforma y tipo de duración, esta función carga un archivo CSV que contiene 
        información sobre películas y programas de TV, filtra los datos según los parámetros y devuelve una tupla que 
        contiene el valor máximo de duración, el tipo de duración y el título de la película con la duración máxima.

    Args:
    
        year (int, opcional): Si se especifica, filtra los datos para incluir solo películas y programas de TV lanzados 
        en ese año. 
        
        platform (str, opcional): Si se especifica, filtra los datos para incluir solo películas y programas de TV 
        disponibles en una plataforma de streaming (Amazon, Disney, Hulu, Netflix) que comience con la letra especificada.
        De no especificarse, devolverá la película o serie de mayor duración para todas las plataformas.
        
        duration_type (str, opcional): Si se especifica, filtra los datos para incluir solo películas o programas de TV 
        con este tipo de duración (por ejemplo, 'min' para películas, 'season' para programa de TV).
        
    Returns:
    
        Una tupla que contiene cuatro valores:
        - max_duration (int): El valor máximo de la columna 'duration_int' en los datos filtrados.
        - max_duration_type (str): El valor de la columna 'duration_type' para la película o programa de TV con la 
          duración máxima.
        - max_duration_title (str): El valor de la columna 'title' para la película o programa de TV con la duración 
          máxima.
        - max_duration_year (int): El año más antiguo que tiene la plataforma para la película o serie (si el año especificado era menor);
          el año más reciente que tiene la plataforma para la película o serie (si el año especificado era mayor); el año especificado (si esta dentro de rango).
        
    """
    # Crear data frame 
    df = pd.read_csv('plata_stars.csv')
    
    # Filtrar el data frame con los parámetros opcionales
    
    if platform is not None:
        
        # Convierte la plataforma a minúsculas
        platform = platform.lower()
    
        # Verifica si la plataforma es válida
        if 'net' in platform: 
            platform = 'n'
        elif 'hu' in platform:
            platform = 'h'
        elif 'di' in platform: 
            platform = 'd'
        elif 'am' in platform:
            platform = 'a'
        else:
            # Devuelve un mensaje de error si la plataforma no es válida
            return "Platform sólo toma alguna de estas opciones: 'amazon', 'disney', 'hulu', 'netflix'"
            
        # Filtra el DataFrame por la plataforma especificada
        df = df[df['show_id'].str[0] == platform]
        
    if duration_type is not None:
        duration_type = duration_type.lower()

        # Verifica si el tipo es válido
        if "se" in duration_type:
            duration_type = "s"
        else: 
            duration_type = "m"

        df = df[df['duration_type'].str[0] == duration_type]

    
    # En caso de que al parámetro opcional year se le haya asignado valor
    observ = "None"
    if year != None:
        year_parametro = year
        
        # Verifica si el año es válido
        rango = list(df['release_year'].unique())
  
        mini = df['release_year'].min()
        maxi = df['release_year'].max()
            
        if year < mini:
            year = mini

        elif year > maxi:
            year = maxi
            
        elif year not in rango:
            rango.append(year)
            rango.sort()
            pos = rango.index(year)
            if year == rango[-1]: 
                year = rango[pos - 1]
            elif year == rango[0]:
                year = rango[pos + 1]
            elif abs(year - (rango[pos - 1])) < abs((rango[pos + 1]) - year):
                year = rango[pos - 1]
            else: 
                year = rango[pos + 1]
                
        if year_parametro != year:
            if duration_type == "m":
                observ = "No hay películas para el año y/o la plataforma especificada. Se toma el año más cercano"
            else: 
                observ = "No hay series para el año y/o la plataforma especificada. Se toma el año más cercano"
            
            
        # Filtra por el año más reciente que tenga la plataforma para película o serie
        df = df[df['release_year'] == year]
             
            
        
    # Obtine el máximo valor de duration_int y el título de la película
    
    max_duration = df['duration_int'].max()
    max_duration = int(max_duration)
    max_duration_type = df.loc[df['duration_int'].idxmax(), 'duration_type']
    max_duration_title = df.loc[df['duration_int'].idxmax(), 'title']
    max_duration_year = df.loc[df['duration_int'].idxmax(), 'release_year']
    max_duration_year = int(max_duration_year)


    # Regresa resultados
    return {
        'max_duration': max_duration,
        'max_duration_type': max_duration_type,
        'max_duration_title': max_duration_title,
        'year': max_duration_year,
        'Observaciones': observ
    }
    
import pandas as pd

def get_score_count(score=None, platform=None, year=None):
    """ 
       Regresa el número de películas con una calificación igual o mayor a cierto puntaje
       para los principales servicios de streaming (amazon, disney, hulu, netflix). 
       
       Filtra por el puntaje (1 a 10) si se utiliza el parámetro 'score', regresando el número de películas
       mayores o iguales a ese puntaje. De no seleccionarse regresa el número de películas con puntaje de 8 o mayor. 
       
       Filtra por servicio (platform=amazon, platform=disney, platform=hulu, platform=netflix)
       si se utiliza el parámetro opcional 'platform'.
       
       Filtra por año de lanazamiento si se utiliza el parámetro opcional 'year'. 

    Args:
    
        platform (_str_): una de las siguintes: amazon, disney, hulu, netflix 
        
        score (_float_): valor entre 1 y 10
        
        year (_int_): valor entre 1920 y 2021

    Returns:
    
        num_movies (_int_): número de películas con puntaje mayor al especificado. 
    """
    # Carga el archivo CSV como un DataFrame
    df = pd.read_csv('plata_stars.csv')
    
    
    # Verifica que se haya asignado valor al parámetro score y que sea menor al máximo
    if score == None:
        stars = 8
    
    elif score < 1: 
        stars = 1
        
    elif score > 10:
        stars = 10
        
    elif score in range(1,11):
        stars = score
    
    # Filtra el DataFrame por el score asignado (películas con score mayor o igual)    
    df = df[df['stars'] >= stars]
    
    # En caso de que al parámetro opcional platform se le haya asignado valor
    if platform != None: 
        
        # Convierte la plataforma a minúsculas
        platform = platform.lower()
    
        # Verifica si la plataforma es válida
        if 'net' in platform: 
            platform = 'n'
        elif 'hu' in platform:
            platform = 'h'
        elif 'di' in platform: 
            platform = 'd'
        elif 'am' in platform:
            platform = 'a'
        else:
            # Devuelve un mensaje de error si la plataforma no es válida
            return {"error": "Platform sólo toma alguna de estas opciones: 'amazon', 'disney', 'hulu', 'netflix'"}
            
        # Filtra el DataFrame por la plataforma especificada
        df = df[df['show_id'].str[0] == platform]
    
    observ = " "
    # En caso de que al parámetro opcional year se le haya asignado valor
    if year != None:
        
        # Verifica si el año es válido
        rango = list(df['release_year'].unique())
  
        mini = df['release_year'].min()
        maxi = df['release_year'].max()
            
        if year < mini:
            year = mini
            observ = f"No hay películas con puntaje igual o mayor a {stars} para la plataforma y año seleccionado"

        elif year > maxi:
            year = maxi
            observ = f"No hay películas con puntaje igual o mayor a {stars} para la plataforma y año seleccionado"
            
        elif year not in rango:
            rango.append(year)
            rango.sort()
            pos = rango.index(year)
            if year == rango[-1]: 
                year = rango[pos - 1]
            elif year == rango[0]:
                year = rango[pos + 1]
            elif abs(year - (rango[pos - 1])) < abs((rango[pos + 1]) - year):
                year = rango[pos - 1]
            else: 
                year = rango[pos + 1]
            observ = f"No hay películas con puntaje igual o mayor a {stars} para la plataforma y año seleccionado"
            
            
        # Filtra por el año más reciente que tenga la plataforma para película o serie
        df = df[df['release_year'] == year]
            
    
    # Si no se seleccionaron parámetros opcionales    
    
    # Cuenta el número de películas que cumplen con el criterio de score
    num_movies = int((df['stars'] >= stars).sum())
    
    # para output de num_movies
    num_movies = int(num_movies)
    
    # para output de stars
    stars = int(stars)
    
    # para output de plataformas
    if platform == None: 
        plataformas = "Todas las plataformas"
    else:
        if platform == "a": 
            plataformas = "amazon"
        elif platform == "h":
            plataformas = "hulu"
        elif platform == "d":
            plataformas = "disney"
        elif platform == "n":
            plataformas = "netflix"
     
    # para output de year       
    if year == None:
        year = "Para todos los años"
    else:
        year = int(year)
        
    return {'num_movies': num_movies,
            'con puntaje igual o mayor a': stars,
            'En el año': year,
            'Plataforma': plataformas,
            'score': 'los putajes corresponden a una escala de 1 a 10',
            'Observaciones': observ}

import pandas as pd

def get_count_platform(platform):
    """
    Cuenta el número de películas en una plataforma de streaming específica 
    basándose en un archivo CSV que contiene una columna 'show_id' que indica 
    la plataforma de cada película.

    Args:
        platform (str): La abreviatura de la plataforma de streaming que se desea contar. 
                        Puede ser una de las siguientes opciones: 'net' para Netflix, 
                        'hu' para Hulu, 'di' para Disney+, o 'am' para Amazon Prime Video.

    Returns:
        int: El número de películas en la plataforma de streaming especificada.

        str: Si la plataforma especificada no es reconocida, se devuelve un mensaje de error.

    """

    df = pd.read_csv('plata_stars.csv')

    # Convierte la plataforma a minúsculas
    platform = platform.lower()

    # Verifica si la plataforma es válida
    if 'net' in platform: 
        platform = 'n'
    elif 'hu' in platform:
        platform = 'h'
    elif 'di' in platform: 
        platform = 'd'
    elif 'am' in platform:
        platform = 'a'
    else:
        # Devuelve un mensaje de error si la plataforma no es válida
        return {"error": "Platform sólo toma alguna de estas opciones: 'amazon', 'disney', 'hulu', 'netflix'"}

    # Filtra el DataFrame para incluir solo las películas de la plataforma seleccionada
    num_pelis = int((df['show_id'].str[0] == platform).sum())

    return {"num_pelis":num_pelis}

import pandas as pd

def get_actor(platform=None, year=None):
    
    """
    Obtiene el actor con más menciones de una plataforma y un año específicos.

    Args:
    
        platform (str): El nombre de la plataforma en minúsculas (ej: 'netflix','disney', 'amazon').
        
        year (int): El año de lanzamiento de la película o serie a buscar.

    Returns:
    
        str: El nombre del actor con más menciones en la plataforma y año especificados.
        
        int: El número de veces que el actor aparece en distintas películas

        Si la plataforma ingresada no es válida (no se encuentra en la lista de plataformas soportadas), se devuelve
        una cadena que indica que el nombre de la plataforma es incorrecto.

    """
    # Carga el archivo CSV como un DataFrame
    df = pd.read_csv('plata_stars.csv')
    
    # En caso de que al parámetro opcional platform se le haya asignado valor
    if platform != None: 
        
        # Convierte la plataforma a minúsculas
        platform = platform.lower()
    
        # Verifica si la plataforma es válida
        if 'net' in platform: 
            platform = 'n'
        elif 'di' in platform: 
            platform = 'd'
        elif 'hu' in platform:
            return {"disculpas": "no se tiene información sobre actor para plataforma 'hulu'"}
        elif 'am' in platform:
            platform = 'a'
        else:
            # Devuelve un mensaje de error si la plataforma no es válida
            return {"error": "Platform sólo toma alguna de estas opciones: 'amazon', 'disney', 'netflix'"}
            
        # Filtra el DataFrame por la plataforma especificada
        df = df[df['show_id'].str[0] == platform]
    
    # En caso de que al parámetro opcional year se le haya asignado valor
    if year != None:
        
        # Verifica si el año es válido
        mini = df['release_year'].min()
        maxi = df['release_year'].max()
        
        if year in range(mini,(maxi + 1)):
        
            # Filtra el Data Frame por año especificado
            df = df[df['release_year'] == year]
            
        elif year < mini:
            year = mini
            df = df[df['release_year'] == mini] 
        
        elif year > maxi:
            year = maxi
            df = df[df['release_year'] == maxi]
            
    
    # Concatena las cadenas en la columna 'cast'
    cast_string = df['cast'].str.cat(sep=',')

    # Separa la cadena concatenada por comas para obtener una lista de todos los actores
    cast_list = cast_string.split(',')

    # Crea un diccionario para contar el número de apariciones de cada actor
    actor_counts = {}
    for actor in cast_list:
        if actor in actor_counts:
            actor_counts[actor] += 1
        else:
            actor_counts[actor] = 1

    # Encuentra el actor con más apariciones
    most_common_actor = max(actor_counts, key=actor_counts.get)
    num_apariciones = int(actor_counts[most_common_actor])
    if year == None: 
        year = "Para todos los años"
    else:
        year = int(year)

    return {"most_common_actor":most_common_actor, "num_apariciones":num_apariciones, 'año': year}
