CREATE DATABASE IF NOT EXISTS chocolate_world;
USE chocolate_world;

CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    price INT NOT NULL,
    image VARCHAR(150)
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    address VARCHAR(255),
    phone VARCHAR(20),
    payment_method VARCHAR(10),
    total INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO menu_items (name, description, price, image) VALUES
('Chocolate Cake',               'Soft chocolate cake and delicious',                70,  'chocolate cake.JPEG.jpeg'),
('Tiramisu',                     'Light and creamy Italian dessert',                 80,  'Tiramisu.JPEG.jpeg'),
('Toffee Latte',                 'Sweet coffee made with espresso',                  100, 'Toffee latte.JPEG.jpeg'),
('Cupcake',                      'Small soft cake baked in a cup',                   35,  'Cupcake.JPEG.jpeg'),
('Cookies',                      'Small sweet with Belgian chocolate',               60,  'Cookies.JPEG.jpeg'),
('Brownies',                     'Rich chocolate dessert',                            80,  'Brownies.JPEG.jpeg'),
('Hot Chocolate with Marshmallows','Warm comforting drink with rich chocolate',      120, 'Hot chocolate with marshmallows.JPEG.jpeg'),
('Mini Chocolate Tart',          'Small elegant dessert filled with chocolate ganache', 40, 'Mini chocolate tarts.JPEG.jpeg');
