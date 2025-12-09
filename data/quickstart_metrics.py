#!/usr/bin/env python3
"""
Quick Start Guide - Metrics Tracking System
Generate demo data and test the real metrics dashboard
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("🚀 METRICS TRACKING SYSTEM - QUICK START")
print("=" * 70)

# Step 1: Initialize the database
print("\n📊 Step 1: Initializing Metrics Database...")
from core.metrics_tracker import get_metrics_tracker

tracker = get_metrics_tracker()
print("✅ Database initialized successfully!")
print(f"📁 Database location: {tracker.db_path}")

# Step 2: Generate demo data
print("\n📊 Step 2: Generating Demo Data...")
print("   (30 days of realistic user activity)")

from datetime import datetime, timedelta
import random

base_date = datetime.now()
jobs_total = 0
resumes_total = 0
attempts_total = 0

for day_offset in range(30, -1, -1):
    current_date = base_date - timedelta(days=day_offset)
    
    # Generate job analyses
    num_analyses = random.randint(5, 15)
    for _ in range(num_analyses):
        tracker.record_job_analysis(
            user_id="default",
            job_id=f"job_{int(current_date.timestamp())}_{random.randint(1000, 9999)}",
            match_score=random.uniform(45, 95)
        )
    jobs_total += num_analyses
    
    # Generate resume analyses
    num_resumes = random.randint(2, 5)
    for _ in range(num_resumes):
        tracker.record_resume_analysis(
            user_id="default",
            resume_id=f"resume_{int(current_date.timestamp())}_{random.randint(1000, 9999)}",
            ats_score=random.uniform(60, 95),
            parsing_success=random.choice([True, True, True, False])
        )
    resumes_total += num_resumes
    
    # Generate application attempts
    num_attempts = random.randint(1, 3)
    for _ in range(num_attempts):
        tracker.record_application_attempt(
            user_id="default",
            job_id=f"job_{int(current_date.timestamp())}_{random.randint(1000, 9999)}",
            result=random.choice(['success', 'success', 'success', 'pending', 'rejected'])
        )
    attempts_total += num_attempts

print(f"✅ Generated {jobs_total} job analyses")
print(f"✅ Generated {resumes_total} resume analyses")
print(f"✅ Generated {attempts_total} application attempts")

# Step 3: Display Today's Metrics
print("\n📊 Step 3: Today's Metrics (Dashboard Display)")
print("-" * 70)

metrics = tracker.get_today_metrics(user_id="default")
jobs_change_str, _ = tracker.get_formatted_change(metrics['jobs_change'])
score_change_str, _ = tracker.get_formatted_change(metrics['score_change'])
success_change_str, _ = tracker.get_formatted_change(metrics['success_change'])

print(f"\n📊 Today's Insights")
print(f"  🔹 Jobs Analyzed Today: {metrics['jobs_analyzed']:,} {jobs_change_str}")
print(f"  🔹 Average Match Score: {metrics['avg_match_score']:.1f}% {score_change_str}")
print(f"  🔹 Success Rate: {metrics['success_rate']:.1f}% {success_change_str}")

# Step 4: Display Weekly Metrics
print("\n📊 Step 4: This Week's Metrics")
print("-" * 70)

weekly = tracker.get_this_week_metrics(user_id="default")
weekly_change_str, _ = tracker.get_formatted_change(weekly['jobs_change'])

print(f"\n📈 Weekly Statistics")
print(f"  🔹 Jobs Analyzed: {weekly['jobs_analyzed']:,} {weekly_change_str}")
print(f"  🔹 Average Match Score: {weekly['avg_match_score']:.1f}%")
print(f"  🔹 Resume Parse Success: {weekly['parsing_success_rate']:.1f}%")
print(f"  🔹 Total Resumes Analyzed: {weekly['total_resumes_analyzed']}")

# Step 5: Display All-Time Metrics
print("\n📊 Step 5: All-Time Metrics")
print("-" * 70)

all_time = tracker.get_all_time_metrics(user_id="default")

print(f"\n🏆 All-Time Statistics")
print(f"  🔹 Total Jobs Analyzed: {all_time['total_jobs_analyzed']:,}")
print(f"  🔹 Average Match Score: {all_time['avg_match_score']:.1f}%")
print(f"  🔹 Total Applications: {all_time['total_applications']:,}")
print(f"  🔹 Successful Applications: {all_time['successful_applications']:,}")
print(f"  🔹 Overall Success Rate: {all_time['success_rate']:.1f}%")
print(f"  🔹 Total Resumes Analyzed: {all_time['total_resumes_analyzed']}")
print(f"  🔹 Average ATS Score: {all_time['avg_ats_score']:.1f}%")

# Step 6: Code Examples
print("\n💻 Step 6: Code Examples")
print("-" * 70)

print("\n📝 Example 1: Get Today's Metrics")
print("""
from core.metrics_tracker import get_metrics_tracker

