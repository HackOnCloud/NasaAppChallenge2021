import requests
import typing
import pandas as pd
import json

lat_default = 1.3237801565033704
long_default = 103.92672074738805
year_start_default = 2019
year_end_default = 2020
parameter_climatology = 'SI_EF_TILTED_SURFACE'
parameter_daily = 'ALLSKY_SFC_SW_DWN'
is_region_default = 0

def nasa_monthly_climatology_point(latitude: float = lat_default
            , longitude: float = long_default
            , year_start: int = year_start_default
            , year_end: int = year_end_default
            , parameters: str = parameter_climatology
            , is_region: int = is_region_default
            , latitude_max: float = lat_default+2
            , longitude_max: float = long_default+5                                   
            ) -> dict:
    """
    See https://power.larc.nasa.gov/api/pages/?urls.primaryName=Climatology
    Function call the above API directly and return a dict of response status and content if successful,
        either for a point, or a region (whose values will be average into points)
    Content if successful include average monthly metrics for the chosen parameters.
    By default the metrics are under the Solar Irradiance Equator-facing Tilted Surface metric group
        and other attributes like definition, unit, coordinates, etc.
    """

    for arg in [latitude, longitude, latitude_max, longitude_max]:
        if not isinstance(arg,float):
            raise TypeError('Latitude and longtitude must be of type float')

    for arg in [year_start, year_end]:
        if not isinstance(arg,int):
            raise TypeError('year_start and year_end must be of type int')

    if is_region not in [0,1]:
        raise TypeError('is_region must be either 1 or 0')
            
    for arg in [parameters]:
        if not isinstance(arg,str):
            raise TypeError('year_start and year_end must be of type str')            
            
    if year_end - year_start < 1:
        raise ValueError('year_end {} is not larger than year_start {} by at least 1 year'.format(year_end,year_start))

    if is_region == 0:
        payload = {'start':str(year_start)
                ,'end':str(year_end)
                ,'latitude':str(latitude)
                ,'longitude':str(longitude)
                ,'community':'re'
                ,'parameters':parameters
                ,'format':'json'}
        r =  requests.get(r'https://power.larc.nasa.gov/api/temporal/climatology/point?',params=payload)
        content = r.json()
    else:
        payload = {'start':str(year_start)
                ,'end':str(year_end)
                ,'latitude-min':str(latitude_min)
                ,'latitude-max':str(latitude_max)
                ,'longitude-min':str(longitude_min)
                ,'longitude-max':str(longitude_max)
                ,'community':'re'
                ,'parameters':parameters
                ,'format':'json'}
        r =  requests.get(r'https://power.larc.nasa.gov/api/temporal/climatology/point?',params=payload)
        content = r.json()
        content = convert_region_to_point()
    return {'response':r.status_code,'content':content}
    
def nasa_daily_point(latitude: float = lat_default
                    , longitude: float = long_default
                    , year_start: int = year_start_default
                    , year_end: int = year_end_default
                    , parameters: str = parameter_daily) -> dict:
    """
    See https://power.larc.nasa.gov/api/pages/?urls.primaryName=Daily
    Function call the above API directly and return a dict of response status and content if successful, FOR A POINT
    Content if successful include average daily metrics under the Solar Irradiance Equator-facing Tilted Surface metric group
        and other attributes like definition, unit, coordinates, etc.
    """

    for arg in [latitude ,longitude]:
        if not isinstance(arg,float):
            raise TypeError('Latitude and longtitude must be of type float')

    for arg in [year_start ,year_end]:
        if not isinstance(arg,int):
            raise TypeError('year_start and year_end must be of type int')
            
    for arg in [parameters]:
        if not isinstance(arg,str):
            raise TypeError('year_start and year_end must be of type str')                        
            
    if year_end - year_start < 1:
        raise ValueError('year_end {} is not larger than year_start {} by at least 1 year'.format(year_end,year_start))

    payload = {'start':str(year_start)
            ,'end':str(year_end)
            ,'latitude':str(latitude)
            ,'longitude':str(longitude)
            ,'community':'re'
            ,'parameters':parameters
            ,'format':'json'}
    r =  requests.get(r'https://power.larc.nasa.gov/api/temporal/daily/point?',params=payload)
    return {'response':r.status_code,'content':r.json()}

