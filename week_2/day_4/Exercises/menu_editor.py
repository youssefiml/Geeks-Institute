from menu_item import MenuItem
from menu_manager import MenuManager

def show_user_menu():
    while True:
        print("View an Item (V)")
        print("Add an Item (A)")
        print("Delete an Item (D)")
        print("Update an Item (U)")
        print("Show the Menu (S)")
        selected_item = input("what do you want: ").strip().lower()

        if selected_item == 'v':
            view_item()
        elif selected_item == 'a':
            add_item_to_menu()
        elif selected_item == 'd':
            remove_item_from_menu()
        elif selected_item == 'u':
            update_item_from_menu()
        elif selected_item == 's':
            show_full_menu()
        else:
            print("Wrong choice!")

def add_item_to_menu():
    item_name = input("write the item name: ")
    item_price = float(input("write the item price: "))
    item = MenuItem(item_name, item_price)
    response, status = item.save_item()
    print(response)

def remove_item_from_menu():
    item_name = input("Enter the name of the item to remove: ")
    item = MenuManager.get_by_name(item_name)
    if item:
        response, status = item.delete_item()
        print(response)
    else:
        print("Item not found")

def update_item_from_menu():
    item_name = input("Enter the name of the item to update: ")
    item = MenuManager.get_by_name(item_name)
    if item:
        new_name = input("Enter the new name: ")
        new_price = float(input("Enter the new price: "))
        response, status = item.update_item(new_name, new_price)
        print(response)
    else:
        print("Item not found")

def view_item():
    item_name = input("Enter the name of the item to view: ")
    item = MenuManager.get_by_name(item_name)
    if item:
        print(f"Item found: {item.item_name} - ${item.item_price}")
    else:
        print("Item not found.")

def show_full_menu():
    items = MenuManager.all_items()
    if items:
        print("Full Menu:")
        for item in items:
            print(f"{item.item_name} - ${item.item_price}")
    else:
        print("No items found.")

if __name__ == "__main__":
    show_user_menu()