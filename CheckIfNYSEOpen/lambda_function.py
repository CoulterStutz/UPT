import datetime
import pytz

def is_market_open(event, context):
    # Market holidays in YYYY-MM-DD format (customize as needed)
    market_holidays = [
        "2024-01-01",  # New Year's Day
        "2024-01-15",  # Martin Luther King Jr. Day
        "2024-02-19",  # Presidents' Day
        "2024-04-05",  # Good Friday
        "2024-05-27",  # Memorial Day
        "2024-07-04",  # Independence Day
        "2024-09-02",  # Labor Day
        "2024-11-28",  # Thanksgiving Day
        "2024-12-25"   # Christmas Day
    ]
    
    # Convert holidays to datetime.date objects
    market_holidays = [datetime.datetime.strptime(date, "%Y-%m-%d").date() for date in market_holidays]

    # Define market hours in Eastern Time
    eastern_tz = pytz.timezone('US/Eastern')
    utc_now = datetime.datetime.now(pytz.utc)  # Current time in UTC
    eastern_now = utc_now.astimezone(eastern_tz)  # Convert to Eastern Time
    
    # Extract day, time, and date
    day_of_week = eastern_now.weekday()  # Monday = 0, Sunday = 6
    current_time = eastern_now.time()
    current_date = eastern_now.date()

    # Market open and close times
    market_open = datetime.time(9, 30)  # 9:30 AM ET
    market_close = datetime.time(16, 0)  # 4:00 PM ET

    # Check if the market is closed (weekends, holidays, or outside market hours)
    if day_of_week >= 5:  # Saturday (5) or Sunday (6)
        return {"status": "closed", "reason": "weekend"}
    if current_date in market_holidays:
        return {"status": "closed", "reason": "holiday"}
    if not (market_open <= current_time <= market_close):
        return {"status": "closed", "reason": "outside market hours"}
    
    # If none of the above conditions are met, the market is open
    return {"status": "open"}

# Example event and context for testing
if __name__ == "__main__":
    print(is_market_open({}, None))
