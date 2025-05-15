# CoinTracker

CoinTracker is a cryptocurrency tracking application that allows users to monitor the prices of popular cryptocurrencies and visualize their historical data.

## Features
- Track real-time prices of 20 popular cryptocurrencies.
- Visualize historical price data with interactive graphs.
- Set price alerts for specific cryptocurrencies.
- User-friendly GUI built with Tkinter.

## Prerequisites
- Python 3.13 or higher
- MongoDB installed and running locally

## Setup Instructions

### 1. Clone the Repository
```bash
# Clone the repository from GitHub
git clone https://github.com/Thridioux/CoinTracker.git
cd CoinTracker
```

### 2. Create and Activate a Virtual Environment
```bash
# Create a virtual environment
python3 -m venv CoinTracker

# Activate the virtual environment
source CoinTracker/bin/activate  # On macOS/Linux
CoinTracker\Scripts\activate   # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start MongoDB
Ensure MongoDB is running locally. You can start it with:
```bash
mongod
```

### 5. Run the Application
```bash
python main.py
```

## Usage Manual

### Main Features
1. **Dashboard**:
   - View the current price of selected cryptocurrencies.
   - Visualize historical price data for different time ranges (1 hour, 24 hours, 1 month, etc.).

2. **Price Alerts**:
   - Set alerts for specific price thresholds (above or below a certain value).
   - Receive notifications when the price crosses the set threshold.

3. **Auto-Refresh**:
   - Enable or disable auto-refresh to update prices and graphs periodically.

### Navigation
- Use the dropdown menu to select a cryptocurrency.
- Use the time range buttons to filter historical data.
- Set price alerts using the "Price Alerts" section.

## Contributing
Feel free to fork the repository and submit pull requests. Contributions are welcome!

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or issues, please contact [Thridioux](https://github.com/Thridioux).
