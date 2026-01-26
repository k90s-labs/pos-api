PRAGMA foreign_keys = OFF;

DELETE FROM sale_items;
DELETE FROM sales;
DELETE FROM products;
DELETE FROM members;
DELETE FROM suppliers;
DELETE FROM categories;
DELETE FROM sales_catalog_items;
DELETE FROM sales_catalogs;

DELETE FROM sqlite_sequence
WHERE name IN (
  'sale_items',
  'sales',
  'products',
  'members',
  'suppliers',
  'categories',
  'sales_catalog_items',
  'sales_catalogs'
);

PRAGMA foreign_keys = ON;