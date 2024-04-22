-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 21, 2024 at 06:42 PM
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
-- Table structure for table `evenement`
--

CREATE TABLE `evenement` (
  `nom` varchar(20) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL,
  `date` date NOT NULL,
  `emplacement` varchar(100) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL,
  `total_seat` int(11) NOT NULL,
  `prix` int(15) NOT NULL,
  `id_evenement` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `evenement`
--

INSERT INTO `evenement` (`nom`, `date`, `emplacement`, `total_seat`, `prix`, `id_evenement`) VALUES
('Bingo', '2024-06-25', 'Centre Bingo', 100, 30, 'BINGO2025'),
('Escalade', '2024-06-16', 'Mont-Royal', 30, 20, 'ESCAL2415'),
('Luge', '2024-03-16', 'Mont-Royal', 20, 15, 'LUGE5245'),
('Natation', '2024-07-15', 'Piscine Saint-Jean', 200, 15, 'NPSJ524');

-- --------------------------------------------------------

--
-- Table structure for table `paiement`
--

CREATE TABLE `paiement` (
  `montant` int(20) NOT NULL,
  `mode_paiement` varchar(20) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL,
  `numero_carte` int(100) NOT NULL,
  `date_expiration` date NOT NULL,
  `cvv` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `paiement`
--

INSERT INTO `paiement` (`montant`, `mode_paiement`, `numero_carte`, `date_expiration`, `cvv`) VALUES
(20, 'mastercard', 254625476, '2026-04-15', 253);

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

CREATE TABLE `reservation` (
  `nom` varchar(20) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL,
  `date` date NOT NULL,
  `place` int(200) NOT NULL,
  `id_evenement` varchar(20) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL,
  `id_user` varchar(100) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL,
  `id_reservation` varchar(15) NOT NULL,
  `statut` varchar(20) CHARACTER SET armscii8 COLLATE armscii8_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reservation`
--

INSERT INTO `reservation` (`nom`, `date`, `place`, `id_evenement`, `id_user`, `id_reservation`, `statut`) VALUES
('Natation', '2024-07-15', 2, '', '', '1', 'En attente'),
('Crochet', '2025-01-01', 1, 'CROCHET1235', '4', '3568', 'Annule'),
('Luge', '2024-03-16', 2, 'LUGE545', '7', '35698', 'en attente'),
('Escalade', '2024-06-16', 2, 'ESCAL2415', '6', '6663', 'en attente');

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
('Berube Samuel', 'Berubin4', 'Beru497', '', 0, 5),
('Emmanuella Bertrand', 'EmmaNA', '$2b$12$T4dYkeqWxD54HmEbG8eNHe45/3WXEvnWcpjlpSiEodjhyzdySFulm', '', 0, 6),
('Xin Long', 'Xlong', '$2b$12$/zk4gcHpzGofiX6km.mRTecJsEHRjKL/OsZa6v0CeqlEQdzr/cTRi', 'Xingonl@yahoo.com', 0, 7);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `evenement`
--
ALTER TABLE `evenement`
  ADD UNIQUE KEY `id_evenement` (`id_evenement`);

--
-- Indexes for table `paiement`
--
ALTER TABLE `paiement`
  ADD UNIQUE KEY `numero_carte` (`numero_carte`);

--
-- Indexes for table `reservation`
--
ALTER TABLE `reservation`
  ADD UNIQUE KEY `id_reservation` (`id_reservation`);

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
  MODIFY `id_user` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
