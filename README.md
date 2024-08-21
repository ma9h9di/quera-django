# Simple Wallet System

## Overview
This project is a basic implementation of a digital wallet system built using the Django web framework. It allows users to store, send, and receive money electronically, functioning as a virtual wallet. This project is designed for beginner developers who want to learn the basics of Django by building a practical application.

## Features
- **User Registration & Authentication:** Users can create accounts, log in, and log out securely.
- **Wallet Management:** Users can manage their wallet, add money, view their balance, and see transaction history.
- **Send Money:** Users can transfer money to other registered users within the system.
- **Receive Money:** Users can receive money from other users directly into their digital wallet.
- **Transaction History:** Users can view a history of all transactions (both sent and received).

## Installation

### Prerequisites
- Docker & Docker Compose
- Python 3.x
- Django 5.x
- A virtual environment (recommended)

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ma9h9di/quera-django
   cd quera-django
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r pip/requirements.txt
   ```

4. **Run Docker Compose**
   Start the PostgreSQL database and pgAdmin using Docker Compose.
   ```bash
   cd deploy
   docker-compose up -d
   ```

5. **Connect to pgAdmin**
   - Open your web browser and navigate to `http://localhost:5050`.
   - Use the credentials provided in the `docker-compose.yml` file to log in:
     - **Email:** `mahdikhazayi75@gmail.com`
     - **Password:** `bazaarpay`
   - Once logged in, add a new server with the following details:
     - **Host:** `finance`
     - **Port:** `5432`
     - **Username:** `quera`
     - **Password:** `quera`

6. **Apply Migrations**
   With the database running, apply the necessary migrations.
   ```bash
   python manage.py migrate
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   Open your web browser and navigate to `http://127.0.0.1:8000/` to start using the application.

## Usage

### Creating an Account
1. Open the application in your browser.
2. Register for a new account.
3. Log in with your credentials.

### Adding Money to Your Wallet
1. After logging in, navigate to the "Add Money" section.
2. Enter the amount you wish to add to your wallet.
3. Confirm the transaction to see your updated balance.

### Sending Money to a Friend
1. Go to the "Send Money" section.
2. Enter your friend's username and the amount you want to send.
3. Confirm the transaction. The amount will be deducted from your wallet and added to your friend's wallet.

## Project Structure

- `wallet/`: Main app containing the core functionality of the wallet system.
- `templates/`: HTML templates for rendering the UI.
- `static/`: Static files such as CSS and JavaScript.
- `manage.py`: Django's command-line utility.
- `pip/requirements.txt`: Lists the Python dependencies for the project.
- `deploy/docker-compose.yml`: Configuration for Docker services including PostgreSQL and pgAdmin.

## Security

- The project uses Django's built-in security features, such as CSRF protection and secure password hashing.
- Transactions are securely handled and recorded in the database.

## Contributing
We welcome contributions! If you have suggestions or improvements, feel free to submit a pull request or open an issue.

## Acknowledgements
Special thanks to the Django community for their excellent documentation and support.