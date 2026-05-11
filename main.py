# ============================================================
# main.py
# ============================================================
# PURPOSE:
#   This is the ENTRY POINT of the project.
#   Run this file to start the AI Quality Checker.
#
#   HOW TO RUN:
#       python main.py
#
# WHAT IT DOES:
#   1. Defines test cases (prompt + expected keywords)
#   2. Calls Claude AI with each prompt
#   3. Runs all quality checks on each response
#   4. Prints results to terminal
#   5. Saves a report file to the /reports folder
#
# THINK OF THIS AS:
#   The "main stage" that coordinates everything else.
#   It imports from our other files and runs the full workflow.
# ============================================================

# Import our own modules (the files we built)
from checker.api_caller import call_claude
from checker.quality_checks import (
    check_not_empty,
    check_minimum_length,
    check_keyword_relevance,
    check_no_harmful_content,
    check_no_api_error,
    check_reasonable_length
)
from checker.report_generator import print_results_to_terminal, save_report_to_file


# ============================================================
# DEFINE TEST CASES
# ============================================================
# Each test case is a dictionary with:
#   - "prompt"   : What we send to Claude
#   - "keywords" : Words we expect to see in the response
#                  (used for the keyword relevance check)
#
# Add your own prompts here to test different scenarios!
# ============================================================

TEST_CASES = [
    {
        "prompt": "Explain what AWS cloud computing is in simple terms.",
        "keywords": ["cloud", "amazon", "services", "computing", "infrastructure"]
    },
    {
        "prompt": "What is the difference between unit testing and integration testing?",
        "keywords": ["unit", "integration", "test", "function", "component"]
    },
    {
        "prompt": "What is a REST API?",
        "keywords": ["api", "http", "request", "response", "endpoint", "web"]
    }
]


def run_quality_check(test_case: dict) -> bool:
    """
    Runs the complete quality check workflow for ONE test case.

    Steps:
        1. Call Claude with the prompt
        2. Run all quality checks on the response
        3. Determine overall pass/fail
        4. Print to terminal
        5. Save to file

    Parameters:
        test_case : A dictionary with "prompt" and "keywords" keys

    Returns:
        True if all checks passed, False if any check failed
    """

    prompt = test_case["prompt"]
    keywords = test_case["keywords"]

    print(f"\n⏳ Testing prompt: '{prompt[:60]}...'")

    # Step 1: Call the AI and get a response
    response = call_claude(prompt)

    # Step 2: Run all quality checks on the response
    # Each check function returns a dict with "check", "passed", "reason"
    results = [
        check_no_api_error(response),           # Must run FIRST - if API errored, other checks don't matter
        check_not_empty(response),              # Is the response blank?
        check_minimum_length(response),         # Does it have at least 10 words?
        check_keyword_relevance(response, keywords),  # Does it mention expected topics?
        check_no_harmful_content(response),     # Any dangerous content?
        check_reasonable_length(response)       # Is it excessively long?
    ]

    # Step 3: Overall pass = ALL individual checks must pass
    # all() returns True only if every item in the list is True
    overall_passed = all(result["passed"] for result in results)

    # Step 4: Print results to terminal with colors
    print_results_to_terminal(prompt, response, results, overall_passed)

    # Step 5: Save report to file and tell user where it was saved
    report_path = save_report_to_file(prompt, response, results, overall_passed)
    print(f"📁 Report saved to: {report_path}")

    return overall_passed


def main():
    """
    Main function - runs all test cases and prints a final summary.
    This is the function called when you run "python main.py"
    """

    print("\n" + "🚀 " * 20)
    print("   AI RESPONSE QUALITY CHECKER - STARTING")
    print("🚀 " * 20)
    print(f"\nRunning {len(TEST_CASES)} test case(s)...\n")

    # Track how many tests passed and failed
    passed_count = 0
    failed_count = 0

    # Loop through each test case
    for i, test_case in enumerate(TEST_CASES, start=1):
        print(f"\n{'─' * 60}")
        print(f"  TEST {i} of {len(TEST_CASES)}")
        print(f"{'─' * 60}")

        # Run the quality check for this test case
        passed = run_quality_check(test_case)

        # Update our counters
        if passed:
            passed_count += 1
        else:
            failed_count += 1

    # Print final summary after all tests are done
    print("\n" + "=" * 60)
    print("   FINAL SUMMARY")
    print("=" * 60)
    print(f"  Total Tests  : {len(TEST_CASES)}")
    print(f"  ✅ Passed    : {passed_count}")
    print(f"  ❌ Failed    : {failed_count}")
    print(f"  📁 Reports   : Check the /reports folder")
    print("=" * 60 + "\n")


# ============================================================
# This block ensures main() only runs when you run THIS file
# directly - not when another file imports from it.
# This is a standard Python best practice.
# ============================================================
if __name__ == "__main__":
    main()
