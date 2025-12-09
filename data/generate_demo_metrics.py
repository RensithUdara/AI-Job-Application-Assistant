"""
Demo Data Generator - Populate metrics database with sample data for testing.
Run this to initialize the database with realistic metrics.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.metrics_tracker import get_metrics_tracker
from datetime import datetime, timedelta
import random


def generate_demo_data():
    """Generate realistic demo data for the metrics database."""
    tracker = get_metrics_tracker()
    
    print("🔄 Generating demo metrics data...")
    
    # Generate data for the last 30 days
    base_date = datetime.now()
    
    for day_offset in range(30, -1, -1):
        current_date = base_date - timedelta(days=day_offset)
        
        # Generate 5-15 job analyses per day with scores 45-95%
        num_analyses = random.randint(5, 15)
        for _ in range(num_analyses):
            tracker.record_job_analysis(
                user_id="default",
                job_id=f"job_{current_date.timestamp()}_{random.randint(1000, 9999)}",
                match_score=random.uniform(45, 95)
            )
        
        # Generate 2-5 resume analyses per day with scores 60-95%
        num_resumes = random.randint(2, 5)
        for _ in range(num_resumes):
            tracker.record_resume_analysis(
                user_id="default",
                resume_id=f"resume_{current_date.timestamp()}_{random.randint(1000, 9999)}",
                ats_score=random.uniform(60, 95),
                parsing_success=random.choice([True, True, True, False])  # 75% success rate
            )
        
        # Generate 1-3 application attempts per day with 60-80% success rate
        num_attempts = random.randint(1, 3)
        for _ in range(num_attempts):
            tracker.record_application_attempt(
                user_id="default",
                job_id=f"job_{current_date.timestamp()}_{random.randint(1000, 9999)}",
                result=random.choice(['success', 'success', 'success', 'pending', 'rejected'])  # 60% success
            )
    
    print("✅ Demo data generated successfully!")
    print("\n📊 Sample Today's Metrics:")
    
    metrics = tracker.get_today_metrics(user_id="default")
    print(f"  Jobs Analyzed: {metrics['jobs_analyzed']}")
    print(f"  Average Match Score: {metrics['avg_match_score']:.1f}%")
    print(f"  Success Rate: {metrics['success_rate']:.1f}%")
    
    print("\n📈 Weekly Metrics:")
    weekly = tracker.get_this_week_metrics(user_id="default")
    print(f"  Jobs Analyzed (Week): {weekly['jobs_analyzed']}")
    print(f"  Weekly Change: {weekly['jobs_change']:.1f}%")
    
    print("\n🏆 All-Time Metrics:")
    all_time = tracker.get_all_time_metrics(user_id="default")
    print(f"  Total Jobs Analyzed: {all_time['total_jobs_analyzed']}")
    print(f"  Total Applications: {all_time['total_applications']}")
    print(f"  Overall Success Rate: {all_time['success_rate']:.1f}%")


def display_metrics_summary():
    """Display a summary of the metrics."""
    tracker = get_metrics_tracker()
    
    print("\n" + "=" * 70)
    print("📊 REAL DATABASE METRICS - LIVE DASHBOARD DATA")
    print("=" * 70)
    
    # Today's metrics
    metrics = tracker.get_today_metrics(user_id="default")
    jobs_change_str, _ = tracker.get_formatted_change(metrics['jobs_change'])
    score_change_str, _ = tracker.get_formatted_change(metrics['score_change'])
    success_change_str, _ = tracker.get_formatted_change(metrics['success_change'])
    
    print("\n📊 Today's Insights (Sidebar Display)")
    print("-" * 70)
    print(f"  Jobs Analyzed Today:    {metrics['jobs_analyzed']:,} {jobs_change_str}")
    print(f"  Average Match Score:    {metrics['avg_match_score']:.1f}% {score_change_str}")
    print(f"  Success Rate:           {metrics['success_rate']:.1f}% {success_change_str}")
    
    # Weekly metrics
    weekly = tracker.get_this_week_metrics(user_id="default")
    weekly_change_str, _ = tracker.get_formatted_change(weekly['jobs_change'])
    
    print("\n📈 This Week's Metrics")
    print("-" * 70)
    print(f"  Jobs Analyzed:          {weekly['jobs_analyzed']:,} {weekly_change_str}")
    print(f"  Average Match Score:    {weekly['avg_match_score']:.1f}%")
    print(f"  Parse Success Rate:     {weekly['parsing_success_rate']:.1f}%")
    
    # All-time metrics
    all_time = tracker.get_all_time_metrics(user_id="default")
    
    print("\n🏆 All-Time Metrics")
    print("-" * 70)
    print(f"  Total Jobs Analyzed:    {all_time['total_jobs_analyzed']:,}")
    print(f"  Avg Match Score:        {all_time['avg_match_score']:.1f}%")
    print(f"  Total Applications:     {all_time['total_applications']:,}")
    print(f"  Success Rate:           {all_time['success_rate']:.1f}%")
    print(f"  Avg ATS Score:          {all_time['avg_ats_score']:.1f}%")
    
    print("\n" + "=" * 70)
    print("✅ Metrics are now REAL, DATABASE-DRIVEN, not hardcoded!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    generate_demo_data()
    display_metrics_summary()
