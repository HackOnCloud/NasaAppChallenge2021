import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';
import styles from '../../styles/Home.module.css';
import { API_KEY, TITLE } from '../../utils/constants';
import { COUNTRIES, SOLAR_PANEL_PROVIDERS, PANEL_PROVIDER } from '../../utils/constants';
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
import { Header } from '../../components/header';

interface GeographicCoordinate {
  lng?: number;
  lat?: number;
}

interface Props {
  setStep: (step) => void;
}

const Form = (props: Props) => {
  const [autoComplete, setAutoComplete] = useState(null);
  const [country, setCountry] = useState('');
  const [provider, setProvider] = useState('');
  const [coordinate, setCoordinate] = useState<GeographicCoordinate>({});

  const addressId = 'address';
  const monthlyBillId = 'monthlyBill';
  const solarPanelDurationId = 'solarPanelDuration';

  const inputProps: TextFieldProps = {
    required: true,
    fullWidth: true,
    variant: 'outlined',
    size: 'small',
  };

  useEffect(() => {
    loadAsyncScript(`https://maps.googleapis.com/maps/api/js?key=${API_KEY}&libraries=places`, () => {
      if (window.google) {
        const input = document.getElementById(addressId) as HTMLInputElement;

        const options = {
          fields: ['formatted_address', 'geometry', 'name'],
          strictBounds: false,
          types: ['establishment'],
        };
        const autocomplete = new google.maps.places.Autocomplete(input, options);
        setAutoComplete(autocomplete);

        autocomplete.addListener('place_changed', () => {
          const {
            geometry: {
              location: { lat, lng },
            },
          } = autocomplete.getPlace();
          console.log('asdasd', {
            lat: lat(),
            lng: lng(),
          });

          setCoordinate({
            lat: lat(),
            lng: lng(),
          });
        });
      }
    });
  }, []);

  const theme = useTheme();
  const isAboveSm = useMediaQuery(theme.breakpoints.up('sm'));

  const handleChangeCountry = (e) => {
    setCountry(e.target.value);
    const restrictions = {
      country: e.target.value,
    };

    autoComplete.setComponentRestrictions(restrictions);
  };

  const handleChangeRetailer = (e) => {
    setProvider(e.target.value);
  };

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
    setStep(2);
  };

  const detailRetailer = PANEL_PROVIDER[provider];

  return (
    <>
      <Header />
      <div className={styles.container}>
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
                      Enter information
                    </Typography>

                    <Typography variant="subtitle2" component="p" sx={{ fontStyle: 'italic', fontWeight: 'normal' }}>
                      to estimate your solar plan
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
                      <TextField id={addressId} {...inputProps} label="Home Address" />
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
                        label="Average Electric Bill"
                        id={monthlyBillId}
                        type="number"
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
                      <TextField
                        {...inputProps}
                        label="Solar Panel Duration"
                        id={solarPanelDurationId}
                        type="number"
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
      </div>
    </>
  );
};

export { Form };