from flask import render_template, request, session
import random
from typing import List, Tuple, Dict

class Card:
    """Representa uma carta do baralho"""
    
    def __init__(self, suit: str, value: str, numeric_value: int):
        self.suit = suit
        self.value = value
        self.numeric_value = numeric_value
    
    def __str__(self):
        return f"{self.value} de {self.suit}"
    
    def display_name(self):
        """Retorna o nome da carta para exibição"""
        return f"{self.value} de {self.suit}"

class BlackjackGame:
    """Lógica do jogo de Blackjack"""
    
    def __init__(self, random_generator=None):
        """Inicializa o jogo com gerador de números aleatórios opcional para testes"""
        if random_generator is None:
            self.random_generator = random
        else:
            self.random_generator = random_generator
        
        self.suits = ["♠", "♣", "♥", "♦"]
        self.values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.numeric_values = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    
    def create_deck(self) -> List[Card]:
        """Cria um baralho completo"""
        deck = []
        for suit in self.suits:
            for i, value in enumerate(self.values):
                card = Card(suit, value, self.numeric_values[i])
                deck.append(card)
        return deck
    
    def shuffle_deck(self, deck: List[Card]) -> List[Card]:
        """Embaralha o baralho"""
        self.random_generator.shuffle(deck)
        return deck
    
    def deal_card(self, deck: List[Card]) -> Tuple[Card, List[Card]]:
        """Distribui uma carta do baralho"""
        if not deck:
            deck = self.create_deck()
            deck = self.shuffle_deck(deck)
        
        card = deck.pop()
        return card, deck
    
    def calculate_hand_value(self, hand: List[Card]) -> int:
        """Calcula o valor total da mão"""
        total = 0
        aces = 0
        
        for card in hand:
            if card.value == "A":
                aces += 1
            else:
                total += card.numeric_value
        
        # Adiciona os ases
        for _ in range(aces):
            if total + 11 <= 21:
                total += 11
            else:
                total += 1
        
        return total
    
    def is_bust(self, hand: List[Card]) -> bool:
        """Verifica se a mão estourou (passou de 21)"""
        return self.calculate_hand_value(hand) > 21
    
    def is_blackjack(self, hand: List[Card]) -> bool:
        """Verifica se a mão é um blackjack (21 com 2 cartas)"""
        return len(hand) == 2 and self.calculate_hand_value(hand) == 21
    
    def dealer_should_hit(self, hand: List[Card]) -> bool:
        """Lógica do dealer: hit em 16 ou menos, stand em 17 ou mais"""
        return self.calculate_hand_value(hand) <= 16
    
    def determine_winner(self, player_hand: List[Card], dealer_hand: List[Card]) -> str:
        """Determina o vencedor do jogo"""
        player_value = self.calculate_hand_value(player_hand)
        dealer_value = self.calculate_hand_value(dealer_hand)
        
        # Verifica se alguém estourou
        if self.is_bust(player_hand):
            return "Você perdeu! Estourou!"
        if self.is_bust(dealer_hand):
            return "Você venceu! Dealer estourou!"
        
        # Verifica blackjacks
        if self.is_blackjack(player_hand) and not self.is_blackjack(dealer_hand):
            return "Blackjack! Você venceu!"
        if self.is_blackjack(dealer_hand) and not self.is_blackjack(player_hand):
            return "Dealer fez Blackjack! Você perdeu!"
        if self.is_blackjack(player_hand) and self.is_blackjack(dealer_hand):
            return "Empate! Ambos fizeram Blackjack!"
        
        # Compara valores
        if player_value > dealer_value:
            return "Você venceu!"
        elif dealer_value > player_value:
            return "Dealer venceu!"
        else:
            return "Empate!"

