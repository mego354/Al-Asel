Al Asel Store:

Al Asel is a kit shop owned by a friend, specializing in selling equipment and various related items. Currently, transactions are managed using Excel, which may not be the most efficient or accurate method. To address this, I envisioned a specialized system tailored for managing the store's operations, from inventory and orders to client management and sales analysis. This report outlines the key components and functionalities of the proposed system.

Distinctiveness and Complexity:

File Structure:

The application comprises over 25 HTML pages and 2 layout templates. One layout is dedicated to standard or main pages, while the other serves for alternate pages. Additionally, there are static files including a logo and a main CSS file containing all styles. JavaScript files contain functions utilized across different HTML pages to optimize code reuse.

Running the Application:

Creating an Order:
On the home page, the cashier can select products to include in an order. The items are covered in a category box, which can be hidden by clicking on it for a cleaner interface. After specifying quantities and selecting the client (regular or branch has sold the order to random buyer) and type of the order (regular, wholesale), the form is submitted to proceed to the order's page. Here, additional actions such as adding offers, modifying prices or quantities, and removing or adding items are possible.

Inserting an Order:
Alternatively, users can input orders already made by the owner. This involves specifying quantities for each item, identifying the seller of the order, and selecting an accepting branch. Orders are sorted in a sorted way starting from the most recent order to the oldest, allowing for easy tracking and management. Different features are available for modifying orders, including adjusting prices due to changes and ensuring orders are closed once edited to prevent potential bugs.

The application also facilitates creating items, categories, and clients (both suppliers and buyers). It allows for recording partial payments and displaying unpaid amounts, with details accessible by clicking on client names (in the top of the client's page under the percentage bar which is the percent of all the money that the user have to pay in general and how much is the rest of it).

then the view of clients, orders:
orders arranged by the most recent ones, and you can just type the id and click enter to open a specific order,
besides the clients search bar can help you by serching in the name, id of the user and get you the all possible results for your search and the enter leads you to the most suggest in the top.

each client page contains all of his orders, arranged as well as the user can hide months or years to focus on a specific duration.

if the client is also a branch page it their page must have a link in the top leads you to the provided orders and also the percentage and the payments details


Details of Sales Pages:

The sales section of the application offers in-depth analysis and visualization of sales data. It includes the following components:

Sales Overview: Provides a comprehensive overview of sales data across all years, offering insights into overall performance.

Yearly Breakdown: Allows users to delve into sales data for each year individually. Users can analyze sales trends, and revenue generated for each year.

Monthly Analysis: Within each yearly breakdown, users can further explore sales data on a monthly basis. This granular view enables tracking of monthly sales fluctuations and identification of peak periods. Users can also hide each month's orders or the whole year for better focus and analysis besides that the only opened year is the recent one.

Graphical Representation: Utilizes various chart types, such as bar graphs and pie charts, from chartjs and Google Charts. These graphical representations enhance data interpretation and facilitate quick insights into sales trends.

Detailed Reports: Provides detailed reports containing specific sales metrics, including total revenue, average order value, and top-selling products. These reports offer valuable insights for strategic decision-making and business planning.

Project Distinctiveness and Complexity:

The project is distinct and complex due to the following reasons:

Utilization of around 7 models, demonstrating originality and depth in design.
Integration of external resources such as Chart.js, Google Charts, Font Awesome icons, and Google Fonts, enhancing the visual appeal and functionality of the application.
The system addresses real-life business needs, offering a tailored solution for managing a retail store's operations efficiently.
It accommodates various scales of operation and is not limited to mobile devices, ensuring flexibility and usability across different contexts.

i've used:
chartjs, google fonts, google charts and font awesome for the icons all as cdn s no need for installing any other libraries than django's

what i did: 

i started by cresting the model of the customer, order, item, category to specify the items,
then i faced a problem which is that the order contains a lot of items but the each item could be more than one, after research i found that i could make another class 

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_itemss')
    quantity = models.PositiveIntegerField()
    real_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    gomla_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    market_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)


which contains the number of the items that i want to add to the order and that was a way satisfing as a result
besides i could  make it more useful because now i can detrmine the price for that piece of items as well and in case i've updated the item's price a long the way that piece of order price would not change which leads the past orders prices stable
so as a result i reached a really good structure 

that's not the end in that part of models because after a bit when i was working on the orders that inserted to the store i found another issue that each piece of the order influence on the like if i anserted 2 pieces of item1 then item1.quantity must be edited and if i deleted that item from the order(which is an easy reachable feture after creating the order) i though that it was easier for me to reverse that influence in the delete function of the class:

    def delete(self, *args, **kwargs):
        self.update_item_prices(reverse=True)
        super().delete(*args, **kwargs)

    def update_item_prices(self, reverse=False):
        if reverse:
            factor = -1
        else:
            factor = 1

        self.item.real_price += factor * self.change_real_price
        self.item.gomla_price += factor * self.change_gomla_price
        self.item.market_price += factor * self.change_market_price
        self.item.stock_quantity += factor * self.quantity
        self.item.save()
        self.item.update_item()

        self.order.total_order_price += factor * self.total_real_price
        self.order.save()
so for sure it works on both save and delete which made that class works automatically and has it's influence stable without any function in my view.by

as a result of well structured models, you can imagine the range of control and ability i had in the other steps along the way of creating a way useful well designed app.

