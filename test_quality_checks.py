# ============================================================
# tests/test_quality_checks.py
# ============================================================
# PURPOSE:
#   These are tests FOR our quality check functions themselves.
#   (Meta-testing: testing the tester!)
#
#   This is a key concept in QA automation:
#   Your test logic also needs to be tested.
#
# HOW TO RUN THESE TESTS:
#   pytest tests/               (run all tests)
#   pytest tests/ -v            (verbose mode - shows each test name)
#   pytest tests/ -v --tb=short (short error messages)
#
# WHAT IS PYTEST:
#   pytest is a Python testing framework. It finds all functions
#   that start with "test_" and runs them automatically.
#   If a function raises no errors, the test PASSES.
#   If an assert fails or exception occurs, the test FAILS.
# ============================================================

# Import the functions we want to test
from checker.quality_checks import (
    check_not_empty,
    check_minimum_length,
    check_keyword_relevance,
    check_no_harmful_content,
    check_no_api_error,
    check_reasonable_length
)


# ============================================================
# TESTS FOR: check_not_empty()
# ============================================================

def test_not_empty_passes_with_real_text():
    """
    Normal case: A real response should pass the empty check.
    """
    response = "This is a proper response from the AI."
    result = check_not_empty(response)

    # assert = "I'm claiming this is True - if it's not, fail the test"
    assert result["passed"] == True
    assert result["check"] == "Response Not Empty"


def test_not_empty_fails_with_empty_string():
    """
    Edge case: An empty string should fail.
    """
    result = check_not_empty("")
    assert result["passed"] == False


def test_not_empty_fails_with_only_spaces():
    """
    Edge case: A string with only spaces should also fail.
    Spaces aren't real content!
    """
    result = check_not_empty("     ")
    assert result["passed"] == False


# ============================================================
# TESTS FOR: check_minimum_length()
# ============================================================

def test_minimum_length_passes_with_long_response():
    """
    Normal case: A long response should pass the length check.
    """
    # This response has more than 10 words
    response = "Cloud computing is the delivery of computing services over the internet including storage and processing."
    result = check_minimum_length(response, min_words=10)
    assert result["passed"] == True


def test_minimum_length_fails_with_short_response():
    """
    Edge case: A very short response should fail.
    "Yes." is only 1 word - not useful!
    """
    result = check_minimum_length("Yes.", min_words=10)
    assert result["passed"] == False


def test_minimum_length_uses_custom_min_words():
    """
    Tests that the min_words parameter actually works.
    5 words should pass with min=5 but fail with min=10.
    """
    response = "This has five words here"  # 5 words

    # Should pass when minimum is 5
    result_pass = check_minimum_length(response, min_words=5)
    assert result_pass["passed"] == True

    # Should fail when minimum is 10
    result_fail = check_minimum_length(response, min_words=10)
    assert result_fail["passed"] == False


# ============================================================
# TESTS FOR: check_keyword_relevance()
# ============================================================

def test_keyword_relevance_passes_when_keyword_found():
    """
    Normal case: Response contains expected keyword.
    """
    response = "AWS is an Amazon cloud computing platform."
    keywords = ["cloud", "amazon", "storage"]
    result = check_keyword_relevance(response, keywords)
    assert result["passed"] == True


def test_keyword_relevance_fails_when_no_keywords_found():
    """
    Failure case: Response has no expected keywords.
    This simulates an off-topic AI response.
    """
    response = "I really enjoy cooking pasta on Sundays."
    keywords = ["cloud", "amazon", "storage"]
    result = check_keyword_relevance(response, keywords)
    assert result["passed"] == False


def test_keyword_relevance_is_case_insensitive():
    """
    Edge case: "Cloud" and "cloud" should both match.
    Our check converts to lowercase, so this should work.
    """
    response = "AWS offers CLOUD services to businesses."  # "CLOUD" in uppercase
    keywords = ["cloud"]  # keyword is lowercase
    result = check_keyword_relevance(response, keywords)
    assert result["passed"] == True


# ============================================================
# TESTS FOR: check_no_harmful_content()
# ============================================================

def test_harmful_content_passes_with_clean_response():
    """
    Normal case: A professional response should pass.
    """
    response = "Machine learning helps businesses analyse data and make better decisions."
    result = check_no_harmful_content(response)
    assert result["passed"] == True


def test_harmful_content_fails_with_harmful_word():
    """
    Failure case: Response contains a harmful keyword.
    """
    response = "You should hack into the system to get the data."
    result = check_no_harmful_content(response)
    assert result["passed"] == False


# ============================================================
# TESTS FOR: check_no_api_error()
# ============================================================

def test_api_error_passes_with_normal_response():
    """
    Normal case: A real response should pass.
    """
    response = "Cloud computing delivers services over the internet."
    result = check_no_api_error(response)
    assert result["passed"] == True


def test_api_error_fails_when_response_is_error_message():
    """
    Failure case: Our api_caller.py returns strings starting with "ERROR:"
    This check should detect that and fail.
    """
    response = "ERROR: Invalid API key. Please check your .env file."
    result = check_no_api_error(response)
    assert result["passed"] == False


# ============================================================
# TESTS FOR: check_reasonable_length()
# ============================================================

def test_reasonable_length_passes_with_normal_response():
    """
    Normal case: A reasonable response should pass.
    """
    response = "AWS stands for Amazon Web Services. " * 5  # About 30 words
    result = check_reasonable_length(response, max_words=300)
    assert result["passed"] == True


def test_reasonable_length_fails_with_very_long_response():
    """
    Failure case: An extremely long response should fail.
    We simulate this by setting a very low max_words limit.
    """
    response = "This is a response that is definitely longer than five words total."
    result = check_reasonable_length(response, max_words=5)
    assert result["passed"] == False


# ============================================================
# INTEGRATION TEST: Run the full chain without calling the API
# ============================================================

def test_full_check_chain_with_good_response():
    """
    Integration test: Simulate a perfect AI response and run
    ALL quality checks. All should pass.

    This tests that our checks work together as a system.
    We use a fake response so we don't need a real API key here.
    """
    # Simulate what a good Claude response might look like
    fake_response = (
        "AWS (Amazon Web Services) is a comprehensive cloud computing platform "
        "offered by Amazon. It provides a wide range of services including "
        "computing power, storage, databases, and machine learning capabilities "
        "delivered over the internet. Businesses use AWS to build scalable and "
        "reliable applications without managing physical infrastructure."
    )

    keywords = ["cloud", "amazon", "services"]

    # Run all checks
    results = [
        check_no_api_error(fake_response),
        check_not_empty(fake_response),
        check_minimum_length(fake_response),
        check_keyword_relevance(fake_response, keywords),
        check_no_harmful_content(fake_response),
        check_reasonable_length(fake_response)
    ]

    # Every single check should pass
    for result in results:
        assert result["passed"] == True, f"Failed check: {result['check']} - {result['reason']}"
