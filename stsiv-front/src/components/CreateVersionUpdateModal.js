import React, { useState } from 'react';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import OutlinedInput from '@mui/material/OutlinedInput';
import Chip from '@mui/material/Chip';
import CircularProgress from '@mui/material/CircularProgress';

const testsOptions = [
  { id: 0, name: "Run all tests (1-15)" },
  { id: 1, name: "Frequency" },
  { id: 2, name: "Block Frequency"},
  { id: 3, name: "Cumulative Sums"},
  { id: 4, name: "Runs"},
  { id: 5, name: "Longest Run of Ones"},
  { id: 6, name: "Rank"},
  { id: 7, name: "Discrete Fourier Transform"},
  { id: 8, name: "Nonperiodic Template Matchings"},
  { id: 9, name: "Overlapping Template Matchings"},
  { id: 10, name: "Universal Statistical"},
  { id: 11, name: "Approximate Entropy"},
  { id: 12, name: "Random Excursions"},
  { id: 13, name: "Random Excursions Variant"},
  { id: 14, name: "Serial"},
  { id: 15, name: "Linear Complexity" },
];

export default function CreateVersionUpdateModal({ isOpen, toggle, onUpdate }) {
  const [file, setFile] = useState(null);
  const [selectedTests, setSelectedTests] = useState([]);
  const [testParams, setTestParams] = useState({
    blockFrequencyTestBlockLength: { id: "1", value: 16384 },
    nonOverlappingTemplateTestBlockLength: { id: "2", value: 9 },
    overlappingTemplateTestBlockLength: { id: "3", value: 9 },
    approximateEntropyTestBlockLength: { id: "4", value: 10 },
    serialTestBlockLength: { id: "5", value: 16 },
    linearComplexityTestBlockLength: { id: "6", value: 500 },
    numberOfBitcountRuns: { id: "7", value: 1 },
    uniformityBins: { id: "8", value: 18.12 },
    bitsToProcessPerIteration: { id: "9", value: 1048576 },    
  });
  const [iterations, setIterations] = useState(1000);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleTestsChange = (event) => {
    const value = event.target.value;
    // Check if "Run all tests" is selected
    if (value.includes(0) && selectedTests.length === 0) {
      // If "Run all tests" is newly selected and no other test is currently selected
      setSelectedTests([0]);
    } else if (value.includes(0) && selectedTests.length > 0) {
      // If "Run all tests" is selected and there are other tests selected
      setSelectedTests(value.filter(test => test === 0));
    } else {
      // If "Run all tests" is not selected
      setSelectedTests(value.filter(test => test !== 0));
    }
  };

  const handleParamValueChange = (paramName, newValue) => {
    setTestParams(prevParams => ({
      ...prevParams,
      [paramName]: { ...prevParams[paramName], value: newValue }
    }));
  };


  const handleSubmit = () => {
    const params = {
      tests: {
        alias: "-t",
        value: selectedTests
      },
      parameters: {
        alias: "-P",
        ...testParams,
        "uniformityCutoffLevel": {
          "id": "10",
          "value": 0.0001
        },
        "alphaConfidenceLevel": {
            "id": "11",
            "value": 0.01
        }
      },
      "iterations": {
        "alias": "-i",
        "value": iterations
      },
      "workDir": {
        "alias": "-w",
        "value": "."
      },
      "createResultFiles": {
          "alias": "-s",
          "value": ""
      },
      "bitcount": {
          "alias": "-S",
          "value": 1048576
      },
      "numOfThreads": {
          "alias": "-T",
          "value": 4
      }
    };
    onUpdate(params, file);
    toggle(); // Close modal after submission
  };

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
          <FormControl fullWidth>
            <InputLabel id="select-tests-label">Select Tests</InputLabel>
            <Select
              labelId="select-tests-label"
              multiple
              value={selectedTests}
              onChange={handleTestsChange}
              input={<OutlinedInput id="select-multiple-chip" label="Select Tests" />}
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {selected.map((value) => (
                    <Chip key={value} label={testsOptions.find(test => test.id === value).name} />
                  ))}
                </Box>
              )}
            >
              {testsOptions.map((test) => (
                <MenuItem key={test.id} value={test.id}>
                  {test.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField
              margin="normal"
              fullWidth
              type="number"
              label="Block Frequency Test Block Length"
              value={testParams.blockFrequencyTestBlockLength.value}
              onChange={(e) => handleParamValueChange('blockFrequencyTestBlockLength', e.target.value)}
            />

          <TextField
              margin="normal"
              fullWidth
              type="number"
              label="Non Overlapping Test Block Length"
              value={testParams.nonOverlappingTemplateTestBlockLength.value}
              onChange={(e) => handleParamValueChange('nonOverlappingTemplateTestBlockLength', e.target.value)}
            />

          <TextField
              margin="normal"
              fullWidth
              type="number"
              label="Overlapping Test Block Length"
              value={testParams.overlappingTemplateTestBlockLength.value}
              onChange={(e) => handleParamValueChange('overlappingTemplateTestBlockLength', e.target.value)}
            />

          <TextField
              margin="normal"
              fullWidth
              type="number"
              label="Approximate Entropy Test Block Length"
              value={testParams.approximateEntropyTestBlockLength.value}
              onChange={(e) => handleParamValueChange('approximateEntropyTestBlockLength', e.target.value)}
            />

          <TextField
              margin="normal"
              fullWidth
              type="number"
              label="Serial Test Block Length"
              value={testParams.serialTestBlockLength.value}
              onChange={(e) => handleParamValueChange('serialTestBlockLength', e.target.value)}
            />

          <TextField
              margin="normal"
              fullWidth
              type="number"
              label="Linear Complexity Test Block Length"
              value={testParams.linearComplexityTestBlockLength.value}
              onChange={(e) => handleParamValueChange('linearComplexityTestBlockLength', e.target.value)}
            />

          <TextField
              margin="normal"
              fullWidth
              type="number"
              label="Iterations"
              value={iterations}
              onChange={(e) => setIterations(Number(e.target.value))}
            />

          <TextField
              margin="normal"
              fullWidth
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
            />
          {/* ... other fields ... */}
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
            disabled={isSubmitting}
          >
            Cancel
          </Button>
        </Box>
      </Box>
    </Modal>
  </div>
);
}