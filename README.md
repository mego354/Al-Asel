# Al Asel Store Management System

Al Asel is a kit shop owned by a friend, specializing in selling equipment and related items. Currently, transactions are managed using Excel, which may not be the most efficient or accurate method. To address this, I envisioned a specialized system tailored for managing the store's operations, from inventory and orders to client management and sales analysis. This report outlines the key components and functionalities of the proposed system.

## 🚀 Live Demo
[Visit the Website](https://mego354.github.io/Al-Asel/)

## Technologies Used
- Django
- JavaScript
- HTML
- CSS
- Chart.js
- Google Fonts
- Google Charts
- Font Awesome

## Features

### File Structure
- **HTML Pages**: Over 25 HTML pages and 2 layout templates (one for main pages, one for alternate pages).
- **Static Files**: Logo, main CSS file containing all styles.
- **JavaScript Files**: Functions utilized across different HTML pages to optimize code reuse.

### Running the Application
1. **Creating an Order**:
   - Cashiers can select products, specify quantities, and select the client and order type (regular, wholesale).
   - Additional actions such as adding offers, modifying prices or quantities, and adding/removing items are possible.
   
2. **Inserting an Order**:
   - Users can input orders made by the owner, specifying quantities, identifying the seller, and selecting the accepting branch.
   - Orders are sorted from the most recent to the oldest, allowing for easy tracking and management.
   - Features are available for modifying orders, including adjusting prices and ensuring orders are closed once edited to prevent potential bugs.

### Clients and Orders View
- **Clients**: View all clients and their orders, with search functionality by name or ID. Each client page displays orders and payment details, including unpaid amounts.
- **Orders**: Orders are arranged by the most recent ones, with search functionality by order ID. Orders contain links for editing, deleting, and managing payments.

### Sales Analysis
- **Sales Overview**: Comprehensive overview of sales data across all years.
- **Yearly Breakdown**: Analyze sales trends and revenue generated for each year.
- **Monthly Analysis**: Explore sales data on a monthly basis, tracking fluctuations and identifying peak periods.
- **Graphical Representation**: Bar graphs and pie charts from Chart.js and Google Charts enhance data interpretation.
- **Detailed Reports**: Specific sales metrics, including total revenue, average order value, and top-selling products.

### Project Distinctiveness and Complexity
- Utilization of around 7 models, demonstrating originality and depth in design.
- Integration of external resources (Chart.js, Google Charts, Font Awesome icons, Google Fonts) enhancing the visual appeal and functionality of the application.
- The system addresses real-life business needs, offering a tailored solution for managing a retail store's operations efficiently.
- Accommodates various scales of operation and is not limited to mobile devices, ensuring flexibility and usability across different contexts.

### Development Insights
- **Model Creation**: Created models for customers, orders, items, and categories.
- **OrderItem Class**: To manage order items efficiently, including tracking prices and quantities.
- **Order Management**: Implemented features to manage order items, including saving, editing, and deleting orders while maintaining consistency in item prices and quantities.

### Views and Templates
- **Order Views**: Functions for making, editing, and adding items to orders, ensuring only items not already in the order are visible.
- **Client and Order Management**: Flexible editing, deleting, and adding features for both orders and client details.
- **Sales Views**: Graphical representation of sales data, with detailed analysis and reports for strategic decision-making.

### Additional Features
- **Sidebar**: Links to create new items, clients, and categories. View all orders, inserted orders, and orders with unpaid amounts. Comprehensive item view for editing items.

## Conclusion
The Al Asel Store management system is a comprehensive solution designed to streamline operations and enhance efficiency in managing inventory, orders, clients, and sales analysis. Its distinctive features, complexity, and integration of external resources make it a robust solution for modern retail management needs. I am extremely proud of achieving such a high level of flexibility and efficiency.

[Demo Video](https://youtu.be/0q1bPAbHGvk)

**THANKS!**
