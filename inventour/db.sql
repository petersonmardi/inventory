DROP TABLE IF EXISTS user;
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(100) UNIQUE NOT NULL,
  password VARCHAR(120) NOT NULL
);
-- 1. Categories
CREATE TABLE IF NOT EXISTS "category" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Subcategories
CREATE TABLE IF NOT EXISTS "subcategory" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE
);

-- 3. Products
CREATE TABLE IF NOT EXISTS "product" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    barcode VARCHAR(50) UNIQUE,
    subcategory_id INTEGER,
    FOREIGN KEY (subcategory_id) REFERENCES subcategory(id) ON DELETE SET NULL
);

-- 4. Product Variants
CREATE TABLE IF NOT EXISTS "product_variant" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    size VARCHAR(50),
    color VARCHAR(50),
    price DECIMAL(10,2),
    stock INT DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

-- 5. Product Images
CREATE TABLE IF NOT EXISTS "product_image" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    image_url TEXT NOT NULL,
    alt_text VARCHAR(255),
    is_primary BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

-- 6. Tags
CREATE TABLE IF NOT EXISTS "tag" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- 7. Product Tags (many-to-many)
CREATE TABLE IF NOT EXISTS "product_tag" (
    product_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (product_id, tag_id),
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
);

-- 8. Variant Discounts
CREATE TABLE IF NOT EXISTS "variant_discount" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    variant_id INTEGER,
    discount_percent DECIMAL(5,2),
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (variant_id) REFERENCES product_variant(id) ON DELETE CASCADE
);

-- 9. Product Translations
CREATE TABLE IF NOT EXISTS "product_translation" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    language_code VARCHAR(10),
    translated_name VARCHAR(150),
    translated_description TEXT,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE,
    UNIQUE (product_id, language_code)
);
