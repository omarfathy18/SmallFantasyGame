# Fantasy League Web App

This project is a web application for managing a fantasy league for football (soccer) fans. It supports two leagues: the Egyptian Premier League and the English Premier League. Users can create accounts, build their own fantasy teams, and track the performance of players and teams throughout the season.

## Features

- **User Authentication**: Register, log in, and manage user accounts.
- **Team Creation**: Build and manage fantasy teams for both leagues.
- **Match Data**: View fixtures, results, and league standings.
- **Dynamic Scoring**: Calculate and display weekly and total points for fantasy teams based on player performances.
- **Admin Controls**:
  - Add or update players, matches, and results.
  - Reset data for new league seasons.
- **Interactive UI**: Separate views for user and admin functionalities.

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML templates rendered by Flask

## Prerequisites

Before running the project, ensure you have the following installed:
- Python 3.x
- MySQL

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/fantasy-league-app.git
   cd fantasy-league-app

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Set up the database:
- Create a MySQL database named fantasy.
- Import the database schema (provided in schema.sql) into the database.

4. Update configuration:
- Open app.py and modify the database connection details in the fantasy.config section:
   ```bash
   fantasy.config['MYSQL_USER'] = 'your-username'
   fantasy.config['MYSQL_PASSWORD'] = 'your-password'
   fantasy.config['MYSQL_HOST'] = 'localhost'

5. Run the app:
   ```bash
   python app.py

6. Access the app in your browser at http://localhost:5000.

## Usage

### User Views

- **Home Page**: Displays league standings and upcoming matches.
- **Team Management**: Build your team and set captains to maximize points.
- **Points Overview**: See your team's weekly and total points.

### Admin Views

- **Control Panel**: Manage player data, match results, and reset league data for new seasons.
- **Player and Match Management**: Add and update data for both leagues.

## Known Issues & Improvements

- Some routes require additional session validation for enhanced security.
- The UI could benefit from responsive design improvements.
- More robust error handling and validation are needed.
- Introduce a limited budget for player purchasing.
- Limit only 3 players from the same club.

## Contributing

Feel free to fork the repository and submit pull requests. Contributions are welcome!
