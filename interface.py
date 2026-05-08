"""
============================================================
  Expert System for Disease Diagnosis - Python Interface
  File: interface.py
  Course: AI406 - Knowledge Representation and Reasoning
  Pharos University in Alexandria
============================================================
"""

# ── Imports ────────────────────────────────────────────────
from pyswip import Prolog          # Bridge between Python and Prolog
import os                          # For file path handling

# ── Step 1: Initialize Prolog and load knowledge base ──────
prolog = Prolog()

# Get the directory where this script lives, then build path to .pl file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH  = os.path.join(BASE_DIR, "expert_system.pl")

prolog.consult(KB_PATH)            # Load the Prolog knowledge base
print("✅  Knowledge base loaded successfully.\n")


# ── Helper Functions ────────────────────────────────────────

def get_all_symptoms():
    """Return a sorted list of every symptom known in the KB."""
    results = list(prolog.query("symptom(_, S)"))   # Query all symptom facts
    symptoms = sorted({str(r["S"]) for r in results})
    return symptoms


def diagnose(symptom_list):
    """
    Ask Prolog to find diseases whose symptoms match the input.
    Returns a list of (disease, score) tuples sorted by score descending.
    """
    # Build a Prolog list string from the Python list
    # e.g. ['fever','cough','fatigue']  →  [fever,cough,fatigue]
    prolog_list = "[" + ",".join(symptom_list) + "]"

    # Run the diagnose/3 predicate we defined in the .pl file
    query = f"diagnose({prolog_list}, Disease, Score)"
    results = list(prolog.query(query))

    # Convert results to Python tuples and sort by score (highest first)
    diagnoses = [(str(r["Disease"]), int(r["Score"])) for r in results]
    diagnoses.sort(key=lambda x: x[1], reverse=True)
    return diagnoses


def get_treatment(disease):
    """Fetch the treatment string for a given disease from the KB."""
    query = f"get_treatment({disease}, Treatment)"
    results = list(prolog.query(query))
    if results:
        return str(results[0]["Treatment"])
    return "No treatment information available."


def print_banner():
    """Print a decorative welcome banner."""
    print("=" * 60)
    print("   🏥  EXPERT SYSTEM FOR DISEASE DIAGNOSIS")
    print("   Course: AI406 | Pharos University")
    print("=" * 60)
    print()


def print_all_symptoms():
    """Display every symptom available in the system."""
    symptoms = get_all_symptoms()
    print("\n📋  Available Symptoms in the Knowledge Base:")
    print("-" * 40)
    # Print in columns of 3
    for i, s in enumerate(symptoms, 1):
        print(f"  {i:2}. {s:<28}", end="" if i % 3 != 0 else "\n")
    print("\n")


def get_user_symptoms():
    """
    Interactively ask the user to enter their symptoms one by one.
    Returns a list of valid symptom atoms.
    """
    known_symptoms = set(get_all_symptoms())
    entered = []

    print("💬  Enter your symptoms one by one.")
    print("    Type 'done' when finished, 'list' to see all symptoms.\n")

    while True:
        raw = input("   ➤  Symptom: ").strip().lower().replace(" ", "_")

        if raw == "done":
            if len(entered) == 0:
                print("   ⚠️  Please enter at least one symptom.")
                continue
            break

        elif raw == "list":
            print_all_symptoms()
            continue

        elif raw == "":
            continue

        elif raw in known_symptoms:
            if raw in entered:
                print(f"   ℹ️  '{raw}' already added.")
            else:
                entered.append(raw)
                print(f"   ✅  Added: {raw}")

        else:
            print(f"   ❌  '{raw}' is not in the knowledge base. Try 'list' to see options.")

    return entered


def display_results(diagnoses, user_symptoms):
    """Pretty-print the diagnosis results with treatments."""
    print("\n" + "=" * 60)
    print("   🔬  DIAGNOSIS RESULTS")
    print("=" * 60)
    print(f"   Symptoms entered: {', '.join(user_symptoms)}")
    print("-" * 60)

    if not diagnoses:
        print("\n   ⚠️  No matching disease found.")
        print("   Please consult a doctor for a professional diagnosis.\n")
        return

    for rank, (disease, score) in enumerate(diagnoses, 1):
        treatment = get_treatment(disease)
        disease_display = disease.replace("_", " ").title()

        # Bar chart to show confidence visually
        bar = "█" * score + "░" * (10 - score)

        print(f"\n   #{rank}  {disease_display}")
        print(f"        Match Score : {score} symptoms  [{bar}]")
        print(f"        💊 Treatment: {treatment}")

    print("\n" + "=" * 60)
    print("   ⚕️  DISCLAIMER: This is NOT a substitute for a real doctor.")
    print("=" * 60 + "\n")


# ── Main Program Loop ───────────────────────────────────────

def main():
    print_banner()

    while True:
        print("📌  MENU:")
        print("   1. Start Diagnosis")
        print("   2. View All Symptoms")
        print("   3. Exit")
        choice = input("\n   Choose an option (1/2/3): ").strip()

        if choice == "1":
            user_symptoms = get_user_symptoms()
            diagnoses = diagnose(user_symptoms)
            display_results(diagnoses, user_symptoms)

        elif choice == "2":
            print_all_symptoms()

        elif choice == "3":
            print("\n👋  Thank you for using the Expert System. Stay healthy!\n")
            break

        else:
            print("   ⚠️  Invalid choice. Please enter 1, 2, or 3.\n")


# ── Entry Point ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
