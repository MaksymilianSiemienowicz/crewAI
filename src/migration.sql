CREATE TABLE price_list (
    id SERIAL PRIMARY KEY,
    technique VARCHAR(50) NOT NULL,
    size VARCHAR(50) NOT NULL,
    estimated_time_days INT NOT NULL,
    price NUMERIC(10, 2) NOT NULL 
);

INSERT INTO price_list (technique, size, estimated_time_days, price) VALUES
    ('realistic', 'A4', 7, 300.00),
    ('realistic', 'A3', 10, 450.00),
    ('realistic', 'A2', 14, 700.00),
    ('realistic', '50x70 cm', 14, 600.00),
    ('realistic', '70x100 cm', 20, 1200.00),
    ('abstract', 'A4', 5, 250.00),
    ('abstract', 'A3', 8, 400.00),
    ('abstract', 'A2', 12, 650.00),
    ('abstract', '50x70 cm', 10, 500.00),
    ('abstract', '70x100 cm', 15, 1000.00),
    ('oil', 'A4', 10, 350.00),
    ('oil', 'A3', 15, 550.00),
    ('oil', 'A2', 20, 900.00),
    ('oil', '50x70 cm', 18, 800.00),
    ('oil', '70x100 cm', 25, 1500.00),
    ('watercolor', 'A4', 5, 200.00),
    ('watercolor', 'A3', 8, 350.00),
    ('watercolor', 'A2', 12, 600.00),
    ('watercolor', '50x70 cm', 10, 550.00),
    ('watercolor', '70x100 cm', 15, 1100.00),
    ('charcoal', 'A4', 4, 150.00),
    ('charcoal', 'A3', 6, 250.00),
    ('charcoal', 'A2', 8, 400.00),
    ('charcoal', '50x70 cm', 7, 350.00),
    ('charcoal', '70x100 cm', 10, 700.00),
    ('digital', 'A4', 3, 100.00),
    ('digital', 'A3', 5, 200.00),
    ('digital', 'A2', 7, 350.00),
    ('digital', '50x70 cm', 6, 300.00),
    ('digital', '70x100 cm', 10, 600.00);
