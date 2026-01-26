-- Coffee category / Bean Bros supplier
INSERT INTO products
(
 category_id,
 name_en, name_ko,
 purchase_price, sale_price,
 discount_price, discount_start_at, discount_end_at,
 is_weight_based, weight_kg,
 supplier_id,
 is_stock_managed, stock_quantity,
 is_taxable,
 barcode,
 is_fixed_price,
 nickname,
 created_at, updated_at
)
VALUES
(
 (SELECT id FROM categories WHERE name_en='Coffee' LIMIT 1),
 'Americano', '아메리카노',
 2.50, 4.50,
 NULL, NULL, NULL,
 0, NULL,
 (SELECT id FROM suppliers WHERE supplier_name='Bean Bros' LIMIT 1),
 1, 100,
 1,
 '880000000001',
 1,
 '아아',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
),
(
 (SELECT id FROM categories WHERE name_en='Coffee' LIMIT 1),
 'Latte', '라떼',
 3.00, 5.50,
 4.90, datetime('now','-1 day'), datetime('now','+7 day'),
 0, NULL,
 (SELECT id FROM suppliers WHERE supplier_name='Bean Bros' LIMIT 1),
 1, 80,
 1,
 '880000000002',
 1,
 '라떼',
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
),
(
 (SELECT id FROM categories WHERE name_en='Coffee' LIMIT 1),
 'Espresso', '에스프레소',
 2.00, 3.50,
 NULL, NULL, NULL,
 0, NULL,
 (SELECT id FROM suppliers WHERE supplier_name='Bean Bros' LIMIT 1),
 1, 60,
 1,
 '880000000003',
 1,
 NULL,
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

-- Dessert category / Sweet Factory supplier
INSERT INTO products
(
 category_id,
 name_en, name_ko,
 purchase_price, sale_price,
 discount_price, discount_start_at, discount_end_at,
 is_weight_based, weight_kg,
 supplier_id,
 is_stock_managed, stock_quantity,
 is_taxable,
 barcode,
 is_fixed_price,
 nickname,
 created_at, updated_at
)
VALUES
(
 (SELECT id FROM categories WHERE name_en='Dessert' LIMIT 1),
 'Cheesecake', '치즈케이크',
 3.50, 6.90,
 NULL, NULL, NULL,
 0, NULL,
 (SELECT id FROM suppliers WHERE supplier_name='Sweet Factory' LIMIT 1),
 1, 40,
 1,
 '880000000010',
 1,
 NULL,
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
),
(
 (SELECT id FROM categories WHERE name_en='Dessert' LIMIT 1),
 'Cookie', '쿠키',
 0.60, 1.80,
 NULL, NULL, NULL,
 0, NULL,
 (SELECT id FROM suppliers WHERE supplier_name='Sweet Factory' LIMIT 1),
 1, 200,
 1,
 '880000000011',
 1,
 NULL,
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);

-- Beverages top category / Fresh Farm supplier (weight-based example)
INSERT INTO products
(
 category_id,
 name_en, name_ko,
 purchase_price, sale_price,
 discount_price, discount_start_at, discount_end_at,
 is_weight_based, weight_kg,
 supplier_id,
 is_stock_managed, stock_quantity,
 is_taxable,
 barcode,
 is_fixed_price,
 nickname,
 created_at, updated_at
)
VALUES
(
 (SELECT id FROM categories WHERE name_en='Beverages' LIMIT 1),
 'Banana (kg)', '바나나(kg)',
 NULL, 6.00,
 NULL, NULL, NULL,
 1, NULL,
 (SELECT id FROM suppliers WHERE supplier_name='Fresh Farm' LIMIT 1),
 0, NULL,
 0,
 '880000000020',
 0,
 NULL,
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);