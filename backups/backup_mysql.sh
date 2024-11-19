#!/bin/bash
# Respaldo de MySQL
mysqldump -u admin -p'admin123' customer_care > customer_care_backup.sql
