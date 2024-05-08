# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 08:23:23 2023

@author: cs11
"""

import random
import textwrap
import csv
import google.generativeai as genai

print("Loading Gemini...")

# CHANGE THIS TO YOUR OWN API KEY FOR YOUR OWN USE
GOOGLE_API_KEY = "AIzaSyBmFVUgOgUwChhgrTrJmS0OzYkKPsaj5GA"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.0-pro-latest")

w = textwrap.TextWrapper(width=100,break_long_words=False,replace_whitespace=False)

CORRECT_COUNT = 0
QUESTIONS_ANSWERED = 0
STREAK = 0


def load_questions_and_answers(file_name):
    """Get questions and answers from file"""
    with open(file_name) as f:
        tsv_file = list(csv.reader(f, delimiter='\t'))[1:]
    return tsv_file


def get_random_question(qa):
    """Get a random question from list"""
    return random.choice(qa)


def ask_question(qa):
    """Ask a random question and test for correct answer"""
    global QUESTIONS_ANSWERED
    global STREAK
    QUESTIONS_ANSWERED += 1
    
    q = get_random_question(qa)
    # Print question information
    prompt = q[0]+'\n'+q[1]+'\n\n'+q[2]+'\n'
    ltr = 65
    questions = q[3:-1]
    # random.shuffle(questions)
    for answer in questions:
        if "n/a" in answer.lower():
            continue
        prompt += f"\n{chr(ltr)}. {answer}"
        ltr += 1
    print('\n'.join('\n'.join(w.wrap(i)) for i in prompt.split('\n')))

    # Get answer and check it
    a = input()
    print()
    while True:
        if a not in "abcde":
            continue
        if a.lower() == q[-1].lower():
            STREAK += 1
            print("Correct")
            print(f"Current score: {(CORRECT_COUNT + 1) / QUESTIONS_ANSWERED * 100:.2f}%"
                f" ({CORRECT_COUNT + 1} / {QUESTIONS_ANSWERED})")
            print(f"Streak: {STREAK}")
            print("==========")
            qa.remove(q)
            return True
        else:
            break
    STREAK = 0
    print("Incorrect")

    # Gemini Explanation
    print(f"The correct answer is {q[-1]}.\n")
    print("Explanation by Gemini (may be incorrect):")
    response = model.generate_content(
"""Answer any following multiple choice questions with an extremely brief explanation on why the correct answer is correct and why the others are wrong in this format:
`
The correct answer is (Answer Letter). (Answer Name)

Explanation: (Explanation on why the correct answer is correct)

(Explanation on the other answers)
`

Here's an example:
`
The correct answer is A. OCSP

Explanation: OCSP (Online Certificate Status Protocol) is specifically designed to check for certificate revocation by allowing the browser to request the status of a certificate from a designated OCSP responder.

TLS (B) is a transport layer security protocol that establishes a secure connection, but it does not directly check for certificate revocation.
CN (C) refers to the Common Name field in a certificate, which identifies the subject of the certificate, not its revocation status.
CSR (D) is a Certificate Signing Request, which is used to request a certificate from a Certificate Authority (CA).
CA (E) is the Certificate Authority that issues certificates, but it is not responsible for checking certificate revocation.
`

Do not use any markdown formatting. Define any abbreviations.

"""+"Question:\n"+prompt+f"\n\nThe correct answer is {q[-1]}."
    )

    print('\n'.join('\n'.join(w.wrap(i)) for i in response.text.split('\n')))

    input("\nPress Enter to continue.")

    print(f"Current score: {CORRECT_COUNT / QUESTIONS_ANSWERED * 100:.2f}%"
          f" ({CORRECT_COUNT} / {QUESTIONS_ANSWERED})")
    print("==========")
    return False


def main():
    """stuff"""
    global CORRECT_COUNT

    file_name = "questions.tsv" #input('What is the name of the QA file? ')
    while True:
        number_of_questions = input('How many questions should be asked (Type "all" if you want all the questions)? ')
        questions_answers = load_questions_and_answers(file_name)
        if number_of_questions.lower() == "all":
            number_of_questions = len(questions_answers)
            break
        else:
            try:
                number_of_questions = int(number_of_questions)
                break
            except ValueError:
                print("That is not a valid option.")
    print("==========")

    for _ in range(number_of_questions):
        CORRECT_COUNT += ask_question(questions_answers)

    print('You got', CORRECT_COUNT, 'out of', number_of_questions, 'correct.')
    print(f"Your percentage grade: {CORRECT_COUNT / number_of_questions * 100:.2f}%")
    input('Press ENTER to exit')


if __name__ == "__main__":
    main()
