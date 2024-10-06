  DROP TABLE IF EXISTS cart;
  DROP TABLE IF EXISTS users;
  DROP TABLE IF EXISTS products;
  DROP TABLE IF EXISTS cart;
  DROP TABLE IF EXISTS orders;
  DROP TABLE IF EXISTS orderss_products;
CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    hash TEXT NOT NULL,
                    access TEXT NOT NULL);

INSERT INTO users (username, hash, access)
       VALUES ("admin", "scrypt:32768:8:1$py2xjAE75jftzhz9$8d51f666de58e2a9badf899beb900bfb30d40184f918b98574f53e00f34d36f4a866fc8e25cfc14db86e25c59377d6ca33c38fa5903e6c563fba0d3a9dca22dd", "admin");



CREATE TABLE products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        brand TEXT NOT NULL,
                        price FLOAT NOT NULL,
                        descript TEXT,
                        img_route TEXT,
                        ram INTEGER,
                        memory INTEGER,
                        os_system TEXT,
                        release INTEGER,
                        color TEXT
                    );

INSERT INTO products (title, brand, price, descript,
                        img_route, ram, memory, os_system, release, color)
       VALUES ("iPhone 15 5G (6GB/128GB)", "apple", 799.00,
             "iPhone 15 offers Dynamic Island, a 48MP main camera and a USB-C port — all in a durable design that combines aluminum and color-infused glass.",
             "/static/product_img/iphone_15_128.jpeg", 6, 128, "ios", 2023, "black"),
            ("Samsung Galaxy S23 FE (Exynos) 5G (8GB/128GB)", "samsung", 488.88,
             "Epic moments are now accessible to everyone. The Galaxy S23 FE opens the door for more people to experience the extraordinary. With long-lasting power and stunning night shots, the phone becomes your gateway to epic memories that last.",
             "/static/product_img/sam_s23_fe_256.jpeg", 8, 128, "android", 2023, "black");


CREATE TABLE cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                    );

CREATE TABLE orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    the_date TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                    );

CREATE TABLE orderss_products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id)
                    );
