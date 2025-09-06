from celery.schedules import crontab

app.conf.beat_schedule = {
    "detect-suspicious-ips": {
        "task": "ip_tracking.tasks.detect_suspicious_ips",
        "schedule": crontab(minute=0),  # Run hourly
    },
}
