-- 가장 최근 sale(오늘) 1건에 아메리카노 1개
INSERT INTO sale_items
(
 sale_id,
 product_id,
 product_name_en, product_name_ko,
 barcode,
 unit_price,
 quantity,
 weight_kg,
 line_total
)
VALUES
(
 (SELECT id FROM sales ORDER BY sold_at DESC LIMIT 1),
 (SELECT id FROM products WHERE barcode='880000000001' LIMIT 1),
 'Americano', '아메리카노',
 '880000000001',
 4.50,
 1,
 NULL,
 4.50
);

-- 어제 sale(두번째 최근)에 라떼 1개 + 쿠키 2개
INSERT INTO sale_items
(
 sale_id, product_id,
 product_name_en, product_name_ko,
 barcode, unit_price, quantity, weight_kg, line_total
)
VALUES
(
 (SELECT id FROM sales ORDER BY sold_at DESC LIMIT 1 OFFSET 1),
 (SELECT id FROM products WHERE barcode='880000000002' LIMIT 1),
 'Latte', '라떼',
 '880000000002', 5.50, 1, NULL, 5.50
),
(
 (SELECT id FROM sales ORDER BY sold_at DESC LIMIT 1 OFFSET 1),
 (SELECT id FROM products WHERE barcode='880000000011' LIMIT 1),
 'Cookie', '쿠키',
 '880000000011', 1.80, 2, NULL, 3.60
);

-- 이틀 전 sale(세번째 최근)에 치즈케이크 1개
INSERT INTO sale_items
(
 sale_id, product_id,
 product_name_en, product_name_ko,
 barcode, unit_price, quantity, weight_kg, line_total
)
VALUES
(
 (SELECT id FROM sales ORDER BY sold_at DESC LIMIT 1 OFFSET 2),
 (SELECT id FROM products WHERE barcode='880000000010' LIMIT 1),
 'Cheesecake', '치즈케이크',
 '880000000010', 6.90, 1, NULL, 6.90
);