from fastapi import FastAPI
from schema import DataSchema
import joblib
from forex_python.converter import CurrencyRates
import requests
import os
from validation import Validation
from contextlib import asynccontextmanager

app = FastAPI()

FILE_ID = "1L8p2V6DLzIYRoWhos6momcSWKQ9Vg753"
MODEL_PATH = "modelo.pkl"

def download_from_drive(file_id: str, destination: str):
    """
    Descarga archivos desde Google Drive
    """
    
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = None

    # Buscar token de confirmación
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    # Guardar en destino
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

    return destination

@asynccontextmanager
async def lifespan(app: FastAPI):
    global modelo

    if not os.path.exists(MODEL_PATH):
        print("Descargando modelo desde Google Drive...")
        download_from_drive(FILE_ID, MODEL_PATH)

    print("Cargando modelo...")
    with open(MODEL_PATH, "rb") as f:
        modelo = joblib.load(f)

    print("Modelo listo.")

from fastapi.responses import PlainTextResponse

@app.get("/info", response_class=PlainTextResponse)
async def info():
    """
        Endpoint que proporciona informacion sobre los parametros esperados por la API para realizar la prediccion
    """
    
    time_taken = "número de minutos que tarda el vuelo en llegar a su destino (int)"
    day = "día de la semana del vuelo [lunes, martes, miércoles, jueves, viernes, sábado, domingo]"
    airline = "aerolínea del vuelo [air india, airasia, go first, indigo, spicejet, starair, trujet, vistara]"
    from_city = "ciudad de origen [bangalore, chennai, delhi, hyderabad, kolkata, mumbai]"
    to_city = "ciudad de destino [bangalore, chennai, delhi, hyderabad, kolkata, mumbai]"
    stops = "escalas del vuelo [zero, one, two_plus]"
    flight_class = "clase del vuelo [economy, business]"
    departure_time = "hora de salida [early_morning, morning, afternoon, night]"
    arrival_time = "hora de llegada [early_morning, morning, afternoon, night]"
    
    mensaje = f"""
        API para predecir el precio de vuelos

        Parámetros esperados:

        time_taken: {time_taken}
        day: {day}
        airline: {airline}
        from_city: {from_city}
        to_city: {to_city}
        stops: {stops}
        flight_class: {flight_class}
        departure_time: {departure_time}
        arrival_time: {arrival_time}
    """
    
    return mensaje

@app.get("/")
async def root(
    data: DataSchema
):
    validar = Validation()
    information = []
    
    information.append(data.time_taken)
    information.append(validar.validate_day_week(data.day))
    information.extend(validar.airline_checkin(data.airline))
    information.extend(validar.city_validation(data.from_city))
    information.extend(validar.city_validation(data.to_city))
    information.extend(validar.stops_validation(data.stops))
    information.extend(validar.class_validation(data.flight_class))
    information.extend(validar.time_validation(data.departure_time))
    information.extend(validar.time_validation(data.arrival_time))
    
    prediccion = modelo.predict([information])[0]
    
    
    c = CurrencyRates()
    monto_rupias = prediccion
    valor_en_usd = c.convert('INR', 'USD', monto_rupias)
    print(prediccion)
    print(valor_en_usd)
    print(valor_en_usd*3800)
    
    return {
        "precio_inr": prediccion,
        "precio_usd": valor_en_usd,
        "precio_cop": valor_en_usd * 3800
    }