import sys
from tools.resume_parser import parse_resume
from graph.agent_workflow import build_graph


def print_section(title: str, content: str):
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)
    print(content)


def main():
    # --- Resume ---
    if len(sys.argv) > 1:
        resume_path = sys.argv[1]
    else:
        resume_path = input("Enter path to your resume (PDF): ").strip()

    print("\n📄 Parsing resume...")
    try:
        resume_text = parse_resume(resume_path)
    except Exception as e:
        print(f"❌ Could not parse resume: {e}")
        sys.exit(1)

    # --- Job input ---
    print("\nEnter one of the following:")
    print("  • A job posting URL")
    print("  • A company website URL")
    print("  • A company name")
    print("  • Paste a job description")
    user_input = input("\nYour input: ").strip()

    if not user_input:
        print("❌ No input provided.")
        sys.exit(1)

    # --- Build & run graph ---
    state = {
        "resume_text": resume_text,
        "user_input": user_input,
        "input_type": "",
        "job_description": "",
        "scraped_job_title": "",
        "personal_info": {},
        "resume_skills": [],
        "job_skills": [],
        "match_results": {},
        "cover_letter": "",
        "improved_cover_letter": "",
    }

    print("\n🤖 Running agent pipeline...")
    graph = build_graph()
    result = graph.invoke(state)

    # --- Output ---
    match = result.get("match_results", {})
    print_section("SKILL MATCH RESULTS", (
        f"  Match Score  : {match.get('match_score', 0)}%\n"
        f"  Matched      : {', '.join(match.get('matched_skills', [])) or 'None'}\n"
        f"  Missing      : {', '.join(match.get('missing_skills', [])) or 'None'}"
    ))

    print_section("FINAL COVER LETTER", result.get("improved_cover_letter", ""))

    # Optionally save to file
    save = input("\n💾 Save cover letter to file? (y/n): ").strip().lower()
    if save == "y":
        out_path = "cover_letter.txt"
        with open(out_path, "w") as f:
            f.write(result.get("improved_cover_letter", ""))
        print(f"✅ Saved to {out_path}")


if __name__ == "__main__":
    main()