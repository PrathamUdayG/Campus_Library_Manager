# Campus Library Manager

A Python application designed for campus libraries to manage lending and returning for three kinds of items: Books, Magazines, and DVDs. The system demonstrates core Object-Oriented Programming (OOP) concepts including inheritance, polymorphism, encapsulation, class attributes, and robust exception handling.

---

## Project Structure

```text
library_manager/
│── models.py          # Abstract LibraryItem, concrete subclasses (Book, Magazine, DVD), and Member
│── main.py            # Demonstration script covering all brief requirements and checkpoints
│── test_library.py    # Comprehensive unit tests verifying models, error handling, and rates
│── output.txt         # Console output from running main.py
└── README.md          # Project documentation and conceptual reflection
```

---

## How to Run

### Requirements
- Python 3.12 or later
- No third-party packages required (uses Python standard library exclusively)

### Running the Main Demonstration
```bash
python main.py
```
*(Or from the repository root: `python library_manager/main.py`)*

### Running Unit Tests
```bash
python -m unittest discover -s library_manager
```

---

## Core Features & Design

1. **Inheritance & Abstraction**:
   - `LibraryItem` is an abstract base class inheriting from `abc.ABC`.
   - Declares common attributes (`title`, `item_id`, `__available`), state-management methods (`is_available`, `mark_borrowed`, `mark_returned`), and abstract methods (`late_fee`, `describe`).
   - Concrete subclasses (`Book`, `Magazine`, `DVD`) call `super().__init__(title, item_id)` and implement specific daily rates and descriptions.

2. **Polymorphic Late Fee Calculation**:
   - **Book**: Rs 2 / day
   - **Magazine**: Rs 1 / day
   - **DVD**: Rs 5 / day
   - Heterogeneous lists of items can be iterated through polymorphically to compute late fees without `isinstance()` or `if/elif` type checks.

3. **Encapsulation & Information Hiding**:
   - `__available` and `__borrowed` are private attributes mangled by Python.
   - External callers interact with state solely through public methods (`is_available()`, `borrowed_titles()`, `borrow()`, `return_item()`).

4. **Robust Exception Handling**:
   - `borrow()` raises a `ValueError` with descriptive messages if an item is already borrowed or if the member has reached their borrowing limit (`max_items`).
   - `return_item()` raises a `ValueError` if attempting to return an item not present in the member's borrowed list.

---

## Reflection Questions & Answers

### 1. Why is LibraryItem abstract, and what happens if DVD forgets to write late_fee()?
`LibraryItem` is made abstract because a generic item does not possess a specific rate or category and should serve solely as a common blueprint rather than a concrete instance. If `DVD` inherits from `LibraryItem` without implementing the `@abstractmethod` `late_fee()`, Python considers `DVD` to be abstract as well. Attempting to instantiate `DVD` will raise a runtime `TypeError` stating that the class cannot be instantiated without implementing abstract method `'late_fee'`.

### 2. What happens when you read item.__available from outside the class, and why do we use is_available() instead?
Reading `item.__available` from outside the class raises an `AttributeError` because Python's name mangling renames private double-underscore attributes to `_LibraryItem__available`. We use the public getter `is_available()` instead to preserve encapsulation and expose read-only state safely. This protects internal invariants and ensures that item availability can only be altered through authorized methods like `mark_borrowed()` and `mark_returned()`.

### 3. What is the difference between LibraryItem.total_items and self.title?
`LibraryItem.total_items` is a class attribute shared across the class and all subclasses, acting as a global counter for all library items instantiated. In contrast, `self.title` is an instance attribute tied strictly to an individual object, storing the unique title of that specific item. Modifying `LibraryItem.total_items` affects the shared state seen across all instances, whereas modifying `self.title` only affects that single instance.
