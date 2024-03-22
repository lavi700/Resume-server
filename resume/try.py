from datetime import datetime

# Get the current date and time
current_datetime = datetime.now()

# Format the current date in a readable format
formatted_date = current_datetime.strftime('%Y-%m-%d')

print(formatted_date)
