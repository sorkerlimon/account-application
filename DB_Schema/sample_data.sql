-- Insert single admin user
INSERT INTO users (email, password) VALUES
('admin@company.com', 'admin123');

-- Insert sample employees
INSERT INTO employees (first_name, last_name, email, phone, department, position, hire_date) VALUES
('John', 'Doe', 'john.doe@company.com', '1234567890', 'IT', 'Senior Developer', '2022-01-01'),
('Jane', 'Smith', 'jane.smith@company.com', '0987654321', 'HR', 'HR Manager', '2022-02-15'),
('Mike', 'Johnson', 'mike.johnson@company.com', '5555555555', 'Finance', 'Accountant', '2022-03-01');

-- Insert sample salaries
INSERT INTO salaries (employee_id, base_salary, bonus, payment_date, payment_status) VALUES
(1, 75000.00, 5000.00, '2024-03-01', 'paid'),
(2, 65000.00, 3000.00, '2024-03-01', 'paid'),
(3, 55000.00, 2000.00, '2024-03-01', 'paid');

-- Insert sample expenses
INSERT INTO expenses (category, amount, description, expense_date, created_by) VALUES
('Office Supplies', 500.00, 'Monthly office supplies', '2024-03-01', 1),
('Travel', 1200.00, 'Business trip to New York', '2024-03-05', 1),
('Equipment', 2000.00, 'New laptops', '2024-03-10', 2);

-- Insert sample invoices
INSERT INTO invoices (employee_id, invoice_number, amount, issue_date, due_date, status) VALUES
(1, 'INV-2024-001', 6666.67, '2024-03-01', '2024-03-15', 'paid'),
(2, 'INV-2024-002', 5666.67, '2024-03-01', '2024-03-15', 'sent'),
(3, 'INV-2024-003', 4750.00, '2024-03-01', '2024-03-15', 'draft'); 