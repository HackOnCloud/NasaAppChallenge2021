import requests
import typing
import pandas as pd
import json

lat_default = 1.3237801565033704
long_default = 103.92672074738805
year_start_default = 2019
year_end_default = 2020

def handler(event, context):
    # TODO implement
    return nasa_monthly_climatology_point_optimal_object();    

def nasa_monthly_climatology_si_ef_tilted_surface_point(latitude: float = lat_default
            , longitude: float = long_default
            , year_start: int = year_start_default
            , year_end: int = year_end_default) -> dict:
    """
    See https://power.larc.nasa.gov/api/pages/?urls.primaryName=Climatology
    Function call the above API directly and return a dict of response status and content if successful, FOR A POINT
    Content if successful include average monthly metrics under the Solar Irradiance Equator-facing Tilted Surface metric group
        and other attributes like definition, unit, coordinates, etc.
    """

    for arg in [latitude ,longitude]:
        if not isinstance(arg,float):
            raise TypeError('Latitude and longtitude must be of type float')

    for arg in [year_start ,year_end]:
        if not isinstance(arg,int):
            raise TypeError('year_start and year_end must be of type int')
            
    if year_end - year_start < 1:
        raise ValueError('year_end {} is not larger than year_start {} by at least 1 year'.format(year_end,year_start))

    payload = {'start':str(year_start)
            ,'end':str(year_end)
            ,'latitude':str(latitude)
            ,'longitude':str(longitude)
            ,'community':'re'
            ,'parameters':'SI_EF_TILTED_SURFACE'
            ,'format':'json'}
    r =  requests.get(r'https://power.larc.nasa.gov/api/temporal/climatology/point?',params=payload)        
    return {'response':r.status_code,'content':r.json()}
    
    # r =  requests.get(r'https://power.larc.nasa.gov/api/temporal/climatology/point?',params=payload)       
    # return {
        # 'statusCode': r.status_code,
        # 'body': r.text
    # }

def nasa_monthly_climatology_si_ef_tilted_surface_region(latitude_min: float = lat_default
            , latitude_max: float = lat_default+2
            , longitude_min: float = long_default
            , longitude_max: float = long_default+5
            , year_start: int = 2019
            , year_end: int = 2020) -> dict:
    """
    See https://power.larc.nasa.gov/api/pages/?urls.primaryName=Climatology
    Function call the above API directly and return a dict of response status and content if successful, FOR POINTS IN A REGION
    Content if successful include average monthly metrics under the Solar Irradiance Equator-facing Tilted Surface metric group
        and other attributes like definition, unit, coordinates, etc.
    """

    for arg in [latitude_min, latitude_max, longitude_min, longitude_max]:
        if not isinstance(arg,float):
            raise TypeError('Latitude and longtitude must be of type float')

    for arg in [year_start ,year_end]:
        if not isinstance(arg,int):
            raise TypeError('year_start and year_end must be of type int')
            
    if year_end - year_start < 1:
        raise ValueError('year_end {} is not larger than year_start {} by at least 1 year'.format(year_end,year_start))

    if latitude_max - latitude_min < 2:
        raise ValueError('latitude_max {} is not larger than or equal to latitude_min {} by at least 2 degrees'.format(latitude_max,latitude_min))

    if latitude_max - latitude_min > 10:
        raise ValueError('latitude_max {} is larger than latitude_min {} by 10 degrees or less'.format(latitude_max,latitude_min))

    if longitude_max - longitude_min < 2:
        raise ValueError('longitude_max {} is not larger than or equal to longitude_min {} by at least 2 degrees'.format(longitude_max,longitude_min))

    if longitude_max - longitude_min > 10:
        raise ValueError('longitude_max {} is not larger than longitude_min {} by 10 degrees or less'.format(longitude_max,longitude_min))        
        
    payload = {'start':str(year_start)
            ,'end':str(year_end)
            ,'latitude-min':str(latitude_min)
            ,'latitude-max':str(latitude_max)
            ,'longitude-min':str(longitude_min)
            ,'longitude-max':str(longitude_max)
            ,'community':'re'
            ,'parameters':'SI_EF_TILTED_SURFACE'
            ,'format':'json'}
    r =  requests.get(r'https://power.larc.nasa.gov/api/temporal/climatology/regional?',params=payload)
    return {'response':r.status_code,'content':r.json()}
    
