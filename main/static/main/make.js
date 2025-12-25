// Test if script is loading
console.log('make.js script loaded');

// Define calculateTotal function immediately (before DOM ready)
function calculateTotal() {
  try {
    // console.log('calculateTotal called');
    let total = 0;
    let itemCount = 0;
    
    // Check if elements exist
    const priceTypeElement = document.getElementById('price-type');
    const itemCountElement = document.getElementById('item-count');
    const totalElement = document.getElementById('total-price');
    
    // Determine price type (default to market)
    let priceType = 'market';
    let priceTypeText = 'سعر الماركت';
    
    const marketRadio = document.getElementById('market');
    const gomlaRadio = document.getElementById('gomla');
    const gomlaGomlaRadio = document.getElementById('gomla_gomla');
    
    if (gomlaRadio && gomlaRadio.checked) {
      priceType = 'gomla';
      priceTypeText = 'سعر الجملة';
    } else if (gomlaGomlaRadio && gomlaGomlaRadio.checked) {
      priceType = 'gomla_gomla';
      priceTypeText = 'سعر جملة الجملة';
    }
    
    // Update price type display if element exists
    if (priceTypeElement) {
      priceTypeElement.textContent = priceTypeText;
    }
    
    // Calculate total
    const inputs = document.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
      const quantity = parseInt(input.value) || 0;
      if (quantity > 0) {
        itemCount += quantity;
        
        // Get price based on type
        let price = 0;
        if (priceType === 'market') {
          price = parseFloat(input.dataset.marketPrice) || 0;
        } else if (priceType === 'gomla') {
          price = parseFloat(input.dataset.gomlaPrice) || 0;
        } else if (priceType === 'gomla_gomla') {
          price = parseFloat(input.dataset.gomlaGomlaPrice) || 0;
        }
        
        total += quantity * price;
      }
    });
    
    // Update display
    if (itemCountElement) {
      itemCountElement.textContent = itemCount + ' عنصر';
    }
    
    if (totalElement) {
      totalElement.textContent = total.toFixed(2) + ' ج.م';
      
      // Add animation effect
      totalElement.style.transition = 'transform 0.15s ease-in-out';
      totalElement.style.transform = 'scale(1.05)';
      setTimeout(() => {
        totalElement.style.transform = 'scale(1)';
      }, 150);
    }
    
  } catch (error) {
    console.error('Error in calculateTotal:', error);
  }
}

// Make function globally available immediately
window.calculateTotal = calculateTotal;
console.log('calculateTotal function made globally available');

document.addEventListener('DOMContentLoaded', function () {
  console.log('make.js loaded and DOM ready');

  // Category toggle functionality
  const categoryHeaders = document.querySelectorAll('.category-header');
  console.log('Found category headers:', categoryHeaders.length);

  categoryHeaders.forEach(category => {
    category.addEventListener('click', hide_category);
  });

  // Input field functionality
  document.querySelectorAll('input[type="number"]').forEach(input => {
    // Add input listener for real-time updates
    input.addEventListener('input', calculateTotal);
    
    input.addEventListener('focus', () => {
      if (input.value === "0") {
        input.value = "";
      }
    });

    input.addEventListener('blur', () => {
      if (input.value === "") {
        input.value = "0";
      }
      calculateTotal(); // Ensure total is updated on blur
    });

    input.addEventListener('wheel', (event) => {
      event.preventDefault();
      input.blur();
    });
  });

  // Radio button functionality
  const radioButtons = document.querySelectorAll('input[name="market_or_gomla"]');
  radioButtons.forEach(radio => {
    radio.addEventListener('change', calculateTotal);
  });

  // Stock availability display
  document.querySelectorAll('.stock').forEach(stock => {
    if (stock.dataset.quantity === "0") {
      stock.innerHTML = "غير متوفر";
      stock.classList.add('text-red-500');
    }
  });

  // Calculate total on page load
  setTimeout(calculateTotal, 100);

  // Make sure calculateTotal is globally available
  window.calculateTotal = calculateTotal;
  console.log('calculateTotal function made globally available');

  // Search Functionality
  const searchInput = document.getElementById('product-search');
  if (searchInput) {
    // 1. Check URL for search param on load
    const urlParams = new URLSearchParams(window.location.search);
    const searchParam = urlParams.get('search');

    if (searchParam) {
      searchInput.value = searchParam;
      // Trigger filter immediately
      filterProducts(searchParam);
    }

    // 2. Real-time filtering
    searchInput.addEventListener('input', function (e) {
      filterProducts(e.target.value);
    });

    // 3. Enter key to reload with URL param
    searchInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault(); // Prevent form submission if inside a form
        const searchText = this.value.trim();

        // Update URL with search param and reload
        const url = new URL(window.location);
        if (searchText) {
          url.searchParams.set('search', searchText);
        } else {
          url.searchParams.delete('search');
        }
        window.location.href = url.toString();
      }
    });
  }
});

function filterProducts(searchText) {
  searchText = searchText.toLowerCase();

  document.querySelectorAll('.category-container').forEach(categoryContainer => {
    const items = categoryContainer.querySelectorAll('.item-card');
    let hasVisibleItems = false;

    items.forEach(item => {
      const itemNameElement = item.querySelector('.item-name');
      if (itemNameElement) {
        const itemName = itemNameElement.textContent.toLowerCase();
        if (itemName.includes(searchText)) {
          item.style.display = '';
          hasVisibleItems = true;
        } else {
          item.style.display = 'none';
        }
      }
    });

    if (hasVisibleItems) {
      categoryContainer.style.display = '';
    } else {
      categoryContainer.style.display = 'none';
    }
  });
}

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