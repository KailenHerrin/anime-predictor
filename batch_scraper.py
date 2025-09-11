import sys
import csv
"""

Currently not sure how I want this to work yet so all this is just a placeholder plus some code that got moved around

        header = ["anime", 
                  "seasons", 
                  "episodes", 
                  "score", 
                  "rank", 
                  "popularity",
                  "members",
                  "favorites", 
                  "age",
                  "time_since_addition",
                  "action",
                  "comedy",
                  "romance",
                  "mystery",
                  "drama",
                  "status"]

try: 
            # Attempt to open and write to filepath
            file_exists = os.path.isfile(filepath)

            with open(filepath, "a", newline="") as fp:
                writer = csv.writer(fp)

                if not file_exists:
                # Check if file exists, if not write a header 
                    writer.writerow(header)

                # Write row of data
                writer.writerow(row)
            
            print(f"Data saved to {filepath}")

        except FileNotFoundError:
            print("Error: The specified filepath is not valid.")



"""