import { NextPage } from 'next';
import { useState } from 'react';
import { Form } from '../containers/form';
import { Report } from '../containers/report';
import { GeographicCoordinate } from '../utils/interface';

const Home: NextPage = () => {
  const [step, setStep] = useState(1);
  const [country, setCountry] = useState('');
  const [provider, setProvider] = useState('');
  const [averageBill, setAverageBill] = useState('');
  const [duration, setDuration] = useState(1);
  const [address, setAddress] = useState('');
  const [coordinate, setCoordinate] = useState<GeographicCoordinate>({});

  const handleGotoStep = (step) => setStep(step);

  return (
    <>
      {step === 1 && (
        <Form
          country={country}
          address={address}
          provider={provider}
          averageBill={averageBill}
          duration={duration}
          coordinate={coordinate}
          setStep={handleGotoStep}
          setCountry={setCountry}
          setAddress={setAddress}
          setProvider={setProvider}
          setAverageBill={setAverageBill}
          setDuration={setDuration}
          setCoordinate={setCoordinate}
        />
      )}

      {step === 2 && (
        <Report
          address={address}
          provider={provider}
          averageBill={averageBill}
          duration={duration}
          coordinate={coordinate}
          setStep={handleGotoStep}
        />
      )}
    </>
  );
};

export default Home;
