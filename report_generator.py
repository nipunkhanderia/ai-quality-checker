# ============================================================
# checker/report_generator.py
# ============================================================
# PURPOSE:
#   Takes the results of all quality checks and:
#   1. Prints a colorful summary to the terminal
#   2. Saves a detailed report as a text file in the /reports folder
#
# THINK OF THIS AS:
#   The "printer" that formats and outputs test results.
#   Like generating a QA test report in any professional project.
# ============================================================

import os
from datetime import datetime  # To timestamp our reports
from colorama import Fore, Style, init  # For colored terminal output

# Initialize colorama - this makes colors work on Windows too
init(autoreset=True)


def print_results_to_terminal(prompt: str, response: str, results: list, overall_passed: bool):
    """
    Prints the quality check results to the terminal in a readable format.
    Uses colors: GREEN for pass, RED for fail.

    Parameters:
        prompt         : The original prompt that was sent to the AI
        response       : The AI's response text
        results        : List of check result dictionaries from quality_checks.py
        overall_passed : True if ALL checks passed, False otherwise
    """

    print("\n" + "=" * 60)
    print("         AI RESPONSE QUALITY CHECKER - RESULTS")
    print("=" * 60)

    # Show what prompt was tested
    print(f"\n📝 PROMPT TESTED:")
    # Truncate long prompts to 100 chars so terminal doesn't overflow
    print(f"   {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

    # Show the AI's response (truncated for readability)
    print(f"\n🤖 AI RESPONSE (first 200 chars):")
    print(f"   {response[:200]}{'...' if len(response) > 200 else ''}")

    print(f"\n📊 QUALITY CHECKS:")
    print("-" * 60)

    # Loop through each check result and print with color
    for result in results:
        if result["passed"]:
            # Green checkmark for pass
            status = f"{Fore.GREEN}✅ PASS{Style.RESET_ALL}"
        else:
            # Red X for fail
            status = f"{Fore.RED}❌ FAIL{Style.RESET_ALL}"

        print(f"  {status} | {result['check']}")
        print(f"         └── {result['reason']}")

    print("-" * 60)

    # Show overall result with big colored text
    if overall_passed:
        print(f"\n🎯 OVERALL RESULT: {Fore.GREEN}ALL CHECKS PASSED ✅{Style.RESET_ALL}")
    else:
        # Count how many checks failed
        failed_count = sum(1 for r in results if not r["passed"])
        print(f"\n🎯 OVERALL RESULT: {Fore.RED}{failed_count} CHECK(S) FAILED ❌{Style.RESET_ALL}")

    print("=" * 60 + "\n")


def save_report_to_file(prompt: str, response: str, results: list, overall_passed: bool):
    """
    Saves the complete test results to a text file in the /reports folder.
    The filename includes a timestamp so each run creates a new file.

    Parameters:
        prompt         : The original prompt that was sent to the AI
        response       : The AI's response text
        results        : List of check result dictionaries from quality_checks.py
        overall_passed : True if ALL checks passed, False otherwise

    Returns:
        The file path where the report was saved
    """

    # Create the reports folder if it doesn't exist yet
    reports_folder = "reports"
    os.makedirs(reports_folder, exist_ok=True)

    # Create a timestamp for the filename (e.g., "2024-01-15_14-30-45")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{reports_folder}/report_{timestamp}.txt"

    # Write the report content to the file
    with open(filename, "w", encoding="utf-8") as file:

        file.write("=" * 60 + "\n")
        file.write("   AI RESPONSE QUALITY CHECKER - DETAILED REPORT\n")
        file.write("=" * 60 + "\n\n")

        # Timestamp of when this report was generated
        file.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Full prompt
        file.write("PROMPT:\n")
        file.write(f"{prompt}\n\n")

        # Full AI response
        file.write("AI RESPONSE:\n")
        file.write(f"{response}\n\n")

        # All check results
        file.write("QUALITY CHECKS:\n")
        file.write("-" * 60 + "\n")
        for result in results:
            status = "PASS ✅" if result["passed"] else "FAIL ❌"
            file.write(f"[{status}] {result['check']}\n")
            file.write(f"  Reason: {result['reason']}\n\n")

        # Overall verdict
        file.write("-" * 60 + "\n")
        overall = "ALL CHECKS PASSED ✅" if overall_passed else "ONE OR MORE CHECKS FAILED ❌"
        file.write(f"OVERALL RESULT: {overall}\n")
        file.write("=" * 60 + "\n")

    return filename
