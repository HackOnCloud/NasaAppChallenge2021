import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import { SECOND_FORM_NAME } from '../../utils/constants';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

interface Props {
  onClick: (e?) => void;
}

export function SecondaryHeader(props: Props) {
  const { onClick } = props;

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton size="large" edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }} onClick={onClick}>
            <ArrowBackIcon />
          </IconButton>
          <Typography noWrap={true} variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {SECOND_FORM_NAME}
          </Typography>
        </Toolbar>
      </AppBar>
    </Box>
  );
}
