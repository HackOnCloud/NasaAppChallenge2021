const API_URL =
  'https://5j689hu1a9.execute-api.ap-southeast-1.amazonaws.com/default/nasa_monthly_climatology_point_optimal_object';

export async function fetchData(postData: PostData): Promise<Data> {
  try {
    const res = await fetch(API_URL, {
      method: 'post',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
    });

    const data = await res.json();
    const { config, recommends, lat, lng } = data;
    return {
      lat,
      lng,
      config,
      recommends: JSON.parse(recommends),
    };
  } catch (e) {
    return;
  }
}

interface Data {
  config: Config;
  recommends: Recommend[];
  lat: number;
  lng: number;
}

interface Config {
  breakEven: number;
  breakEvenInYear: number;
  cost: number;
  maintenance: number;
  outputPerPanelPerMonth: number;
  recommendedPanelPerMonth: number;
  totalPanelSize: number;
  totalSaving: number;
}

interface Recommend {
  angle: number;
  orientation: string;
  month: string;
}

export interface PostData {
  lat: number;
  lng: number;
  provider: string;
  monthlybill: number;
  duration: number;
}
