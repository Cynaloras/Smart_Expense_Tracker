import sqlite3
import os

def run_migration():
    """Run the database migration script"""
    
    # Connect to the database
    db_path = 'expense_tracker.db'  # Adjust path if needed
    
    if not os.path.exists(db_path):
        print("❌ Database file not found! Make sure the database exists first.")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Running database migration...")
        
        # Read and execute the SQL script
        with open('scripts/add_user_settings_api.sql', 'r') as file:
            sql_script = file.read()
        
        # Split by semicolon and execute each statement
        statements = sql_script.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement:  # Skip empty statements
                cursor.execute(statement)
                print(f"✅ Executed: {statement[:50]}...")
        
        # Commit changes
        conn.commit()
        
        # Verify the migration worked
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        email_notifications_exists = any(col[1] == 'email_notifications' for col in columns)
        
        if email_notifications_exists:
            print("✅ Migration successful! email_notifications column added.")
            
            # Show current status
            cursor.execute("""
                SELECT COUNT(*) as total_users, 
                       SUM(CASE WHEN email_notifications = 1 THEN 1 ELSE 0 END) as users_with_notifications
                FROM users
            """)
            result = cursor.fetchone()
            print(f"📊 Total users: {result[0]}, Users with notifications enabled: {result[1]}")
        else:
            print("❌ Migration failed! Column not found.")
            
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error running migration: {e}")
        return False

if __name__ == "__main__":
    run_migration()
