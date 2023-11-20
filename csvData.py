import csv
from school import csvPreparedInformation

def create_csv_files(csv_prepared_info):
    success, departments_data = csv_prepared_info 

    if not success:
        raise ValueError("The data preparation was not successful.")

    for department_name, courses in departments_data:
        sanitized_department_name = "".join(char for char in department_name if char.isalnum() or char in (' ', '_')).rstrip()
        filename = f"{sanitized_department_name.replace(' ', '_')}.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            headers = courses[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()

            for course in courses:
                writer.writerow(course)

        print(f"CSV file created for department: {department_name}")

if isinstance(csvPreparedInformation, tuple) and csvPreparedInformation[0]:
    create_csv_files(csvPreparedInformation)
else:
    print("csvPreparedInformation has an unexpected structure or the preparation was unsuccessful.")

