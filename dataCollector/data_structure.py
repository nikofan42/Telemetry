# Driving Status
class DrivingStatus:
    def __init__(self, ir):
        self.brake = ir['Brake']
        self.brake_raw = ir['BrakeRaw']
        self.clutch = ir['Clutch']
        self.gear = ir['Gear']
        self.throttle = ir['Throttle']
        self.throttle_raw = ir['ThrottleRaw']

# Engine Status
class EngineStatus:
    def __init__(self, ir):
        self.engine_warnings = ir['EngineWarnings']
        self.fuel_level = ir['FuelLevel']
        self.fuel_level_pct = ir['FuelLevelPct']
        self.fuel_press = ir['FuelPress']
        self.fuel_use_per_hour = ir['FuelUsePerHour']
        self.rpm = ir['RPM']
        self.shift_grind_rpm = ir['ShiftGrindRPM']
        self.shift_indicator_pct = ir['ShiftIndicatorPct']
        self.shift_power_pct = ir['ShiftPowerPct']

# Lap and Timing Data
class LapTimingData:
    def __init__(self, ir):
        self.lap = ir['Lap']
        self.lap_best_lap = ir['LapBestLap']
        self.lap_best_lap_time = ir['LapBestLapTime']
        self.lap_best_nlap_lap = ir['LapBestNLapLap']
        self.lap_best_nlap_time = ir['LapBestNLapTime']
        self.lap_current_lap_time = ir['LapCurrentLapTime']
        self.lap_delta_to_best_lap = ir['LapDeltaToBestLap']
        self.lap_delta_to_best_lap_dd = ir['LapDeltaToBestLap_DD']
        self.lap_delta_to_best_lap_ok = ir['LapDeltaToBestLap_OK']
        self.lap_delta_to_optimal_lap = ir['LapDeltaToOptimalLap']
        self.lap_delta_to_optimal_lap_dd = ir['LapDeltaToOptimalLap_DD']
        self.lap_delta_to_optimal_lap_ok = ir['LapDeltaToOptimalLap_OK']
        self.lap_delta_to_session_best_lap = ir['LapDeltaToSessionBestLap']
        self.lap_delta_to_session_best_lap_dd = ir['LapDeltaToSessionBestLap_DD']
        self.lap_delta_to_session_best_lap_ok = ir['LapDeltaToSessionBestLap_OK']
        self.lap_delta_to_session_last_lap = ir['LapDeltaToSessionLastLap']
        self.lap_delta_to_session_last_lap_dd = ir['LapDeltaToSessionLastLap_DD']
        self.lap_delta_to_session_last_lap_ok = ir['LapDeltaToSessionLastLap_OK']
        self.lap_delta_to_session_optimal_lap = ir['LapDeltaToSessionOptimalLap']
        self.lap_delta_to_session_optimal_lap_dd = ir['LapDeltaToSessionOptimalLap_DD']
        self.lap_delta_to_session_optimal_lap_ok = ir['LapDeltaToSessionOptimalLap_OK']
        self.lap_dist = ir['LapDist']
        self.lap_dist_pct = ir['LapDistPct']
        self.lap_last_lap_time = ir['LapLastLapTime']
        self.lap_last_nlap_time = ir['LapLastNLapTime']
        self.lap_las_nlap_seq = ir['LapLasNLapSeq']

# Speed and Velocity
class SpeedVelocity:
    def __init__(self, ir):
        self.speed = ir['Speed']
        self.velocity_x = ir['VelocityX']
        self.velocity_y = ir['VelocityY']
        self.velocity_z = ir['VelocityZ']

class SteeringWheelData:
    def __init__(self, ir):
        self.steering_wheel_angle = ir['SteeringWheelAngle']
        self.steering_wheel_angle_max = ir['SteeringWheelAngleMax']
        self.steering_wheel_pct_damper = ir['SteeringWheelPctDamper']
        self.steering_wheel_pct_torque = ir['SteeringWheelPctTorque']
        self.steering_wheel_pct_torque_sign = ir['SteeringWheelPctTorqueSign']
        self.steering_wheel_pct_torque_sign_stops = ir['SteeringWheelPctTorqueSignStops']
        self.steering_wheel_peak_force_nm = ir['SteeringWheelPeakForceNm']
        self.steering_wheel_torque = ir['SteeringWheelTorque']