def handle_blackjack():
    """Manipula a lógica do jogo de blackjack - manipulador de rota Flask"""
    game = BlackjackGame()
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "new_game":
            # Inicia um novo jogo
            deck = game.create_deck()
            deck = game.shuffle_deck(deck)
            
            # Distribui cartas iniciais
            player_card1, deck = game.deal_card(deck)
            dealer_card1, deck = game.deal_card(deck)
            player_card2, deck = game.deal_card(deck)
            dealer_card2, deck = game.deal_card(deck)
            
            player_hand = [player_card1, player_card2]
            dealer_hand = [dealer_card1, dealer_card2]
            
            # Salva o estado do jogo na sessão
            session["bj_deck"] = [(card.suit, card.value, card.numeric_value) for card in deck]
            session["bj_player_hand"] = [(card.suit, card.value, card.numeric_value) for card in player_hand]
            session["bj_dealer_hand"] = [(card.suit, card.value, card.numeric_value) for card in dealer_hand]
            session["bj_game_state"] = "player_turn"
            
            return render_template("blackjack_game.html", 
                                 player_hand=player_hand,
                                 dealer_hand=[dealer_card1],  # Mostra apenas a primeira carta
                                 player_value=game.calculate_hand_value(player_hand),
                                 dealer_value=game.calculate_hand_value([dealer_card1]),
                                 game_state="player_turn")
        
        elif action == "hit":
            # Jogador pede mais uma carta
            deck_data = session.get("bj_deck", [])
            player_hand_data = session.get("bj_player_hand", [])
            dealer_hand_data = session.get("bj_dealer_hand", [])
            
            # Reconstrói os objetos
            deck = [Card(suit, value, num_val) for suit, value, num_val in deck_data]
            player_hand = [Card(suit, value, num_val) for suit, value, num_val in player_hand_data]
            dealer_hand = [Card(suit, value, num_val) for suit, value, num_val in dealer_hand_data]
            
            # Distribui carta para o jogador
            new_card, deck = game.deal_card(deck)
            player_hand.append(new_card)
            
            # Atualiza a sessão
            session["bj_deck"] = [(card.suit, card.value, card.numeric_value) for card in deck]
            session["bj_player_hand"] = [(card.suit, card.value, card.numeric_value) for card in player_hand]
            
            if game.is_bust(player_hand):
                # Jogador estourou
                session["bj_game_state"] = "game_over"
                result = "Você perdeu! Estourou!"
                return render_template("blackjack_result.html",
                                     player_hand=player_hand,
                                     dealer_hand=dealer_hand,
                                     player_value=game.calculate_hand_value(player_hand),
                                     dealer_value=game.calculate_hand_value(dealer_hand),
                                     result=result)
            else:
                # Jogador ainda pode continuar
                return render_template("blackjack_game.html",
                                     player_hand=player_hand,
                                     dealer_hand=[dealer_hand[0]],  # Mostra apenas a primeira carta
                                     player_value=game.calculate_hand_value(player_hand),
                                     dealer_value=game.calculate_hand_value([dealer_hand[0]]),
                                     game_state="player_turn")
        
        elif action == "stand":
            # Jogador para, vez do dealer
            deck_data = session.get("bj_deck", [])
            player_hand_data = session.get("bj_player_hand", [])
            dealer_hand_data = session.get("bj_dealer_hand", [])
            
            # Reconstrói os objetos
            deck = [Card(suit, value, num_val) for suit, value, num_val in deck_data]
            player_hand = [Card(suit, value, num_val) for suit, value, num_val in player_hand_data]
            dealer_hand = [Card(suit, value, num_val) for suit, value, num_val in dealer_hand_data]
            
            # Dealer joga
            while game.dealer_should_hit(dealer_hand):
                new_card, deck = game.deal_card(deck)
                dealer_hand.append(new_card)
            
            # Determina o vencedor
            result = game.determine_winner(player_hand, dealer_hand)
            
            # Limpa a sessão
            session.pop("bj_deck", None)
            session.pop("bj_player_hand", None)
            session.pop("bj_dealer_hand", None)
            session.pop("bj_game_state", None)
            
            return render_template("blackjack_result.html",
                                 player_hand=player_hand,
                                 dealer_hand=dealer_hand,
                                 player_value=game.calculate_hand_value(player_hand),
                                 dealer_value=game.calculate_hand_value(dealer_hand),
                                 result=result)
    
    # GET: Mostra a tela inicial
    return render_template("blackjack.html") 