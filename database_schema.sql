-- Create necessary tables for the financial application

-- Users table for authentication (simplified)
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employees table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    position VARCHAR(50),
    hire_date DATE NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Salary table
CREATE TABLE salaries (
    salary_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    base_salary DECIMAL(10, 2) NOT NULL,
    bonus DECIMAL(10, 2) DEFAULT 0,
    payment_date DATE NOT NULL,
    payment_status ENUM('pending', 'paid') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Expenses table
CREATE TABLE expenses (
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    category VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    expense_date DATE NOT NULL,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

-- Invoices table
CREATE TABLE invoices (
    invoice_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    invoice_number VARCHAR(20) UNIQUE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE NOT NULL,
    status ENUM('draft', 'sent', 'paid', 'cancelled') DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
); 