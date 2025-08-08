import pytest
import random
from games.penalty import PenaltyGame

class TestPenaltyGame:
    """Test cases for the Penalty game"""
    
    def test_play_round_goal(self):
        """Test that a goal is scored when directions differ"""
        # Create a mock random generator that always returns different direction
        class MockRandom:
            def choice(self, directions):
                return 'right' if 'left' in directions else 'left'
        
        game = PenaltyGame(random_generator=MockRandom())
        
        player_direction, goalkeeper_direction, result = game.play_round("left")
        
        assert player_direction == "left"
        assert goalkeeper_direction == "right"
        assert result == "GOAL"
    
    def test_play_round_saved(self):
        """Test that a shot is saved when directions match"""
        # Create a mock random generator that always returns same direction
        class MockRandom:
            def choice(self, directions):
                return 'left'
        
        game = PenaltyGame(random_generator=MockRandom())
        
        player_direction, goalkeeper_direction, result = game.play_round("left")
        
        assert player_direction == "left"
        assert goalkeeper_direction == "left"
        assert result == "SAVED"
    
    def test_play_round_center_goal(self):
        """Test center shot when goalkeeper goes to side"""
        class MockRandom:
            def choice(self, directions):
                return 'left'
        
        game = PenaltyGame(random_generator=MockRandom())
        
        player_direction, goalkeeper_direction, result = game.play_round("center")
        
        assert player_direction == "center"
        assert goalkeeper_direction == "left"
        assert result == "GOAL"
    
    def test_play_round_center_saved(self):
        """Test center shot when goalkeeper stays center"""
        class MockRandom:
            def choice(self, directions):
                return 'center'
        
        game = PenaltyGame(random_generator=MockRandom())
        
        player_direction, goalkeeper_direction, result = game.play_round("center")
        
        assert player_direction == "center"
        assert goalkeeper_direction == "center"
        assert result == "SAVED"
    
    def test_game_initialization(self):
        """Test that the game initializes correctly"""
        game = PenaltyGame()
        
        # Test that random_generator is set correctly
        assert game.random_generator is not None
        assert hasattr(game.random_generator, 'choice')
    
    def test_all_directions(self):
        """Test all possible directions"""
        game = PenaltyGame()
        directions = ["left", "center", "right"]
        
        for direction in directions:
            player_direction, goalkeeper_direction, result = game.play_round(direction)
            
            assert player_direction == direction
            assert goalkeeper_direction in directions
            assert result in ["GOAL", "SAVED"]
            
            # Verify the result logic
            if player_direction == goalkeeper_direction:
                assert result == "SAVED"
            else:
                assert result == "GOAL"

if __name__ == "__main__":
    pytest.main([__file__]) 
