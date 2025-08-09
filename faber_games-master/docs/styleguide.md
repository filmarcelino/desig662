# Guia de Estilo

Este guia resume tokens visuais e componentes comuns utilizados no projeto.

## Cores

| Token | Valor | Uso |
|-------|-------|-----|
| `--fg-cyan` | `#00fff7` | Destaques e bordas.
| `--fg-pink` | `#ff0080` | Ações principais, títulos.
| `--fg-green` | `#39ff14` | Feedback positivo e texto em botões escuros.
| `--fg-dark` | `#222` | Plano de fundo principal.
| `--fg-light` | `#fff` | Texto sobre fundos escuros.

## Tipografia

- Fonte primária: **Inter**, pesos 400, 600 e 700.
- Títulos seguem hierarquia `h1 > h2 > h3`.

## Componentes

### Botão Arcade

```
<button class="arcade-btn">Exemplo</button>
```

- Bordas arredondadas de 6px.
- Animação de hover com mudança de cor e glow.

### Card de Jogo

```
<div class="game-card">
    <img src="images/placeholder.png" alt="Nome do jogo">
    <h3>Nome do Jogo</h3>
</div>
```

- Utiliza sombra leve e bordas de 8px.

## Espaçamentos

- Unidade base: `8px`.
- Gutters entre elementos: `16px`.

Este documento deve ser expandido conforme novos componentes e tokens forem adicionados.
