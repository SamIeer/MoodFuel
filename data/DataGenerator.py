import random
import pandas as pd

def generate_coffee_dataset(n_samples=1000):
    data = []

    for _ in range(n_samples):
        sleep_hours = round(random.uniform(4, 9), 1)
        stress_level = random.randint(1, 10)
        workload_level = random.randint(1, 10)
        time_of_day = random.randint(6, 22)

        # Base coffee strength
        coffee_strength = 5.0

        # Sleep impact
        if sleep_hours < 5:
            coffee_strength += 2.5
        elif sleep_hours < 6:
            coffee_strength += 1.5
        elif sleep_hours > 7.5:
            coffee_strength -= 1.0

        # Stress impact
        coffee_strength += (stress_level - 5) * 0.3

        # Workload impact
        coffee_strength += (workload_level - 5) * 0.25

        # Time-of-day impact
        if time_of_day < 10:          # Morning
            coffee_strength += 1.0
        elif time_of_day > 17:        # Evening
            coffee_strength -= 1.5

        # Noise (to make data realistic)
        coffee_strength += random.uniform(-0.5, 0.5)

        # Clamp values between 1 and 10
        coffee_strength = round(max(1, min(10, coffee_strength)), 1)

        data.append([
            sleep_hours,
            stress_level,
            time_of_day,
            workload_level,
            coffee_strength
        ])

    columns = [
        "sleep_hours",
        "stress_level",
        "time_of_day",
        "workload_level",
        "coffee_strength"
    ]

    return pd.DataFrame(data, columns=columns)

# Generate dataset
df = generate_coffee_dataset(1000)

# Save to CSV
df.to_csv("coffee_strength_dataset.csv", index=False)

print(df.head())
