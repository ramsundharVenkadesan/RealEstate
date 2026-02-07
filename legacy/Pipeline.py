# File: pipeline.py
import subprocess
import sys
import os
import re

# --- Constants & Configuration ---
# Set the correct working directory path for subprocess execution
# This assumes the original Spider.py, Analyze.py, and Plot.py are in the same directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_spider(area: str):
    """Executes Spider.py to scrape data for the specified area."""
    json_file = f"{area}.json"
    print(f"STEP 1: Running Spider.py for area: {area}")

    try:
        result = subprocess.run(
            [sys.executable, os.path.join(BASE_DIR, "Spider.py"), area],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Spider.py output:\n{result.stdout}")

        if os.path.exists(os.path.join(BASE_DIR, json_file)):
            return True, json_file
        else:
            print(f"✗ Error: {json_file} not found after spider execution.")
            return False, None
    except subprocess.CalledProcessError as e:
        print(f"Error running Spider.py: {e.stderr}")
        return False, None
    except Exception as e:
        print(f"Unexpected error in Spider.py: {e}")
        return False, None


def run_analysis_and_plot(json_file: str):
    """
    Executes Analyze.py and Plot.py sequentially using the generated JSON file.

    This function temporarily modifies the Python files to accept the dynamic
    JSON filename, as your original execution script does.
    """
    base_name = json_file.replace('.json', '')
    output_plot_file = f"price_analysis_{base_name}.jpeg"

    # --- Step 2: Run Analyze.py ---
    print("\nSTEP 2: Running Analyze.py")
    if not _run_script_with_dynamic_file("Analyze.py", json_file, 'JSON_FILE_NAME = "globe.json"',
                                         'analyze_real_estate_data'):
        return False, None

    # --- Step 3: Run Plot.py ---
    print("\nSTEP 3: Running Plot.py")
    if not _run_script_with_dynamic_file("Plot.py", json_file,
                                         'JSON_FILE_NAME = "globe.json"', 'generate_analysis_plot',
                                         secondary_replace=('OUTPUT_FILE_NAME = \'price_analysis_globe.jpeg\'',
                                                            f'OUTPUT_FILE_NAME = \'price_analysis_{base_name}.jpeg\'')):
        return False, None

    return True, output_plot_file


def _run_script_with_dynamic_file(script_name, file_to_use, placeholder_replace, func_to_run, secondary_replace=None):
    """
    Helper to temporarily modify and run Analyze.py or Plot.py.
    """
    original_path = os.path.join(BASE_DIR, script_name)
    temp_path = os.path.join(BASE_DIR, f"{script_name.replace('.py', '_temp.py')}")

    try:
        with open(original_path, "r") as f:
            content = f.read()

        # Primary replacement: JSON filename
        modified_content = content.replace(placeholder_replace, f'JSON_FILE_NAME = "{file_to_use}"')

        # Secondary replacement (for Plot.py's output filename)
        if secondary_replace:
            modified_content = modified_content.replace(secondary_replace[0], secondary_replace[1])

        # Write temporary file
        with open(temp_path, "w") as f:
            f.write(modified_content)

        # Run the modified script
        result = subprocess.run(
            [sys.executable, temp_path],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
        )

        print(f"{script_name} output:\n{result.stdout}")

        if result.returncode != 0:
            print(f"Error executing {script_name}:\n{result.stderr}")
            return False

        return True

    except Exception as e:
        print(f"Error during temporary execution of {script_name}: {e}")
        return False
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


def run_full_pipeline(area: str):
    """Runs the full scraping, analysis, and plotting pipeline."""
    success, json_file = run_spider(area)
    if not success:
        return {"status": "error", "message": "Failed to scrape data."}

    success, plot_file = run_analysis_and_plot(json_file)
    if not success:
        return {"status": "error", "message": "Failed during analysis or plotting."}

    return {
        "status": "success",
        "message": f"Pipeline completed for area '{area}'.",
        "json_file": json_file,
        "plot_file": plot_file,
        "plot_url": f"/plots/{plot_file}"
    }


if __name__ == "__main__":
    # Example usage for testing the pipeline directly
    if len(sys.argv) > 1:
        AREA = sys.argv[1]
    else:
        AREA = "globe"

    result = run_full_pipeline(AREA)
    print("\n--- Final Pipeline Result ---")
    import json

    print(json.dumps(result, indent=4))
