                                            #   Format checker  #

def TryFormat(airport):
    #   ICAO Validation Format, if it's not and string || it's too short or longer to be a ICAO code
    if not(isinstance(airport.icao, str)):        #   Checks if it's and str
        raise Exception("Invalid icao format, needs to be a string!")
    elif not(len(airport.icao) == 4):                                       #   Checks if it's len 4
        raise Exception("Invalid icao format, needs to be a string with len 4!")
    #   If it's all right, check's the lat and lon value
    else:
        try:
            #   Excep in the case that you put in lat/lon a Boolean value!
            if isinstance(airport.lat, bool) or isinstance(airport.lon, bool):
                raise ValueError("Latitude and Longitude must be numbers, not boolean")
            else:
                airport.lat = float(airport.lat)                            # Pass the format to float
                airport.lon = float(airport.lon)                            # Pass the format to a float
            #In case that you can't pass to float type, give and advice and stop the process!
        except (ValueError, TypeError):
            raise ValueError("Invalid lat/lon Format, needs to be a number!")
    return True                                                             #   If it's all right return a True