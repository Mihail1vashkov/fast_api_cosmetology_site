import json
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal
from models import Service, Appointment


def init_db_from_json(json_file: str):
    db: Session = SessionLocal()
    try:
        # Удаляем старые записи, если есть
        db.query(Service).delete()
        db.query(Appointment).delete()
        db.commit()  # Commit the deletion of old records

        # Читаем данные из JSON файла
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading JSON file '{json_file}': {e}")
            return

        services = []
        appointments = []

        # First pass: Create Service entries and collect data
        for entry in data:
            try:
                name = entry.get("name")
                description = entry.get("description", "")
                working_hours = entry.get("working_hours", "")
                appointment_time_str = entry.get("appointment_time")

                if not name or not appointment_time_str:
                    print(f"Missing required data in JSON entry: {entry}")
                    continue

                # Create and add the Service record
                service = Service(
                    name=name,
                    description=description,
                    working_hours=working_hours
                )
                services.append(service)

            except KeyError as e:
                print(f"Missing expected key in JSON entry: {e}")
            except ValueError as e:
                print(f"Error processing data: {e}")

        # Add all services to the database and commit to get IDs
        db.add_all(services)
        db.commit()

        # Create a dictionary to map service names to their IDs
        service_id_map = {service.name: service.id for service in services}

        # Second pass: Create Appointment entries
        for entry in data:
            try:
                service_name = entry.get("name")
                appointment_time_str = entry.get("appointment_time")
                service_id = service_id_map.get(service_name)

                if not service_id:
                    print(f"Service '{service_name}' not found, skipping appointment.")
                    continue

                appointment_time = datetime.strptime(appointment_time_str, '%Y-%m-%d %H:%M:%S')
                appointment = Appointment(
                    appointment_time=appointment_time,
                    service_id=service_id
                )
                appointments.append(appointment)

            except KeyError as e:
                print(f"Missing expected key in JSON entry: {e}")
            except ValueError as e:
                print(f"Error processing data: {e}")

        # Add all appointments to the database and commit
        db.add_all(appointments)
        db.commit()

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db_from_json('procedures.json')
