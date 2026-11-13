# main.py
from models import Book, DVD, Magazine, Member

# Create items of each type
book = Book("Python 101", 1, "A. Rao")
magazine = Magazine("Tech Monthly", 2, 42)
dvd = DVD("Inception", 3, 148)

# Create two members (Alice with default max_items=3, Bob with max_items=1)
alice = Member("Alice", 101)
bob = Member("Bob", 102, max_items=1)

print("=== 1. Borrowing with Error Handling (Item Already Borrowed) ===")
try:
    alice.borrow(book)
    print("Alice borrowed:", book.describe())
    bob.borrow(book)  # should fail: already borrowed
except ValueError as e:
    print("Could not borrow:", e)

print("\n=== 2. Borrow Limit and Not-Borrowed Error Handling ===")
# Trigger borrow-limit error: Bob's limit is 1
try:
    bob.borrow(magazine)
    print("Bob borrowed:", magazine.describe())
    bob.borrow(dvd)  # should fail: limit reached
except ValueError as e:
    print("Could not borrow:", e)

# Trigger not-borrowed error: Alice attempts to return an item she never borrowed
try:
    alice.return_item(dvd)  # should fail: not in Alice's borrowed list
except ValueError as e:
    print("Could not return:", e)

# Successful return demonstrating late fee calculation
print("\n--- Successful Return & Late Fee ---")
fee = alice.return_item(book, days_late=3)
print(f"Alice returned '{book.title}' (3 days late). Late fee charged: Rs {fee}")

print("\n=== 3. Polymorphism: One Loop, No Type Checks ===")
items = [book, magazine, dvd]
for item in items:
    print(item.describe(), "-> late fee for 3 days: Rs", item.late_fee(3))

print("\n=== 4. Class Attribute Shared by All Objects ===")
print("Total items created:", Book.total_items)

print("\n=== 5. Encapsulation Proof ===")
# Attempting direct access to private attribute __available
try:
    print(book.__available)
except AttributeError as e:
    print("Direct private access (book.__available) failed as expected:", e)

print("Safe access via getter is_available():", book.is_available())

# Attempting direct access to private attribute __borrowed
try:
    print(bob.__borrowed)
except AttributeError as e:
    print("Direct private access (bob.__borrowed) failed as expected:", e)

print("Safe access via getter borrowed_titles():", bob.borrowed_titles())
