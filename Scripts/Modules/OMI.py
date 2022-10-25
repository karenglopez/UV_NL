"""
Conjunto de clases para la lectura y organizacion de los archivos
"""

from os.path import join
from h5py import File
from numpy import (
    nansum,
    array,
    sum,
    nan,
)


class OzoneOMI:
    def __init__(self) -> None:
        self.kernel = array([
            [0.5, 0.5, 0.5],
            [0.5, 1, 0.5],
            [0.5, 0.5, 0.5],
        ])

    def _normalize_kernel(self,
                          kernel: array) -> array:
        kernel = kernel/nansum(kernel)
        return kernel

    def _read_file(self,
                   filename: str) -> array:
        data = File(filename)
        data = data["HDFEOS"]
        data = data["GRIDS"]
        data = data["OMI Column Amount O3"]
        data = data["Data Fields"]
        data = data["ColumnAmountO3"]
        data = array(data)
        return data

    def _select_area(self,
                     params: dict,
                     data: array) -> array:
        latitude = params["latitude"]
        longitude = params["longitude"]
        latitude = self._transform_location(latitude,
                                            -90)
        longitude = self._transform_location(longitude,
                                             -180)
        latitude_i = latitude-1
        latitude_f = latitude+2
        longitude_i = longitude-1
        longitude_f = longitude+2
        select_data = data[latitude_i:latitude_f,
                           longitude_i:longitude_f]
        select_data[select_data < 0] = 0
        return select_data

    def _transform_location(self,
                            location: float,
                            factor: int) -> int:
        location = location-factor
        location = round(location/0.25)
        return location

    def _get_mean(self,
                  data: array) -> array:
        kernel = self.kernel.copy()
        kernel[data <= 0] = nan
        kernel = self._normalize_kernel(kernel)
        mean = sum(data*kernel)
        mean = round(mean, 3)
        if mean < 200:
            mean = nan
        return mean

    def _get_date(self,
                  filename) -> str:
        date = filename.split("_")[2]
        year = date[:4]
        month = date[5:7]
        day = date[7:10]
        date = "-".join([year,
                         month,
                         day])
        return date

    def _get_filename(self,
                      params: dict,
                      filename: str) -> str:
        filename = join(params["path Ozone OMI"],
                        filename)
        return filename

    def read(self,
             params: dict,
             filename: str) -> float:
        date = self._get_date(filename)
        filename = self._get_filename(params,
                                      filename)
        data = self._read_file(filename)
        data = self._select_area(params,
                                 data)
        data = self._get_mean(data)
        return date, data


class AODOMI:
    def __init__(self) -> None:
        self.kernel = array([
            [0.5, 0.5, 0.5],
            [0.5, 1, 0.5],
            [0.5, 0.5, 0.5],
        ])

    def _normalize_kernel(self,
                          kernel: array) -> array:
        kernel = kernel/nansum(kernel)
        return kernel

    def _read_file(self,
                   filename: str) -> dict:
        header = "FinalAerosolOpticalDepth"
        wavelenght = [
            "354",
            "388",
            "500",
        ]
        data = dict()
        file_data = File(filename)
        file_data = file_data["HDFEOS"]
        file_data = file_data["GRIDS"]
        file_data = file_data["Aerosol NearUV Grid"]
        file_data = file_data["Data Fields"]
        for wave in wavelenght:
            wv_header = f"{header}{wave}"
            data[wave] = array(file_data[wv_header])
        return data

    def _select_area(self,
                     params: dict,
                     data: array) -> dict:
        latitude = params["latitude"]
        longitude = params["longitude"]
        latitude = self._transform_location(latitude,
                                            -90)
        longitude = self._transform_location(longitude,
                                             -180)
        latitude_i = latitude-1
        latitude_f = latitude+2
        longitude_i = longitude-1
        longitude_f = longitude+2
        for wave in data:
            data_wave = data[wave]
            select_data = data_wave[latitude_i:latitude_f,
                                    longitude_i:longitude_f]
            select_data[select_data < 0] = 0
            data[wave] = select_data.copy()
        return data

    def _transform_location(self,
                            location: float,
                            factor: int) -> int:
        location = location-factor
        location = round(location)
        return location

    def _get_mean(self,
                  data: array) -> dict:
        for wave in data:
            data_wave = data[wave]
            kernel = self.kernel.copy()
            kernel[data_wave <= 0] = nan
            kernel = self._normalize_kernel(kernel)
            kernel[data_wave <= 0] = 0
            mean = sum(data_wave*kernel)
            mean = round(mean, 3)
            if mean <= 0:
                mean = nan
            data[wave] = mean
        return data

    def _get_date(self,
                  filename) -> str:
        date = filename.split("_")[2]
        year = date[:4]
        month = date[5:7]
        day = date[7:10]
        date = "-".join([year,
                         month,
                         day])
        return date

    def _get_filename(self,
                      params: dict,
                      filename: str) -> str:
        filename = join(params["path AOD OMI"],
                        filename)
        return filename

    def read(self,
             params: dict,
             filename: str) -> dict:
        date = self._get_date(filename)
        filename = self._get_filename(params,
                                      filename)
        data = self._read_file(filename)
        data = self._select_area(params,
                                 data)
        data = self._get_mean(data)
        return date, data


if __name__ == "__main__":
    pass
