from bs4 import BeautifulSoup
import statistics
from collections import Counter
import random
import requests
import pandas as pd

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
        # Get the file content and parse it using BeautifulSoup
        file_content = get_google_drive_file(file_id)
        soup = BeautifulSoup(file_content, 'html.parser')
        
        rows = soup.find_all("tr")  # Find all the rows in the table
        colors = []

        # Go through each row and get color data
        for row in rows:
            td_elements = row.find_all("td")  # Find all the columns in this row
            
            if len(td_elements) > 1:  # Only proceed if there's more than 1 column
                try:
                    color_text = td_elements[1].text.strip()  # Get the second column text (color info)
                    if color_text:
                        colors.extend([color.strip() for color in color_text.split(",")])  # Add the colors to the list
                except IndexError:
                    continue  # Skip if something is wrong with this row
        return colors
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []  # Return an empty list if anything goes wrong

# Step 3: Calculate some statistics (Mean, Mode, Median, Variance)
def compute_statistics(colors):
    color_counts = Counter(colors)  # Count how many times each color appears
    most_common_color = color_counts.most_common(1)[0][0] if color_counts else None  # Find the most common color

    color_mapping = {color: i+1 for i, color in enumerate(set(colors))}  # Map each color to a number
    color_values = [color_mapping[color] for color in colors] if colors else []  # Get the numeric values for the colors

    mean_color = statistics.mean(color_values) if color_values else None  # Calculate the mean (average) color
    median_color = statistics.median(color_values) if color_values else None  # Calculate the median color
    variance = statistics.variance(color_values) if len(color_values) > 1 else None  # Calculate the variance

    # Reverse the numeric values back to color names for mean and median
    mean_color_name = min(color_mapping, key=lambda k: abs(color_mapping[k] - mean_color)) if mean_color else None
    median_color_name = min(color_mapping, key=lambda k: abs(color_mapping[k] - median_color)) if median_color else None

    return most_common_color, mean_color_name, median_color_name, variance

# Step 4: Calculate the probability of 'Red' showing up in the data
def calculate_red_probability(colors):
    color_counts = Counter(colors)
    return color_counts.get("Red", 0) / len(colors) if colors else 0  # If there's no data, return 0

# Step 5: Store the frequency of each color in a dictionary
def store_in_dict(colors):
    color_counts = Counter(colors)  # Count the frequency of each color
    return dict(color_counts)  # Convert the counter to a dictionary

# Step 6: Simple binary search algorithm
def iterative_search(arr, target):
    low, high = 0, len(arr) - 1  # Set the starting and ending points for the search
    while low <= high:
        mid = (low + high) // 2  # Find the middle index
        if arr[mid] == target:
            return mid  # If found, return the index
        elif arr[mid] > target:
            high = mid - 1  # Look in the left half
        else:
            low = mid + 1  # Look in the right half
    return -1  # Return -1 if the target isn't found

# Step 7: Generate a random 4-bit binary number and convert it to base 10
def generate_binary():
    binary_number = "".join(str(random.randint(0, 1)) for _ in range(4))  # Randomly generate a 4-bit binary number
    base10_number = int(binary_number, 2)  # Convert the binary number to base 10
    return binary_number, base10_number

# Step 8: Calculate the sum of the first 50 Fibonacci numbers
def fibonacci_sum(n):
    a, b = 0, 1  # Starting values for Fibonacci numbers
    total = 0  # The sum of the Fibonacci numbers
    for _ in range(n):
        total += a  # Add the current Fibonacci number to the total
        a, b = b, a + b  # Move to the next Fibonacci numbers
    return total

# Main function that ties everything together
def main():
    random.seed(42)  # Set the seed for randomness, so it's always the same each time we run
    file_id = "1nf9WMDjZWIUnlnKyz7qomEYDdtWfW1Uf"  # The ID of the Google Drive file
    
    colors = fetch_and_parse_colors(file_id)  # Get and parse the color data from the file
    colors.sort()  # Sort the colors so that order doesn't change on different runs

    most_common_color, mean_color_name, median_color_name, variance = compute_statistics(colors)  # Calculate stats

    prob_red = calculate_red_probability(colors)  # Calculate the probability of 'Red'

    color_frequencies = store_in_dict(colors)  # Store color frequencies in a dictionary

    sorted_colors = sorted(colors)  # Sort the colors for binary search
    target_color = "Blue"  # We're searching for 'Blue'
    search_result = iterative_search(sorted_colors, target_color)  # Perform binary search

    binary_number, base10_number = generate_binary()  # Generate a random binary number and convert to base 10

    fib_sum = fibonacci_sum(50)  # Get the sum of the first 50 Fibonacci numbers

    # Print the results
    print(f"Mean Color: {mean_color_name}")
    print(f"Most Worn Color: {most_common_color}")
    print(f"Median Color: {median_color_name}")
    print(f"Variance: {variance}")
    print(f"Probability of Red: {prob_red:.2f}")
    print(f"Generated Binary Number: {binary_number}, Base 10: {base10_number}")
    print(f"Sum of First 50 Fibonacci Numbers: {fib_sum}")
    print(f"Search Result for '{target_color}': {search_result if search_result != -1 else 'Not Found'}")
    print(f"Color Frequencies: {color_frequencies}")

# If this is the main file, run the main function
if __name__ == "__main__":
    main()
