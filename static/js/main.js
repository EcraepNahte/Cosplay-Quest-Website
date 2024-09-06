
function showOverlay() {
    const overlay = document.getElementById('overlay');
    overlay.style.display = 'block';
    setTimeout(() => {
      overlay.classList.add('active');
    }, 10); // Small delay to ensure the display change has taken effect
  }
  
  function hideOverlay() {
    const overlay = document.getElementById('overlay');
    overlay.classList.remove('active');
    setTimeout(() => {
      overlay.style.display = 'none';
    }, 300); // Wait for the fade out transition to complete
  }

