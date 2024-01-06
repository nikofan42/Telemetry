# driver_data.py

def fetch_driver_data(ir):
    drivers_data = {}

    # Find the active session (the one with the highest SessionNum)
    active_session = max(ir['SessionInfo']['Sessions'], key=lambda s: s['SessionNum'])
    session_type = active_session['SessionName']

    # Create a dictionary to map CarIdx to UserID
    car_idx_to_user_id = {driver['CarIdx']: driver['UserID'] for driver in ir['DriverInfo']['Drivers']}

    drivers = ir['DriverInfo']['Drivers']
    for driver in drivers:
        car_idx = driver['CarIdx']
        drivers_data[car_idx] = {
            'user_id': car_idx_to_user_id[car_idx],
            'name': driver['UserName'],
            'car_number': str(driver['CarNumber']).replace("'", '"'),
            'car_class': driver['CarPath'],
            'car_rating': driver['IRating'],
            'team_name': driver['TeamName'],
            'car_idx': car_idx,
            'session_type': session_type,
            'session_id': ir['WeekendInfo']['SessionID'],
            'track_name': ir['WeekendInfo']['TrackName']
        }

    return drivers_data
