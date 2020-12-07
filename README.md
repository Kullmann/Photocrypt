# RSAPhotoCryptography
The purpose of this project is to encrypt and decrypt photos using the RSA algorithm.

## Installation

To install photocrypt package simply run following command on root directory:

```pip3 install .```

## Running

### Run GUI Application

from the root directory, run following command:

```python3 bin```

### Run CUI Application

from the root directory, run following command:

```python3 bin [-h] [-i image path] [-k key path] [--encrypt] [--decrypt]```

#### arguments:

  **-h**, **--help**            show this help message and exit

  **-i** **[image path]**  image file path to encrypt/decrypt

  **-k** **[key path]**       public key path    

  **--encrypt**                 encrypt given image using provided key

  **--decrypt**                 decrypt given image using provided key

#### example usage:

```python3 bin -i samples/tuatara.jpg -k public.pem --encrypt```

```python3 bin -i samples/tuatara_enc -k private.pem --decrypt```

## Testing

test scripts are available in tests/ directory.

Run following command to run tests.
```python3 tests/<test name>.py```

## Requirements

photocrypt package requires python3.6 or above.

## Known Bugs

- Double encryption is not supported because crypto header is overwritten on encryption.

## Contributors

Hosung Lee

Sean Kullmann
