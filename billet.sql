-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 24, 2024 at 05:57 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `billet`
--

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `nom_complet` varchar(20) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL,
  `username` varchar(20) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL,
  `password` varchar(200) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL,
  `email` varchar(30) NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT 0,
  `id_user` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`nom_complet`, `username`, `password`, `email`, `is_admin`, `id_user`) VALUES
('Sandler Ben', 'Sam4Beru', '$2b$15$Oohtz4DdV8KzG5TPSpTsbuvR9lRgV6.nebk5GjZe3j8l8xeseCjuG', 'SamBen@yahoo.fr', 1, 1),
('Jean Marchand', 'marchandJean', '$2b$15$c16eqQiNmizbE9oMPHlbWO.0rAbqp3RVGYMzp3pJ3JhH6q0a777cq', '', 0, 2),
('Miguel Lecompte', 'MLcompte', '$2b$15$2/t6xbaJENgce7GhZWsGBeKeJjf8CtF7ud1njhmYebasA4OKn9DKi', '', 1, 3),
('Diallo Abdou', 'Diallo123', '$2b$12$qXvgOgOTWD3Ih4wD.SaYnugKDjtwdHIrvrPpxdPAol7QU5LLl8oLK', '', 0, 4),
('Emmanuella Bertrand', 'EmmaNA', '$2b$12$T4dYkeqWxD54HmEbG8eNHe45/3WXEvnWcpjlpSiEodjhyzdySFulm', '', 0, 6),
('Xin Long', 'Xlong', '$2b$12$/zk4gcHpzGofiX6km.mRTecJsEHRjKL/OsZa6v0CeqlEQdzr/cTRi', 'Xingonl@yahoo.com', 0, 7),
('Karine Renaud', 'Reine@Renaud', '$2b$12$atKVurMWwa89wQaLDkJ/J.M5mtyQo0py6oOieHH8JKp527cZSV.eu', 'Renaud56@gmail.com', 0, 8),
('Berube Samuel', 'Berubin4', '$2b$12$SdMyH821vTO6pv2DVEj0GOYZ/sdfdRdAjXQ4gzzynf6T2hpsBBrn2', 'BerubySammy@yahoo.fr', 0, 9);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `password` (`password`),
  ADD UNIQUE KEY `id` (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
