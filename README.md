# EEE3097S Project

## Usage
### Run
Batches data from a `DataSource` object at a regular interval and outputs the compressed and encrypted data to the `/batches` directory.
```
make run
```

### Reverse
Decrypts and decompresses all files in the `/batches` directory and outputs CSV files to `/batches/output`.
```
make reverse
```