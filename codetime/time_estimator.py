from datetime import timedelta

def group_commits_into_sessions(timestamps, session_gap_minutes=60):
    """
    Groups commit timestamps into work sessions.
    Returns the number of sessions.
    """
    if not timestamps:
        return 0

    # Sort timestamps (most recent to oldest)
    timestamps.sort()

    session_count = 1
    last_time = timestamps[0]

    for current_time in timestamps[1:]:
        gap = current_time - last_time
        if gap > timedelta(minutes=session_gap_minutes):
            session_count += 1
        last_time = current_time

    return session_count

def estimate_total_time(session_count, avg_minutes_per_session=30):
    """
    Estimate total hours spent coding based on sessions.
    """
    total_minutes = session_count * avg_minutes_per_session
    total_hours = round(total_minutes / 60, 2)
    return total_hours
