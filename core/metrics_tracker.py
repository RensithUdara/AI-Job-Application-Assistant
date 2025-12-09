"""
Metrics Tracker - Track user activity, analysis stats, and performance metrics.
Stores session and historical data for dashboard insights.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import sqlite3
from pathlib import Path


class MetricsTracker:
    """Singleton class for tracking and retrieving application metrics."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetricsTracker, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize metrics tracker with database."""
        if self._initialized:
            return
        
        self.db_path = Path(__file__).parent.parent / "data" / "metrics.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_db()
        self._initialized = True
    
    def _initialize_db(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Table for job analyses
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                job_id TEXT,
                match_score REAL,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'analyzed'
            )
        ''')
        
        # Table for resume analyses
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resume_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                resume_id TEXT,
                ats_score REAL,
                parsing_success BOOLEAN,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table for application attempts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS application_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                job_id TEXT,
                result TEXT,
                attempt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table for daily metrics (cached aggregates)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                metric_date DATE,
                jobs_analyzed INTEGER DEFAULT 0,
                avg_match_score REAL DEFAULT 0,
                success_count INTEGER DEFAULT 0,
                total_attempts INTEGER DEFAULT 0,
                ats_avg_score REAL DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_job_analysis(self, user_id: str, job_id: str, match_score: float) -> bool:
        """Record a job analysis event."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO job_analyses (user_id, job_id, match_score)
                VALUES (?, ?, ?)
            ''', (user_id, job_id, match_score))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error recording job analysis: {e}")
            return False
    
    def record_resume_analysis(self, user_id: str, resume_id: str, 
                              ats_score: float, parsing_success: bool) -> bool:
        """Record a resume analysis event."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO resume_analyses (user_id, resume_id, ats_score, parsing_success)
                VALUES (?, ?, ?, ?)
            ''', (user_id, resume_id, ats_score, parsing_success))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error recording resume analysis: {e}")
            return False
    
    def record_application_attempt(self, user_id: str, job_id: str, result: str) -> bool:
        """Record an application attempt (success/failure)."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO application_attempts (user_id, job_id, result)
                VALUES (?, ?, ?)
            ''', (user_id, job_id, result))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error recording application attempt: {e}")
            return False
    
    def get_today_metrics(self, user_id: str = "default") -> Dict:
        """Get aggregated metrics for today."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            today = datetime.now().date().isoformat()
            yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
            
            # Today's job analyses
            cursor.execute('''
                SELECT COUNT(*) as count, AVG(match_score) as avg_score
                FROM job_analyses
                WHERE user_id = ? AND DATE(analyzed_at) = ?
            ''', (user_id, today))
            
            today_jobs = cursor.fetchone()
            jobs_analyzed = today_jobs[0] if today_jobs and today_jobs[0] else 0
            avg_match_score = today_jobs[1] if today_jobs and today_jobs[1] else 0
            
            # Yesterday's job analyses for comparison
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM job_analyses
                WHERE user_id = ? AND DATE(analyzed_at) = ?
            ''', (user_id, yesterday))
            
            yesterday_result = cursor.fetchone()
            yesterday_count = yesterday_result[0] if yesterday_result and yesterday_result[0] else 0
            
            # Calculate change percentage
            jobs_change = 0
            if yesterday_count > 0:
                jobs_change = ((jobs_analyzed - yesterday_count) / yesterday_count) * 100
            elif jobs_analyzed > 0:
                jobs_change = 100  # First day, show as 100% increase
            
            # Success rate (application attempts)
            cursor.execute('''
                SELECT COUNT(*) as total, 
                       SUM(CASE WHEN result = 'success' THEN 1 ELSE 0 END) as success_count
                FROM application_attempts
                WHERE user_id = ? AND DATE(attempt_date) = ?
            ''', (user_id, today))
            
            attempts = cursor.fetchone()
            total_attempts = attempts[0] if attempts and attempts[0] else 0
            success_count = attempts[1] if attempts and attempts[1] else 0
            success_rate = (success_count / total_attempts * 100) if total_attempts > 0 else 0
            
            # Yesterday's success rate for comparison
            cursor.execute('''
                SELECT COUNT(*) as total, 
                       SUM(CASE WHEN result = 'success' THEN 1 ELSE 0 END) as success_count
                FROM application_attempts
                WHERE user_id = ? AND DATE(attempt_date) = ?
            ''', (user_id, yesterday))
            
            yesterday_attempts = cursor.fetchone()
            yesterday_success = (yesterday_attempts[1] / yesterday_attempts[0] * 100 
                               if yesterday_attempts and yesterday_attempts[0] and yesterday_attempts[0] > 0 else 0)
            
            success_change = success_rate - yesterday_success
            
            # Average match score comparison
            cursor.execute('''
                SELECT AVG(match_score)
                FROM job_analyses
                WHERE user_id = ? AND DATE(analyzed_at) = ?
            ''', (user_id, yesterday))
            
            yesterday_score_result = cursor.fetchone()
            yesterday_avg_score = yesterday_score_result[0] if yesterday_score_result and yesterday_score_result[0] else 0
            score_change = avg_match_score - (yesterday_avg_score if yesterday_avg_score else 0)
            
            conn.close()
            
            return {
                'jobs_analyzed': jobs_analyzed,
                'jobs_change': jobs_change,
                'avg_match_score': round(avg_match_score, 1),
                'score_change': round(score_change, 1),
                'success_rate': round(success_rate, 1),
                'success_change': round(success_change, 1),
                'total_attempts': total_attempts,
                'success_count': success_count
            }
        
        except Exception as e:
            print(f"Error getting today metrics: {e}")
            return self._get_default_metrics()
    
    def get_this_week_metrics(self, user_id: str = "default") -> Dict:
        """Get aggregated metrics for this week."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            week_ago = (datetime.now() - timedelta(days=7)).date().isoformat()
            today = datetime.now().date().isoformat()
            
            # This week's stats
            cursor.execute('''
                SELECT COUNT(*) as count, AVG(match_score) as avg_score
                FROM job_analyses
                WHERE user_id = ? AND DATE(analyzed_at) BETWEEN ? AND ?
            ''', (user_id, week_ago, today))
            
            week_jobs = cursor.fetchone()
            jobs_analyzed = week_jobs[0] if week_jobs and week_jobs[0] else 0
            avg_match_score = week_jobs[1] if week_jobs and week_jobs[1] else 0
            
            # Last week's stats
            last_week_start = (datetime.now() - timedelta(days=14)).date().isoformat()
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM job_analyses
                WHERE user_id = ? AND DATE(analyzed_at) BETWEEN ? AND ?
            ''', (user_id, last_week_start, week_ago))
            
            last_week_result = cursor.fetchone()
            last_week_count = last_week_result[0] if last_week_result and last_week_result[0] else 0
            jobs_change = ((jobs_analyzed - last_week_count) / last_week_count * 100 
                          if last_week_count > 0 else (100 if jobs_analyzed > 0 else 0))
            
            # Resume parsing success
            cursor.execute('''
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN parsing_success = 1 THEN 1 ELSE 0 END) as success_count
                FROM resume_analyses
                WHERE user_id = ? AND DATE(analyzed_at) BETWEEN ? AND ?
            ''', (user_id, week_ago, today))
            
            resume_data = cursor.fetchone()
            total_resumes = resume_data[0] if resume_data and resume_data[0] else 0
            successful_parses = resume_data[1] if resume_data and resume_data[1] else 0
            parsing_rate = (successful_parses / total_resumes * 100) if total_resumes > 0 else 0
            
            conn.close()
            
            return {
                'jobs_analyzed': jobs_analyzed,
                'jobs_change': jobs_change,
                'avg_match_score': round(avg_match_score, 1),
                'parsing_success_rate': round(parsing_rate, 1),
                'total_resumes_analyzed': total_resumes
            }
        
        except Exception as e:
            print(f"Error getting week metrics: {e}")
            return self._get_default_metrics()
    
    def get_all_time_metrics(self, user_id: str = "default") -> Dict:
        """Get all-time aggregated metrics."""
        try:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()
            
            # All time job analyses
            cursor.execute('''
                SELECT COUNT(*) as count, AVG(match_score) as avg_score
                FROM job_analyses
                WHERE user_id = ?
            ''', (user_id,))
            
            total_jobs = cursor.fetchone()
            jobs_analyzed = total_jobs[0] if total_jobs and total_jobs[0] else 0
            avg_match_score = total_jobs[1] if total_jobs and total_jobs[1] else 0
            
            # All time applications
            cursor.execute('''
                SELECT COUNT(*) as total, 
                       SUM(CASE WHEN result = 'success' THEN 1 ELSE 0 END) as success_count
                FROM application_attempts
                WHERE user_id = ?
            ''', (user_id,))
            
            attempts = cursor.fetchone()
            total_attempts = attempts[0] if attempts and attempts[0] else 0
            success_count = attempts[1] if attempts and attempts[1] else 0
            success_rate = (success_count / total_attempts * 100) if total_attempts > 0 else 0
            
            # All time resume analyses
            cursor.execute('''
                SELECT COUNT(*) as total, AVG(ats_score) as avg_ats
                FROM resume_analyses
                WHERE user_id = ?
            ''', (user_id,))
            
            resume_data = cursor.fetchone()
            total_resumes = resume_data[0] if resume_data and resume_data[0] else 0
            avg_ats_score = resume_data[1] if resume_data and resume_data[1] else 0
            
            conn.close()
            
            return {
                'total_jobs_analyzed': jobs_analyzed,
                'avg_match_score': round(avg_match_score, 1),
                'total_applications': total_attempts,
                'successful_applications': success_count,
                'success_rate': round(success_rate, 1),
                'total_resumes_analyzed': total_resumes,
                'avg_ats_score': round(avg_ats_score, 1)
            }
        
        except Exception as e:
            print(f"Error getting all-time metrics: {e}")
            return self._get_default_metrics()
    
    def _get_default_metrics(self) -> Dict:
        """Return default metrics when database is empty."""
        return {
            'jobs_analyzed': 0,
            'jobs_change': 0,
            'avg_match_score': 0,
            'score_change': 0,
            'success_rate': 0,
            'success_change': 0,
            'total_attempts': 0,
            'success_count': 0
        }
    
    def get_formatted_change(self, value: float) -> Tuple[str, str]:
        """Format change value with appropriate arrow and sign.
        
        Returns:
            Tuple of (formatted_string, direction) - e.g., ("↗ +12%", "up")
        """
        if value > 0:
            return (f"↗ +{value:.1f}%", "up")
        elif value < 0:
            return (f"↘ {value:.1f}%", "down")
        else:
            return ("→ 0%", "neutral")


# Singleton instance
metrics = MetricsTracker()


def get_metrics_tracker() -> MetricsTracker:
    """Get the metrics tracker instance."""
    return MetricsTracker()