views.py
after the login,logout view there is the some useful views as make_order(which allow me to save the order in db), add_items which is way useful route to allow the save order to be editeable and could add another item to the order but with a great useablity that the OrderItem.item in the order must not be visible while i'm adding another items because it's allready there in the oreder so reached all the items aleady in the order by
    un_wanted_items = OrderItem.objects.filter(order=order).values_list('item', flat=True)
and then i restrucured the the items would be visible on add_items.html by
    for category in categories:
        items = Item.objects.exclude(id__in=un_wanted_items)
        items_object[f"{category.name}"] = items.filter(category=category)

besides edit_orderm which allow the admin to edit letirally every thing like amount of items amount of discount or the final price and due to the conflict of that the discount may be edited at the same time as the full price as well as the amount of items which may be a huge bug so i strucured that function to work in arranged way that it'd first look at the discount if changed then edit the the full price and save the model then return
if not then look at the full price if it's not the same then edit the discout(as i said that they have influence on each other) and then return
if it's all ok?
then look for every order_item update it the update the full price and the discount then return

from the features in this part is that the order could've rest money(unpaid money yet "dept") becuase in whole sale that thing might happenn alot, then there is a feature to edit or remove or add that particular part of order aswell the payment is maybe wholesale or not so that the admin could also change the by a click on a button with it's function(change rank)

which in conclusion way too flexable of editing deleting adding everything and that strucure works the same on the exported orders and the inserted ones

now lets move to the second part of the project

users & orders

users(clients)
in the main view of users there are all the users as well as the branches and the orders in revesed way by date, there is a search for each which works on custmers name or id and if clicked enter while searching you'd be taken to the first suggestion's appeared to you and if there is not you'd be taken to and error page which by the way you'd be taken to if any wrong usege happed and specify the error and suggest a way out of it(which i think it's one of many owerfull detail in the site).
in every client page there is a persent line which specify that if the cliend bought n items with s usd and they've paid 70% of s then the persent line would be blue and has "70%" on it (under 50% would be red & over 80% would be green)
clicking on the client name would show a box that contains all of these details and specifing which orders that has un paid money and how much is that "rest money" and a link for view each 
under that there is the main part of the client order, and if branch, there'd be aroute for the recieved orders "coming orders" with the same info and strucure.
orders are orderd by years(each year in a box that could be hidden and shown) and in each year orders still orderd by their month all in reverse to show the latest orders first

orders
it's search only works by the id and only recieve numbers for that, and it's not the only way to view orders it's just a quick way to get a specific order (in the side bar there is a link for all orders and all coming orders which is well designed for viewing this amount of data)
and in each order as i explained the edit, delete, add features there is also a link to put unpaid money(rest_money) or pay it if there(amount'd be visible in the same place).

the deffrence between the order and coming_order view is the that while the user could change the item's price (because it may happened that the he bought it with a new price) but after finishing the edit of the order he must close it (done editing?) so that the user would not be able to edit that again to avoid any bug would happed if and old order has an edit in one of it's item's price
as if each coming order has the change rate of price of specific item change_real_price, change_gomla_price, change_market_price

which has it's influence automatically as in :

    def save(self, *args, **kwargs):
        self.total_real_price = self.quantity * self.single_real_price
        self.total_gomla_price = self.quantity * self.single_gomla_price
        self.total_market_price = self.quantity * self.single_market_price

        self.change_real_price = self.single_real_price - self.item.real_price
        self.change_gomla_price = self.single_gomla_price - self.item.gomla_price
        self.change_market_price = self.single_market_price - self.item.market_price

        super().save(*args, **kwargs)

        self.update_item_prices()

    def delete(self, *args, **kwargs):
        self.update_item_prices(reverse=True)
        super().delete(*args, **kwargs)

    def update_item_prices(self, reverse=False):
        if reverse:
            factor = -1
        else:
            factor = 1

        self.item.real_price += factor * self.change_real_price
        self.item.gomla_price += factor * self.change_gomla_price
        self.item.market_price += factor * self.change_market_price
        self.item.stock_quantity += factor * self.quantity
        self.item.save()
        self.item.update_item()

        self.order.total_order_price += factor * self.total_real_price
        self.order.save()

and creating new coming_order would close every older one anyway in case that the user forgot to close it and if the user deleted the last coming_order so the first older one would get be open again because it's now the latest order and has the latest prices virsion.

final part is the most intresting one

sales

in sales there is two main graphical charts with the main data the owner would wanna be aware of the some boxes also could be hidden or not but as default the current year box would be opened for the admin.
anyway in each year there would be another chart with more the same types of data and link for the working months (months that has sales during it only) clicking on the link would take the user of the site to another route contains much more detailed data of the sales in that month also with some charts to represent some sales details.

sidebar

contains some extra features as creating new item, client, category
besides some links to view all orders, all coming(inserted) orders, orders that has unpaid money on it and a all items view in which there would be all items so that the user could be able to edit the item.


Conclusion:

In conclusion, the Al Asel Store management system is a comprehensive solution designed to streamline operations and enhance efficiency in managing inventory, orders, clients, and sales analysis. Its distinctive features, complexity, and integration of external resources make it a robust solution for modern retail management needs.

Iam way so grateful happy and proud of achieve that huge range of flexabilty and efficiency

Demo video: https://youtu.be/0q1bPAbHGvk

THANKS!
