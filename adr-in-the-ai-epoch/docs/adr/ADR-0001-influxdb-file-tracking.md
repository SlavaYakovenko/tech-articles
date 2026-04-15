# ADR-0001: InfluxDB-based File Tracking and Temporary Storage

**Date:** 2026-04-14
**Status:** Accepted

## Context
After deleting the local `data/` folder, a regression occurred: the system lost track of which files had already been processed and began re-importing all old data from Google Drive into InfluxDB. Local checks for file presence in the `data/` folder and text logs proved unreliable when the filesystem was cleaned.

## Options
* *Option 1: Local JSON/Database* — Store the list of processed files in a local JSON file. (Simple to implement, but retains the vulnerability to project folder deletion).
* *Option 2: InfluxDB Tracking* — Use a separate measurement in InfluxDB to track processed files. (Reliable, centralized, and independent of the local disk state).

## Decision
It was decided to use InfluxDB as the "source of truth." A `processed_files` measurement was created, where each file is recorded by its `filename` tag. The import process now begins by checking for the file's presence in this list.

## Consequences
* **FS Independence:** Deleting the `data/` or `logs/` folders no longer triggers a re-import.
* **Storage Optimization:** The `data/` folder is now used as a temporary buffer. Files are copied there for processing and deleted immediately after successful upload to the DB.
* **Performance:** A single lightweight request to InfluxDB is added before processing each file.
* **Atomicity:** A file is marked as processed only after successful confirmation of the data write.

## Relations
* This is the first architectural decision (base synchronization mechanism).
