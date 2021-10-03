import requests
import typing
import pandas as pd
import json
import math

lat_default = 1.3237801565033704
long_default = 103.92672074738805
year_start_default = 2019
year_end_default = 2020
parameter_climatology = 'SI_EF_TILTED_SURFACE'
parameter_daily = 'ALLSKY_SFC_SW_DWN'
is_region_default = 0
coefficient_default = 0.15
size_default = 1.6
epsilon_default = 0.95
electricity_cost_per_kwh_default = 0.17
installation_cost_per_sm_default = 450.0
maintenance_cost_per_sm_default = 4.0
nasa_growth_max = 0.05
nasa_growth_min = -0.05
depreciation_rate_default = 0.005

def nasa_monthly_climatology_point(latitude: float = lat_default
            , longitude: float = long_default
            , year_start: int = 2019
            , year_end: int = 2020
            , parameters: str = parameter_climatology
            , is_region: int = is_region_default
            , latitude_max: float = lat_default+2
            , longitude_max: float = long_default+5                                   
            ) -> dict:
    """
    See https://power.larc.nasa.gov/api/pages/?urls.primaryName=Climatology
    Function call the above API directly and return a dict of response status and content if successful,
        either for a point, or a region (whose values will be average into points)
    Content if successful include average monthly metrics for the chosen parameters
        and other attributes like definition, unit, coordinates, etc.
    By default the metrics are under the Solar Irradiance Equator-facing Tilted Surface metric group
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
                ,'latitude-min':str(latitude)
                ,'latitude-max':str(latitude_max)
                ,'longitude-min':str(longitude)
                ,'longitude-max':str(longitude_max)
                ,'community':'re'
                ,'parameters':parameters
                ,'format':'json'}
        r =  requests.get(r'https://power.larc.nasa.gov/api/temporal/climatology/regional?',params=payload)
        content = r.json()
#         content = convert_region_to_point()
    return {'response':r.status_code,'content':content}
    
def nasa_daily_point(latitude: float = lat_default
            , longitude: float = long_default
            , date_start: int = 20200101
            , date_end: int = 20201231
            , parameters: str = parameter_daily
            , is_region: int = is_region_default
            , latitude_max: float = lat_default+2
            , longitude_max: float = long_default+5                                   
            ) -> dict:
    """
    See https://power.larc.nasa.gov/api/pages/?urls.primaryName=Daily
    Function call the above API directly and return a dict of response status and content if successful,
        either for a point, or a region (whose values will be average into points)
    Content if successful include daily metrics for the chosen parameters
        and other attributes like definition, unit, coordinates, etc.
    By default the metrics are under the Solar Irradiance Equator-facing Tilted Surface metric group
    """

    for arg in [latitude, longitude, latitude_max, longitude_max]:
        if not isinstance(arg,float):
            raise TypeError('Latitude and longtitude must be of type float')

    for arg in [date_start, date_end]:
        if not isinstance(arg,int):
            raise TypeError('year_start and year_end must be of type int')

    if is_region not in [0,1]:
        raise TypeError('is_region must be either 1 or 0')
            
    for arg in [parameters]:
        if not isinstance(arg,str):
            raise TypeError('year_start and year_end must be of type str')            
            
    if date_end - date_start < 1:
        raise ValueError('date_end {} is before date_start {}'.format(year_end,year_start))

    if is_region == 0:
        payload = {'start':str(date_start)
                ,'end':str(date_end)
                ,'latitude':str(latitude)
                ,'longitude':str(longitude)
                ,'community':'re'
                ,'parameters':parameters
                ,'format':'json'}
        r =  requests.get(r'https://power.larc.nasa.gov/api/temporal/daily/point?',params=payload)
        content = r.json()
    else:
        payload = {'start':str(date_start)
                ,'end':str(date_end)
                ,'latitude-min':str(latitude)
                ,'latitude-max':str(latitude_max)
                ,'longitude-min':str(longitude)
                ,'longitude-max':str(longitude_max)
                ,'community':'re'
                ,'parameters':parameters
                ,'format':'json'}
        r =  requests.get(r'https://power.larc.nasa.gov/api/temporal/daily/regional?',params=payload)
        content = r.json()
#         content = convert_region_to_point()
    return {'response':r.status_code,'content':content,'object':r}
    
def daily_data_for_David(years: list = [20160000,20170000,20180000,20190000,20200000]):
    df_base = pd.DataFrame()
    latitudes = [-10.0,0.0,10.0,20.0]
    longitudes = [100.0,110.0,120.0,130.0]
    year_thousand = years
    for year in year_thousand:
        date_start = year + 101
        date_end = year + 1231
        for latitude in latitudes:
            latitude_start = latitude
            latitude_end = latitude_start+10
            for longitude in longitudes:
                longitude_start = longitude
                longitude_end = longitude_start+10
                output = nasa_daily_point(date_start=date_start
                                 ,date_end=date_end
                                 ,longitude=longitude_start
                                 ,longitude_max=longitude_end
                                 ,latitude=latitude_start
                                 ,latitude_max=latitude_end
                                 ,is_region=1)
                print(output['object'].url)
                print(output['response'])
                
                features = output['content']['features']
                for feature in features:
                    longitude = feature['geometry']['coordinates'][0]
                    latitude = feature['geometry']['coordinates'][1]
                    altitude = feature['geometry']['coordinates'][2]
                    df = pd.DataFrame(pd.Series(feature['properties']['parameter']['ALLSKY_SFC_SW_DWN'])
                                      ,columns=['ALLSKY_SFC_SW_DWN'])
                    print('Processed {}'.format(str(feature['geometry']['coordinates'])))
                    df['longitude'] = longitude
                    df['latitude'] = latitude
                    df['altitude'] = altitude
                    df = df.reset_index()
                    df_base = pd.concat([df_base,df],ignore_index=True)
    if df_base[df_base.duplicated(['index','longitude','latitude','altitude'])].shape[0] != 0:
        print('!!!There are duplicates!!!')
    return df_base

# from pathlib import Path
# df_david_final = pd.concat([df_david_pre_2020,df_david_2020],ignore_index=True)
# df_david_final = daily_data_for_David([20200000])
# df_david_final.to_csv(Path.home().joinpath('Onedrive','Desktop','david_daily.csv'))    

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
    
    series = pd.Series(optimal_energy['Optimal Energy'])
    min_index = series[series.index[series.index != 'ANN']].idxmin()
    
    days_per_month = {'JAN':31,'FEB':28,'MAR':31,'APR':30,'MAY':31,'JUN':30
                     ,'JUL':31,'AUG':31,'SEP':30,'OCT':31,'NOV':30,'DEC':31}
    
    return {'energy':series[min_index]
            ,'days_per_month':days_per_month[min_index]}

def average_monthly_input_post_depreciation(optimal_energy: dict
                                           , panel_duration: int
                                           , depreciation_rate: float = depreciation_rate_default) -> float:    
    df = pd.DataFrame()
    series = pd.Series(optimal_energy).drop('ANN')
    df['Year 0'] = series
    for i in range(1,panel_duration):
        col_new = 'Year {}'.format(i)
        col_previous = 'Year {}'.format(i-1)
        df[col_new] = df[col_previous]*(1-depreciation_rate)
    return df.mean().mean()

def panel_recommendation(average_monthly_electricity_bill: float
                         , panel_duration: int
                         , electricity_cost_per_kwh: float = electricity_cost_per_kwh_default
                         , depreciation_rate: float = depreciation_rate_default
                         , latitude: float = lat_default
                         , longitude: float = long_default
                         , year_start: int = year_start_default
                         , year_end: int = year_end_default
                         , is_region: int = is_region_default
                         , coefficient: float = coefficient_default
                         , size: float = size_default
                         , epsilon: float = epsilon_default
                         , installation_cost_per_sm: float = installation_cost_per_sm_default
                         , maintenance_cost_per_sm_per_year: float = maintenance_cost_per_sm_default
                         ) -> float:
    """
    coefficient of panel efficiency is in decimal (min 0, max 1)
    size of panel is in square meter
    year_start and year_end refers to the timeframe for NASA data extraction
    Return the energy output per panel
    """
    for arg in [average_monthly_electricity_bill,coefficient,size,epsilon
                ,installation_cost_per_sm,maintenance_cost_per_sm_per_year]:
        if not isinstance(arg,float):
            raise TypeError('Coefficient, Epsilon, Size, Depreciation Rate, and dollar values args must be in float')
    
    if panel_duration <= 0:
        raise ValueError('Panel Duration must be a positive int')
    
#     optimal_energy_dict = nasa_monthly_climatology_point_optimal_energy_lowest_month(latitude = latitude
#                                                                                 , longitude = longitude
#                                                                                 , year_start = year_start
#                                                                                 , year_end = year_end
#                                                                                 , is_region = is_region
#                                                                                 )
#     optimal_energy_month = optimal_energy_dict['energy'] * optimal_energy_dict['days_per_month']
    optimal_energy = nasa_monthly_climatology_point_optimal_energy(latitude = latitude
                                                                    , longitude = longitude
                                                                    , year_start = year_start
                                                                    , year_end = year_end
                                                                    , is_region = is_region
                                                                    )

    optimal_energy_month = average_monthly_input_post_depreciation(optimal_energy=optimal_energy['Optimal Energy']
                                                                  ,panel_duration=panel_duration
                                                                  ,depreciation_rate=depreciation_rate)*30
    
    average_monthly_electricity = average_monthly_electricity_bill/electricity_cost_per_kwh

    output_per_panel_month =  (optimal_energy_month 
                               * coefficient 
                               * size 
                               * epsilon)
    
    rec_panel = math.ceil(average_monthly_electricity/ output_per_panel_month)
    total_panel_size = rec_panel * size

    installation_cost = total_panel_size * installation_cost_per_sm
    maintenance_cost_per_year = total_panel_size * maintenance_cost_per_sm_per_year
    maintenance_cost_total = maintenance_cost_per_year * panel_duration
    total_cost = installation_cost + maintenance_cost_total

    savings_month = average_monthly_electricity_bill
    savings_total = savings_month * 12 * panel_duration
    savings_net = savings_total - total_cost
    break_even_month = total_cost/savings_month
    break_even_year = break_even_month/12
    
    return {'panel_coefficient_of_your_chosen_provider':coefficient
           ,'panel_size_of_your_chosen_provider':size
           ,'panel_depreciation_of_your_chosen_provider':depreciation_rate
           ,'input_average_electricity_usage':average_monthly_electricity
           ,'nasa_data_start_year':year_start
           ,'nasa_data_end_year':year_end
           ,'optimal_energy_of_the_chosen_location_month':optimal_energy_month
           ,'depreciation_rate':depreciation_rate
           ,'output_per_panel_per_month':output_per_panel_month
           ,'recommended_panel':rec_panel
           ,'total_panel_size':total_panel_size
           ,'total_installation_cost':installation_cost
           ,'total_maintenance_cost_per_year':maintenance_cost_per_year
           ,'total_maintenance_cost':maintenance_cost_total
           ,'total_cost':total_cost
           ,'total_saving':savings_total
           ,'number_of_years_till_breakeven':break_even_year
           ,'number_of_months_till_breakeven':break_even_month
           }

#panel_recommendation(average_monthly_electricity_bill=100.0
#                     ,panel_duration=25
#                     ,year_start=1990
#                     ,year_end=2020
#                     ,depreciation_rate=0.005
#                    )           