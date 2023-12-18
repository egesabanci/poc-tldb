# TLDB (TX-logs Database) - PoC imp.

**Important:** Since it is PoC implementation, it is not suitable for production environments

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Contributions and Feedback](#contributions-and-feedback)

## Overview (WIP)

This project is a proof of concept implementation of a TSM-based (Time Structured Merge Tree) database designed to handle high write-throughput scenarios, specifically tailored for financial transactions. Traditional databases may face challenges in maintaining performance and consistency when dealing with a large volume of financial transactions.

### Key Features

- **TSM (Time Structured Merge):** The database leverages a TSM algorithm to efficiently store and retrieve financial transaction data. This model is optimized for scenarios where data is chronologically ordered, making it suitable for real-time financial applications.

- **High Write-Throughput:** The primary focus of this database is to provide a solution for environments where write-intensive operations, such as financial transactions, are critical. The architecture is designed to scale horizontally to accommodate increasing write loads.

### Contributions and Feedback

Contributions to enhance and expand the functionality of this proof of concept are welcome. If you encounter issues or have suggestions for improvement, please open an issue.