tracker = get_metrics_tracker()
metrics = tracker.get_today_metrics(user_id="default")

print(f"Jobs analyzed: {metrics['jobs_analyzed']}")
print(f"Average score: {metrics['avg_match_score']}%")
""")

print("\n📝 Example 2: Record a Job Analysis")
print("""
from core.matcher import Matcher

matcher = Matcher()
result = matcher.match_resume_to_jd(resume_data, jd_data)
# Automatically recorded: match_score_overall = result['match_score_overall']
""")

print("\n📝 Example 3: Record a Resume Analysis")
print("""
from core.resume_parser import ResumeParser

parser = ResumeParser()
parsed = parser.parse_resume(file_content=pdf_bytes)
# Automatically recorded: ats_score from parsed['ats_analysis']['score']
""")

print("\n📝 Example 4: Record an Application Attempt")
print("""
from core.metrics_tracker import get_metrics_tracker

tracker = get_metrics_tracker()
tracker.record_application_attempt(
    user_id="default",
    job_id="job_12345",
    result="success"  # or "pending", "rejected"
)
""")

print("\n📝 Example 5: Display in Sidebar")
print("""
from core.metrics_tracker import get_metrics_tracker

tracker = get_metrics_tracker()
metrics = tracker.get_today_metrics(user_id="default")

jobs_change_str, _ = tracker.get_formatted_change(metrics['jobs_change'])
score_change_str, _ = tracker.get_formatted_change(metrics['score_change'])
success_change_str, _ = tracker.get_formatted_change(metrics['success_change'])

st.metric("Jobs Analyzed Today", f"{metrics['jobs_analyzed']:,}", jobs_change_str)
st.metric("Average Match Score", f"{metrics['avg_match_score']:.0f}%", score_change_str)
st.metric("Success Rate", f"{metrics['success_rate']:.0f}%", success_change_str)
""")

# Summary
print("\n" + "=" * 70)
print("✅ METRICS SYSTEM READY!")
print("=" * 70)

print("""
📚 Documentation:
   - Full Guide: docs/METRICS_TRACKING_SYSTEM.md
   - Complete Migration: docs/HARDCODE_MIGRATION_COMPLETE.md

🚀 Next Steps:
   1. Run the Streamlit app to see live metrics
   2. Perform job analyses to see metrics update
   3. Check the database: sqlite3 data/metrics.db
   4. Review metrics in sidebar for real-time updates

📊 Key Features:
   ✓ Real database-driven metrics (SQLite)
   ✓ Automatic tracking in matcher & parser
   ✓ Daily, weekly, all-time metrics
   ✓ Comparison with previous periods
   ✓ User-specific tracking (scalable)
   ✓ Demo data generation included

🔗 Integration Points:
   - core/matcher.py: Records job match analyses
   - core/resume_parser.py: Records resume ATS scores
   - ui/sidebar.py: Displays real-time metrics

💡 Pro Tips:
   - Use get_metrics_tracker() to access metrics
   - Metrics update automatically after analysis
   - SQLite database is persistent across sessions
   - User ID allows multi-user support

""")

print("=" * 70)
