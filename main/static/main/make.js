document.addEventListener('DOMContentLoaded', function() {
  // Category toggle functionality
  document.querySelectorAll('.category-header').forEach(category => {
    category.addEventListener('click', hide_category);
  });

  // Input field functionality
  document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('focus', () => {
      if (input.value === "0") {
        input.value = "";
      }
    });
    
    input.addEventListener('blur', () => {
      if (input.value === "") {
        input.value = "0";
      }
    });

    input.addEventListener('wheel', (event) => {
      event.preventDefault();
      input.blur();
    });
  });

  // Stock availability display
  document.querySelectorAll('.stock').forEach(stock => {
    if (stock.dataset.quantity === "0") {
      stock.innerHTML = "غير متوفر";
      stock.classList.add('text-red-500');
    }
  });
});

function hide_category() {
  const icon = document.querySelector(`.toggle-icon[data-toggle="${this.dataset.code}"] i`);
  const categoryBlock = document.querySelector(`#${this.dataset.code}`);
  
  if (categoryBlock.classList.contains('hidden')) {
    categoryBlock.classList.remove('hidden');
    icon.classList.remove("fa-angle-up");
    icon.classList.add("fa-angle-down");
  } else {
    categoryBlock.classList.add('hidden');
    icon.classList.remove("fa-angle-down");
    icon.classList.add("fa-angle-up");
  }
}


  