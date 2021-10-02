export const API_KEY = '';

export const TITLE = 'You are my sunshine';

export const TEAM_NAME = 'HackOnCloud';

export const COUNTRIES: Data[] = [
  { name: 'Singapore', code: 'SG' },
];

export const CONTACT_LINK = 'https://2021.spaceappschallenge.org/challenges/statements/you-are-my-sunshine/teams/hack-on-cloud/members';

export const SOLAR_PANEL_PROVIDERS: Data[] = [{ name: 'Sembcorp', code: 'sembcorp' }];

export const PANEL_PROVIDER = {
  sembcorp: {
    price: '$0.1805',
    monthlyBill: '$64.98',
  },
};

export const recommends = [
  {
    month: 'Jan',
    angle: '5',
    orientation: 'North',
    saving: '$100'
  },
  {
    month: 'Feb',
    angle: '5',
    orientation: 'North',
    saving: '$100'
  },
  {
    month: 'Mar',
    angle: '5',
    orientation: 'South',
    saving: '$100'
  },
  {
    month: 'Apr',
    angle: '5',
    orientation: 'North',
    saving: '$100'
  },
  {
    month: 'May',
    angle: '5',
    orientation: 'North',
    saving: '$100'
  },
  {
    month: 'Jun',
    angle: '5',
    orientation: 'North',
    saving: '$100'
  },
  {
    month: 'Jul',
    angle: '5',
    orientation: 'South',
    saving: '$200'
  },
  {
    month: 'Aug',
    angle: '5',
    orientation: 'South',
    saving: '$200'
  },
  {
    month: 'Sep',
    angle: '5',
    orientation: 'South',
    saving: '$200'
  },
  {
    month: 'Oct',
    angle: '5',
    orientation: 'South',
    saving: '$200'
  },
  {
    month: 'Nov',
    angle: '5',
    orientation: 'South',
    saving: '$200'
  },
  {
    month: 'Dec',
    angle: '5',
    orientation: 'South',
    saving: '$200'
  },
];

interface Data {
  name: string;
  code: string;
}
