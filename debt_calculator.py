"""
Debt Payoff Calculator
Implements various debt payoff strategies including snowball and avalanche methods
"""

import math
from typing import List, Dict, Any

class DebtCalculator:
    def __init__(self, credit_cards):
        self.credit_cards = credit_cards
    
    def snowball_method(self, extra_payment: float = 0) -> Dict[str, Any]:
        """
        Debt Snowball Method: Pay minimums on all cards, then pay extra on smallest balance
        """
        cards_data = []
        for card in self.credit_cards:
            cards_data.append({
                'name': card.name,
                'balance': card.balance,
                'apr': card.apr,
                'minimum_payment': card.minimum_payment
            })
        
        # Sort by balance (smallest first)
        cards_data.sort(key=lambda x: x['balance'])
        
        return self._calculate_payoff_plan(cards_data, extra_payment, 'Snowball (Smallest Balance First)')
    
    def avalanche_method(self, extra_payment: float = 0) -> Dict[str, Any]:
        """
        Debt Avalanche Method: Pay minimums on all cards, then pay extra on highest APR
        """
        cards_data = []
        for card in self.credit_cards:
            cards_data.append({
                'name': card.name,
                'balance': card.balance,
                'apr': card.apr,
                'minimum_payment': card.minimum_payment
            })
        
        # Sort by APR (highest first)
        cards_data.sort(key=lambda x: x['apr'], reverse=True)
        
        return self._calculate_payoff_plan(cards_data, extra_payment, 'Avalanche (Highest Interest First)')
    
    def _calculate_payoff_plan(self, cards_data: List[Dict], extra_payment: float, method_name: str) -> Dict[str, Any]:
        """
        Calculate the detailed payoff plan for a given strategy
        """
        if not cards_data:
            return {
                'method': method_name,
                'total_interest': 0,
                'payoff_time_months': 0,
                'monthly_payments': [],
                'cards': []
            }
        
        # Copy data to avoid modifying original
        cards = [card.copy() for card in cards_data]
        monthly_payments = []
        total_interest_paid = 0
        month = 0
        
        # Calculate total minimum payments
        total_minimum = sum(card['minimum_payment'] for card in cards)
        total_available = total_minimum + extra_payment
        
        while any(card['balance'] > 0 for card in cards):
            month += 1
            if month > 600:  # Safety break - 50 years max
                break
            
            month_data = {
                'month': month,
                'cards': [],
                'total_payment': 0,
                'total_interest': 0
            }
            
            # Calculate interest for all cards
            for card in cards:
                if card['balance'] > 0:
                    monthly_interest = card['balance'] * (card['apr'] / 100 / 12)
                    total_interest_paid += monthly_interest
                    month_data['total_interest'] += monthly_interest
                    card['balance'] += monthly_interest
            
            # Make minimum payments on all cards
            remaining_payment = total_available
            for card in cards:
                if card['balance'] > 0:
                    payment = min(card['minimum_payment'], card['balance'], remaining_payment)
                    card['balance'] -= payment
                    remaining_payment -= payment
                    month_data['total_payment'] += payment
                    
                    month_data['cards'].append({
                        'name': card['name'],
                        'payment': payment,
                        'remaining_balance': max(0, card['balance'])
                    })
            
            # Apply extra payment to the target card (first in sorted list with balance > 0)
            if remaining_payment > 0:
                for card in cards:
                    if card['balance'] > 0:
                        extra_applied = min(remaining_payment, card['balance'])
                        card['balance'] -= extra_applied
                        month_data['total_payment'] += extra_applied
                        
                        # Update the card payment in month_data
                        for card_data in month_data['cards']:
                            if card_data['name'] == card['name']:
                                card_data['payment'] += extra_applied
                                card_data['remaining_balance'] = max(0, card['balance'])
                                break
                        break
            
            monthly_payments.append(month_data)
        
        # Prepare summary for each card
        card_summaries = []
        for original_card in cards_data:
            card_summaries.append({
                'name': original_card['name'],
                'original_balance': original_card['balance'],
                'apr': original_card['apr'],
                'minimum_payment': original_card['minimum_payment']
            })
        
        return {
            'method': method_name,
            'total_interest': round(total_interest_paid, 2),
            'payoff_time_months': month,
            'payoff_time_years': round(month / 12, 1),
            'total_payments': round(sum(card['balance'] for card in cards_data) + total_interest_paid, 2),
            'monthly_payments': monthly_payments[:12],  # Show first 12 months
            'cards': card_summaries,
            'extra_payment': extra_payment
        }
    
    def compare_methods(self, extra_payment: float = 0) -> Dict[str, Any]:
        """
        Compare snowball vs avalanche methods
        """
        snowball = self.snowball_method(extra_payment)
        avalanche = self.avalanche_method(extra_payment)
        
        interest_savings = snowball['total_interest'] - avalanche['total_interest']
        time_savings = snowball['payoff_time_months'] - avalanche['payoff_time_months']
        
        return {
            'snowball': snowball,
            'avalanche': avalanche,
            'avalanche_saves_interest': round(interest_savings, 2),
            'avalanche_saves_months': time_savings,
            'recommendation': 'avalanche' if interest_savings > 100 or time_savings > 2 else 'snowball'
        }