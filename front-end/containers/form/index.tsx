import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { useTheme } from '@mui/material/styles';
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
import { EMPTY_WARNING_MESSAGE } from '../../utils/constants';

interface Props {
  country?: string;
  address?: string;
  coordinate?: GeographicCoordinate;
  averageBill?: string;
  provider?: string;
  duration?: number;
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
    country,
    setCountry,
    address,
    setAddress,
    provider,
    setProvider,
    averageBill,
    setAverageBill,
    duration,
    setDuration,
    coordinate,
    setCoordinate,
  } = props;

  const [errorAddress, setErrorAddress] = useState(null);
  const [errorAvgBill, setErrorAvgBill] = useState(null);
  const [errorSolarPanelProvider, setErrorSolarPanelProvider] = useState(null);
  const [errorDuration, setErrorDuration] = useState(null);

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
      };
    }

    const autocomplete = new google.maps.places.Autocomplete(input, options);
    setAutoComplete(autocomplete);
    autocomplete.setComponentRestrictions;

    autocomplete.addListener('place_changed', () => {
      const {
        geometry: {
          location: { lat, lng },
        },
        name,
        formatted_address,
      } = autocomplete.getPlace();
      setAddress(`${name} - ${formatted_address}`);
      setCoordinate({ lat: lat(), lng: lng() });
    });
  };

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

  const isDisableSubmitButton = () => {
    return errorAddress || errorAvgBill || errorSolarPanelProvider || errorDuration;
  };

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

  const handleChangeAddress = (e) => {
    setAddress(e.target.value);

    let isInvalid = false;
    if (!e.target.value) {
      isInvalid = true;
    }
    setErrorAddress(isInvalid);
  };

  const handleChangeAvgBill = (e) => {
    setAverageBill(e.target.value);

    let isInvalid = false;
    if (!e.target.value) {
      isInvalid = true;
    }
    setErrorAvgBill(isInvalid);
  };

  const handleChangeProvider = (e) => {
    setProvider(e.target.value);

    let isInvalid = false;
    if (!e.target.value) {
      isInvalid = true;
    }
    setErrorSolarPanelProvider(isInvalid);
  };

  const handleChangeDuration = (e) => {
    setDuration(e.target.value);

    let isInvalid = false;
    if (!e.target.value) {
      isInvalid = true;
    }
    setErrorDuration(isInvalid);
  };

  const handleSubmit = () => {
    let isInvalid = false;
    if (!address) {
      isInvalid = true;
      setErrorAddress(true);
    }

    if (!averageBill) {
      isInvalid = true;
      setErrorAvgBill(true);
    }

    if (!provider) {
      isInvalid = true;
      setErrorSolarPanelProvider(true);
    }

    if (!duration) {
      isInvalid = true;
      setErrorDuration(true);
    }

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

    !isInvalid && setStep(FORM_STEP.SECOND);
  };

  const detailRetailer = PANEL_PROVIDER[provider];

  return (
    <>
      <PrimaryHeader />
      <Box sx={{ my: 4 }}>
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
                <Grid item xs={12} sx={{ my: 0 }}>
                  <Box>
                    <CardMedia component="img" className={style.img} image="/images/solar-3.jpeg" alt={TITLE} />
                  </Box>

                  <Box sx={{ px: 2, pt: 2 }}>
                    <Typography variant="h6" component="h6">
                      A bit more about you
                    </Typography>

                    <Typography variant="subtitle2" component="p" sx={{ fontStyle: 'italic', fontWeight: 'normal' }}>
                      1. You can view sunshine information in your location in the past year
                    </Typography>
                    <Typography variant="subtitle2" component="p" sx={{ fontStyle: 'italic', fontWeight: 'normal' }}>
                      2. You can view our recommendations on solar panel installation based on your needs
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
                        error={errorAddress}
                        id={addressId}
                        value={address}
                        onChange={handleChangeAddress}
                        label="Home Address"
                      />
                      {errorAddress && <FormHelperText error>{EMPTY_WARNING_MESSAGE}</FormHelperText>}
                    </Box>

                    <Box sx={{ mt: 4 }}>
                      <TextField
                        {...inputProps}
                        error={errorAvgBill}
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
                      {errorAvgBill && <FormHelperText error>{EMPTY_WARNING_MESSAGE}</FormHelperText>}
                    </Box>

                    <Box sx={{ mt: 4 }}>
                      <FormControl size="small" fullWidth>
                        <InputLabel id="demo-simple-select-autowidth-label">Solar Panel Provider *</InputLabel>
                        <Select
                          labelId="demo-simple-select-autowidth-label"
                          id="demo-simple-select-autowidth"
                          error={errorSolarPanelProvider}
                          autoWidth
                          required
                          label="Solar Panel Provider"
                          value={provider}
                          onChange={handleChangeProvider}
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
                      </FormControl>
                      <FormHelperText>Select your preferred providers in your country</FormHelperText>
                      {errorSolarPanelProvider && <FormHelperText error>{EMPTY_WARNING_MESSAGE}</FormHelperText>}

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
                    </Box>

                    <Box sx={{ mt: 4 }}>
                      <TextField
                        {...inputProps}
                        label="Duration of solar panel"
                        id={solarPanelDurationId}
                        type="number"
                        error={errorDuration}
                        value={duration}
                        onChange={handleChangeDuration}
                        InputProps={{
                          inputProps: {
                            min: 1,
                            max: 25,
                          },
                          endAdornment: <InputAdornment position="end">year(s)</InputAdornment>,
                        }}
                      />
                      <FormHelperText>Ranging on average from 10 - 25 years.</FormHelperText>
                      {errorDuration && <FormHelperText error>{EMPTY_WARNING_MESSAGE}</FormHelperText>}
                    </Box>

                    <Box sx={{ mt: 2 }}>
                      <Button disabled={isDisableSubmitButton()} onClick={handleSubmit} fullWidth variant="contained">
                        Next
                      </Button>
                    </Box>
                  </CardContent>
                </Grid>
              </Grid>
            </Box>
          </Paper>
        </Container>
      </Box>
    </>
  );
};

export { Form };
