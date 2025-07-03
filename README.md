# SQLite Table Comparator

Version: 1.0
Date: July 2025

## Author
@nicolasfernandol

## 🧾 Overview

This project is part of a real-world internship experience in which I developed a Python-based system to **track changes between a temporary dataset and an internal catalog** of cosmetic ingredients.

The purpose of this script is to **compare and detect new, updated, or removed records**, starting from an external data source, and sync them into a local SQLite catalog.

> NOTE: Only the comparison logic is published here. Other modules used in the original project, such as data downloader from external sources and data sync to official SQL Server systems, are excluded for confidentiality reasons. The full dataset originally included over 36,000 cosmetic ingredients and substances.
To reduce file size and comply with data usage practices, the public version of the database only retains a small subset (e.g., 50 records) for demonstration and testing purposes.

---

## What this project does

- Compares two SQLite tables:
  - `ingredients` → Temporary table from external data source
  - `compared_ingredients` → Local catalog version
- Detects:
  - New ingredients → inserted with `insert_date`
  - Updated ingredients → updated with `modify_date`
  - Removed ingredients → flagged with `removed = 1`
- Handles version-tracking fields (`modify_date`, `insert_date`) using UTC timestamps
- Built using clean ORM models with SQLAlchemy
- Includes test coverage with `pytest`

---

## Structure