# Debt Payoff Planner

A comprehensive web application to help you strategically pay off your credit card debt using proven methods like the Debt Snowball and Debt Avalanche strategies. Built with Python Flask and designed for deployment on Azure Web Apps.

## Features

### 🎯 Core Functionality
- **Credit Card Management**: Add, edit, and delete credit cards with balance, APR, and minimum payment tracking
- **Debt Payoff Strategies**: 
  - **Snowball Method**: Pay off smallest balances first for psychological wins
  - **Avalanche Method**: Pay off highest interest rates first to save money
- **Interactive Calculations**: Adjust extra payment amounts and see real-time impact
- **Detailed Payment Plans**: View month-by-month breakdown of your debt payoff journey

### 💻 Technical Features
- **Responsive Web Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Persistent Data Storage**: SQLite database keeps your data safe and accessible
- **Professional UI**: Bootstrap-based interface with intuitive navigation
- **Real-time Updates**: AJAX-powered calculations without page refreshes

### ☁️ Deployment Ready
- **Azure Web App Compatible**: Pre-configured for Azure deployment
- **GitHub Actions CI/CD**: Automated deployment pipeline included
- **Environment Configuration**: Production-ready with environment variables
- **Scalable Architecture**: Can easily migrate to PostgreSQL for production

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/iwindon/debt.git
   cd debt
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

### Production Deployment on Azure

1. **Create an Azure Web App**
   - Choose Python 3.11 runtime
   - Configure for Linux

2. **Set up GitHub Actions**
   - Add your Azure publish profile to GitHub secrets as `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Update the `AZURE_WEBAPP_NAME` in `.github/workflows/azure-deploy.yml`

3. **Push to main branch**
   - The GitHub Action will automatically deploy your app

## Usage Guide

### Adding Credit Cards
1. Click "Add Credit Card" from the dashboard
2. Enter your card details:
   - **Card Name**: A recognizable name (e.g., "Chase Freedom")
   - **Current Balance**: Outstanding amount owed
   - **APR**: Annual Percentage Rate (found on your statement)
   - **Minimum Payment**: Required monthly minimum

### Generating Payoff Plans
1. Add all your credit cards
2. Click "Generate Payoff Plan"
3. Compare Snowball vs Avalanche methods
4. Adjust extra payment amount to see impact
5. View detailed month-by-month schedules

### Understanding the Methods

**Debt Snowball Method:**
- Pays off cards with smallest balances first
- Provides psychological motivation through quick wins
- May cost more in total interest

**Debt Avalanche Method:**
- Pays off cards with highest interest rates first
- Saves the most money in total interest
- May take longer to see initial progress

## Development

### Project Structure
```
debt/
├── app.py                 # Main Flask application
├── debt_calculator.py     # Core calculation logic
├── requirements.txt       # Python dependencies
├── startup.py            # Azure startup script
├── web.config            # Azure configuration
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── add_card.html
│   ├── edit_card.html
│   └── payoff_plan.html
├── static/               # CSS and JavaScript
│   ├── css/style.css
│   └── js/app.js
├── tests/                # Unit tests
│   └── test_debt_calculator.py
└── .github/workflows/    # GitHub Actions
    └── azure-deploy.yml
```

### Running Tests
```bash
python -m pytest tests/
```

### Environment Variables
Copy `.env.example` to `.env` and configure:
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: Set to 'production' for production

## Security Considerations

- All data is stored locally in your database
- No sensitive financial information is transmitted to external services
- Use strong secret keys in production
- Consider HTTPS for production deployments
- Regularly backup your database

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions, issues, or feature requests, please open an issue on GitHub.

---

**Take control of your financial future with strategic debt payoff planning!** 🚀
