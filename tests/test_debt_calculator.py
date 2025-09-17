"""
Unit tests for the debt calculator functionality
"""

import unittest
from unittest.mock import Mock
from debt_calculator import DebtCalculator

class TestDebtCalculator(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create mock credit cards
        self.mock_cards = []
        
        # Card 1: High balance, medium APR
        card1 = Mock()
        card1.name = "Chase Freedom"
        card1.balance = 5000.0
        card1.apr = 18.99
        card1.minimum_payment = 100.0
        self.mock_cards.append(card1)
        
        # Card 2: Low balance, high APR
        card2 = Mock()
        card2.name = "Capital One"
        card2.balance = 2000.0
        card2.apr = 24.99
        card2.minimum_payment = 50.0
        self.mock_cards.append(card2)
        
        # Card 3: Medium balance, low APR
        card3 = Mock()
        card3.name = "Discover"
        card3.balance = 3000.0
        card3.apr = 12.99
        card3.minimum_payment = 75.0
        self.mock_cards.append(card3)
        
        self.calculator = DebtCalculator(self.mock_cards)
    
    def test_snowball_method_ordering(self):
        """Test that snowball method orders cards by balance (smallest first)"""
        result = self.calculator.snowball_method()
        
        self.assertEqual(result['method'], 'Snowball (Smallest Balance First)')
        self.assertEqual(len(result['cards']), 3)
        
        # Should be ordered: Capital One (2000), Discover (3000), Chase Freedom (5000)
        self.assertEqual(result['cards'][0]['name'], 'Capital One')
        self.assertEqual(result['cards'][1]['name'], 'Discover')
        self.assertEqual(result['cards'][2]['name'], 'Chase Freedom')
    
    def test_avalanche_method_ordering(self):
        """Test that avalanche method orders cards by APR (highest first)"""
        result = self.calculator.avalanche_method()
        
        self.assertEqual(result['method'], 'Avalanche (Highest Interest First)')
        self.assertEqual(len(result['cards']), 3)
        
        # Should be ordered: Capital One (24.99%), Chase Freedom (18.99%), Discover (12.99%)
        self.assertEqual(result['cards'][0]['name'], 'Capital One')
        self.assertEqual(result['cards'][1]['name'], 'Chase Freedom')
        self.assertEqual(result['cards'][2]['name'], 'Discover')
    
    def test_empty_cards_list(self):
        """Test behavior with no credit cards"""
        empty_calculator = DebtCalculator([])
        
        snowball_result = empty_calculator.snowball_method()
        avalanche_result = empty_calculator.avalanche_method()
        
        self.assertEqual(snowball_result['total_interest'], 0)
        self.assertEqual(snowball_result['payoff_time_months'], 0)
        self.assertEqual(len(snowball_result['cards']), 0)
        
        self.assertEqual(avalanche_result['total_interest'], 0)
        self.assertEqual(avalanche_result['payoff_time_months'], 0)
        self.assertEqual(len(avalanche_result['cards']), 0)
    
    def test_extra_payment_reduces_time(self):
        """Test that extra payments reduce payoff time"""
        result_no_extra = self.calculator.snowball_method(0)
        result_with_extra = self.calculator.snowball_method(200)
        
        # With extra payment, should take less time and cost less interest
        self.assertLess(result_with_extra['payoff_time_months'], 
                       result_no_extra['payoff_time_months'])
        self.assertLess(result_with_extra['total_interest'], 
                       result_no_extra['total_interest'])
    
    def test_avalanche_saves_interest(self):
        """Test that avalanche method typically saves interest compared to snowball"""
        snowball_result = self.calculator.snowball_method(100)
        avalanche_result = self.calculator.avalanche_method(100)
        
        # Avalanche should usually save interest (not always, but with our test data it should)
        self.assertLessEqual(avalanche_result['total_interest'], 
                            snowball_result['total_interest'])
    
    def test_calculation_with_single_card(self):
        """Test calculation with only one credit card"""
        single_card = [self.mock_cards[0]]  # Just Chase Freedom
        single_calculator = DebtCalculator(single_card)
        
        result = single_calculator.snowball_method()
        
        self.assertEqual(len(result['cards']), 1)
        self.assertEqual(result['cards'][0]['name'], 'Chase Freedom')
        self.assertGreater(result['payoff_time_months'], 0)

if __name__ == '__main__':
    unittest.main()