class EnvironmentalData:
    def __init__(self, ir):
        self.air_density = ir['AirDensity']
        self.air_pressure = ir['AirPressure']
        self.air_temp = ir['AirTemp']
        self.alt = ir['Alt']
        self.relative_humidity = ir['RelativeHumidity']
        self.skies = ir['Skies']
        self.track_temp = ir['TrackTemp']
        self.track_temp_crew = ir['TrackTempCrew']
        self.weather_type = ir['WeatherType']
        self.wind_dir = ir['WindDir']
        self.wind_vel = ir['WindVel']

# Camera and Session Data
class CameraSessionData:
    def __init__(self, ir):
        self.cam_camera_number = ir['CamCameraNumber']
        self.cam_camera_state = ir['CamCameraState']
        self.cam_car_idx = ir['CamCarIdx']
        self.cam_group_number = ir['CamGroupNumber']
        self.session_flags = ir['SessionFlags']
        self.session_laps_remain = ir['SessionLapsRemain']
        self.session_num = ir['SessionNum']
        self.session_state = ir['SessionState']
        self.session_time = ir['SessionTime']
        self.session_time_remain = ir['SessionTimeRemain']
        self.session_unique_id = ir['SessionUniqueID']

class DriverPitstopData:
    def __init__(self, ir):
        self.cpu_usage_bg = ir['CpuUsageBG']
        self.dc_drivers_so_far = ir['DcDriversSoFar']
        self.dc_lap_status = ir['DcLapStatus']
        self.display_units = ir['DisplayUnits']
        self.driver_marker = ir['DriverMarker']
        self.enter_exit_reset = ir['EnterExitReset']
        self.pit_opt_repair_left = ir['PitOptRepairLeft']
        self.pit_repair_left = ir['PitRepairLeft']
        self.pit_sv_flags = ir['PitSvFlags']
        self.pit_sv_fuel = ir['PitSvFuel']
        self.pit_sv_lfp = ir['PitSvLFP']
        self.pit_sv_lrp = ir['PitSvLRP']
        self.pit_sv_rfp = ir['PitSvRFP']
        self.pit_sv_rrp = ir['PitSvRRP']
        self.player_car_class_position = ir['PlayerCarClassPosition']
        self.player_car_position = ir['PlayerCarPosition']
        self.race_laps = ir['RaceLaps']
        self.radio_transmit_car_idx = ir['RadioTransmitCarIdx']
        self.radio_transmit_frequency_idx = ir['RadioTransmitFrequencyIdx']
        self.radio_transmit_radio_idx = ir['RadioTransmitRadioIdx']

class GeolocationData:
    def __init__(self, ir):
        self.lat = ir['Lat']
        self.lat_accel = ir['LatAccel']
        self.lon = ir['Lon']
        self.long_accel = ir['LongAccel']

class OrientationData:
    def __init__(self, ir):
        self.pitch = ir['Pitch']
        self.pitch_rate = ir['PitchRate']
        self.roll = ir['Roll']
        self.roll_rate = ir['RollRate']
        self.yaw = ir['Yaw']
        self.yaw_north = ir['YawNorth']
        self.yaw_rate = ir['YawRate']


class CFSuspensionData:
    def __init__(self, ir):
        self.cf_ride_height = ir['CfRideHeight']
        self.cf_shock_defl = ir['CfShockDefl']
        self.cf_shock_vel = ir['CfShockVel']

class CFSRSuspensionData:
    def __init__(self, ir):
        self.cfsr_ride_height = ir['CfsrRideHeight']

class CRSuspensionData:
    def __init__(self, ir):
        self.cr_ride_height = ir['CrRideHeight']
        self.cr_shock_defl = ir['CrShockDefl']
        self.cr_shock_vel = ir['CrShockVel']
### In-Car Adjustments Data
class InCarAdjustmentsData:
    def __init__(self, ir):
        self.dc_abs = ir['DC_ABS']
        self.dc_anti_roll_front = ir['DC_AntiRollFront']
        self.dc_anti_roll_rear = ir['DC_AntiRollRear']
        self.dc_boost_level = ir['DC_BoostLevel']
        self.dc_brake_bias = ir['DC_BrakeBias']
        self.dc_diff_entry = ir['DC_DiffEntry']
        self.dc_diff_exit = ir['DC_DiffExit']
        self.dc_diff_middle = ir['DC_DiffMiddle']
        self.dc_engine_braking = ir['DC_EngineBraking']
        self.dc_engine_power = ir['DC_EnginePower']
        self.dc_fuel_mixture = ir['DC_FuelMixture']
        self.dc_rev_limiter = ir['DC_RevLimiter']
        self.dc_throttle_shape = ir['DC_ThrottleShape']
        self.dc_traction_control = ir['DC_TractionControl']
        self.dc_traction_control_2 = ir['DC_TractionControl2']
        self.dc_traction_control_toggle = ir['DC_TractionControlToggle']
        self.dc_weight_jacker_left = ir['DC_WeightJackerLeft']
        self.dc_weight_jacker_right = ir['DC_WeightJackerRight']
        self.dc_wing_front = ir['DC_WingFront']
        self.dc_wing_rear = ir['DC_WingRear']

