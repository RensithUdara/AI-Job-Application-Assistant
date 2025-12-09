"""
Demo Data Generator - Populate metrics database with sample data for testing.
Run this to initialize the database with realistic metrics.
"""

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


if __name__ == "__main__":
    generate_demo_data()
