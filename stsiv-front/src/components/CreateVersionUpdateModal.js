import React, { useState } from 'react';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

export default function CreateVersionUpdateModal({ isOpen, toggle, onUpdate }) {
  const [file, setFile] = useState(null);
  // State for each parameter
  const [parameterValues, setParameterValues] = useState({
    // Initialize with default values or empty
  });

  const handleParamChange = (paramName, value) => {
    setParameterValues(prevParams => ({ ...prevParams, [paramName]: value }));
  };

  const handleSubmit = () => {
    onUpdate(parameterValues, file);
    toggle(); // Close modal after submission
  };

  return (
    <div>
      <Modal
        open={isOpen}
        onClose={toggle}
        aria-labelledby="create-version-update-modal-title"
        aria-describedby="create-version-update-modal-description"
      >
        <Box sx={style}>
          <Typography id="create-version-update-modal-title" variant="h6" component="h2">
            Update Version
          </Typography>
          <Box component="form" noValidate sx={{ mt: 1 }}>
            {/* TextFields for each parameter */}
            {/* Example for one parameter */}
            <TextField
              margin="normal"
              fullWidth
              label="Parameter Name"
              value={parameterValues.parameterName}
              onChange={(e) => handleParamChange('parameterName', e.target.value)}
            />
            {/* File Input */}
            <TextField
              margin="normal"
              fullWidth
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
            />
            <Button
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              onClick={handleSubmit}
            >
              Update
            </Button>
            <Button
              fullWidth
              variant="outlined"
              sx={{ mt: 1, mb: 2 }}
              onClick={toggle}
            >
              Cancel
            </Button>
          </Box>
        </Box>
      </Modal>
    </div>
  );
}