### Pitstop Adjustments Data
class PitstopAdjustmentsData:
    def __init__(self, ir):
        self.dp_fnom_knob_setting = ir['DP_FNomKnobSetting']
        self.dp_fuf_angle_index = ir['DP_FufAngleIndex']
        self.dp_fwing_angle = ir['DP_FWingAngle']
        self.dp_fwing_index = ir['DP_FWingIndex']
        self.dp_lr_wedge_adj = ir['DP_LrWedgeAdj']
        self.dp_ps_setting = ir['DP_PSSetting']
        self.dp_qtape = ir['DP_QTape']
        self.dp_r_bar_setting = ir['DP_RBarSetting']
        self.dp_rf_truckarm_p1_dz = ir['DP_RfTruckarmP1Dz']
        self.dp_rr_damper_perch_offset_m = ir['DP_RrDamperPerchOffsetM']
        self.dp_rr_perch_offset_m = ir['DP_RrPerchOffsetM']
        self.dp_rr_wedge_adj = ir['DP_RrWedgeAdj']
        self.dp_rw_wing_angle = ir['DP_RwWingAngle']
        self.dp_rw_wing_index = ir['DP_RwWingIndex']
        self.dp_rw_wing_setting = ir['DP_RwWingSetting']
        self.dp_truckarm_p1_dz = ir['DP_TruckarmP1Dz']
        self.dp_wedge_adj = ir['DP_WedgeAdj']

### Tire Data
class TireData:
    def __init__(self, ir):
        self.brake_line_press = ir['BrakeLinePress']
        self.cold_pressure = ir['ColdPressure']
        self.pressure = ir['Pressure']
        self.ride_height = ir['RideHeight']
        self.shock_defl = ir['ShockDefl']
        self.shock_vel = ir['ShockVel']
        self.speed = ir['Speed']
        self.temp_cl = ir['TempCL']
        self.temp_cm = ir['TempCM']
        self.temp_cr = ir['TempCR']
        self.temp_l = ir['TempL']
        self.temp_m = ir['TempM']
        self.temp_r = ir['TempR']
        self.wear_l = ir['WearL']
        self.wear_m = ir['WearM']
        self.wear_r = ir['WearR']

class CarData:
    def __init__(self, ir, car_idx):
        self.car_idx = car_idx
        self.car_class_position = ir['CarClassPosition'][car_idx]
        self.est_time = ir['EstTime'][car_idx]
        self.f2_time = ir['F2Time'][car_idx]
        self.gear = ir['Gear'][car_idx]
        self.lap = ir['Lap'][car_idx]
        self.lap_dist_pct = ir['LapDistPct'][car_idx]
        self.on_pit_road = ir['OnPitRoad'][car_idx]
        self.position = ir['Position'][car_idx]
        self.rpm = ir['RPM'][car_idx]
        self.steer = ir['Steer'][car_idx]
        self.track_surface = ir['TrackSurface'][car_idx]

class CarArrayData:
    def __init__(self):
        self.car_data = []

    def add_car_data(self, car_data):
        self.car_data.append(car_data)

# To save the data for each car 10 times a second, you can create instances of CarData and add them to CarArrayData as needed.

