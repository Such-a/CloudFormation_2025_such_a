import json
import pymysql
from datetime import datetime
import random
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        db_host = os.environ['DB_HOST']
        db_user = os.environ['DB_USER']
        db_pass = os.environ['DB_PASS']
        db_name = os.environ['DB_NAME']

        # Connect to RDS
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name,
            connect_timeout=5
        )
        cursor = conn.cursor()

        # Ensure table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS click_counter (
                id INT PRIMARY KEY AUTO_INCREMENT,
                clicks INT NOT NULL
            )
        """)
        conn.commit()

        # Ensure initial row exists
        cursor.execute("SELECT COUNT(*) FROM click_counter WHERE id=1")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO click_counter (clicks) VALUES (0)")
            conn.commit()

        # Increment counter
        cursor.execute("UPDATE click_counter SET clicks = clicks + 1 WHERE id=1")
        conn.commit()
        cursor.execute("SELECT clicks FROM click_counter WHERE id=1")
        count = cursor.fetchone()[0]

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "status": "OK",
                "message": "Backend is healthy",
                "server_time": datetime.utcnow().isoformat(),
                "request_id": context.aws_request_id,
                "random_value": random.randint(1, 100),
                "request_count": count
            })
        }

    except Exception as e:
        logger.error("Error: %s", e)
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"status": "ERROR", "message": str(e)})
        }
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()
