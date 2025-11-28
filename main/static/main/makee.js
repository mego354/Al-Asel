// Test if script is loading
console.log('makee.js script loaded');

// Define calculateTotal function immediately (before DOM ready)
function calculateTotal() {
  try {
    console.log('calculateTotal called');
    let total = 0;
    let itemCount = 0;

    // Check if elements exist
    const priceTypeElement = document.getElementById('price-type');
    const itemCountElement = document.getElementById('item-count');
    const totalElement = document.getElementById('total-price');

    // If elements don't exist (e.g. in create_store_order), just return or handle gracefully
    if (!totalElement) {
      return;
    }

    // Get selected price type
    const selectedPriceType = document.querySelector('input[name="market_or_gomla"]:checked');
    // If no price type (e.g. coming_order doesn't have market/gomla radio), default to something or skip
    const isGomla = selectedPriceType ? selectedPriceType.value === 'gomla' : false;

    // Update price type display if element exists
    if (priceTypeElement) {
      if (isGomla) {
        priceTypeElement.textContent = 'سعر الجملة';
      } else {
        priceTypeElement.textContent = 'سعر الماركت';
      }
    }

    // Calculate total for all quantity inputs
    document.querySelectorAll('input[type="number"][name^="quantity_"]').forEach(input => {
      const quantity = parseFloat(input.value) || 0;
      const marketPrice = parseFloat(input.getAttribute('data-market-price')) || 0;
      const gomlaPrice = parseFloat(input.getAttribute('data-gomla-price')) || 0;

      if (quantity > 0) {
        itemCount++;
        const price = isGomla ? gomlaPrice : marketPrice;
        total += quantity * price;
      }
    });

    // Update total display
    totalElement.textContent = total.toFixed(2) + ' ج.م';

    // Update item count
    if (itemCountElement) {
      itemCountElement.textContent = itemCount + ' عنصر';
    }

    // Add animation effect
    totalElement.style.transition = 'transform 0.15s ease-in-out';
    totalElement.style.transform = 'scale(1.05)';
    setTimeout(() => {
      totalElement.style.transform = 'scale(1)';
    }, 150);
  } catch (error) {
    console.error('Error in calculateTotal:', error);
  }
}

// Make function globally available immediately
window.calculateTotal = calculateTotal;
console.log('calculateTotal function made globally available');

// Add fallback function in case the main one fails
window.calculateTotalFallback = function () {
  console.log('Using fallback calculateTotal function');
  try {
    const totalElement = document.getElementById('total-price');
    if (totalElement) {
      totalElement.textContent = '0.00 ج.م';
    }
  } catch (error) {
    console.error('Fallback function also failed:', error);
  }
};

document.addEventListener('DOMContentLoaded', function () {
  console.log('makee.js loaded and DOM ready');

  // Category toggle functionality
  const categoryHeaders = document.querySelectorAll('.category-header');
  console.log('Found category headers:', categoryHeaders.length);

  categoryHeaders.forEach(category => {
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