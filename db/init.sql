CREATE TABLE IF NOT EXISTS measurements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(1) NOT NULL,
    age INTEGER NOT NULL,
    height NUMERIC(5,1) NOT NULL,
    weight NUMERIC(5,1) NOT NULL,
    bmi NUMERIC(4,1),
    category VARCHAR(50),
    calories INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO measurements (name, gender, age, height, weight, bmi, category, calories) VALUES
('Иван', 'm', 21, 180, 75, 23.1, 'Норма', 2751),
('Мария', 'f', 20, 165, 50, 18.4, 'Недостаток массы', 1747),
('Алексей', 'm', 35, 175, 95, 31.0, 'Ожирение', 2248);
