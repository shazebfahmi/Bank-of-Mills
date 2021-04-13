-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 17, 2020 at 08:53 PM
-- Server version: 8.0.13-4
-- PHP Version: 7.2.24-0ubuntu0.18.04.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Q4WIoIq4gO`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE `account` (
  `account_id` int(9) NOT NULL,
  `customer_id` int(9) NOT NULL,
  `account_type` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `balance` int(11) NOT NULL,
  `message` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `account_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_updated` timestamp NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`account_id`, `customer_id`, `account_type`, `balance`, `message`, `last_updated`, `status`) VALUES
(114021101, 100000275, 'savings', 24000, 'account credited successfully', '2020-06-17 20:52:07', 1),
(114021140, 100000212, 'current', 43000, 'amount deposited successfully', '2020-06-17 20:46:21', 1),
(114021141, 100000224, 'savings', 24000, 'account credited successfully', '2020-06-17 20:52:07', 1),
(114021142, 100000280, 'current', 4000, 'amount deposited successfully', '2020-06-17 20:50:26', 1),
(114021143, 100000265, 'current', 11800, 'account debited successfully', '2020-06-17 20:52:07', 1),
(114021144, 100000280, 'savings', 2220, 'account deleted successfully', '2020-06-17 20:40:52', 0),
(114021145, 100000281, 'savings', 2300, 'account deleted successfully *', '2020-06-17 20:42:06', 0),
(114021146, 100000218, 'current', 12000, 'amount withdrawn successfully', '2020-06-17 20:49:09', 1),
(114021147, 100000265, 'savings', 24000, 'account credited successfully', '2020-06-17 20:52:07', 1),
(114021148, 100000280, 'savings', 24000, 'account credited successfully', '2020-06-17 20:52:07', 1);

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `customer_id` int(9) NOT NULL,
  `customer_ssn` int(9) NOT NULL,
  `name` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `age` int(3) NOT NULL,
  `address` mediumtext COLLATE utf8_unicode_ci NOT NULL,
  `city` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `customer_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `state` varchar(15) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci ROW_FORMAT=COMPACT;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`customer_id`, `customer_ssn`, `name`, `age`, `address`, `city`, `state`) VALUES
(100000212, 123456789, 'Parinitha', 35, 'Rajajinagar,bangalore', 'BENGALURU', 'KARNATAKA'),
(100000218, 123456782, 'mari', 20, '3rd cross Shivaji nagar ', 'Mysore', 'KARNATAKA'),
(100000222, 123456783, 'Shravan', 45, '4th block manojnagar', 'Mangalore', 'Karnataka'),
(100000224, 123456736, 'Mohak', 19, '21st main kalyan nagar', 'Mangalore', 'Karnataka'),
(100000228, 987654321, 'Suman', 15, '2nd cross near palace ground', 'mysore', 'Karnataka'),
(100000256, 987766541, 'Soma', 21, 'balaji nagar Niranjan Circle Lakshmipura', 'Hassan', 'KARNATAKA'),
(100000262, 123456777, 'Prajwal', 19, 'vijaynagar,Bangalore', 'BENGALURU', 'KARNATAKA'),
(100000264, 123456666, 'Rahim', 23, '10th cross, gangamma garden', 'BENGALURU', 'KARNATAKA'),
(100000265, 100000265, 'shazeb', 46, '2nd cross MG road', 'tumkur', 'Karnataka'),
(100000266, 100000299, 'Sahzeb', 21, '8th main pulikeshi nagar', 'Mangalore', 'Karnataka'),
(100000268, 100000277, 'Bhim', 35, 'RR circle santhe maidana', 'Hubli', 'Karnataka'),
(100000270, 100000270, 'Sohan', 32, '4th cross Richmond road', 'Dharwad', 'Karnataka'),
(100000273, 100000399, 'Manjunath', 77, 'kushal nagar 8th main', 'Mysore', 'Karnataka'),
(100000274, 100000499, 'Srihari', 32, '8th main jayanagar', 'Bangalore', 'Karnataka'),
(100000275, 232143432, 'Ruthvik', 22, '2nd cross malleshvaram', 'Bengaluru', 'Karnataka'),
(100000276, 876123454, 'Sumangala', 54, 'ramnagar 4th block', 'Mangalore', 'Karnataka'),
(100000280, 878787878, 'Suhas S', 27, '3rd stage nagarbhavi', 'Bangalore', 'Karnataka'),
(100000281, 412412412, 'Sham', 22, 'Vijaynagar 2nd cross', 'Bangalore', 'Karnataka');

