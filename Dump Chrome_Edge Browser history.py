###Dumps Chrome/Edge Browser history


import sqlite3
import os
import shutil
from datetime import datetime, timedelta

def chrome_date_to_datetime(chrome_date):
    """Convert Chrome timestamp to datetime object"""
    if chrome_date != 0:
        # Chrome timestamps are in microseconds since January 1, 1601
        return datetime(1601, 1, 1) + timedelta(microseconds=chrome_date)
    return None

def get_edge_history():
    """Extract and print Microsoft Edge browsing history"""
    
    # Get username from environment
    username = os.environ.get('USERNAME') or os.environ.get('USER')
    
    # Construct the Edge history database path
    edge_history_path = f"C:\\Users\\{{ .username }}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\History"
    
    print(f"Looking for Edge history at: {edge_history_path}")
    
    # Check if the history file exists
    if not os.path.exists(edge_history_path):
        print("\nHistory file not found!")
        print(f"Expected location: {edge_history_path}")
        print("\nPlease verify:")
        print("1. Microsoft Edge is installed")
        print("2. You have browsing history")
        print("3. The path is correct for your profile")
        return
    
    # Create a temporary copy (Edge locks the file when running)
    temp_history = 'temp_edge_history.db'
    try:
        shutil.copy2(edge_history_path, temp_history)
        print("✓ History file copied successfully\n")
    except PermissionError:
        print("\n⚠ Permission Error: Please close Microsoft Edge and try again.")
        return
    except Exception as e:
        print(f"\n✗ Error copying history file: {e}")
        return
    
    try:
        # Connect to the database
        conn = sqlite3.connect(temp_history)
        cursor = conn.cursor()
        
        # Query to get browsing history
        query = """
            SELECT url, title, visit_count, last_visit_time
            FROM urls
            ORDER BY last_visit_time DESC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        print(f"{'='*100}")
        print(f"Microsoft Edge Browsing History")
        print(f"Profile: Default")
        print(f"Total entries: {len(results)}")
        print(f"{'='*100}\n")
        
        if len(results) == 0:
            print("No browsing history found.")
        else:
            for i, (url, title, visit_count, last_visit) in enumerate(results, 1):
                visit_date = chrome_date_to_datetime(last_visit)
                
                print(f"{i}. {title or 'No Title'}")
                print(f"   URL: {url}")
                print(f"   Visit Count: {visit_count}")
                if visit_date:
                    print(f"   Last Visit: {visit_date.strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    print(f"   Last Visit: Unknown")
                print()
                
        
        conn.close()
        print(f"\n{'='*100}")
        print("History extraction complete!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(temp_history):
            os.remove(temp_history)
            print("Temporary files cleaned up.")

if __name__ == "__main__":
    print("="*100)
    print("Edge Browser History Viewer")
    print("="*100)
    print()
    get_edge_history()
