#!/bin/bash
# Respaldo de MongoDB Atlas
mongodump --uri="mongodb+srv://agent_user:password123@cluster0.mongodb.net/customerCareComments" --out /path/to/backup/folder