class WeekendInfo:
    def __init__(self, ir):
        self.track_name = ir['TrackName']
        self.track_id = ir['TrackID']
        self.track_length = ir['TrackLength']
        self.track_display_name = ir['TrackDisplayName']
        self.track_display_short_name = ir['TrackDisplayShortName']
        self.track_config_name = ir['TrackConfigName']
        self.track_city = ir['TrackCity']
        self.track_country = ir['TrackCountry']
        self.track_altitude = ir['TrackAltitude']
        self.track_latitude = ir['TrackLatitude']
        self.track_longitude = ir['TrackLongitude']
        self.track_north_offset = ir['TrackNorthOffset']
        self.track_num_turns = ir['TrackNumTurns']
        self.track_pit_speed_limit = ir['TrackPitSpeedLimit']
        self.track_type = ir['TrackType']
        self.track_weather_type = ir['TrackWeatherType']
        self.track_skies = ir['TrackSkies']
        self.track_surface_temp = ir['TrackSurfaceTemp']
        self.track_air_temp = ir['TrackAirTemp']
        self.track_air_pressure = ir['TrackAirPressure']
        self.track_wind_vel = ir['TrackWindVel']
        self.track_wind_dir = ir['TrackWindDir']
        self.track_relative_humidity = ir['TrackRelativeHumidity']
        self.track_fog_level = ir['TrackFogLevel']
        self.track_cleanup = ir['TrackCleanup']
        self.track_dynamic_track = ir['TrackDynamicTrack']
        self.series_id = ir['SeriesID']
        self.season_id = ir['SeasonID']
        self.session_id = ir['SessionID']
        self.sub_session_id = ir['SubSessionID']
        self.league_id = ir['LeagueID']
        self.official = ir['Official']
        self.race_week = ir['RaceWeek']
        self.event_type = ir['EventType']
        self.category = ir['Category']
        self.sim_mode = ir['SimMode']
        self.team_racing = ir['TeamRacing']
        self.min_drivers = ir['MinDrivers']
        self.max_drivers = ir['MaxDrivers']
        self.dc_rule_set = ir['DCRuleSet']
        self.qualifier_must_start_race = ir['QualifierMustStartRace']
        self.num_car_classes = ir['NumCarClasses']
        self.num_car_types = ir['NumCarTypes']
        self.weekend_options = ir['WeekendOptions']

class WeekendOptions:
    def __init__(self, ir):
        self.num_starters = ir['NumStarters']
        self.starting_grid = ir['StartingGrid']
        self.qualify_scoring = ir['QualifyScoring']
        self.course_cautions = ir['CourseCautions']
        self.standing_start = ir['StandingStart']
        self.restarts = ir['Restarts']
        self.weather_type = ir['WeatherType']
        self.skies = ir['Skies']
        self.wind_direction = ir['WindDirection']
        self.wind_speed = ir['WindSpeed']
        self.weather_temp = ir['WeatherTemp']
        self.relative_humidity = ir['RelativeHumidity']
        self.fog_level = ir['FogLevel']
        self.unofficial = ir['Unofficial']
        self.commercial_mode = ir['CommercialMode']
        self.night_mode = ir['NightMode']
        self.is_fixed_setup = ir['IsFixedSetup']
        self.strict_laps_checking = ir['StrictLapsChecking']
        self.has_open_registration = ir['HasOpenRegistration']
        self.hardcore_level = ir['HardcoreLevel']
        self.telemetry_options = ir['TelemetryOptions']


class SessionInfo:
    def __init__(self, ir):
        self.num_sessions = ir['NumSessions']
        self.sessions = [Session(ir, i) for i in range(self.num_sessions)]

class Session:
    def __init__(self, ir, session_index):
        session_data = ir['SessionInfo']['Sessions'][session_index]
        self.session_num = session_data['SessionNum']
        self.session_laps = session_data['SessionLaps']
        self.session_time = session_data['SessionTime']
        self.session_num_laps_to_avg = session_data['SessionNumLapsToAvg']
        self.session_type = session_data['SessionType']
        self.session_track_rubber_state = session_data['SessionTrackRubberState']
        self.results_positions = session_data['ResultsPositions']
        self.results_fastest_lap = session_data['ResultsFastestLap']
        self.results_average_lap_time = session_data['ResultsAverageLapTime']
        self.results_num_caution_flags = session_data['ResultsNumCautionFlags']
        self.results_num_caution_laps = session_data['ResultsNumCautionLaps']
        self.results_num_lead_changes = session_data['ResultsNumLeadChanges']
        self.results_laps_complete = session_data['ResultsLapsComplete']
        self.results_official = session_data['ResultsOfficial']

class ResultPosition:
    def __init__(self, result_data):
        self.position = result_data['Position']
        self.class_position = result_data['ClassPosition']
        self.car_idx = result_data['CarIdx']
        self.lap = result_data['Lap']
        self.time = result_data['Time']
        self.fastest_lap = result_data['FastestLap']
        self.fastest_time = result_data['FastestTime']
        self.last_time = result_data['LastTime']
        self.laps_led = result_data['LapsLed']
        self.laps_complete = result_data['LapsComplete']
        self.laps_driven = result_data['LapsDriven']
        self.incidents = result_data['Incidents']
        self.reason_out_id = result_data['ReasonOutId']
        self.reason_out_str = result_data['ReasonOutStr']

