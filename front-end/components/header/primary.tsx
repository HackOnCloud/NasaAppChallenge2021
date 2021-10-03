import React, { useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import { TEAM_NAME, CONTACT_LINK } from '../../utils/constants';
import { Drawer, Divider, List, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import ContactsIcon from '@mui/icons-material/Contacts';

export function PrimaryHeader() {
  const [openDrawer, setOpenDrawer] = useState(false);

  const toggleDrawer = (val) => {
    return () => {
      setOpenDrawer(val);
    };
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={toggleDrawer(true)}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {TEAM_NAME}
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer anchor={'left'} open={openDrawer} onClose={toggleDrawer(false)}>
        <Box sx={{ width: 250 }} role="presentation">
          <Toolbar sx={{ mt: 1 }}>
            <Box sx={{ mr: 1 }}>
              <img width={50} height={50} src="/logo/192x192.png" alt="HackOnCloud" />
            </Box>
            <Typography variant="h6" component="h6">
              {TEAM_NAME}
            </Typography>
          </Toolbar>
          <Divider />
          <List>
            <ListItemButton component="a" href="/">
              <ListItemIcon>
                <HomeIcon />
              </ListItemIcon>
              <ListItemText primary={'Home'} />
            </ListItemButton>

            <ListItemButton component="a" href={CONTACT_LINK}>
              <ListItemIcon>
                <ContactsIcon />
              </ListItemIcon>
              <ListItemText primary={'About us'} />
            </ListItemButton>
          </List>
        </Box>
      </Drawer>
    </Box>
  );
}
