class Validation():
    
    @staticmethod
    def validate_day_week(day: str) -> int:
    
        if day.lower() == "lunes":
            return 1
        elif day.lower() == "martes":
            return 2
        elif day.lower() == "miércoles":
            return 3
        elif day.lower() == "jueves":
            return 4
        elif day.lower() == "viernes":
            return 5
        elif day.lower() == "sábado":
            return 6
        elif day.lower() == "domingo":
            return 7

    @staticmethod
    def airline_checkin(airline: str) -> list:
        airline = airline.lower()
        
        columnas = [
            "air india",
            "airasia",
            "go first",
            "indigo",
            "spicejet",
            "starair",
            "trujet",
            "vistara"
        ]
        
        return [1 if airline == col else 0 for col in columnas]

    @staticmethod
    def city_validation(city_validation: str) -> list:
        city_validation = city_validation.lower()
        
        columnas = [
            "bangalore",
            "chennai",
            "delhi",
            "hyderabad",
            "kolkata",
            "mumbai"
        ]
        
        return [1 if city_validation == col else 0 for col in columnas]

    @staticmethod
    def stops_validation(stops: str) -> list:
        
        stops = stops.lower()
        
        columnas = [
            "one",
            "two_plus",
            "zero"
        ]
        
        return [1 if stops == col else 0 for col in columnas]

    @staticmethod
    def class_validation(flight_class: str) -> list:
        
        flight_class = flight_class.lower()
        
        columnas = [
            "business",
            "economy"
        ]
        
        return [1 if flight_class == col else 0 for col in columnas]

    @staticmethod
    def time_validation(time: str) -> list:
        
        time = time.lower()
        
        columnas = [
            "afternoon",
            "early_morning",
            "morning",
            "night"
        ]
        
        return [1 if time == col else 0 for col in columnas]
