import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        return f"Error: Location '{location}' not found in data_columns."

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    try:
        return round(__model.predict([x])[0], 2)
    except AttributeError:
        return "Prediction error: Model is not loaded correctly."


def load_saved_artifacts():
    global __data_columns
    global __locations

    print("Loading saved artifacts...start")
    try:
        with open("./artifacts/columns.json", "r") as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

        global __model
        if __model is None:
            with open('./artifacts/banglore_home_prices_model.pickle', 'rb') as f:
                __model = pickle.load(f)

        print("Loading saved artifacts...done")
    except Exception as e:
        print(f"Error loading artifacts: {e}")


def get_location_names():
    return __locations


def get_data_columns():
    return __data_columns


if __name__ == '__main__':
    load_saved_artifacts()
    print("Available Locations:", get_location_names())

    print("Estimated Price (1st Phase JP Nagar, 3 BHK, 3 Bath): ₹",
          get_estimated_price('1st Phase JP Nagar', 1000, 4, 3))
    print("Estimated Price (1st Phase JP Nagar, 2 BHK, 2 Bath): ₹",
          get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print("Estimated Price (Kalhalli, 2 BHK, 2 Bath): ₹", get_estimated_price('Kalhalli', 1000, 2, 2))  # other location
    print("Estimated Price (Ejipura, 2 BHK, 2 Bath): ₹", get_estimated_price('Ejipura', 1000, 2, 2))  # other location