def nasa_monthly_climatology_point_optimal_orientation(latitude: float = lat_default
            , longitude: float = long_default
            , year_start: int = year_start_default
            , year_end: int = year_end_default) -> dict:
    """
    Extract the values and definition of SI_EF_TILTED_SURFACE_OPTIMAL_ANG_ORT from
    nasa_monthly_climatology_si_ef_tilted_surface_point
    Use case: Recommendation on optimal orientation of the panel by month
    """
    climatology_output = nasa_monthly_climatology_si_ef_tilted_surface_point(latitude=latitude
                                                                              ,longitude=longitude
                                                                              ,year_start=year_start
                                                                              ,year_end=year_end)

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
                                                                , year_end: int = year_end_default) -> dict:
    """
    Extract the values and definition of SI_EF_TILTED_SURFACE_OPTIMAL from
    nasa_monthly_climatology_si_ef_tilted_surface_point
    Use case:
    1. Recommendation on optimal energy obtained per panel by month given the optimal angle and orientation
    2. Intermediary function for nasa_monthly_climatology_si_ef_tilted_surface_point_optimal_rec
    """
    climatology_output = nasa_monthly_climatology_si_ef_tilted_surface_point(latitude=latitude
                                                                              ,longitude=longitude
                                                                              ,year_start=year_start
                                                                              ,year_end=year_end)

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
                                                                    , year_end: int = year_end_default) -> dict:
    """
    Extract the values and definition of SI_EF_TILTED_SURFACE_OPTIMAL_ANG from
    nasa_monthly_climatology_si_ef_tilted_surface_point
    Use case:
    1. Recommendation on optimal angle of the panel by month
    2. Intermediary function for nasa_monthly_climatology_si_ef_tilted_surface_point_optimal_rec
    """
    climatology_output = nasa_monthly_climatology_si_ef_tilted_surface_point(latitude=latitude
                                                                              ,longitude=longitude
                                                                              ,year_start=year_start
                                                                              ,year_end=year_end)

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
                                                         ) -> dict:
    """
    Get the values and definition of the following:
    - nasa_monthly_climatology_si_ef_tilted_surface_point_optimal_angle
    - nasa_monthly_climatology_si_ef_tilted_surface_point_optimal_orientation
    to recommend optimal fixed yearly angle (with associated optimal output for that angle)
    
    """

    optimal_energy_monthly = nasa_monthly_climatology_point_optimal_energy(latitude=latitude
                                                                          ,longitude=longitude
                                                                          ,year_start=year_start
                                                                          ,year_end=year_end)
    optimal_angle_monthly = nasa_monthly_climatology_point_optimal_angle(latitude=latitude
                                                                          ,longitude=longitude
                                                                          ,year_start=year_start
                                                                          ,year_end=year_end)
    
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
                                                         ) -> dict:
    angle = nasa_monthly_climatology_point_optimal_angle(latitude=latitude
                                                          ,longitude=longitude
                                                          ,year_start=year_start
                                                          ,year_end=year_end)
    energy = nasa_monthly_climatology_point_optimal_energy(latitude=latitude
                                                          ,longitude=longitude
                                                          ,year_start=year_start
                                                          ,year_end=year_end)
    orientation = nasa_monthly_climatology_point_optimal_orientation(latitude=latitude
                                                          ,longitude=longitude
                                                          ,year_start=year_start
                                                          ,year_end=year_end)
    
    def nasa_monthly_climatology_point_optimal_dict(month: str):
        if month not in ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']:
            raise ValueError("month must be one of the following: 'JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'".format(month))
        return {'angle':angle['Angle'][month]
               ,'energy':energy['Optimal Energy'][month]
               ,'orientation':orientation['Orientation'][month]}
    
    class OptimalObject():
        
        def __init__(self):
            self.Jan = nasa_monthly_climatology_point_optimal_dict('JAN')
            self.Feb = nasa_monthly_climatology_point_optimal_dict('FEB')
            self.Mar = nasa_monthly_climatology_point_optimal_dict('MAR')
            self.Apr = nasa_monthly_climatology_point_optimal_dict('APR')
            self.May = nasa_monthly_climatology_point_optimal_dict('MAY')
            self.Jun = nasa_monthly_climatology_point_optimal_dict('JUN')
            self.Jul = nasa_monthly_climatology_point_optimal_dict('JUL')
            self.Aug = nasa_monthly_climatology_point_optimal_dict('AUG')
            self.Sep = nasa_monthly_climatology_point_optimal_dict('SEP')
            self.Oct = nasa_monthly_climatology_point_optimal_dict('OCT')
            self.Nov = nasa_monthly_climatology_point_optimal_dict('NOV')
            self.Dec = nasa_monthly_climatology_point_optimal_dict('DEC')
    
    return json.dumps(OptimalObject(),default=lambda x:x.__dict__)