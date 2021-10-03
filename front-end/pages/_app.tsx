import * as React from 'react';
import Head from 'next/head';
import { AppProps } from 'next/app';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { CacheProvider, EmotionCache } from '@emotion/react';
import { theme } from '../theme';
import { createEmotionCache } from '../utils/create-emotion-cache';
import { Footer } from '../components/footer';
import { TITLE, MAIN_COLOR } from '../utils/constants'

// Client-side cache, shared for the whole session of the user in the browser.
const clientSideEmotionCache = createEmotionCache();

interface MyAppProps extends AppProps {
  emotionCache?: EmotionCache;
}

export default function MyApp(props: MyAppProps) {
  const { Component, emotionCache = clientSideEmotionCache, pageProps } = props;
  return (
    <CacheProvider value={emotionCache}>
      <Head>
        <title>My page</title>
        {renderPWAMetaLinks()}
        <meta name="viewport" content="initial-scale=1, width=device-width" />
      </Head>
      <ThemeProvider theme={theme}>
        {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
        <CssBaseline />

        <Component {...pageProps} />

        <Footer />
      </ThemeProvider>
    </CacheProvider>
  );
}

function renderPWAMetaLinks() {
  return (
    <>
      <meta name="application-name" content={TITLE} />
      <meta name="apple-mobile-web-app-capable" content="yes" />
      <meta name="apple-mobile-web-app-status-bar-style" content="default" />
      <meta name="apple-mobile-web-app-title" content={TITLE} />
      <meta name="format-detection" content="telephone=no" />
      <meta name="mobile-web-app-capable" content="yes" />
      <meta name="msapplication-TileColor" content={MAIN_COLOR} />
      <meta name="msapplication-tap-highlight" content="no" />
      <meta name="theme-color" content={MAIN_COLOR} />

      <link rel="apple-touch-icon" sizes="192x192" href="/logo/192x192.png" />
      <link rel="icon" type="image/png" sizes="32x32" href="/logo/32x32.png" />
      <link rel="icon" type="image/png" sizes="16x16" href="/logo/16x16.png" />
      <link rel="mask-icon" href="/logo/192x192.png" color="#3a3a33" />
      <link rel="manifest" href="/manifest.json" />
    </>
  );
}
