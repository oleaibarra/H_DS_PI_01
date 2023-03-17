import pandas as pd
from fastapi import FastAPI
from mis_funciones import get_max_duration
from mis_funciones import get_score_count
from mis_funciones import get_count_platform
from mis_funciones import get_actor

app = FastAPI()



@app.get("/max-duration/")
async def get_max_duration_endpoint(platform: str = None, duration_type: str = None, year: int = None):
    
    """duration_type toma valores "min" (para películas) y "season" (para series).
       year es el año de lanzamiento, toma valores de 1920 a 2021"""
       
    result = get_max_duration(platform=platform, duration_type=duration_type, year=year)
    return result


@app.get("/score-count/")
async def get_score_count_endpoint(score: int = None, platform: str = None, year: int = None):
    
    """score toma valores de 1 a 10
       platform toma valores "amazon", "disney", "hulu", "netflix"
       year es el año de lanzamiento, toma valores de 1920 a 2021"""
       
    result = get_score_count(score=score, platform=platform, year=year)
    return result 

@app.get("/platform-count/")
async def get_count_platform_endpoint(platform: str):
    
    """Platform toma: "amazon", "disney", "hulu", "netflix".
       El uso de comillas dobles (" ") es indispensable"""
    
    result = get_count_platform(platform=platform)
    return result

@app.get("/actor/")
async def get_actor_endpoint(platform: str = None, year: int = None):
    
    """platform toma valores "amazon", "disney", "hulu", "netflix" (escribir la plataforma entre comillas dobles " ")
       year es el año de lanzamiento, toma valores de 1920 a 2021"""
       
    result = get_actor(platform=platform, year=year)
    return result
    