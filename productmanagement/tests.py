from django.test import TestCase
from .models import Stock  # Import your Stock model

class StockModelTestCase(TestCase):
    def test_create_stock(self):
        # Create a new Stock instance
        new_stock = Stock(
            name="Example Stock",
            price=100,
            quantity="10",
            stock=50,
            description="This is a sample stock item.",
            category_id=1,  # Replace with the actual category ID
            proOffer=5,
        )
        
        # Save the new stock item to the database
        new_stock.save()
        
        # Retrieve the stock item from the database
        retrieved_stock = Stock.objects.get(pk=new_stock.pk)
        
        # Assert that the retrieved stock matches the created stock
        self.assertEqual(new_stock.name, retrieved_stock.name)
        self.assertEqual(new_stock.price, retrieved_stock.price)
        # Add more assertions for other fields as needed

    # Add more test methods for other scenarios as needed