# from pathlib import Path
# output = nasa_daily_point(year_start=1990,year_end=2020)
# pd.Series(output['content']['properties']['parameter']['ALLSKY_SFC_SW_DWN'])

def nasa_monthly_climatology_point_optimal_orientation(latitude: float = lat_default
            , longitude: float = long_default
            , year_start: int = year_start_default
            , year_end: int = year_end_default
            , is_region: int = is_region_default) -> dict:
    """
    Extract the values and definition of SI_EF_TILTED_SURFACE_OPTIMAL_ANG_ORT from
    nasa_monthly_climatology_si_ef_tilted_surface_point
    Use case: Recommendation on optimal orientation of the panel by month
    """
    climatology_output = nasa_monthly_climatology_point(latitude=latitude
                                                  ,longitude=longitude
                                                  ,year_start=year_start
                                                  ,year_end=year_end
                                                  ,is_region=is_region)

    response =  climatology_output['response']
    error_message = climatology_output['content']
    if response != 200:
        raise RuntimeError('Core NASA API called unsuccessfully\nAPI response: {}\nError message: {}'.format(response
                                                                                                    ,error_message
                                                                                                    ,link))

    return {'Orientation':climatology_output['content']['properties']['parameter']['SI_EF_TILTED_SURFACE_OPTIMAL_ANG_ORT']
            ,'Definition':climatology_output['content']['parameters']['SI_EF_TILTED_SURFACE_OPTIMAL_ANG_ORT']}

def nasa_monthly_climatology_point_optimal_energy(latitude: float = lat_default
                                                                , longitude: float = long_default
                                                                , year_start: int = year_start_default
                                                                , year_end: int = year_end_default
                                                                , is_region: int = is_region_default) -> dict:
    """
    Extract the values and definition of SI_EF_TILTED_SURFACE_OPTIMAL from
    nasa_monthly_climatology_si_ef_tilted_surface_point
    Use case:
    1. Recommendation on optimal energy obtained per panel by month given the optimal angle and orientation
    2. Intermediary function for nasa_monthly_climatology_si_ef_tilted_surface_point_optimal_rec
    """
    climatology_output = nasa_monthly_climatology_point(latitude=latitude
                                                      , longitude=longitude
                                                      , year_start=year_start
                                                      , year_end=year_end
                                                      , is_region=is_region)

    response =  climatology_output['response']
    error_message = climatology_output['content']
    if response != 200:
        raise RuntimeError('Core NASA API called unsuccessfully\nAPI response: {}\nError message: {}'.format(response
                                                                                                    ,error_message
                                                                                                    ,link))    

    return {'Optimal Energy':climatology_output['content']['properties']['parameter']['SI_EF_TILTED_SURFACE_OPTIMAL']
            ,'Definition':climatology_output['content']['parameters']['SI_EF_TILTED_SURFACE_OPTIMAL']}

def nasa_monthly_climatology_point_optimal_angle(latitude: float = lat_default
                                                                    , longitude: float = long_default
                                                                    , year_start: int = year_start_default
                                                                    , year_end: int = year_end_default
                                                                    , is_region: int = is_region_default) -> dict:                                                 
    """
    Extract the values and definition of SI_EF_TILTED_SURFACE_OPTIMAL_ANG from
    nasa_monthly_climatology_si_ef_tilted_surface_point
    Use case:
    1. Recommendation on optimal angle of the panel by month
    2. Intermediary function for nasa_monthly_climatology_si_ef_tilted_surface_point_optimal_rec
    """
    climatology_output = nasa_monthly_climatology_point(latitude=latitude
                                                      ,longitude=longitude
                                                      ,year_start=year_start
                                                      ,year_end=year_end
                                                      ,is_region=is_region)

    response =  climatology_output['response']
    error_message = climatology_output['content']
    if response != 200:
        raise RuntimeError('Core NASA API called unsuccessfully\nAPI response: {}\nError message: {}'.format(response
                                                                                                    ,error_message
                                                                                                    ,link))    
    
    return {'Angle':climatology_output['content']['properties']['parameter']['SI_EF_TILTED_SURFACE_OPTIMAL_ANG']
            ,'Definition':climatology_output['content']['parameters']['SI_EF_TILTED_SURFACE_OPTIMAL_ANG']}

