import utils
import pandas as pd
import scipy.interpolate as interpolator
import numpy as np
from glob import glob

logger = utils.get_logger()

def extrapolator(input_data, to_extrapolate_data_path, model="NearestNDInterpolator"):
    """
    A function which extrapolates PM 2.5 from input coordinates to output coordinates.
    Args:
        model: The interpolation model, the default model is NearestNDInterpolator
        input_data: The input data is dataframe created from the downloaded ECMWF data
        to_extrapolate_data_path: The CSV file path which contains the coordinates at which we want to extrapolate.
    """
    logger.info('interpolating data')
    output = pd.read_csv(to_extrapolate_data_path)

    x = np.array(input_data["longitude"])
    y = np.array(input_data["latitude"])
    z = np.array(input_data["pm25"])

    interpolate = interpolator.NearestNDInterpolator(list(zip(x, y)), z)

    xi = output["longitude"]
    yi = output["latitude"]
    output["pm25"] = 1e+9 * interpolate(xi, yi) # converting kg/m3 to ug/m3
    output.drop(columns=['longitude', 'latitude', 'k_id'], inplace=True)
    output.dropna(inplace=True)
    logger.info('data interpolated')
    return output