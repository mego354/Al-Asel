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
});

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



