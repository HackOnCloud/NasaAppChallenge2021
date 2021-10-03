import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import styles from '../../styles/Home.module.css';
import { API_KEY, FORM_STEP, TITLE, COUNTRIES, SOLAR_PANEL_PROVIDERS, PANEL_PROVIDER } from '../../utils/constants';
import {
  Button,
  Box,
  CardMedia,
  CardContent,
  TextField,
  Grid,
  Paper,
  InputAdornment,
  Typography,
  InputLabel,
  Select,
  MenuItem,
  FormControl,
  Container,
  FormHelperText,
} from '@mui/material';
import type { TextFieldProps } from '@mui/material';
import { loadAsyncScript } from '../../utils/load-script';
import style from '../../styles/Home.module.css';
import { PrimaryHeader } from '../../components/header';
import { GeographicCoordinate } from '../../utils/interface';


interface Props {
  country?: string;
  address?: string;
  coordinate?: GeographicCoordinate;
  averageBill?: string;
  provider?: string;
  duration?: string;
}

interface EvenProps {
  setCountry: (value) => void;
  setAddress: (value) => void;
  setProvider: (value) => void;
  setDuration: (value) => void;
  setAverageBill: (value) => void;
  setCoordinate: (value: GeographicCoordinate) => void;
  setStep: (step) => void;
}

