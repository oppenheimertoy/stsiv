import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import TextField from '@mui/material/TextField';

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

export default function CreateVersionModal({ isOpen, toggle, onCreate }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = () => {
    onCreate(name, description);
    toggle(); // Close modal after creation
  };

  return (
    <div>
      <Modal
        open={isOpen}
        onClose={toggle}
        aria-labelledby="create-version-modal-title"
        aria-describedby="create-version-modal-description"
      >
        <Box sx={style}>
          <Typography id="create-version-modal-title" variant="h6" component="h2">
            Create New Version
          </Typography>
          <Box component="form" noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="versionName"
              label="Version Name"
              name="versionName"
              autoFocus
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="versionDescription"
              label="Description"
              id="versionDescription"
              multiline
              rows={4}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
            {/* You can add more fields here such as file upload or parameters */}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              onClick={handleSubmit}
            >
              Create
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
