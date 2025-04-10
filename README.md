# Web Framework Benchmark: Python vs Rust

This project benchmarks the performance of web frameworks in Python (FastAPI, Django DRF, Django Ninja) and Rust (Axum, Rocket, Actix) using the `wrk` load testing tool. It measures Requests per Second (RPS) under varying concurrent connection loads and generates a comparative plot.

## Features

- Tests multiple web frameworks with configurable connection loads, durations, and thread counts.
- Supports three test modes: `fast`, `full`, and `stress`.
- Generates a plot comparing RPS across frameworks.
- Automated setup and cleanup using Docker Compose and a Bash script.
- Saves results in JSON format for further analysis.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.8+](https://www.python.org/downloads/)
- [wrk](https://github.com/wg/wrk) (load testing tool)
- Bash (for running the test script on Unix-like systems)

## Project Structure

```
├── docker-compose.yml      # Defines services for Python and Rust frameworks
├── run_test.sh             # Bash script to run tests and clean up
├── benchmark_wrk.py        # Python script for benchmarking and plotting
├── python_apps/            # Directory with Python framework apps
│   ├── fastapi_app/
│   ├── drf_app/
│   └── ninja_app/
├── rust_apps/              # Directory with Rust framework apps
│   ├── rust_axum/
│   ├── rust_rocket/
│   └── rust_actix/
└── README.md               # This file
```

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/fzappa/benchmarking_apis.git
   cd benchmarking_api
   ```

2. **Install Python Dependencies**
   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   If a `requirements.txt` doesn't exist yet, install these manually:

   ```bash
   pip install matplotlib numpy tqdm
   ```

3. **Install wrk**

   - On Ubuntu/Debian:
     ```bash
     sudo apt-get install wrk
     ```
   - On macOS:
     ```bash
     brew install wrk
     ```
   - See [wrk's GitHub](https://github.com/wg/wrk#installing) for other systems.

4. **Ensure Docker is Running**
   Verify Docker is installed and running:
   ```bash
   docker --version
   docker compose version
   ```

## Usage

The project includes a Bash script (`run.sh`) to automate building, testing, and cleanup.

1. **Run the Full Test**

   ```bash
   bash run.sh
   ```

   This will:

   - Build and start Docker containers for all frameworks.
   - Run the `full` benchmark mode with 5 repetitions.
   - Stop and remove containers and images afterward.
   - Generate a plot (`benchmark_wrk_result.png`) and save data (`wrk_data.json`).

2. **Customize the Test**
   Modify `run_test.sh` or run `benchmark_wrk.py` directly with arguments:

   ```bash
   python benchmark_wrk.py --mode full --reps 5 --timestamp
   ```

   - `--mode`: `fast`, `full`, or `stress` (default: `fast`).
   - `--reps`: Number of test repetitions (default: 3).
   - `--timestamp`: Append a timestamp to output files.

3. **View Results**
   - **Plot**: Check `benchmark_wrk_result.png` (or a timestamped version if `--timestamp` is used).
   - **Data**: Open `wrk_data.json` for raw RPS values.

## Test Modes

- **`fast`**: Quick test with 1 and 10 connections, 3-second duration, 1 thread.
- **`full`**: Comprehensive test with 1 to 1000 connections, 5-second duration, 8 threads.
- **`stress`**: Stress test with 100 to 1000 connections, 20-second duration, 8 threads.

## Docker Services

The `docker-compose.yml` defines six services:

- **FastAPI**: Python, port `8001`
- **Django DRF**: Python, port `8002`
- **Django Ninja**: Python, port `8003`
- **Axum**: Rust, port `3000`
- **Rocket**: Rust, port `8000`
- **Actix**: Rust, port `8080`

Each service has its own Dockerfile in the respective `python_apps/` or `rust_apps/` directory.

## Example Output

After running the test, you’ll get:

- A plot comparing RPS across frameworks on a logarithmic scale.
- A JSON file with connection counts and RPS results.

Example plot:
![Benchmark Result](benchmark_wrk_result.png)

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the GPLv3 License. See [GPLv3](LICENSE) for details.

## Acknowledgments

- Inspired by the need to compare Python and Rust web framework performance.
- Thanks to the `wrk` team for an excellent benchmarking tool.
