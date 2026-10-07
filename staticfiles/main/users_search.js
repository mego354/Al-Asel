document.addEventListener('DOMContentLoaded', function() {
  const customerSearch = document.querySelector('#customer_search');
  const usersDiv = document.querySelector('#users_search');
  
  if (customerSearch && usersDiv) {
    customerSearch.addEventListener('keyup', function() {
      usersDiv.innerHTML = "";
      
      if (this.value === "all") {
        let userDiv = document.createElement('div');
        userDiv.className = 'p-2 bg-gray-100 rounded-lg mb-2';
        userDiv.innerHTML = `<a href="/users/" class="block text-primary hover:text-primary/80 font-medium">عرض جميع العملاء</a>`;
        usersDiv.appendChild(userDiv);
      } else if (this.value.trim().length > 0) {
        fetch(`/users_search/${this.value.trim()}`)
          .then(response => response.json())
          .then(users => {
            if (users.length === 0) {
              let noResultsDiv = document.createElement('div');
              noResultsDiv.className = 'p-3 text-center text-gray-500 text-sm';
              noResultsDiv.innerHTML = 'لا توجد نتائج';
              usersDiv.appendChild(noResultsDiv);
            } else {
              users.forEach((user, index) => {
                let userDiv = document.createElement('div');
                userDiv.className = 'p-2 bg-gray-50 hover:bg-gray-100 rounded-lg mb-2 transition-colors';
                userDiv.innerHTML = `
                  <a href="/users/${user.id}" class="block text-gray-900 hover:text-primary">
                    <div class="flex items-center justify-between">
                      <span class="font-medium">${user.name}</span>
                      <span class="text-sm text-gray-500">#${user.id}</span>
                    </div>
                  </a>
                `;
                usersDiv.appendChild(userDiv);
                
                // Add animation delay
                setTimeout(() => {
                  userDiv.classList.add('opacity-100');
                }, index * 50);
              });
            }
          })
          .catch(error => {
            console.error('Error fetching users:', error);
            let errorDiv = document.createElement('div');
            errorDiv.className = 'p-3 text-center text-red-500 text-sm';
            errorDiv.innerHTML = 'حدث خطأ في البحث';
            usersDiv.appendChild(errorDiv);
          });
      }
    });
  }
});
