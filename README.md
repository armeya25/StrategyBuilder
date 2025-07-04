first install tk/tcl for your respective system.
# StrategyBuilder

A powerful tool for developing, testing, and analyzing trading strategies using Python and Polars.

## Features

- 📊 Strategy Development
  - Create custom trading strategies using technical indicators
  - Flexible signal generation system

- 🔄 To Do
- Performance Analysis
- Strategy Optimization
- Backtesting
- Performance Metrics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/StrategyBuilder.git
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

just run main.py
- select indicator library (currently only ta-lib and custom libs are supported)
- add indicators (click add button) 
- after don selecting indicators click next button
- [optional] if you want to add shift, rolling mean, etc then select on "special case windows" option and dont forgate to add 
- if dont want anything click next button
- on "create strategy window" select what do you want to do
- you can add multiple conditions there
- click finalise button to get strategy build



## Data Requirements
in csv format
The tool expects your data to have at least these columns:
- `date`: Date of the data point
- `open`: Opening price
- `high`: Highest price
- `low`: Lowest price
- `close`: Closing price
- `volume`: Trading volume (optional)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

- Thanks to the Polars team for their amazing DataFrame library
- Special thanks to the open-source community for all the tools and libraries used in this project
