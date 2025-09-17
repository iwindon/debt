"""
Debt Payoff Application
A web application to help users create optimal debt payoff plans
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from debt_calculator import DebtCalculator

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///debt_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class CreditCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    apr = db.Column(db.Float, nullable=False)
    minimum_payment = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CreditCard {self.name}: ${self.balance}>'

# Routes
@app.route('/')
def index():
    """Main dashboard showing all credit cards and debt summary"""
    cards = CreditCard.query.all()
    total_debt = sum(card.balance for card in cards)
    total_minimum = sum(card.minimum_payment for card in cards)
    
    return render_template('index.html', 
                         cards=cards, 
                         total_debt=total_debt,
                         total_minimum=total_minimum)

@app.route('/add_card', methods=['GET', 'POST'])
def add_card():
    """Add a new credit card"""
    if request.method == 'POST':
        name = request.form['name']
        balance = float(request.form['balance'])
        apr = float(request.form['apr'])
        minimum_payment = float(request.form['minimum_payment'])
        
        card = CreditCard(
            name=name,
            balance=balance,
            apr=apr,
            minimum_payment=minimum_payment
        )
        
        db.session.add(card)
        db.session.commit()
        flash(f'Credit card "{name}" added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_card.html')

@app.route('/edit_card/<int:card_id>', methods=['GET', 'POST'])
def edit_card(card_id):
    """Edit an existing credit card"""
    card = CreditCard.query.get_or_404(card_id)
    
    if request.method == 'POST':
        card.name = request.form['name']
        card.balance = float(request.form['balance'])
        card.apr = float(request.form['apr'])
        card.minimum_payment = float(request.form['minimum_payment'])
        
        db.session.commit()
        flash(f'Credit card "{card.name}" updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_card.html', card=card)

@app.route('/delete_card/<int:card_id>')
def delete_card(card_id):
    """Delete a credit card"""
    card = CreditCard.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    flash(f'Credit card "{card.name}" deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/payoff_plan')
def payoff_plan():
    """Generate and display debt payoff plans"""
    cards = CreditCard.query.all()
    
    if not cards:
        flash('Please add some credit cards first!', 'warning')
        return redirect(url_for('index'))
    
    calculator = DebtCalculator(cards)
    snowball_plan = calculator.snowball_method()
    avalanche_plan = calculator.avalanche_method()
    
    return render_template('payoff_plan.html',
                         snowball_plan=snowball_plan,
                         avalanche_plan=avalanche_plan,
                         cards=cards)

@app.route('/api/payoff_calculation', methods=['POST'])
def api_payoff_calculation():
    """API endpoint for dynamic payoff calculations"""
    data = request.get_json()
    extra_payment = data.get('extra_payment', 0)
    
    cards = CreditCard.query.all()
    calculator = DebtCalculator(cards)
    
    snowball_plan = calculator.snowball_method(extra_payment)
    avalanche_plan = calculator.avalanche_method(extra_payment)
    
    return jsonify({
        'snowball': snowball_plan,
        'avalanche': avalanche_plan
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Run in development mode
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))