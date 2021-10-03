import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

interface Props {
  open: boolean;
}

interface EventProps {
  setOpen: (value) => void;
}

export function AlertDialog(props: Props & EventProps) {
  const { open, setOpen } = props;

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle id="alert-dialog-title">
        RECOMMENDED ANGLE SETUP
      </DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          For example, If you see 5 in Angle & North in Orientation, you should adjust the panel such that it is 5 degree titled, and that the surface of the panel pointed towards the North
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} autoFocus>
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
}