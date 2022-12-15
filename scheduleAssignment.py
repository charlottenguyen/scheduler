import time
import pandas as pd
from flask import Flask, request
from datetime import datetime
 
# Make Flask app
app = Flask(__name__)
 
@app.route('/schedule', methods=['POST'])
def schedule():
	request_data = request.get_json()
	
	day_strings = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

	title = "title"
	start = "start"
	end = "end"

	output_schedule = []

	conflict = False

	if request_data:
		for day in day_strings:
			if day in request_data:
				# Determine if there are events for the day before unpacking json
				if (len(request_data[day]) > 0):
					day_schedule = []
					appt_times = []
					# Unpack json
					for appointment in request_data[day]:
						if title in appointment:
							appt_name = appointment[title]
						if start in appointment:
							start_time = convert_time(appointment[start])
						if end in appointment:
							end_time = convert_time(appointment[end])
						
						# Format string to add to schedule
						# Appointment times will be used to check for conflict in schedule
						new_appointment = "{}: {} {}-{}".format(day.capitalize(), appt_name, start_time, end_time)
						day_schedule.append(new_appointment)
						appt_times.append([int(appointment[start]), int(appointment[end])])
					
					# Sort the events of the day by start time
					# Remove trailing minutes when empty as per guidelines
					day_schedule.sort(key = lambda x: x.split()[-1])	
					for event in day_schedule:
						event = event.replace(":00", "")
						output_schedule.append(event)
					
					# If a conflict already exists in the weekly schedule, no need to check further
					if not conflict:
						conflict = check_overlap_list(appt_times)
				else:
					no_appointment = "{}: No Appointment".format(day.capitalize())
					output_schedule.append(no_appointment)
		
		if conflict:
			output_schedule.append("Conflicts?: Yes")
		else:
			output_schedule.append("Conflicts?: No")
		
	return output_schedule

# Time, which is given in seconds, is converted first to 24H then 12H time
def convert_time(time_seconds):
	appt_time  = time.strftime('%H:%M', time.gmtime(int(time_seconds)))
	converted_time = datetime.strptime(appt_time, "%H:%M")
	output_time = converted_time.strftime("%-I:%M %p")

	return output_time

#  If time intervals overlap, there is a conflict in schedule
def check_overlap(interval1, interval2):
	interval1 = pd.Interval(interval1[0], interval1[1])
	interval2 = pd.Interval(interval2[0], interval2[1])
	
	return interval1.overlaps(interval2)

# Check if overlap exists in all events of day
def check_overlap_list(times):
	sorted_times = sorted(times, key=lambda x: x[0])
	for interval1 in sorted_times:
		for interval2 in sorted_times:
			if interval1 != interval2:
				if  check_overlap(interval1, interval2):
					return True
	return False

# Main driver function
if __name__ == '__main__':
    app.run(debug=True, port=5000)
