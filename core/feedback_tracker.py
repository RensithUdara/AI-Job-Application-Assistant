"""
Feedback Tracker - Track user feedback, ratings, and feature requests.
Stores user feedback for continuous system improvement.
"""

from datetime import datetime
from typing import Dict, List, Optional
import sqlite3
from pathlib import Path


class FeedbackTracker:
    """Singleton class for tracking user feedback and ratings."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FeedbackTracker, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize feedback tracker with database."""
        if self._initialized:
            return
        
        self.db_path = Path(__file__).parent.parent / "data" / "metrics.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_db()
        self._initialized = True
    
    def _initialize_db(self):
        """Create feedback tables if they don't exist."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Table for user feedback
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                rating INTEGER,
                feedback_text TEXT,
                feedback_type TEXT,
                feature_mentioned TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                helpful BOOLEAN DEFAULT 0
            )
        ''')
        
        # Table for feedback categories/features
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE,
                description TEXT,
                count INTEGER DEFAULT 0,
                avg_rating REAL DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_feedback(self, user_id: str, rating: int, feedback_text: str, 
                       feedback_type: str = "general", feature_mentioned: str = None) -> bool:
        """
        Record user feedback with rating.
        
        Args:
            user_id: User identifier
            rating: Star rating (1-5)
            feedback_text: User's feedback text
            feedback_type: Type of feedback (general, bug, feature_request, improvement)
            feature_mentioned: Specific feature being reviewed
        
        Returns:
            True if successfully recorded, False otherwise
        """
        try:
            if not 1 <= rating <= 5:
                raise ValueError("Rating must be between 1 and 5")
            
            if not feedback_text or len(feedback_text.strip()) == 0:
                raise ValueError("Feedback text cannot be empty")
            
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO user_feedback 
                (user_id, rating, feedback_text, feedback_type, feature_mentioned)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, rating, feedback_text.strip(), feedback_type, feature_mentioned))
            
            # Update category stats if feature mentioned
            if feature_mentioned:
                self._update_category_stats(cursor, feature_mentioned, rating)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error recording feedback: {e}")
            return False
    
    def _update_category_stats(self, cursor, category: str, rating: int):
        """Update statistics for feedback categories."""
        try:
            # Check if category exists
            cursor.execute('SELECT id, count, avg_rating FROM feedback_categories WHERE category_name = ?', 
                          (category,))
            result = cursor.fetchone()
            
            if result:
                category_id, count, avg_rating = result
                new_count = count + 1
                new_avg = ((avg_rating * count) + rating) / new_count
                cursor.execute('''
                    UPDATE feedback_categories 
                    SET count = ?, avg_rating = ? 
                    WHERE category_name = ?
                ''', (new_count, new_avg, category))
            else:
                cursor.execute('''
                    INSERT INTO feedback_categories (category_name, count, avg_rating)
                    VALUES (?, 1, ?)
                ''', (category, float(rating)))
        except Exception as e:
            print(f"Error updating category stats: {e}")
    
    def get_feedback_summary(self, user_id: str = None) -> Dict:
        """
        Get feedback summary statistics.
        
        Args:
            user_id: Optional user ID to filter by specific user
        
        Returns:
            Dictionary with feedback statistics
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute('''
                    SELECT COUNT(*), AVG(rating), MIN(rating), MAX(rating)
                    FROM user_feedback
                    WHERE user_id = ?
                ''', (user_id,))
            else:
                cursor.execute('''
                    SELECT COUNT(*), AVG(rating), MIN(rating), MAX(rating)
                    FROM user_feedback
                ''')
            
            result = cursor.fetchone()
            
            if result and result[0] is not None:
                total_count, avg_rating, min_rating, max_rating = result
                
                # Get feedback type distribution
                cursor.execute('''
                    SELECT feedback_type, COUNT(*) as count
                    FROM user_feedback
                    GROUP BY feedback_type
                    ORDER BY count DESC
                ''')
                type_dist = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Get top mentioned features
                cursor.execute('''
                    SELECT feature_mentioned, COUNT(*) as count, AVG(rating) as avg_rating
                    FROM user_feedback
                    WHERE feature_mentioned IS NOT NULL
                    GROUP BY feature_mentioned
                    ORDER BY count DESC
                    LIMIT 10
                ''')
                top_features = [
                    {
                        'feature': row[0],
                        'count': row[1],
                        'avg_rating': round(row[2], 2)
                    }
                    for row in cursor.fetchall()
                ]
                
                conn.close()
                
                return {
                    'total_feedbacks': int(total_count),
                    'avg_rating': round(avg_rating, 2) if avg_rating else 0,
                    'min_rating': int(min_rating) if min_rating else 0,
                    'max_rating': int(max_rating) if max_rating else 0,
                    'feedback_type_distribution': type_dist,
                    'top_features': top_features
                }
            
            conn.close()
            return {
                'total_feedbacks': 0,
                'avg_rating': 0,
                'min_rating': 0,
                'max_rating': 0,
                'feedback_type_distribution': {},
                'top_features': []
            }
        except Exception as e:
            print(f"Error getting feedback summary: {e}")
            return {}
    
    def get_recent_feedback(self, limit: int = 10, user_id: str = None) -> List[Dict]:
        """
        Get recent feedback entries.
        
        Args:
            limit: Number of recent entries to retrieve
            user_id: Optional user ID to filter by
        
        Returns:
            List of feedback dictionaries
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute('''
                    SELECT id, rating, feedback_text, feedback_type, feature_mentioned, created_at
                    FROM user_feedback
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (user_id, limit))
            else:
                cursor.execute('''
                    SELECT id, rating, feedback_text, feedback_type, feature_mentioned, created_at
                    FROM user_feedback
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (limit,))
            
            feedback_list = []
            for row in cursor.fetchall():
                feedback_list.append({
                    'id': row[0],
                    'rating': row[1],
                    'text': row[2],
                    'type': row[3],
                    'feature': row[4],
                    'created_at': row[5]
                })
            
            conn.close()
            return feedback_list
        except Exception as e:
            print(f"Error getting recent feedback: {e}")
            return []
    
    def get_rating_distribution(self) -> Dict[int, int]:
        """
        Get distribution of ratings.
        
        Returns:
            Dictionary with rating counts
        """
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT rating, COUNT(*) as count
                FROM user_feedback
                GROUP BY rating
                ORDER BY rating
            ''')
            
            distribution = {i: 0 for i in range(1, 6)}
            for row in cursor.fetchall():
                distribution[row[0]] = row[1]
            
            conn.close()
            return distribution
        except Exception as e:
            print(f"Error getting rating distribution: {e}")
            return {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}


def get_feedback_tracker() -> FeedbackTracker:
    """Get singleton instance of FeedbackTracker."""
    return FeedbackTracker()
