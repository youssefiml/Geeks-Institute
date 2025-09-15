DROP TABLE IF EXISTS menu_items_chefs;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS chefs;
DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE chefs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE,
    phone VARCHAR(30)
);

CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(140) NOT NULL,
    description TEXT,
    price NUMERIC(8,2) NOT NULL,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE menu_items_chefs (
    menu_item_id INTEGER REFERENCES menu_items(id) ON DELETE CASCADE,
    chef_id INTEGER REFERENCES chefs(id) ON DELETE CASCADE,
    PRIMARY KEY (menu_item_id, chef_id)
);

INSERT INTO categories (name) VALUES
('Starters'), ('Mains'), ('Desserts'), ('Beverages'), ('Salads'), ('Sides'), ('Vegan'), ('Seafood'), ('Grill'), ('Pasta');

INSERT INTO chefs (name, email, phone) VALUES
('Fatima El Amrani', 'fatima@example.com','+212600000001'),
('Ahmed Bennani', 'ahmed@example.com','+212600000002'),
('Youssef Oua', 'youssef@example.com','+212600000003'),
('Sara Haddad', 'sara@example.com','+212600000004'),
('Rania Khalid', 'rania@example.com','+212600000005'),
('Omar Z', 'omar@example.com','+212600000006'),
('Mounir Said', 'mounir@example.com','+212600000007'),
('Imane R', 'imane@example.com','+212600000008'),
('Khalid B', 'khalid@example.com','+212600000009'),
('Nora L', 'nora@example.com','+212600000010');

INSERT INTO menu_items (name, description, price, category_id) VALUES
('Marinated Olives', 'Olives marinated in herbs and lemon zest.', 4.50, 1),
('Tomato & Burrata', 'Fresh burrata with heirloom tomatoes.', 9.00, 5),
('Grilled Sea Bass', 'Whole sea bass with lemon butter sauce.', 18.50, 8),
('Ribeye Steak', '10oz ribeye grilled to order.', 22.00, 9),
('Spaghetti Carbonara', 'Classic carbonara with pecorino and guanciale.', 12.00, 10),
('Chocolate Lava Cake', 'Warm cake with a gooey chocolate center.', 6.50, 3),
('Caesar Salad', 'Crisp romaine with parmesan and anchovy dressing.', 7.25, 5),
('Vegetable Tagine', 'Slow-cooked vegetables with ras el hanout.', 11.50, 7),
('Sweet Potato Fries', 'Crispy sweet potato fries with aioli.', 5.00, 6),
('Mint Tea', 'Traditional Moroccan mint tea.', 2.50, 4);

INSERT INTO menu_items_chefs (menu_item_id, chef_id) VALUES
(1,1),(1,2),
(2,3),(2,4),
(3,5),(3,6),
(4,6),(4,7),
(5,8),(5,2),
(6,9),(6,10),
(7,1),(7,5),
(8,4),(8,7),
(9,2),(9,10),
(10,3),(10,1);
