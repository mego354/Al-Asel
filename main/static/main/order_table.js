// Define updateMaxQuantity function globally so it can be called from HTML
function updateMaxQuantity(input, currentQuantity, maxStock) {
  const newMax = parseInt(currentQuantity) + parseInt(maxStock);
  input.setAttribute('max', newMax);
  
  // Add visual feedback
  if (parseInt(input.value) > newMax) {
    input.classList.add('border-red-500', 'bg-red-50');
    input.classList.remove('border-gray-300');
  } else {
    input.classList.remove('border-red-500', 'bg-red-50');
    input.classList.add('border-gray-300');
  }
}

// Price validation function
function validatePriceChange(input) {
  const newPrice = parseFloat(input.value);
  const originalPrice = parseFloat(input.dataset.originalPrice);
  
  if (isNaN(newPrice) || newPrice < 0) {
    input.value = originalPrice;
    showPriceError('السعر يجب أن يكون رقم صحيح أكبر من أو يساوي صفر');
    return false;
  }
  
  if (newPrice > originalPrice) {
    input.value = originalPrice;
    showPriceError('لا يمكن زيادة السعر عن السعر الأصلي');
    return false;
  }
  
  // Calculate percentage change
  const percentageChange = ((originalPrice - newPrice) / originalPrice) * 100;
  
  if (percentageChange > 100) {
    input.value = originalPrice;
    showPriceError('لا يمكن تقليل السعر بأكثر من 100%');
    return false;
  }
  
  // Clear any previous errors
  clearPriceError();
  return true;
}

// Show price error message
function showPriceError(message) {
  // Remove existing error if any
  clearPriceError();
  
  // Create error message element
  const errorDiv = document.createElement('div');
  errorDiv.id = 'price-error';
  errorDiv.className = 'mt-2 text-sm text-red-600 bg-red-50 border border-red-200 rounded p-2';
  errorDiv.innerHTML = `<i class="fa-solid fa-exclamation-triangle ml-1"></i>${message}`;
  
  // Insert after the total price input
  const totalPriceInput = document.querySelector('input[name="total_order_price"]');
  if (totalPriceInput) {
    totalPriceInput.parentNode.insertBefore(errorDiv, totalPriceInput.parentNode.children[1]);
  }
}

// Clear price error message
function clearPriceError() {
  const existingError = document.getElementById('price-error');
  if (existingError) {
    existingError.remove();
  }
}

// Quantity validation function
function validateQuantityChange(input) {
  try {
    if (!input) {
      console.error('Input element not provided to validateQuantityChange');
      return false;
    }

    const newQuantity = parseInt(input.value);
    const maxQuantity = parseInt(input.getAttribute('max')) || 999999;
    const originalQuantity = parseInt(input.dataset.originalQuantity) || 0;
    
    // If input is empty, allow it (user might be typing)
    if (input.value === '') {
      clearQuantityError(input);
      return true;
    }
    
    if (isNaN(newQuantity) || newQuantity < 0) {
      input.value = originalQuantity;
      showQuantityError('الكمية يجب أن تكون رقم صحيح أكبر من أو يساوي صفر', input);
      return false;
    }
    
    if (newQuantity > maxQuantity) {
      input.value = maxQuantity;
      showQuantityError(`الكمية لا يمكن أن تتجاوز ${maxQuantity} (المخزون المتاح)`, input);
      return false;
    }
    
    // Clear any previous errors
    clearQuantityError(input);
    return true;
  } catch (error) {
    console.error('Error in validateQuantityChange:', error);
    return false;
  }
}

// Show quantity error message
function showQuantityError(message, input) {
  // Remove existing error for this specific input
  clearQuantityError(input);
  
  // Create error message element
  const errorDiv = document.createElement('div');
  errorDiv.className = 'quantity-error mt-1 text-xs text-red-600 bg-red-50 border border-red-200 rounded p-1';
  errorDiv.innerHTML = `<i class="fa-solid fa-exclamation-triangle ml-1"></i>${message}`;
  
  // Insert after the input
  input.parentNode.appendChild(errorDiv);
}

// Clear quantity error message for specific input
function clearQuantityError(input) {
  if (input) {
    const existingError = input.parentNode.querySelector('.quantity-error');
    if (existingError) {
      existingError.remove();
    }
  } else {
    // Clear all quantity errors if no specific input provided
    document.querySelectorAll('.quantity-error').forEach(error => error.remove());
  }
}

document.addEventListener('DOMContentLoaded', function() {
  // Discount functionality
  const discountDisplay = document.querySelector('#discount_display');
  const discountEdit = document.querySelector('#discount_edit');
  const editDiscountBtn = document.querySelector('#edit_discount_btn');
  const newDiscountInput = document.querySelector('#new_discount_input');

  if (editDiscountBtn && discountEdit) {
    editDiscountBtn.addEventListener('click', function() {
      discountEdit.classList.toggle('hidden');
      if (!discountEdit.classList.contains('hidden')) {
        newDiscountInput.focus();
        newDiscountInput.select();
      }
    });
  }

  // Delete item functionality
  document.querySelectorAll('.delete_item').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const itemId = this.getAttribute('data-id');
      const itemName = this.closest('tr').querySelector('td:first-child').textContent.trim();
      
      if (confirm(`هل أنت متأكد من حذف ${itemName} من الطلب؟`)) {
        // Show loading state
        this.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        this.classList.add('opacity-50', 'cursor-not-allowed');
        
        // Redirect to delete URL
        window.location.href = this.href;
      }
    });
  });

  // Auto-save functionality for discount changes
  if (newDiscountInput) {
    newDiscountInput.addEventListener('blur', function() {
      const newValue = this.value;
      if (newValue !== discountDisplay.textContent) {
        // You could add auto-save functionality here
        console.log('Discount changed to:', newValue);
      }
    });
  }

  // Add price validation to total price input
  const totalPriceInput = document.querySelector('input[name="total_order_price"]');
  if (totalPriceInput) {
    // Store original price
    totalPriceInput.dataset.originalPrice = totalPriceInput.value;
    
    // Add validation on input and blur
    totalPriceInput.addEventListener('input', function() {
      validatePriceChange(this);
    });
    
    totalPriceInput.addEventListener('blur', function() {
      validatePriceChange(this);
    });
  }

  // Add quantity validation to all quantity inputs
  document.querySelectorAll('input[name^="quantity_"]').forEach(input => {
    console.log('Setting up validation for input:', input.name, 'max:', input.getAttribute('max'), 'original:', input.dataset.originalQuantity);
    
    input.addEventListener('input', function() {
      console.log('Input event triggered for:', this.name, 'value:', this.value);
      validateQuantityChange(this);
    });
    
    input.addEventListener('blur', function() {
      console.log('Blur event triggered for:', this.name, 'value:', this.value);
      validateQuantityChange(this);
    });
  });
});



