// Collapsible sections toggle
function toggleCollapsible(sectionId) {
  var section = document.getElementById(sectionId);
  var button = document.querySelector('[onclick="toggleCollapsible(\'' + sectionId + '\')"]');
  
  if (section.classList.contains('collapsed')) {
    section.classList.remove('collapsed');
    if (button) {
      button.setAttribute('aria-expanded', 'true');
    }
  } else {
    section.classList.add('collapsed');
    if (button) {
      button.setAttribute('aria-expanded', 'false');
    }
  }
}

// Auto-show collapsible sections on page load for better UX
// but keep them collapsed initially for returning visitors
document.addEventListener('DOMContentLoaded', function() {
  // Optionally: show sections by default
  // var sections = document.querySelectorAll('.collapsible-section');
  // sections.forEach(function(section) {
  //   section.classList.add('show');
  // });

  // Initialize collapsible sections as collapsed on mobile
  var sections = document.querySelectorAll('.hover-collapsible .collapsible-section');
  sections.forEach(function(section) {
    section.classList.add('collapsed');
  });
  
  var buttons = document.querySelectorAll('.hover-collapsible .collapsible-button');
  buttons.forEach(function(button) {
    button.setAttribute('aria-expanded', 'false');
  });

  // Click-based toggle for collapsible sections on mobile
  var collapsibleButtons = document.querySelectorAll('.collapsible-button');
  collapsibleButtons.forEach(function(button) {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      var section = this.parentNode.querySelector('.collapsible-section');
      if (section) {
        if (section.classList.contains('collapsed')) {
          section.classList.remove('collapsed');
          this.setAttribute('aria-expanded', 'true');
        } else {
          section.classList.add('collapsed');
          this.setAttribute('aria-expanded', 'false');
        }
      }
    });
  });
});
