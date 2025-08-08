import pytest
import random
from games.blackjack import BlackjackGame, Card

class TestBlackjackGame:
    """Testes para o jogo de Blackjack"""
    
    def setup_method(self):
        """Configuração para cada teste"""
        self.game = BlackjackGame()
    
    def test_create_deck(self):
        """Testa se o baralho é criado corretamente"""
        deck = self.game.create_deck()
        assert len(deck) == 52  # 52 cartas no baralho
        
        # Verifica se todas as cartas são instâncias de Card
        for card in deck:
            assert isinstance(card, Card)
        
        # Verifica se há 13 cartas de cada naipe
        suits_count = {}
        for card in deck:
            suits_count[card.suit] = suits_count.get(card.suit, 0) + 1
        
        for suit in self.game.suits:
            assert suits_count[suit] == 13
    
    def test_shuffle_deck(self):
        """Testa se o baralho é embaralhado"""
        deck1 = self.game.create_deck()
        deck2 = self.game.create_deck()
        
        # Embaralha apenas o segundo baralho
        deck2 = self.game.shuffle_deck(deck2)
        
        # Verifica se os baralhos são diferentes (embaralhamento funcionou)
        # Nota: há uma chance muito pequena de serem iguais mesmo após embaralhar
        cards_different = False
        for i in range(len(deck1)):
            if (deck1[i].suit != deck2[i].suit or 
                deck1[i].value != deck2[i].value):
                cards_different = True
                break
        
        assert cards_different
    
    def test_deal_card(self):
        """Testa se as cartas são distribuídas corretamente"""
        deck = self.game.create_deck()
        original_length = len(deck)
        
        card, new_deck = self.game.deal_card(deck)
        
        assert isinstance(card, Card)
        assert len(new_deck) == original_length - 1
        assert card not in new_deck
    
    def test_calculate_hand_value(self):
        """Testa o cálculo do valor da mão"""
        # Testa mão simples
        hand = [Card("♠", "10", 10), Card("♥", "5", 5)]
        assert self.game.calculate_hand_value(hand) == 15
        
        # Testa com ás valendo 11
        hand = [Card("♠", "A", 11), Card("♥", "5", 5)]
        assert self.game.calculate_hand_value(hand) == 16
        
        # Testa com ás valendo 1 (para não estourar)
        hand = [Card("♠", "A", 11), Card("♥", "10", 10), Card("♦", "5", 5)]
        assert self.game.calculate_hand_value(hand) == 16  # A=1, 10+5+1=16
        
        # Testa com múltiplos ases
        hand = [Card("♠", "A", 11), Card("♥", "A", 11)]
        assert self.game.calculate_hand_value(hand) == 12  # A=1, A=1, 1+1=2
    
    def test_is_bust(self):
        """Testa se a função detecta corretamente quando a mão estourou"""
        # Mão que não estourou
        hand = [Card("♠", "10", 10), Card("♥", "5", 5)]
        assert not self.game.is_bust(hand)
        
        # Mão que estourou
        hand = [Card("♠", "10", 10), Card("♥", "10", 10), Card("♦", "5", 5)]
        assert self.game.is_bust(hand)
    
    def test_is_blackjack(self):
        """Testa se a função detecta corretamente blackjack"""
        # Blackjack válido
        hand = [Card("♠", "A", 11), Card("♥", "10", 10)]
        assert self.game.is_blackjack(hand)
        
        # Não é blackjack (3 cartas)
        hand = [Card("♠", "A", 11), Card("♥", "5", 5), Card("♦", "5", 5)]
        assert not self.game.is_blackjack(hand)
        
        # Não é blackjack (valor diferente de 21)
        hand = [Card("♠", "10", 10), Card("♥", "5", 5)]
        assert not self.game.is_blackjack(hand)
    
    def test_dealer_should_hit(self):
        """Testa a lógica do dealer"""
        # Dealer deve pedir carta (16 ou menos)
        hand = [Card("♠", "10", 10), Card("♥", "6", 6)]
        assert self.game.dealer_should_hit(hand)
        
        # Dealer deve parar (17 ou mais)
        hand = [Card("♠", "10", 10), Card("♥", "7", 7)]
        assert not self.game.dealer_should_hit(hand)
    
    def test_determine_winner(self):
        """Testa a determinação do vencedor"""
        # Jogador estourou
        player_hand = [Card("♠", "10", 10), Card("♥", "10", 10), Card("♦", "5", 5)]
        dealer_hand = [Card("♣", "10", 10), Card("♦", "5", 5)]
        result = self.game.determine_winner(player_hand, dealer_hand)
        assert "perdeu" in result.lower()
        
        # Dealer estourou
        player_hand = [Card("♠", "10", 10), Card("♥", "5", 5)]
        dealer_hand = [Card("♣", "10", 10), Card("♦", "10", 10), Card("♥", "5", 5)]
        result = self.game.determine_winner(player_hand, dealer_hand)
        assert "venceu" in result.lower()
        
        # Jogador vence por valor maior
        player_hand = [Card("♠", "10", 10), Card("♥", "8", 8)]
        dealer_hand = [Card("♣", "10", 10), Card("♦", "5", 5)]
        result = self.game.determine_winner(player_hand, dealer_hand)
        assert "venceu" in result.lower()
        
        # Dealer vence por valor maior
        player_hand = [Card("♠", "10", 10), Card("♥", "5", 5)]
        dealer_hand = [Card("♣", "10", 10), Card("♦", "8", 8)]
        result = self.game.determine_winner(player_hand, dealer_hand)
        assert "dealer" in result.lower() or "perdeu" in result.lower()
        
        # Empate
        player_hand = [Card("♠", "10", 10), Card("♥", "5", 5)]
        dealer_hand = [Card("♣", "10", 10), Card("♦", "5", 5)]
        result = self.game.determine_winner(player_hand, dealer_hand)
        assert "empate" in result.lower()

class TestCard:
    """Testes para a classe Card"""
    
    def test_card_creation(self):
        """Testa a criação de uma carta"""
        card = Card("♠", "A", 11)
        assert card.suit == "♠"
        assert card.value == "A"
        assert card.numeric_value == 11
    
    def test_card_string_representation(self):
        """Testa a representação em string da carta"""
        card = Card("♥", "10", 10)
        assert str(card) == "10 de ♥"
        assert card.display_name() == "10 de ♥" 