import requests
import random
from faker import Faker

BASE_URL = "http://127.0.0.1:8000"
fake = Faker()

num_stages = 10
num_stables = 5
num_results = 50


def create_stages(n):
    """
    Creates and adds n random stages to the database via API.

    Args:
        n (int): Number of stages to create.
    """
    for _ in range(n):
        data = {
            "name": fake.city(),
            "country": fake.country(),
            "date": fake.date_this_year().isoformat(),
            "attendance": random.randint(5000, 50000),
            "lap_length": round(random.uniform(2.0, 5.0), 2),
        }
        response = requests.post(f"{BASE_URL}/stages/", json=data)
        if response.status_code == 201:
            print(f"Stage added: {data}")
        else:
            print(f"Failed to add stage: {response.json()}")


def create_stables(n):
    """
    Creates and adds n random stables to the database via API.

    Args:
        n (int): Number of stables to create.
    """
    for _ in range(n):
        data = {
            "name": fake.company(),
            "country": fake.country(),
            "motor": fake.word(),
            "tire": fake.word(),
        }
        response = requests.post(f"{BASE_URL}/stables/", json=data)
        if response.status_code == 201:
            print(f"Stable added: {data}")
        else:
            print(f"Failed to add stable: {response.json()}")


def create_results(n):
    """
    Creates and adds n random results to the database via API.

    Args:
        n (int): Number of results to create.
    """
    for _ in range(n):
        data = {
            "stage_id": random.randint(1, num_stages),
            "stable_id": random.randint(1, num_stables),
            "driver_name": fake.name(),
            "race_time": round(random.uniform(90.0, 180.0), 2),
            "position": random.randint(1, 10),
            "pit_stops": random.randint(0, 5),
            "laps": random.randint(30, 70),
        }
        response = requests.post(f"{BASE_URL}/results/", json=data)
        if response.status_code == 201:
            print(f"Result added: {data}")
        else:
            print(f"Failed to add result: {response.json()}")


def populate_database():
    """
    Populates the database with random stages, stables, and results.
    """
    print("Adding stages...")
    create_stages(num_stages)
    print("Adding stables...")
    create_stables(num_stables)
    print("Adding results...")
    create_results(num_results)
    print("Database population complete!")


if __name__ == "__main__":
    populate_database()