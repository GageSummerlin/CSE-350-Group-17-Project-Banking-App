# must have pymysql installed, as well as cryptography

import pymysql

# establishes the connection to the online database
timeout = 10
connection = pymysql.connect(
  charset="utf8mb4",
  connect_timeout=timeout,
  cursorclass=pymysql.cursors.DictCursor,
  db="defaultdb",
  host="bank-db-cse-350-bank-project-db.h.aivencloud.com",
  password="AVNS_0n4SZfpgJZYHapcwgPU",
  read_timeout=timeout,
  port=28782,
  user="avnadmin",
  write_timeout=timeout,
)