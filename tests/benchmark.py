import time
import json
from pathlib import Path

from tests.benchmark_questions import QUESTIONS
from app.rag.chain import answer_question


RESULTS_DIR = Path("tests/benchmark_results_ollama")
RESULTS_DIR.mkdir(exist_ok=True)


def main():

    results = []

    total = len(QUESTIONS)

    for idx, question in enumerate(
        QUESTIONS,
        start=1
    ):

        print("=" * 100)
        print(f"[{idx}/{total}] {question}")

        start = time.time()

        try:

            response = answer_question(
                question
            )

            elapsed = round(
                time.time() - start,
                2
            )

            result = {
                "question": question,
                "answer": response["answer"],
                "sources": response["sources"],
                "time_seconds": elapsed
            }

            results.append(result)

            print(f"Completed in {elapsed}s")

        except Exception as e:

            print(f"FAILED: {e}")

            results.append(
                {
                    "question": question,
                    "error": str(e)
                }
            )

    output_file = (
        RESULTS_DIR /
        "benchmark_results.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("\nDone.")
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()