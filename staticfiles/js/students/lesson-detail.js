document.addEventListener('DOMContentLoaded', function() {
    const themeButtons = document.querySelectorAll('.theme-mode-btn');
    const body = document.querySelector('.main-body');
    const storedTheme = localStorage.getItem('theme-mode') || 'light';

    // Apply the stored theme on page load
    applyTheme(storedTheme);

    themeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const mode = this.getAttribute('data-mode');
            localStorage.setItem('theme-mode', mode);
            applyTheme(mode);
        });
    });

    function applyTheme(mode) {
        if (!body) return; // Add a safety check in case the element isn't found

        // Remove all theme classes first
        body.classList.remove('theme-dark', 'theme-lighter-dark', 'theme-blue', 'theme-green');

        // Apply the new theme class
        if (mode === 'dark') {
            body.classList.add('theme-dark');
        } else if (mode === 'lighter-dark') {
            body.classList.add('theme-lighter-dark');
        } else if (mode === 'blue') {
            body.classList.add('theme-blue');
        } else if (mode === 'green') {
            body.classList.add('theme-green');
        }
    }
});