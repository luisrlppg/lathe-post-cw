import re
import sys
import os

def process_gcode_file(file_path):
    """
    Processes a G-code file to:
    1. Find (Q-HERE) markers and insert the N number as a Q value in the preceding G71/G72 line.
    2. Remove the (Q-HERE) marker lines.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except IOError as e:
        print(f"Error reading file: {e}")
        return

    q_markers = {}
    last_g7x_line_index = -1
    lines_to_delete = []

    # First pass: find Q markers and associate them with the preceding G71/G72 line
    for i, line in enumerate(lines):
        # Find the last G71/G72 line that doesn't have a Q value
        # And ensure it's not a comment line that might contain G71/G72
        if ('G71' in line or 'G72' in line) and 'Q' not in line and not line.strip().startswith('('):
            last_g7x_line_index = i
        
        # If we find a marker, store the Q value and the index of the G71/G72 line
        if '(Q-HERE)' in line:
            # The Q value should be the N number of the line *before* the marker
            if i > 0:
                prev_line = lines[i - 1]
                match = re.search(r'N(\d+)', prev_line)
                if match and last_g7x_line_index != -1:
                    q_value = int(match.group(1))
                    q_markers[last_g7x_line_index] = q_value
                    lines_to_delete.append(i)
                    last_g7x_line_index = -1 # Reset for the next one

    new_lines = []
    # Second pass: build the new file content
    for i, line in enumerate(lines):
        if i in lines_to_delete:
            continue

        processed_line = line

        # If this line is a G71/G72 that needs a Q value, insert it
        if i in q_markers:
            q_value = q_markers[i]
            # Ensure we're targeting the correct line that contains G71/G72 P-word
            match = re.search(r'(G7[12]\s*P\d+)', processed_line)
            if match:
                processed_line = processed_line.replace(match.group(1), f'{match.group(1)}Q{q_value}')

        new_lines.append(processed_line)

    try:
        with open(file_path, 'w') as f:
            f.writelines(new_lines)
        print(f"Successfully processed {file_path}")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_gcode.py <path_to_gcode_file>")
        sys.exit(1)

    gcode_file = sys.argv[1]
    process_gcode_file(gcode_file)