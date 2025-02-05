from bs4 import BeautifulSoup
import statistics
import numpy as np
from collections import Counter
import random
import requests

# Step 1: Get the file from Google Drive using the file ID
def get_google_drive_file(file_id):
    url = f"https://drive.google.com/uc?id={file_id}"  # Making the URL to get the file
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text  # If successful, return the file content
    else:
        raise Exception("Something went wrong. Maybe check the file ID or permissions?")

# Step 2: Fetch the colors data from the file
def fetch_and_parse_colors(file_id):
    try:
        file_content = get_google_drive_file(file_id)
        soup = BeautifulSoup(file_content, 'html.parser')

        rows = soup.find_all("tr")  # Find all table rows
        colors = []

        for row in rows:
            td_elements = row.find_all("td")  # Get table columns
            
            if len(td_elements) > 1:  # Ensure there are at least two columns
                try:
                    color_text = td_elements[1].text.strip()  # Get second column (color)
                    if color_text:
                        colors.extend([color.strip() for color in color_text.split(",")])  # Split by commas
                except IndexError:
                    continue  # Skip faulty rows

        return sorted(colors)  # Always return a sorted list for consistency
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []  # Return an empty list if anything goes wrong

# Step 3: Compute statistics (Mean, Mode, Median, Variance)
def compute_statistics(colors):
    color_counts = Counter(colors)  # Count color frequencies
    most_common_color = color_counts.most_common(1)[0][0] if color_counts else None  # Most frequent color

    # Map colors to numbers consistently
    unique_colors = sorted(set(colors))  # Ensure deterministic order
    color_mapping = {color: i+1 for i, color in enumerate(unique_colors)}
    color_values = np.array([color_mapping[color] for color in colors]) if colors else np.array([])

    mean_color = np.mean(color_values) if color_values.size else None
    median_color = np.median(color_values) if color_values.size else None
    variance = np.var(color_values, ddof=1) if color_values.size > 1 else None  # Sample variance

    # Map numeric mean/median back to colors
    mean_color_name = min(color_mapping, key=lambda k: abs(color_mapping[k] - mean_color)) if mean_color else None
    median_color_name = min(color_mapping, key=lambda k: abs(color_mapping[k] - median_color)) if median_color else None

    return most_common_color, mean_color_name, median_color_name, variance

# Step 4: Calculate the probability of 'Red'
def calculate_red_probability(colors):
    color_counts = Counter(colors)
    return color_counts.get("RED", 0) / len(colors) if colors else 0  # Avoid division by zero

# Step 5: Store color frequencies in a dictionary
def store_in_dict(colors):
    return dict(Counter(colors))  # Convert frequency count to dictionary

# Step 6: Iterative binary search
def iterative_search(arr, target):
    low, high = 0, len(arr) - 1  # Search range
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid  # Found it!
        elif arr[mid] > target:
            high = mid - 1  # Search left
        else:
            low = mid + 1  # Search right
    return -1  # Not found

# Step 7: Generate a fixed random 4-bit binary number and convert to base 10
def generate_binary():
    random.seed(42)  # Fixed seed for reproducibility
    binary_number = "".join(str(random.randint(0, 1)) for _ in range(4))
    base10_number = int(binary_number, 2)
    return binary_number, base10_number

# Step 8: Sum of first 50 Fibonacci numbers
def fibonacci_sum(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

# Main function
def main():
    random.seed(42)  # Ensure consistent randomness throughout
    file_id = "1nf9WMDjZWIUnlnKyz7qomEYDdtWfW1Uf"  # Google Drive file ID

    colors = fetch_and_parse_colors(file_id)  # Get color data
    most_common_color, mean_color_name, median_color_name, variance = compute_statistics(colors)

    prob_red = calculate_red_probability(colors)  # Probability of 'Red'
    color_frequencies = store_in_dict(colors)  # Color frequencies dictionary

    sorted_colors = sorted(colors)  # Sort for binary search consistency
    target_color = "BLUE"
    search_result = iterative_search(sorted_colors, target_color)

    binary_number, base10_number = generate_binary()  # Fixed binary number
    fib_sum = fibonacci_sum(50)  # First 50 Fibonacci sum

    # Print results
    print(f"Mean Color: {mean_color_name}")
    print(f"Most Worn Color: {most_common_color}")
    print(f"Median Color: {median_color_name}")
    print(f"Variance: {variance}")
    print(f"Probability of Red: {prob_red:.2f}")
    print(f"Generated Binary Number: {binary_number}, Base 10: {base10_number}")
    print(f"Sum of First 50 Fibonacci Numbers: {fib_sum}")
    print(f"Search Result for '{target_color}': {search_result if search_result != -1 else 'Not Found'}")
    print(f"Color Frequencies: {color_frequencies}")

# Run program
if __name__ == "__main__":
    main()
