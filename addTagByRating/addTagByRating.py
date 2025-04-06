# Need to install "brew install exiftool" and "brew install tag"

import os
import subprocess

# Mapping between ratings and macOS tags
RATING_TO_TAG = {
    1: "Red",
    2: "Orange",
    3: "Yellow",
    4: "Green",
    5: "Blue"
}

def set_tag_by_rating(directory):
    """
    Reads the ratings (1–5 stars) from image files in the given directory
    and sets macOS tags based on the rating.
    """
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.arw')):  # Add other extensions if needed
            filepath = os.path.join(directory, filename)
            try:
                # Run the exiftool command to get metadata
                result = subprocess.run(
                    ["exiftool", "-XMP:Rating", filepath],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                # Parse the output to extract the rating
                output = result.stdout.strip()
                if "Rating" in output:
                    # Extract the rating value
                    rating_line = output.split(":")[-1].strip()
                    try:
                        rating = int(rating_line)
                        tag = RATING_TO_TAG.get(rating)
                        if tag:
                            # Set the macOS tag using the `tag` command
                            subprocess.run(
                                ["tag", "--set", tag, filepath],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True
                            )
                            print(f"File: {filename}, Rating: {rating}, Tag: {tag}")
                        else:
                            print(f"File: {filename}, Rating: {rating}, No tag mapping found.")
                    except ValueError:
                        print(f"File: {filename}, Invalid rating value: {rating_line}")
                else:
                    print(f"File: {filename}, Rating: Not Found")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

if __name__ == "__main__":
    # Prompt the user to input the path to the image directory
    image_directory = input("Enter the path to your image directory: ").strip()
    if os.path.isdir(image_directory):
        set_tag_by_rating(image_directory)
    else:
        print("The provided path is not a valid directory.")