class ResultFastestLap:
    def __init__(self, fastest_lap_data):
        self.car_idx = fastest_lap_data['CarIdx']
        self.fastest_lap = fastest_lap_data['FastestLap']
        self.fastest_time = fastest_lap_data['FastestTime']

class DriverInfo:
    def __init__(self, driver_data):
        self.driver_car_idx = driver_data['CarIdx']
        self.driver_head_pos_x = driver_data['HeadPosX']
        self.driver_head_pos_y = driver_data['HeadPosY']
        self.driver_head_pos_z = driver_data['HeadPosZ']
        self.driver_car_idle_rpm = driver_data['IdleRPM']
        self.driver_car_red_line = driver_data['RedLine']
        self.driver_car_fuel_kg_per_ltr = driver_data['FuelKgPerLtr']
        self.driver_car_fuel_max_ltr = driver_data['FuelMaxLtr']
        self.driver_car_max_fuel_pct = driver_data['MaxFuelPct']
        self.driver_car_sl_first_rpm = driver_data['ShiftLightFirstRPM']
        self.driver_car_sl_shift_rpm = driver_data['ShiftLightShiftRPM']
        self.driver_car_sl_last_rpm = driver_data['ShiftLightLastRPM']
        self.driver_car_sl_blink_rpm = driver_data['ShiftLightBlinkRPM']
        self.driver_pit_trk_pct = driver_data['PitTrkPct']
        self.driver_car_est_lap_time = driver_data['EstLapTime']
        self.driver_setup_name = driver_data['SetupName']
        self.driver_setup_is_modified = driver_data['SetupIsModified']
        self.driver_setup_load_type_name = driver_data['SetupLoadTypeName']
        self.driver_setup_passed_tech = driver_data['SetupPassedTech']
        self.drivers = driver_data['Drivers']

class Driver:
    def __init__(self, driver_data):
        self.car_idx = driver_data['CarIdx']
        self.user_name = driver_data['UserName']
        self.abbrev_name = driver_data['AbbrevName']
        self.initials = driver_data['Initials']
        self.user_id = driver_data['UserID']
        self.team_id = driver_data['TeamID']
        self.team_name = driver_data['TeamName']
        self.car_number = driver_data['CarNumber']
        self.car_number_raw = driver_data['CarNumberRaw']
        self.car_path = driver_data['CarPath']
        self.car_class_id = driver_data['CarClassID']
        self.car_id = driver_data['CarID']
        self.car_screen_name = driver_data['CarScreenName']
        self.car_screen_name_short = driver_data['CarScreenNameShort']
        self.car_class_short_name = driver_data['CarClassShortName']
        self.car_class_rel_speed = driver_data['CarClassRelSpeed']
        self.car_class_license_level = driver_data['CarClassLicenseLevel']
        self.car_class_max_fuel_pct = driver_data['CarClassMaxFuelPct']
        self.car_class_weight_penalty = driver_data['CarClassWeightPenalty']
        self.car_class_color = driver_data['CarClassColor']
        self.irating = driver_data['IRating']
        self.lic_level = driver_data['LicLevel']
        self.lic_sub_level = driver_data['LicSubLevel']
        self.lic_string = driver_data['LicString']
        self.lic_color = driver_data['LicColor']
        self.is_spectator = driver_data['IsSpectator']
        self.car_design_str = driver_data['CarDesignStr']
        self.helmet_design_str = driver_data['HelmetDesignStr']
        self.suit_design_str = driver_data['SuitDesignStr']
        self.car_number_design_str = driver_data['CarNumberDesignStr']
        self.car_sponsor_1 = driver_data['CarSponsor1']
        self.car_sponsor_2 = driver_data['CarSponsor2']
        self.club_name = driver_data['ClubName']
        self.division_name = driver_data['DivisionName']
        # For SectorInfo and SplitTimeInfo, ensure the driver_data contains necessary sector and split time information
        self.sector_info = self.SectorInfo(driver_data['SectorNum'], driver_data['SectorStartPct'])
        self.split_time_info = self.SplitTimeInfo(driver_data['Sectors'])

    class SectorInfo:
        def __init__(self, sector_num, sector_start_pct):
            self.sector_num = sector_num
            self.sector_start_pct = sector_start_pct

    class SplitTimeInfo:
        def __init__(self, sectors):
            self.sectors = sectors

