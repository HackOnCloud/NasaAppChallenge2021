import { NextPage } from 'next';
import { useEffect, useState, useRef } from 'react';
import { Form } from '../containers/form';
import { Report } from '../containers/report';

const Home: NextPage = () => {
  const [step, setStep] = useState(1);

  const handleGotoStep = (step) => {
    setStep(step);
  };

  return (
    <>
      {step === 1 && <Form setStep={handleGotoStep} />}
      {step === 2 && <Report setStep={handleGotoStep} />}
    </>
  );
};

export default Home;
