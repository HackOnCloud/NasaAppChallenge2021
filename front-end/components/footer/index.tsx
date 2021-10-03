import { Divider, Box } from '@mui/material';

export function Footer() {
  const year = new Date().getFullYear();
  return (
    <>
      <Box sx={{ px: 4 }}>
        <Divider />
      </Box>

      <Box component="footer" sx={{ p: 4, textAlign: 'center' }}>
        © {year} HackOnCloud team. All rights reserved.
      </Box>
    </>
  );
}
