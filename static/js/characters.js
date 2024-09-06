
function showDetails(character) {
    const panel = document.getElementById('detailsPanel');
    document.getElementById('characterName').textContent = character.name;
    document.getElementById('characterSource').textContent = character.source_media;
    document.getElementById('characterImage').src = character.reference_picture;
    document.getElementById('characterDescription').textContent = character.description;
    document.getElementById('characterLink').href = character.reference_link;
    document.getElementById('characterImageLink').href = character.reference_picture;
    
    panel.classList.add('open');

    showOverlay();
    document.getElementById('overlay').addEventListener('click', closeDetails);
}

function closeDetails() {
    const panel = document.getElementById('detailsPanel');
    panel.classList.remove('open');

    hideOverlay();
}

document.addEventListener('DOMContentLoaded', function() {
    const toggleNav = document.getElementById('toggleNav');
    const nav = document.getElementById('characterNavigation');

    toggleNav.addEventListener('click', function() {
        nav.classList.toggle('expanded');
        toggleNav.textContent = nav.classList.contains('expanded') ? 'Hide Navigation' : 'Show Navigation';
    });

    // Close navigation when a link is clicked
    nav.addEventListener('click', function(e) {
        if (e.target.tagName === 'A') {
            nav.classList.remove('expanded');
            toggleNav.textContent = 'Show Navigation';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const nav = document.querySelector('.character-navigation');
    const navTop = nav.offsetTop;

    function stickyNavigation() {
        if (window.scrollY >= navTop) {
            nav.classList.add('sticky-nav');
        } else {
            nav.classList.remove('sticky-nav');
        }
    }

    window.addEventListener('scroll', stickyNavigation);
});