def nasa_monthly_climatology_point_optimal_yearly_angle_energy(latitude: float = lat_default
                                                        , longitude: float = long_default
                                                        , year_start: int = year_start_default
                                                        , year_end: int = year_end_default
                                                        , is_region: int = is_region_default) -> dict:
    """
    Get the values and definition of the following:
    - nasa_monthly_climatology_si_ef_tilted_surface_point_optimal_angle
    - nasa_monthly_climatology_si_ef_tilted_surface_point_optimal_orientation
    to recommend optimal fixed yearly angle (with associated optimal output for that angle)
    
    """

    optimal_energy_monthly = nasa_monthly_climatology_point_optimal_energy(latitude=latitude
                                                                          ,longitude=longitude
                                                                          ,year_start=year_start
                                                                          ,year_end=year_end
                                                                          ,is_region=is_region)
    optimal_angle_monthly = nasa_monthly_climatology_point_optimal_angle(latitude=latitude
                                                                          ,longitude=longitude
                                                                          ,year_start=year_start
                                                                          ,year_end=year_end
                                                                          ,is_region=is_region)
    
    df = pd.DataFrame()
    df['Optimal Energy'] = pd.Series(optimal_energy_monthly['Optimal Energy'])
    df.index = [optimal_angle_monthly['Angle']['JAN']
                ,optimal_angle_monthly['Angle']['FEB']
                ,optimal_angle_monthly['Angle']['MAR']
                ,optimal_angle_monthly['Angle']['APR']
                ,optimal_angle_monthly['Angle']['MAY']
                ,optimal_angle_monthly['Angle']['JUN']
                ,optimal_angle_monthly['Angle']['JUL']
                ,optimal_angle_monthly['Angle']['AUG']
                ,optimal_angle_monthly['Angle']['SEP']
                ,optimal_angle_monthly['Angle']['OCT']
                ,optimal_angle_monthly['Angle']['NOV']
                ,optimal_angle_monthly['Angle']['DEC']
                ,optimal_angle_monthly['Angle']['ANN']]
    df = df.loc[df.index[df.index != -999].unique()]
    df_aggregated_sum =  df.groupby(level=0).sum()['Optimal Energy']
    df_aggregated_count = df.groupby(level=0).count()['Optimal Energy']
    angle = df_aggregated_sum.idxmax()
    energy = df_aggregated_sum[angle]
    count = df_aggregated_count[angle]
    result = {'Angle':angle,'Angle Definition':optimal_angle_monthly['Definition']
              ,'Number of months with this recommended angle':count
              ,'Total energy':energy,'Energy Definition':optimal_energy_monthly['Definition']}
    
    return result

def nasa_monthly_climatology_point_optimal_object(latitude: float = lat_default
                                                        , longitude: float = long_default
                                                        , year_start: int = year_start_default
                                                        , year_end: int = year_end_default
                                                        , is_region: int = is_region_default) -> str:
    """
    Return a JSON str containing the recommended angle, orientation, as well as associated energy level in a dict
    """
    angle = nasa_monthly_climatology_point_optimal_angle(latitude=latitude
                                                          ,longitude=longitude
                                                          ,year_start=year_start
                                                          ,year_end=year_end
                                                          ,is_region=is_region)
    energy = nasa_monthly_climatology_point_optimal_energy(latitude=latitude
                                                          ,longitude=longitude
                                                          ,year_start=year_start
                                                          ,year_end=year_end
                                                          ,is_region=is_region)
    orientation = nasa_monthly_climatology_point_optimal_orientation(latitude=latitude
                                                          ,longitude=longitude
                                                          ,year_start=year_start
                                                          ,year_end=year_end
                                                          ,is_region=is_region)                                                                     
    
    months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    
    def nasa_monthly_climatology_point_optimal_dict(month: str):
        if month not in months:
            raise ValueError("month must be one of the following: 'JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'".format(month))
        return {'angle':angle['Angle'][month]
               ,'energy':energy['Optimal Energy'][month]
               ,'orientation':orientation['Orientation'][month]}

    output = []
    for month in months:
        _dict = nasa_monthly_climatology_point_optimal_dict(month)
        _dict['month'] = month
        output.append(_dict)
    
    class OptimalObject():
        pass
