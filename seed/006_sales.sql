INSERT INTO sales
(
 member_id,
 subtotal_amount, discount_amount, total_amount,
 payment_method, status, sold_at,
 created_at, updated_at
)
VALUES
(
 (SELECT id FROM members WHERE member_id='MEM-0001' LIMIT 1),
 4.50, 0.00, 4.50,
 'CARD', 'PAID', CURRENT_TIMESTAMP,
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
),
(
 (SELECT id FROM members WHERE member_id='MEM-0002' LIMIT 1),
 12.40, 1.00, 11.40,
 'CASH', 'PAID', datetime('now','-1 day'),
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
),
(
 NULL,
 6.90, 0.00, 6.90,
 'CARD', 'PAID', datetime('now','-2 day'),
 CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
);