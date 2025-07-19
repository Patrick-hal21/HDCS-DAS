class Node():
    def __init__(self, data, metadata=None):
        self.data = data
        self.metadata = metadata # will be address, etc.
        self.next = None

class LinkedList():
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, data, metadata=None):
        new_node = Node(data, metadata)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        print(f"Added node with data: {data}")

    def display(self):
        if self.head is None:
            # print("List is empty.")
            return "List is empty."
        
        print("Linked List contents:")
        current = self.head
        while current:
            print(f"{current.data} with data {current.metadata}", end=" -> ")
            current = current.next
        print("None")

        # to display Address data
        # current = self.head
        # # if current.metadata is not None:
        # while current:
        #     print(current.metadata, end=" -> ")
        #     current = current.next
        # print("None")

    def search(self, value):
        result = []
        current = self.head
        while current:
            # currently focus on data only not metadata
            if current.data == value:
                print(f"Value {value} found with metadata {current.metadata}.")
                result.append(current)
                return result # return the very first found data
            current = current.next

        print(f"Value {value} not found.")
        return False

    def insert(self, position, data):
        new_node = Node(data)
        if position == 0:
            new_node.next = self.head
            self.head = new_node
            if self.tail is None:
                self.tail = new_node
            print(f"Inserted {data} at position 0.")
            return
        current = self.head
        for _ in range(position - 1):
            if current is None:
                print("Position out of bounds.")
                return
            current = current.next
        if current is None:
            print("Position out of bounds.")
            return
        new_node.next = current.next
        current.next = new_node
        if new_node.next is None:
            self.tail = new_node
        print(f"Inserted {data} at position {position}.")

    def remove(self, value, metadata=None):
        if self.head is None:
            print("List is empty. Nothing to delete.")
            return False
        current = self.head
        if current.data == value:
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                self.head = self.head.next
            print(f"Deleted the head node with value {value} and matching metadata.")
            result = f"Deleted the value '{value}' and matching metadata."
            return result, True
        
        while current.next:
            if current.next.data == value and current.next.metadata == metadata:
                if current.next == self.tail:
                    self.tail = current
                    print(f"Deleted the tail node with value {value} and matching metadata.")
                    result = f"Deleted the value '{value}' and matching metadata."
                else:
                    print(f"Deleted a middle node with value {value} and matching metadata.")
                    result = f"Deleted the value '{value}' and matching metadata."
                current.next = current.next.next
                return result, True
            current = current.next

        print(f"No node found with value {value} and matching metadata.")
        result = f"No node found with value {value} and matching metadata."
        return result, False

    

# ll = LinkedList()
# ll.add(1, ("Micahel", "Yangon"))
# ll.add("John", "Yangon")
# ll.add("Mike")
# ll.add(20, "Yangon") # to add Address data
# ll.add(30)
# ll.display()
# ll.insert(1, 15)
# ll.display()
# ll.search("Patrick")
# ll.remove("John", "Yangon")
# ll.display()

# myll = [1, 2]
# a, b = myll
# print(a, b)
