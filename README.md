## Installation

Create a virtual environment
```bash
python3 -m venv ~/.venv
```

Activate the virtual environment
```bash
source ~/.venv/bin/activate
```
Install the requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.
```bash
pip install -r requirements.txt
```

## Configuration

Create a config.ini file with

- A 'clashofclans' section
- Your api_token variable which is your developer api from https://developer.clashofclans.com/#/account
- The desired clan_id without the # character in the variable

## Usage

Run the Flask App

```bash
flask run
```