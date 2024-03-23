#!/bin/bash

# Check if the number of arguments is correct
if [ $# -lt  1 ]; then
    echo "Usage: $0 <file1> [<file2> ...]"
    exit  1
fi

print_colored_message() {
    local message=$1
    local color=$2
    case $color in
        green) echo -e "\033[1;32m$message\033[0m" ;;
        red) echo -e "\033[1;31m$message\033[0m" ;;
        blue) echo -e "\033[0;34m$message\033[0m" ;;
        *) echo "$message" ;;
    esac
}

passed=0
test_res_dir="tests/systestres"
mkdir -p $test_res_dir
# Loop through each file provided as an argument
for file in "$@"; do
    # Check if the file exists
    if [ ! -f "$file" ]; then
        echo "Error: File '$file' does not exist."
        continue
    fi

    # Run the C program with /bin/bash and ./shell as arguments, redirecting the output to a temporary file
    shell_of=$(mktemp)
    bash_of=$(mktemp)
    ./tests/systests /bin/bash "$file" > "$bash_of"  2>&1
    ./tests/systests ./shell "$file" > "$shell_of"  2>&1

    # Use diff -y to compare the output of the C program with the expected output
    # Assuming the expected output is stored in a file named "expected_output"
    res_of=$test_res_dir/$(basename "$file")
    rm $res_of 2> /dev/null
    diff -y "$shell_of" "$bash_of" > "$res_of"
    if [ "$?" -eq 0 ]; then
        print_colored_message "PASSED $file" green
        ((passed++))
    else
        print_colored_message "FAILED $file" red
        print_colored_message "Test results in $res_of" blue
    fi

    # Clean up the temporary file
    rm "$shell_of" "$bash_of"
done
echo
print_colored_message "Passed $passed/$# tests." blue