-- --------------------------------------------------------

--
-- Table structure for table `customer_status`
--

CREATE TABLE `customer_status` (
  `customer_id` int(9) NOT NULL,
  `message` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `last_updated` timestamp NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `customer_status`
--

INSERT INTO `customer_status` (`customer_id`, `message`, `last_updated`, `status`) VALUES
(100000212, 'customer created successfully', '2020-06-14 17:50:33', 1),
(100000218, 'customer created successfully', '2020-06-14 17:50:33', 1),
(100000222, 'customer created successfully', '2020-06-14 17:50:33', 1),
(100000224, 'customer created successfully', '2020-06-14 17:50:33', 1),
(100000228, 'customer created successfully', '2020-06-14 17:52:43', 1),
(100000256, 'customer deleted successfully', '2020-06-17 20:26:10', 0),
(100000262, 'customer created successfully', '2020-06-15 08:52:58', 1),
(100000264, 'customer update complete', '2020-06-17 20:23:55', 1),
(100000265, 'customer created successfully', '2020-06-15 14:25:10', 1),
(100000266, 'customer created successfully', '2020-06-16 08:05:15', 1),
(100000268, 'customer deleted successfully', '2020-06-17 20:26:50', 0),
(100000270, 'customer created successfully', '2020-06-16 13:06:12', 1),
(100000273, 'customer update complete', '2020-06-17 20:24:37', 1),
(100000274, 'customer created successfully', '2020-06-16 16:07:53', 1),
(100000275, 'customer update complete', '2020-06-17 20:25:20', 1),
(100000276, 'customer created successfully', '2020-06-16 18:35:42', 1),
(100000280, 'customer created successfully', '2020-06-17 09:53:20', 1),
(100000281, 'customer deleted successfully', '2020-06-17 20:42:06', 0);

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `user_id` varchar(15) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `emp_type` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`user_id`, `password`, `emp_type`) VALUES
('Prajwal-M-R', 'Prajwal-M-R', 'executive'),
('shaz', 'shaz', 'cashier'),
('shravan212', 'shravan212', 'executive'),
('shreya-emanti', 'shreya-emanti', 'cashier'),
('shreyasgp', 'shreyasgp', 'cashier');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `transaction_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  `description` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `acc_type` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `amount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`transaction_id`, `customer_id`, `account_id`, `description`, `acc_type`, `amount`) VALUES
(100000201, 100000275, 114021101, 'deposit', 'savings', 2000),
(100000202, 100000212, 114021140, 'deposit', 'current', 30000),
(100000203, 100000224, 114021141, 'deposit', 'savings', 2300),
(100000204, 100000280, 114021142, 'deposit', 'current', 3600),
(100000205, 100000265, 114021143, 'deposit', 'current', 13000),
(100000206, 100000280, 114021144, 'deposit', 'savings', 2220),
(100000207, 100000281, 114021145, 'deposit', 'savings', 2300),
(100000208, 100000218, 114021146, 'deposit', 'current', 23000),
(100000209, 100000265, 114021147, 'deposit', 'savings', 14000),
(100000210, 100000280, 114021144, 'deposit', 'savings', 23000),
(100000211, 100000212, 114021140, 'deposit', 'current', 13000),
(100000212, 100000218, 114021146, 'withdraw', 'current', 11000),
(100000213, 100000280, 114021142, 'withdraw', 'Current', 500),
(100000214, 100000280, 114021148, 'deposit', 'Savings', 500),
(100000215, 100000280, 114021142, 'deposit', 'current', 900),
(100000216, 100000265, 114021143, 'withdraw', 'current', 700),
(100000217, 100000265, 114021143, 'withdraw', 'Current', 500),
(100000218, 100000265, 114021147, 'deposit', 'Savings', 500);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`account_id`),
  ADD KEY `foreign_key2` (`customer_id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `customer_ssn` (`customer_ssn`);

--
-- Indexes for table `customer_status`
--
ALTER TABLE `customer_status`
  ADD KEY `foreign key 1` (`customer_id`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `foreign key3` (`customer_id`),
  ADD KEY `foreign key4` (`account_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `account_id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=114021149;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `customer_id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100000282;

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=100000219;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `account`
--
ALTER TABLE `account`
  ADD CONSTRAINT `foreign_key_2` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `customer_status`
--
ALTER TABLE `customer_status`
  ADD CONSTRAINT `foreign_key_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `foreign_key_3` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `foreign_key_4` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
