document.addEventListener('DOMContentLoaded', () => {
    // Mobile navigation toggle
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const sidebar = document.querySelector('.app-sidebar');

    mobileNavToggle.addEventListener('click', () => {
        const isVisible = sidebar.getAttribute('data-visible') === 'true';
        sidebar.setAttribute('data-visible', !isVisible);
        mobileNavToggle.setAttribute('aria-expanded', !isVisible);
    });


    // General fade-in animation for content
    anime({
        targets: '.app-content',
        opacity: [0, 1],
        translateY: [20, 0],
        duration: 800,
        easing: 'easeOutQuad'
    });

    // Stagger-in animation for game cards
    if (document.querySelector('.games-grid')) {
        anime({
            targets: '.game-card',
            opacity: [0, 1],
            translateY: [40, 0],
            delay: anime.stagger(100),
            duration: 600,
            easing: 'easeOutCubic'
        });
    }

    // Add hover animations to game cards for a more dynamic feel
    const gameCards = document.querySelectorAll('.game-card');
    gameCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            anime({
                targets: card,
                translateY: -5,
                boxShadow: '0 12px 24px rgba(0, 0, 0, 0.25)',
                duration: 300,
                easing: 'easeOutQuad'
            });
        });

        card.addEventListener('mouseleave', () => {
            anime({
                targets: card,
                translateY: 0,
                boxShadow: '0 6px 12px rgba(0, 0, 0, 0.15)',
                duration: 300,
                easing: 'easeOutQuad'
            });
        });
    });
});
