# TLDB (TX-logs Database) - PoC imp.

**Important:** Since it is PoC implementation, it is not suitable for production environments. Note that this implementation already has too many problems.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Contributions and Feedback](#contributions-and-feedback)

## Overview

This project is a proof of concept implementation of a TSM-based (Time Structured Merge Tree) database designed to handle high write-throughput scenarios, specifically tailored for financial transactions. Traditional databases may face challenges in maintaining performance and consistency when dealing with a large volume of financial transactions.

### Installation and Usage

```
>>> docker pull poc-tldb
```

```
>>> docker run -p 5199:5199 poc-tldb
```

Send the first insert request

```
>>> curl -X POST -H "Content-Type: application/json" -d '{"query": "insert 0x000 -> 0x000 : 42"}' http://localhost:5199
```

### Key Features

- **TSM (Time Structured Merge):** The database leverages a TSM algorithm to efficiently store and retrieve financial transaction data. This model is optimized for scenarios where data is chronologically ordered, making it suitable for real-time financial applications.

- **High Write-Throughput:** The primary focus of this database is to provide a solution for environments where write-intensive operations, such as financial transactions, are critical. The architecture is designed to scale horizontally to accommodate increasing write loads.

### Contributions and Feedback

Contributions to enhance and expand the functionality of this proof of concept are welcome. If you encounter issues or have suggestions for improvement, please open an issue.

### Known Issues

- In requests made before the WAL file creates its first segmentation, Disk look-up is performed if the timestamp or timestamp range to be found is not in the Memtable. This results in an error because there is no segmentation yet.

- Since the unique ID of the rows are timestamps, smaller segmentations cannot be created after compaction. For this reason, there is no compaction mechanism for now.

**Workarounds:**
After a certain disk size, the oldest segmentations can be abandoned or compression can be applied to the oldest segmentations with minimum data loss.
