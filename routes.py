from handler import *
handlers = [
    #about login
    #about main page
    (r"/", home_handler),
    (r'/browser',browser_handler),
    (r"/setting", setting_handler),
    (r"/apply_edition", apply_edition_handler),
    (r"/apply_adding", apply_adding_handler),
    (r"/reboot", reboot_handler),
    (r"/device_time", device_time_handler),
    (r"/device_location", device_location_handler),
    (r"/user_observer", user_observer_handler), 
    (r"/time_synchronize", time_synchronize_handler),
    (r"/operater_position", operator_position_handler),
]
