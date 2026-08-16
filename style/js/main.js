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
});
