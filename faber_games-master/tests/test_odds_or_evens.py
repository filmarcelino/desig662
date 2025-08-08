import pytest
from unittest.mock import Mock
from games.odds_or_evens import OddsOrEvensGame


class TestOddsOrEvensGame:
    """Test cases for OddsOrEvensGame class"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.mock_random = Mock()
        self.game = OddsOrEvensGame(random_generator=self.mock_random)
    
    def test_determine_winner_user_wins_par_even_total(self):
        """Test winner determination when user chooses Par and total is even"""
        result = self.game.determine_winner("Par", 8)  # 8 is even
        assert result == "Voce Venceu!"
    
    def test_determine_winner_user_wins_impar_odd_total(self):
        """Test winner determination when user chooses Impar and total is odd"""
        result = self.game.determine_winner("Impar", 7)  # 7 is odd
        assert result == "Voce Venceu!"
    
    def test_determine_winner_user_loses_par_odd_total(self):
        """Test winner determination when user chooses Par but total is odd"""
        result = self.game.determine_winner("Par", 7)  # 7 is odd
        assert result == "Voce Perdeu!"
    
    def test_determine_winner_user_loses_impar_even_total(self):
        """Test winner determination when user chooses Impar but total is even"""
        result = self.game.determine_winner("Impar", 8)  # 8 is even
        assert result == "Voce Perdeu!"
    
    def test_play_round_user_wins(self):
        """Test complete round where user wins"""
        self.mock_random.randint.return_value = 3  # Computer chooses 3
        
        # User chooses Par, picks 5, total = 8 (even), so user wins
        computer_choice, computer_number, total, result = self.game.play_round("Par", 5)
        
        assert computer_choice == "Impar"
        assert computer_number == 3
        assert total == 8
        assert result == "Voce Venceu!"
    
    def test_play_round_user_loses(self):
        """Test complete round where user loses"""
        self.mock_random.randint.return_value = 4  # Computer chooses 4
        
        # User chooses Par, picks 3, total = 7 (odd), so user loses
        computer_choice, computer_number, total, result = self.game.play_round("Par", 3)
        
        assert computer_choice == "Impar"
        assert computer_number == 4
        assert total == 7
        assert result == "Voce Perdeu!"
    
    def test_play_round_edge_cases(self):
        """Test edge cases for play_round"""
        self.mock_random.randint.return_value = 1
        
        # Test with minimum values
        computer_choice, computer_number, total, result = self.game.play_round("Impar", 1)
        assert total == 2
        assert result == "Voce Perdeu!"  # 2 is even, user chose Impar
        
        # Test with maximum values
        self.mock_random.randint.return_value = 10
        computer_choice, computer_number, total, result = self.game.play_round("Par", 10)
        assert total == 20
        assert result == "Voce Venceu!"  # 20 is even, user chose Par


class TestOddsOrEvensGameIntegration:
    """Integration tests for OddsOrEvensGame"""
    
    def test_game_with_real_random(self):
        """Test game with real random generator"""
        game = OddsOrEvensGame()  # Use real random
        
        # Test that computer choice is always opposite
        computer_choice, computer_number, total, result = game.play_round("Par", 5)
        assert computer_choice == "Impar"
        
        computer_choice, computer_number, total, result = game.play_round("Impar", 5)
        assert computer_choice == "Par"
        
        # Test that computer number is within valid range
        for _ in range(100):
            _, computer_number, _, _ = game.play_round("Par", 1)
            assert 1 <= computer_number <= 10
        
        # Test that total calculation works
        _, _, total, _ = game.play_round("Par", 5)
        assert total >= 6 and total <= 15  # 5 + (1-10)
        
        # Test that even/odd detection works in determine_winner
        assert game.determine_winner("Par", 2) == "Voce Venceu!"  # 2 is even
        assert game.determine_winner("Impar", 3) == "Voce Venceu!"  # 3 is odd


if __name__ == "__main__":
    pytest.main([__file__]) 