#         def __init__(self):
#             self.Jan = nasa_monthly_climatology_point_optimal_dict('JAN')
#             self.Feb = nasa_monthly_climatology_point_optimal_dict('FEB')
#             self.Mar = nasa_monthly_climatology_point_optimal_dict('MAR')
#             self.Apr = nasa_monthly_climatology_point_optimal_dict('APR')
#             self.May = nasa_monthly_climatology_point_optimal_dict('MAY')
#             self.Jun = nasa_monthly_climatology_point_optimal_dict('JUN')
#             self.Jul = nasa_monthly_climatology_point_optimal_dict('JUL')
#             self.Aug = nasa_monthly_climatology_point_optimal_dict('AUG')
#             self.Sep = nasa_monthly_climatology_point_optimal_dict('SEP')
#             self.Oct = nasa_monthly_climatology_point_optimal_dict('OCT')
#             self.Nov = nasa_monthly_climatology_point_optimal_dict('NOV')
#             self.Dec = nasa_monthly_climatology_point_optimal_dict('DEC')
    
    return json.dumps(output)

def nasa_monthly_climatology_point_optimal_energy_lowest_month(latitude: float = lat_default
                                                                , longitude: float = long_default
                                                                , year_start: int = year_start_default
                                                                , year_end: int = year_end_default
                                                                , is_region: int = is_region_default
                                                                ) -> float:
    """
    Return optimal energy in kW per hour per squared meter per day of the lowest month
    """
    
    optimal_energy = nasa_monthly_climatology_point_optimal_energy(latitude=latitude
                                                                ,longitude=longitude
                                                                ,year_start=year_start
                                                                ,year_end=year_end
                                                                ,is_region=is_region)
    
    series = pd.Series(a['Optimal Energy'])
    min_index = series[series.index[series.index != 'ANN']].idxmin()
    
    days_per_month = {'JAN':31,'FEB':28,'MAR':31,'APR':30,'MAY':31,'JUN':30
                     ,'JUL':31,'AUG':31,'SEP':30,'OCT':31,'NOV':30,'DEC':31}
    
    return {'energy':series[min_index]
            ,'days_per_month':days_per_month[min_index]}

def panel_recommendation(expected_electricity: float
                         , latitude: float = lat_default
                         , longitude: float = long_default
                         , year_start: int = year_start_default
                         , year_end: int = year_end_default
                         , is_region: int = is_region_default
                         , coefficient: float = 0.15
                         , size: float = 1.6
                         , epsilon: float = 0.95
                         ) -> float:
    """
    coefficient of panel efficiency is in decimal (min 0, max 1)
    size of panel is in square meter
    expected_electricity is in kW per hour per month
    Return the energy output per panel
    """
    optimal_energy_dict = nasa_monthly_climatology_point_optimal_energy_lowest_month(latitude = latitude
                                                                                , longitude = longitude
                                                                                , year_start = year_start
                                                                                , year_end = year_end
                                                                                , is_region = is_region
                                                                                )
    optimal_energy = optimal_energy_dict['energy'] * optimal_energy_dict['days_per_month']
    
    output_per_panel_per_month =  optimal_energy * coefficient * size * epsilon
    rec_panel_per_month = expected_electricity/ output_per_panel_per_month
    total_panel_size = rec_panel_per_month * size
    
    return {'output_per_panel_per_month':output_per_panel_per_month
           ,'recommended_panel_per_month':rec_panel_per_month
           ,'total_panel_size':total_panel_size}

# panel_recommendation(100)
