-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1:3306
-- Время создания: Июн 09 2024 г., 22:50
-- Версия сервера: 8.0.19
-- Версия PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `l2eauto`
--

-- --------------------------------------------------------

--
-- Структура таблицы `brands`
--

CREATE TABLE `brands` (
  `ID` int NOT NULL,
  `BrandName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `CountryID` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `brands`
--

INSERT INTO `brands` (`ID`, `BrandName`, `CountryID`) VALUES
(1, 'Zeekr', 1),
(2, 'Li Xiang', 2);

-- --------------------------------------------------------

--
-- Структура таблицы `cars`
--

CREATE TABLE `cars` (
  `ID` int NOT NULL,
  `BrandID` int DEFAULT NULL,
  `ModelID` int DEFAULT NULL,
  `Color` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Price` decimal(10,2) DEFAULT NULL,
  `SeatCount` int DEFAULT NULL,
  `Length` decimal(10,2) DEFAULT NULL,
  `Width` decimal(10,2) DEFAULT NULL,
  `Height` decimal(10,2) DEFAULT NULL,
  `MaxSpeed` decimal(10,2) DEFAULT NULL,
  `FuelConsumption` decimal(10,2) DEFAULT NULL,
  `StockCount` int DEFAULT NULL,
  `EngineID` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `cars`
--

INSERT INTO `cars` (`ID`, `BrandID`, `ModelID`, `Color`, `Price`, `SeatCount`, `Length`, `Width`, `Height`, `MaxSpeed`, `FuelConsumption`, `StockCount`, `EngineID`) VALUES
(1, 1, 1, 'Blue', '30000.00', 5, '5000.00', '2000.00', '1500.00', '250.00', '15.00', 10, 1),
(2, 2, 2, 'White', '50000.00', 7, '5500.00', '2100.00', '1600.00', '240.00', '12.00', 5, 1);

-- --------------------------------------------------------

--
-- Структура таблицы `countries`
--

CREATE TABLE `countries` (
  `ID` int NOT NULL,
  `CountryName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `CountryCode` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `countries`
--

INSERT INTO `countries` (`ID`, `CountryName`, `CountryCode`) VALUES
(1, 'China', 'CN'),
(2, 'China', 'CN');

-- --------------------------------------------------------

--
-- Структура таблицы `customers`
--

CREATE TABLE `customers` (
  `ID` int NOT NULL,
  `LastName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `FirstName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `MiddleName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `PassportSeries` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `PassportNumber` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `IssueDate` date DEFAULT NULL,
  `IssuedBy` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `RegistrationAddress` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ResidentialAddress` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `customers`
--

INSERT INTO `customers` (`ID`, `LastName`, `FirstName`, `MiddleName`, `Email`, `Phone`, `PassportSeries`, `PassportNumber`, `IssueDate`, `IssuedBy`, `RegistrationAddress`, `ResidentialAddress`) VALUES
(1, 'Smith', 'John', 'Doe', 'john.smith@example.com', '111-222-3333', 'AB', '987654', '2020-01-01', 'Gov Office', '123 Main St', '123 Main St'),
(2, 'Doe', 'Jane', NULL, 'jane.doe@example.com', '222-333-4444', 'CD', '876543', '2019-01-01', 'Gov Office', '456 Elm St', '456 Elm St');

-- --------------------------------------------------------

--
-- Структура таблицы `departments`
--

CREATE TABLE `departments` (
  `ID` int NOT NULL,
  `Name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Department_Phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Description` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `departments`
--

INSERT INTO `departments` (`ID`, `Name`, `Department_Phone`, `Description`) VALUES
(1, 'Юридический отдел', '123-456', 'Legal Department'),
(2, 'Отдел продаж', '234-567', 'Sales Department'),
(3, 'Отдел технического обслуживания', '345-678', 'Technical Service Department'),
(4, 'Отдел маркетинга', '456-789', 'Marketing Department'),
(5, 'Бухгалтерия', '567-890', 'Accounting Department');

-- --------------------------------------------------------

--
-- Структура таблицы `employees`
--

CREATE TABLE `employees` (
  `ID` int NOT NULL,
  `PositionID` int DEFAULT NULL,
  `LastName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `FirstName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `MiddleName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `DateOfBirth` date DEFAULT NULL,
  `PassportSeries` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `PassportNumber` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Phone` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Login` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `Education` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `employees`
--

INSERT INTO `employees` (`ID`, `PositionID`, `LastName`, `FirstName`, `MiddleName`, `DateOfBirth`, `PassportSeries`, `PassportNumber`, `Email`, `Phone`, `Login`, `Password`, `Education`) VALUES
(2, 3, 'Петров', 'Петр', 'Петрович', '1985-05-15', 'CD', '654321', 'petrov@example.com', '234-567-8901', '123', '123', 'Higher'),
(8, 3, 'qwq', 'qwdq', 'dwqwdq', '2000-01-01', 'qwd', 'qdwq', 'wqdwdqd', 'qwdqd', 'qdwqdw', 'qdwqdw', 'qdwq'),
(9, 4, 'wqdq', 'dqwdqd', 'wqdqwd', '2000-01-01', 'qwdqdqdw', 'qwdd', 'dwqqdw', 'wqdqd', '1', '1', 'dqwd');

-- --------------------------------------------------------

--
-- Структура таблицы `engines`
--

CREATE TABLE `engines` (
  `ID` int NOT NULL,
  `EngineName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `engines`
--

INSERT INTO `engines` (`ID`, `EngineName`) VALUES
(1, 'Electric'),
(2, 'Hybrid');

-- --------------------------------------------------------

--
-- Структура таблицы `models`
--

CREATE TABLE `models` (
  `ID` int NOT NULL,
  `ModelName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `models`
--

INSERT INTO `models` (`ID`, `ModelName`) VALUES
(1, '001'),
(2, 'L9');

-- --------------------------------------------------------

--
-- Структура таблицы `paymenttype`
--

CREATE TABLE `paymenttype` (
  `ID` int NOT NULL,
  `Name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `paymenttype`
--

INSERT INTO `paymenttype` (`ID`, `Name`) VALUES
(1, 'Credit Card'),
(2, 'Cash');

-- --------------------------------------------------------

--
-- Структура таблицы `positions`
--

CREATE TABLE `positions` (
  `ID` int NOT NULL,
  `ID_Department` int NOT NULL,
  `Name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Salary` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `Description` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `positions`
--

INSERT INTO `positions` (`ID`, `ID_Department`, `Name`, `Salary`, `Description`) VALUES
(1, 1, 'Юрисконсульт', '50000', 'Lawyer'),
(2, 2, 'Начальник отдела продаж', '70000', 'Head of Sales'),
(3, 2, 'Менеджеры', '40000', 'Sales Manager'),
(4, 3, 'Менеджер отдела технического обслуживания', '60000', 'Technical Service Manager'),
(5, 3, 'Механики', '35000', 'Mechanic'),
(6, 4, 'SMM-специалист', '45000', 'SMM Specialist'),
(7, 5, 'Бухгалтер', '55000', 'Accountant');

-- --------------------------------------------------------

--
-- Структура таблицы `salescontract`
--

CREATE TABLE `salescontract` (
  `ID` int NOT NULL,
  `CarID` int DEFAULT NULL,
  `CustomerID` int DEFAULT NULL,
  `PaymentTypeID` int DEFAULT NULL,
  `Status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `DateTime` timestamp NULL DEFAULT NULL,
  `EmployeeID` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `salescontract`
--

INSERT INTO `salescontract` (`ID`, `CarID`, `CustomerID`, `PaymentTypeID`, `Status`, `DateTime`, `EmployeeID`) VALUES
(3, 1, NULL, NULL, 'dsfds', '2003-01-04 00:00:00', 2),
(7, 1, 2, NULL, 'ыва', '2000-01-02 21:00:00', 2),
(8, 1, 2, NULL, 'bvc', '1999-12-31 21:00:00', 2);

-- --------------------------------------------------------

--
-- Структура таблицы `services`
--

CREATE TABLE `services` (
  `ID` int NOT NULL,
  `ServiceName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ServicePrice` decimal(10,2) DEFAULT NULL,
  `ExecutionTime` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `services`
--

INSERT INTO `services` (`ID`, `ServiceName`, `ServicePrice`, `ExecutionTime`) VALUES
(1, 'Oil Change', '50.00', 30),
(2, 'Tire Rotation', '40.00', 45),
(3, 'Brake Inspection', '60.00', 60),
(4, 'Engine Tune-Up', '200.00', 120);

-- --------------------------------------------------------

--
-- Структура таблицы `technicalservice`
--

CREATE TABLE `technicalservice` (
  `ID` int NOT NULL,
  `CarID` int DEFAULT NULL,
  `ServiceDateTime` timestamp NULL DEFAULT NULL,
  `EmployeeID` int DEFAULT NULL,
  `ServiceID` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `technicalservice`
--

INSERT INTO `technicalservice` (`ID`, `CarID`, `ServiceDateTime`, `EmployeeID`, `ServiceID`) VALUES
(4, 1, '1999-12-31 21:00:00', 8, 4);

-- --------------------------------------------------------

--
-- Структура таблицы `testdrive`
--

CREATE TABLE `testdrive` (
  `ID` int NOT NULL,
  `DateTime` timestamp NULL DEFAULT NULL,
  `CarID` int DEFAULT NULL,
  `Status` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `CustomerID` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `brands`
--
ALTER TABLE `brands`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `CountryID` (`CountryID`);

--
-- Индексы таблицы `cars`
--
ALTER TABLE `cars`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `BrandID` (`BrandID`,`ModelID`,`EngineID`),
  ADD KEY `ModelID` (`ModelID`),
  ADD KEY `EngineID` (`EngineID`);

--
-- Индексы таблицы `countries`
--
ALTER TABLE `countries`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `Login` (`Login`),
  ADD KEY `PositionID` (`PositionID`);

--
-- Индексы таблицы `engines`
--
ALTER TABLE `engines`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `models`
--
ALTER TABLE `models`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `paymenttype`
--
ALTER TABLE `paymenttype`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `positions`
--
ALTER TABLE `positions`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `ID_Department` (`ID_Department`);

--
-- Индексы таблицы `salescontract`
--
ALTER TABLE `salescontract`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `CustomerID` (`CustomerID`),
  ADD KEY `PaymentTypeID` (`PaymentTypeID`),
  ADD KEY `CarID` (`CarID`),
  ADD KEY `salescontract_ibfk_5` (`EmployeeID`);

--
-- Индексы таблицы `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`ID`);

--
-- Индексы таблицы `technicalservice`
--
ALTER TABLE `technicalservice`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `CarID` (`CarID`,`EmployeeID`,`ServiceID`),
  ADD KEY `CarID_2` (`CarID`,`EmployeeID`,`ServiceID`),
  ADD KEY `technicalservice_ibfk_1` (`ServiceID`),
  ADD KEY `EmployeeID` (`EmployeeID`);

--
-- Индексы таблицы `testdrive`
--
ALTER TABLE `testdrive`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `CarID` (`CarID`,`CustomerID`),
  ADD KEY `CustomerID` (`CustomerID`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `brands`
--
ALTER TABLE `brands`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `cars`
--
ALTER TABLE `cars`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `countries`
--
ALTER TABLE `countries`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `customers`
--
ALTER TABLE `customers`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `departments`
--
ALTER TABLE `departments`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `employees`
--
ALTER TABLE `employees`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT для таблицы `engines`
--
ALTER TABLE `engines`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `models`
--
ALTER TABLE `models`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `paymenttype`
--
ALTER TABLE `paymenttype`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `positions`
--
ALTER TABLE `positions`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `salescontract`
--
ALTER TABLE `salescontract`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `services`
--
ALTER TABLE `services`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `technicalservice`
--
ALTER TABLE `technicalservice`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `testdrive`
--
ALTER TABLE `testdrive`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `brands`
--
ALTER TABLE `brands`
  ADD CONSTRAINT `brands_ibfk_1` FOREIGN KEY (`CountryID`) REFERENCES `countries` (`ID`);

--
-- Ограничения внешнего ключа таблицы `cars`
--
ALTER TABLE `cars`
  ADD CONSTRAINT `cars_ibfk_1` FOREIGN KEY (`ModelID`) REFERENCES `models` (`ID`),
  ADD CONSTRAINT `cars_ibfk_2` FOREIGN KEY (`BrandID`) REFERENCES `brands` (`ID`),
  ADD CONSTRAINT `cars_ibfk_3` FOREIGN KEY (`EngineID`) REFERENCES `engines` (`ID`);

--
-- Ограничения внешнего ключа таблицы `employees`
--
ALTER TABLE `employees`
  ADD CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`PositionID`) REFERENCES `positions` (`ID`);

--
-- Ограничения внешнего ключа таблицы `positions`
--
ALTER TABLE `positions`
  ADD CONSTRAINT `positions_ibfk_1` FOREIGN KEY (`ID_Department`) REFERENCES `departments` (`ID`);

--
-- Ограничения внешнего ключа таблицы `salescontract`
--
ALTER TABLE `salescontract`
  ADD CONSTRAINT `salescontract_ibfk_2` FOREIGN KEY (`PaymentTypeID`) REFERENCES `paymenttype` (`ID`),
  ADD CONSTRAINT `salescontract_ibfk_4` FOREIGN KEY (`CarID`) REFERENCES `cars` (`ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `salescontract_ibfk_5` FOREIGN KEY (`EmployeeID`) REFERENCES `employees` (`ID`),
  ADD CONSTRAINT `salescontract_ibfk_6` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`ID`);

--
-- Ограничения внешнего ключа таблицы `technicalservice`
--
ALTER TABLE `technicalservice`
  ADD CONSTRAINT `technicalservice_ibfk_1` FOREIGN KEY (`ServiceID`) REFERENCES `services` (`ID`),
  ADD CONSTRAINT `technicalservice_ibfk_3` FOREIGN KEY (`CarID`) REFERENCES `cars` (`ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `technicalservice_ibfk_4` FOREIGN KEY (`EmployeeID`) REFERENCES `employees` (`ID`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `testdrive`
--
ALTER TABLE `testdrive`
  ADD CONSTRAINT `testdrive_ibfk_1` FOREIGN KEY (`CarID`) REFERENCES `cars` (`ID`),
  ADD CONSTRAINT `testdrive_ibfk_2` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
