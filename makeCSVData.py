import csv

def create_csv_file_for_department(department_name, courses):
    sanitized_department_name = "".join(char for char in department_name if char.isalnum() or char in (' ', '_')).rstrip()
    filename = f"{sanitized_department_name.replace(' ', '_')}.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        headers = courses[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for course in courses:
            writer.writerow(course)

    print(f"CSV file created for department: {department_name}")