const Form = (props: Props & EvenProps) => {
  const {
    country, setCountry,
    address, setAddress,
    provider, setProvider,
    averageBill, setAverageBill,
    duration, setDuration,
    coordinate, setCoordinate,
  } = props;

  const [autoComplete, setAutoComplete] = useState(null);
  const addressId = 'address';
  const monthlyBillId = 'monthlyBill';
  const solarPanelDurationId = 'solarPanelDuration';

  const inputProps: TextFieldProps = {
    required: true,
    fullWidth: true,
    variant: 'outlined',
    size: 'small',
  };

  const initGoogleMapPlaceAutocomplete = () => {
    const input = document.getElementById(addressId) as HTMLInputElement;

    const options = {
      fields: ['formatted_address', 'geometry', 'name'],
      strictBounds: false,
      types: ['establishment'],
    };

    if (country) {
      options['componentRestrictions'] = {
        country,
      }
    }

    const autocomplete = new google.maps.places.Autocomplete(input, options);
    setAutoComplete(autocomplete);
    autocomplete.setComponentRestrictions

    autocomplete.addListener('place_changed', () => {
      const {
        geometry: {
          location: { lat, lng },
        },
        name,
        formatted_address,
      } = autocomplete.getPlace();
      console.log(autocomplete.getPlace())
      setAddress(`${name} - ${formatted_address}`);
      setCoordinate({ lat: lat(), lng: lng() });
    });
  }

  useEffect(() => {
    if (!window.google) {
      loadAsyncScript(`https://maps.googleapis.com/maps/api/js?key=${API_KEY}&libraries=places`, () => {
        initGoogleMapPlaceAutocomplete();
      });
    } else {
      initGoogleMapPlaceAutocomplete();
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const theme = useTheme();
  const isAboveSm = useMediaQuery(theme.breakpoints.up('sm'));

  const handleChangeCountry = (e) => {
    setCountry(e.target.value);
    let options = null;

    if (e.target.value) {
      options = {
        country: e.target.value,
      };
    }

    autoComplete.setComponentRestrictions(options);
  };

  const handleChangeRetailer = (e) => {
    setProvider(e.target.value);
  };

  const handleChangeAvgBill = (e) => {
    setAverageBill(e.target.value);
  }

  const handleChangeAddress = (e) => {
    setAddress(e.target.value);
  }

  const handleChangeDuration = (e) => {
    setDuration(e.target.value);
  }

  const handleSubmit = () => {
    const { setStep } = props;
    const monthlybill = (document.getElementById(monthlyBillId) as HTMLInputElement).value;
    const panelDuration = (document.getElementById(solarPanelDurationId) as HTMLInputElement).value;
    const paramsObj: Record<string, string> = {};

    if (provider) {
      paramsObj.provider = provider;
    }

    if (monthlybill) {
      paramsObj.monthlybill = monthlybill;
    }

    if (panelDuration) {
      paramsObj.panelduration = panelDuration;
    }

    if (coordinate.lat && coordinate.lng) {
      paramsObj.lat = coordinate.lat.toString();
      paramsObj.lng = coordinate.lng.toString();
    }

    const searchParams = new URLSearchParams(paramsObj);

    console.log(searchParams.toString());
    setStep(FORM_STEP.SECOND);
  };

  const detailRetailer = PANEL_PROVIDER[provider];

  return (
    <>
      <PrimaryHeader />
      <Box className={styles.container} sx={{ my: 4 }}>
        <Head>
          <title>{TITLE}</title>
          <meta name="description" content={TITLE} />
          <meta name="viewport" content="width=device-width" />
          <link rel="icon" href="/favicon.ico" />
        </Head>

        <Container maxWidth="md" component="main">
          <Paper elevation={0}>
            <Box sx={{ border: 1, borderRadius: 1, borderColor: '#dadce0' }}>
              <Grid container spacing={2}>
                <Grid item xs={isAboveSm ? 6 : 12} sx={{ my: isAboveSm ? 4 : 0 }}>
                  {!isAboveSm && (
                    <Box>
                      <CardMedia component="img" className={style.img} image="/images/solar-3.jpeg" alt={TITLE} />
                    </Box>
                  )}

                  <Box sx={{ px: 2, pt: 2 }}>
                    <Typography variant="h6" component="h6">
                      We will need to know a bit more about you so that you can
                    </Typography>

                    <Typography variant="subtitle2" component="p" sx={{ fontStyle: 'italic', fontWeight: 'normal' }}>
                      View sunshine information in your area in the past year
                    </Typography>
                    <Typography variant="subtitle2" component="p" sx={{ fontStyle: 'italic', fontWeight: 'normal' }}>
                      View our recommendations on solar panel installation based on your needs
                    </Typography>
                  </Box>

                  <CardContent>
                    <Box sx={{ mt: 4 }}>
                      <Grid container>
                        <Grid item xs={12}>
                          <FormControl size="small" fullWidth>
                            <InputLabel id="demo-simple-select-autowidth-label">Country</InputLabel>
                            <Select
                              labelId="demo-simple-select-autowidth-label"
                              id="demo-simple-select-autowidth"
                              autoWidth
                              label="Country"
                              value={country}
                              onChange={handleChangeCountry}
                            >
                              <MenuItem value="">
                                <em>None</em>
                              </MenuItem>
                              {COUNTRIES.map((item) => (
                                <MenuItem key={item.code} value={item.code}>
                                  {item.name}
                                </MenuItem>
                              ))}
                            </Select>
                          </FormControl>
                        </Grid>
                      </Grid>
                    </Box>

                    <Box sx={{ mt: 4 }}>
                      <TextField
                        {...inputProps}
                        id={addressId}
                        value={address}
                        onChange={handleChangeAddress}
                        label="Home Address"
                      />
                    </Box>

                    <Box sx={{ mt: 4 }}>
                      <TextField
                        {...inputProps}
                        label="Average Electric Bill"
                        value={averageBill}
                        id={monthlyBillId}
                        type="number"
                        onChange={handleChangeAvgBill}
                        InputProps={{
                          startAdornment: <InputAdornment position="start">$</InputAdornment>,
                          endAdornment: <InputAdornment position="end">/mo</InputAdornment>,
                          inputProps: {
                            min: 0,
                          },
                        }}
                      />
                    </Box>

                    <Box sx={{ mt: 4 }}>
                      <FormControl size="small" fullWidth>
                        <InputLabel id="demo-simple-select-autowidth-label">Solar Panel Provider *</InputLabel>
                        <Select
                          labelId="demo-simple-select-autowidth-label"
                          id="demo-simple-select-autowidth"
                          autoWidth
                          required
                          label="Solar Panel Provider"
                          value={provider}
                          onChange={handleChangeRetailer}
                        >
                          <MenuItem value="">
                            <em>None</em>
                          </MenuItem>
                          {SOLAR_PANEL_PROVIDERS.map((item) => (
                            <MenuItem key={item.code} value={item.code}>
                              {item.name}
                            </MenuItem>
                          ))}
                        </Select>

                        {detailRetailer && (
                          <>
                            <FormHelperText>
                              Installation cost: {detailRetailer.price} / m<sup>2</sup>
                            </FormHelperText>
                            <FormHelperText>
                              Maintenance cost: {detailRetailer.monthlyBill} / m<sup>2</sup>
                            </FormHelperText>
                          </>
                        )}
                      </FormControl>
                    </Box>

                    <Box sx={{ mt: 4 }}>
                      <TextField
                        {...inputProps}
                        label="Solar Panel Duration"
                        id={solarPanelDurationId}
                        type="number"
                        value={duration}
                        onChange={handleChangeDuration}
                        InputProps={{
                          inputProps: {
                            min: 1,
                            max: 25,
                          },
                        }}
                      />
                      <FormHelperText>Year from 1 year to 25 years</FormHelperText>
                    </Box>

                    <Box sx={{ mt: 2 }}>
                      <Button onClick={handleSubmit} fullWidth variant="contained">
                        Next
                      </Button>
                    </Box>
                  </CardContent>
                </Grid>

                {isAboveSm && (
                  <Grid item xs={6} sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <img className={style.img} src="/images/solar-2.jpeg" alt={TITLE} />
                  </Grid>
                )}
              </Grid>
            </Box>
          </Paper>
        </Container>
      </Box>
    </>
  );
};

export { Form };
