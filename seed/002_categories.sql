INSERT INTO categories
(name_en, name_ko, parent_id, is_active, sort_order, created_at, updated_at)
VALUES
('Beverages', '음료', NULL, 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Food', '푸드', NULL, 1, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO categories
(name_en, name_ko, parent_id, is_active, sort_order, created_at, updated_at)
VALUES
('Coffee', '커피', (SELECT id FROM categories WHERE name_en='Beverages' LIMIT 1), 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Dessert', '디저트', (SELECT id FROM categories WHERE name_en='Food' LIMIT 1), 1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);