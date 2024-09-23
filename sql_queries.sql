create database 'gitam_transportation_db';

use 'gitam_transportation_db';

CREATE TABLE ev_buses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bus_name VARCHAR(255) NOT NULL,
    source VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL
);


INSERT INTO ev_buses (bus_name, source, destination, date, total_seats, available_seats)
VALUES
    ('EV-101', 'Front Gate', 'Back Gate', '2024-09-24', 50, 50),
    ('EV-102', 'Front Gate', 'Shivaji Building', '2024-09-24', 40, 40),
    ('EV-103', 'Front Gate', 'Boys Hostel', '2024-09-24', 60, 60),
    ('EV-104', 'Back Gate', 'Front Gate', '2024-09-25', 55, 55),
    ('EV-105', 'Back Gate', 'Shivaji Building', '2024-09-25', 45, 45),
    ('EV-105', 'Back Gate', 'Boys Hostel', '2024-09-25', 45, 45),
    ('EV-105', 'Shivaji Building', 'Front Gate', '2024-09-25', 45, 45),
    ('EV-105', 'Shivaji Building', 'Back Gate', '2024-09-25', 45, 45),
    ('EV-105', 'Shivaji Building', 'Boys Hostel', '2024-09-25', 45, 45);
