export const API_KEY = 'AIzaSyABoVT1jKGPYpqaCxNOc7UvfTHQgKM0GtA';

export const TITLE = 'You are my sunshine';

export const EMPTY_WARNING_MESSAGE = 'This field cannot be empty';

export const MAIN_COLOR = '#556cd6';

export const TEAM_NAME = 'HackOnCloud';

export const SECOND_FORM_NAME = 'Sunshine Visualisation and Solar Panel Recommendation';

export const COUNTRIES: Data[] = [{ name: 'Singapore', code: 'SG' }];

export const FORM_STEP = {
  FIRST: 1,
  SECOND: 2,
};

export const CONTACT_LINK =
  'https://2021.spaceappschallenge.org/challenges/statements/you-are-my-sunshine/teams/hack-on-cloud/members';

export const SOLAR_PANEL_PROVIDERS: Data[] = [{ name: 'Sembcorp', code: 'sembcorp' }];

export const PANEL_PROVIDER = {
  sembcorp: {
    price: '$450',
    monthlyBill: '$4',
  },
};

interface Data {
  name: string;
  code: string;
}
