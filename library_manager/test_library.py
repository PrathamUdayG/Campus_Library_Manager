# test_library.py
import unittest
from models import LibraryItem, Book, Magazine, DVD, Member


class TestLibraryManager(unittest.TestCase):
    def setUp(self):
        # Reset counter if needed or record base count
        self.base_count = LibraryItem.total_items

    def test_abstract_class_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            LibraryItem("Generic Title", 999)

    def test_incomplete_subclass_cannot_be_instantiated(self):
        class IncompleteItem(LibraryItem):
            def describe(self):
                return "Incomplete"
            # Missing late_fee implementation

        with self.assertRaises(TypeError):
            IncompleteItem("Incomplete Item", 998)

    def test_item_creation_and_total_items(self):
        initial = LibraryItem.total_items
        b = Book("Clean Code", 10, "Robert C. Martin")
        m = Magazine("Scientific American", 11, 500)
        d = DVD("The Matrix", 12, 136)
        self.assertEqual(LibraryItem.total_items, initial + 3)
        self.assertEqual(Book.total_items, LibraryItem.total_items)

    def test_descriptions(self):
        b = Book("Design Patterns", 20, "GoF")
        m = Magazine("Wired", 21, 105)
        d = DVD("Interstellar", 22, 169)
        self.assertEqual(b.describe(), "Book: Design Patterns by GoF (ID 20)")
        self.assertEqual(m.describe(), "Magazine: Wired Issue #105 (ID 21)")
        self.assertEqual(d.describe(), "DVD: Interstellar (169 mins) (ID 22)")

    def test_late_fees(self):
        b = Book("Book A", 30, "Author A")
        m = Magazine("Mag B", 31, 1)
        d = DVD("DVD C", 32, 120)

        # 3 days late: Book (2 * 3 = 6), Mag (1 * 3 = 3), DVD (5 * 3 = 15)
        self.assertEqual(b.late_fee(3), 6)
        self.assertEqual(m.late_fee(3), 3)
        self.assertEqual(d.late_fee(3), 15)

        # 0 days late or negative
        self.assertEqual(b.late_fee(0), 0)
        self.assertEqual(m.late_fee(-2), 0)

    def test_encapsulation_private_attributes(self):
        b = Book("Private Test", 40, "Author")
        member = Member("Charlie", 201)

        with self.assertRaises(AttributeError):
            _ = b.__available

        with self.assertRaises(AttributeError):
            _ = member.__borrowed

        self.assertTrue(b.is_available())
        self.assertEqual(member.borrowed_titles(), [])

    def test_borrow_and_return_flow(self):
        b = Book("Python 101", 50, "A. Rao")
        member = Member("Alice", 202, max_items=2)

        self.assertTrue(b.is_available())
        member.borrow(b)
        self.assertFalse(b.is_available())
        self.assertEqual(member.borrowed_titles(), ["Python 101"])

        # Return on time
        fee = member.return_item(b, days_late=0)
        self.assertEqual(fee, 0)
        self.assertTrue(b.is_available())
        self.assertEqual(member.borrowed_titles(), [])

    def test_borrow_already_borrowed(self):
        b = Book("Shared Book", 60, "Author")
        alice = Member("Alice", 301)
        bob = Member("Bob", 302)

        alice.borrow(b)
        with self.assertRaises(ValueError) as cm:
            bob.borrow(b)
        self.assertIn("already borrowed", str(cm.exception))

    def test_borrow_limit_exceeded(self):
        member = Member("Bob", 401, max_items=1)
        b1 = Book("Book 1", 71, "Author")
        b2 = Book("Book 2", 72, "Author")

        member.borrow(b1)
        with self.assertRaises(ValueError) as cm:
            member.borrow(b2)
        self.assertIn("reached the borrowing limit", str(cm.exception))

    def test_return_not_borrowed(self):
        member = Member("Alice", 501)
        b = Book("Unborrowed Book", 80, "Author")

        with self.assertRaises(ValueError) as cm:
            member.return_item(b)
        self.assertIn("was not borrowed", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
