  DROP TABLE IF EXISTS cart;
  DROP TABLE IF EXISTS users;
  DROP TABLE IF EXISTS products;
  DROP TABLE IF EXISTS cart;
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
                        active TEXT NOT NULL,
                        category TEXT NOT NULL,
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

INSERT INTO products (active, category, title, brand, price, descript,
                        img_route, ram, memory, os_system, release, color)
       VALUES ("True", "Smartphones","iPhone 15 5G (6GB/128GB)", "apple", 799.00,
             "iPhone 15 offers Dynamic Island, a 48MP main camera and a USB-C port — all in a durable design that combines aluminum and color-infused glass.",
             "/static/product_img/iphone_15_128.jpeg", 6, 128, "ios", 2023, "black"),
            ("True", "Smartphones","Samsung Galaxy S23 FE (Exynos) 5G (8GB/128GB)", "samsung", 488.88,
             "Epic moments are now accessible to everyone. The Galaxy S23 FE opens the door for more people to experience the extraordinary. With long-lasting power and stunning night shots, the phone becomes your gateway to epic memories that last.",
             "/static/product_img/sam_s23_fe_256.jpeg", 8, 128, "android", 2023, "black"),
             ("True", "Laptops","Apple MacBook Pro 16", "Apple", 3790.00,
             "MacBook Pro is for professionals looking for maximum power in areas like video and audio processing, as well as professional developers.",
             "/static/product_img/Apple_MacBook_Pro_16.jpeg", 32, 1000, "IOS", 2021, "Silver"),
             ("True", "Laptops","Lenovo ThinkPad P16v Gen 2 (Intel) 16", "Lenovo", 3063.00,
             "If you want a workstation that's great performance but light and thin at the same time, the Thinkpad P16v Gen2 is the perfect laptop for you.",
             "/static/product_img/Lenovo_ThinkPad_P16v_Gen_2_(Intel).jpeg", 64, 1000, "Windows", 2024, "Black"),
             ("True", "Laptops","Dell XPS 16 9640 16.3", "Dell", 4888.00,
             "Run demanding applications more smoothly and faster with powerful Intel ® Core™ Ultra 9 processors. Performance-class Intel ® Core™ Ultra processors provide a dedicated engine to unlock AI capabilities on the PC.",
             "/static/product_img/Dell_XPS_16_9640_16.3.jpeg", 64, 2000, "Windows", 2024, "Silver"),
             ("True", "Laptops","Razer Blade 15", "Razer", 2222.00,
             "With Razer Blade 15, the real power will always be where you are. Featuring the latest 13th Gen Intel® Core™ i7 processors, NVIDIA® GeForce RTX™ 40 Series graphics, and a stunning 240Hz QHD display, enjoy unrivalled performance packed into one of the thinnest 15 RTX gaming laptop bezels ever made.",
             "/static/product_img/Razer_Blade_15.jpeg", 16, 1000, "Windows", 2023, "Black"),
             ("True", "Smartphones","Xiaomi 14 Ultra 5G", "Xiaomi", 1140.00,
             "The Xiaomi 14 Ultra adopts a brand new integrated 6M42 high-strength aluminum frame material, with the metal frame extending to the back of the frame, doubling the robustness compared to the Xiaomi 13 Pro.",
             "/static/product_img/Xiaomi_14_Ultra_5G.jpeg", 16, 512, "Android", 2023, "Black"),
             ("True", "Smartphones","Google Pixel 9 Pro XL 5G", "Google", 1140.00,
             "The Pixel 9 Pro XL's overhead new design features a silky matte glass back, a beautiful double-finished camera bar, and a polished metal frame that's as good as it looks.",
             "/static/product_img/Google_Pixel_9_Pro_XL_5G.jpeg", 16, 256, "Android", 2023, "Obsidian");



CREATE TABLE cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                    );

  DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    the_date TEXT NOT NULL,
                    shipping_cost REAL NOT NULL,
                    total_cost REAL NOT NULL,
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
