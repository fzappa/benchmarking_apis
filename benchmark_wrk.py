import subprocess
import re
import argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import time
import json
import os
import shutil
import urllib.request
from tqdm import tqdm
from datetime import datetime

# Web framework endpoints
endpoints = {
    "Axum": "http://localhost:3000/ping",
    "Rocket": "http://localhost:8000/ping",
    "Actix": "http://localhost:8080/ping",
    "FastAPI": "http://localhost:8001/ping",
    "Django DRF": "http://localhost:8002/ping",
    "Django Ninja": "http://localhost:8003/ping",
}

# Test mode configurations
modes = {
    "fast": {"connections": [1, 10], "duration": "3s", "threads": 1},
    "full": {"connections": [1, 2, 3, 4, 5, 10, 25, 50, 100, 200, 500, 1000], "duration": "5s", "threads": 8},
    "stress": {"connections": [100, 250, 500, 750, 1000], "duration": "20s", "threads": 8},
}

# Check if wrk is installed
def check_wrk_installed():
    if shutil.which("wrk") is None:
        print("Error: wrk is not installed. Please install wrk first.")
        exit(1)

# Check if an endpoint is accessible
def is_endpoint_up(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.getcode() == 200
    except urllib.error.URLError as e:
        return False

# Run the wrk test
def run_wrk_test(url, connections, duration, threads, reps=3):
    rps_values = []
    for _ in range(reps):
        try:
            actual_threads = min(threads, connections)
            if actual_threads < threads:
                print(f"Adjusting thread count from {threads} to {actual_threads} because connections ({connections}) < threads ({threads})")
            result = subprocess.run(
                ["wrk", "-t", str(actual_threads), "-c", str(connections), "-d", duration, url],
                capture_output=True,
                text=True,
                timeout=duration_to_seconds(duration) + 10
            )
            if result.returncode == 0:
                match = re.search(r"Requests/sec:\s+([\d\.]+)", result.stdout)
                if match:
                    rps_values.append(float(match.group(1)))
                else:
                    print(f"Could not find RPS in output for {url} with {connections} connections")
            else:
                print(f"wrk failed with return code {result.returncode} for {url} with {connections} connections")
                print(f"Error output: {result.stderr}")
        except Exception as e:
            print(f"Exception while testing {url} with {connections} connections: {e}")
    return np.mean(rps_values) if rps_values else 0.0

# Convert duration to seconds
def duration_to_seconds(duration):
    if duration.endswith("s"):
        return int(duration[:-1])
    elif duration.endswith("m"):
        return int(duration[:-1]) * 60
    return 10  # Default value if the unit is not recognized

# Generate the results plot
def plot_results(connections, results, plot_file):
    plt.figure(figsize=(12, 7))
    for api, rps_list in results.items():
        plt.plot(connections, rps_list, marker='o', label=api)
    plt.xscale("log")
    plt.title("Python x Rust Benchmark: FastAPI, DRF, Ninja, Axum, Rocket, Actix")
    plt.xlabel("Concurrent Connections (log)")
    plt.ylabel("Requests per Second (RPS)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.savefig(plot_file)
    print(f"✅ Plot saved as {plot_file}")

# Main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["fast", "full", "stress"], default="fast")
    parser.add_argument("--reps", type=int, default=3)
    parser.add_argument("--timestamp", action="store_true", help="Add timestamp to output files")
    args = parser.parse_args()

    # Check if wrk is installed
    check_wrk_installed()

    # Check if endpoints are accessible
    for api, url in endpoints.items():
        if not is_endpoint_up(url):
            print(f"Warning: {api} endpoint {url} is not responding. Tests may fail.")

    # If data_wrk.json exists and --timestamp is not set,
    # load the data and generate the plot
    if not args.timestamp and os.path.exists("data_wrk.json"):
        print("📊 Found data_wrk.json file. Generating plot...")
        with open("data_wrk.json", "r") as f:
            data = json.load(f)
        connections = data["connections"]
        results = data["results"]
        plot_results(connections, results, "result_benchmark_wrk.png")
        return

    # Selected mode configurations
    config = modes[args.mode]
    connections_list = config["connections"]
    duration = config["duration"]
    threads = config["threads"]

    # Initialize results
    results = {api: [] for api in endpoints}

    # Total number of tests for the progress bar
    total_tests = len(endpoints) * len(connections_list)

    # Run tests with progress bar
    with tqdm(total=total_tests, desc="Running tests") as pbar:
        for api, url in endpoints.items():
            print(f"\n🔍 Testing {api}")
            for c in connections_list:
                print(f"  - {c} connections for {duration}...")
                rps = run_wrk_test(url, c, duration, threads, args.reps)
                results[api].append(rps)
                time.sleep(5)
                pbar.update(1)

    # Define output file names based on --timestamp option
    if args.timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_file = f"data_wrk_{timestamp}.json"
        plot_file = f"result_benchmark_wrk_{timestamp}.png"
    else:
        json_file = "data_wrk.json"
        plot_file = "result_benchmark_wrk.png"

    # Save data to JSON
    with open(json_file, "w") as f:
        json.dump({
            "connections": connections_list,
            "results": results
        }, f)
        print(f"✅ Data saved to {json_file}")

    # Generate the plot
    plot_results(connections_list, results, plot_file)

if __name__ == "__main__":
    main()