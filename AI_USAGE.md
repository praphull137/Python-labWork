# AI Usage Disclosure

<!--
Fill in this file before you submit. Submissions without it are not graded.
If you used no AI tools, delete everything below and write only:
No AI tools were used.
-->

## Tools used

- Tool and version (e.g. ChatGPT GPT-5, Claude, GitHub Copilot):

Tool and version: ChatGPT (OpenAI), GPT-6
## Conversation links

- Link 1: https://chatgpt.com/g/g-p-6af897787fb88191a41ee7a8dbef1a2b-python-lab-help/c/6af8a7cc-0ddc-83ed-a202-b9a8bbffbea8

- Link 2:

## What I used them for

- e.g. explaining argparse, debugging the date validation, generating test data
I used ChatGPT only to get help and guidance while working on this assignment.

I used it for:

Understanding which logic I should implement for the required functions.

Understanding how to handle different test cases.

Getting suggestions when I was confused about the implementation.

Debugging some parts of my code when I faced errors.

Understanding why a particular approach or condition was needed.

## Which parts of the code were AI-generated or substantially AI-assisted

| File | Function or part | How (generated / modified / explained) |
| flight_parser.py--- |main() --- |Used AI for guidance about the logic, handling test cases and debugging some parts. I wrote the implementation myself. --- |
| validator.py |validate_row()  |Used AI to understand which validation logic was required and how to handle different test cases. I wrote the implementation myself.  

## Key prompts

1.what is the requirement of validator function ?;

| `validator.py` | `load_airports(path: str) -> set[str]`, `validate_row(fields: list[str], airports: set[str]) -> str \| None`, `to_record(fields: list[str]) -> dict` |
explain the requirement

2."""Read an airport list file and return the set of codes.

    One code per line. Strip whitespace; skip blank lines and lines
    starting with '#'.
    """ what does this comment means in validator file? does it tells something like, I need to skip the code having whitespace or some other meaning ?

3.error = validate_row(fields, airports)
                file_name = Path(path).name
                original_line = line.rstrip("\r\n")

                if error is not None:
                    errors.append(
                        f"{file_name}:{line_number}: {error} | {original_line}"
                    )
                    is this logic correct for validate row function ?

4.I have one doubt about this duplicate detection code. If I check only flight-id instead of checking both flight_id  and departurei_id, will it still detect duplicates correctly? Because the same flight ID can have different departure times. Should we consider both values to identify a duplicate?

5.I have one doubt about the run_qquery function. If a query contains multiple conditions, like origin, price and sorting, should we first filter all the matching flights and then sort them, or does the order of these operations matter?

6.If one query in a JSON list is invalid, should the program stop processing the remaining queries, or should it return an error for that query and continue with the others? and what logic should I need to implement for this issue ?


7.Why are we checking whether the query is a dictionary at the beginning? What happens if we don't check it? and If a query contains multiple conditions, like origin, destination and price, are we checking all conditions one by one for every flight?
## What I changed or verified myself

I wrote the code myself based on the assignment requirements.

I implemented the logic for the functions myself.

I used the public tests to check my implementation.

I fixed issues in my code after understanding the errors.

I tested the program with single CSV files and folders containing multiple CSV files.

I tested JSON database loading and query processing.

I checked the generated database, error log and response JSON file.

I ran the public test suite and got 29 out of 29 tests passing.

I reviewed the results myself to check that the program worked correctly.


