// Test if script is loading
console.log('make.js script loaded');

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
    
    console.log('Elements found:', {
      priceType: !!priceTypeElement,
      itemCount: !!itemCountElement,
      total: !!totalElement
    });
    
    if (!priceTypeElement || !itemCountElement || !totalElement) {
      console.error('Required elements not found for calculateTotal');
      return;
    }
    
    // Get selected price type
    const selectedPriceType = document.querySelector('input[name="market_or_gomla"]:checked');
    if (!selectedPriceType) {
      console.error('No price type selected');
      return;
    }
    
    const isGomla = selectedPriceType.value === 'gomla';
    
    // Update price type display
    if (isGomla) {
      priceTypeElement.textContent = 'سعر الجملة';
    } else {
      priceTypeElement.textContent = 'سعر الماركت';
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
    itemCountElement.textContent = itemCount + ' عنصر';
    
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
window.calculateTotalFallback = function() {
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

document.addEventListener('DOMContentLoaded', function() {
  console.log('make.js loaded and DOM ready');
  
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



  