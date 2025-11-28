
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asel.settings')
django.setup()

from main.models import Item, Customer, BranchStock

def migrate_stock():
    print("Starting Stock Migration...")

    # 1. Get or Create Main Store Branch
    # We look for a customer with is_shop=True that represents the main store.
    # If none exists, we create one.
    main_store = Customer.objects.filter(is_shop=True, name__icontains="Main").first()
    
    if not main_store:
        # Fallback: try any shop
        main_store = Customer.objects.filter(is_shop=True).first()
        
    if not main_store:
        print("No existing shop found. Creating 'Main Store'...")
        main_store = Customer.objects.create(
            name="Main Store",
            number=1999999999, # Dummy number
            is_shop=True
        )
    
    print(f"Migrating stock to branch: {main_store.name}")

    # 2. Migrate Item Stock
    items = Item.objects.all()
    count = 0
    for item in items:
        if item.stock_quantity > 0:
            # Check if stock already exists
            stock, created = BranchStock.objects.get_or_create(branch=main_store, item=item)
            if created:
                stock.quantity = item.stock_quantity
                stock.save()
                count += 1
                print(f"Moved {item.stock_quantity} of {item.name} to {main_store.name}")
            else:
                print(f"Stock for {item.name} already exists in {main_store.name}. Skipping.")
    
    print(f"Migration Complete. Moved stock for {count} items.")

if __name__ == "__main__":
    migrate_stock()
