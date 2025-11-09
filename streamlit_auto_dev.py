from agents import init_agents
from utils.io_tools import write_app_code
from utils.run_tools import run_streamlit_app

def main():
    engineer, reviewer, user, cfg = init_agents()
    sandbox_path = cfg["sandbox_path"]
    max_iter = cfg["iteration_limit"]

    goal = input("Enter your app goal: ").strip()
    print(f"\n🧩 Building app for goal: {goal}\n")

    # Initial prompt
    prompt = f"Create a Streamlit app: {goal}"
    app_filename = "auto_app.py"

    for i in range(max_iter):
        print(f"\n=== Iteration {i+1}/{max_iter} ===")
        user_message = prompt if i == 0 else f"Please improve the app based on feedback."

        # Engineer writes or refines the code
        engineer_reply = engineer.step(user_message, reviewer)
        code = engineer_reply.get("content", "")
        app_path = write_app_code(code, app_filename, sandbox_path)

        # Run the app to test
        run_output = run_streamlit_app(app_path)
        print("Run feedback:\n", run_output[:500])  # show partial output

        # Reviewer critiques
        review_message = f"Review and suggest improvements for this Streamlit app:\n{code[:1500]}"
        reviewer_reply = reviewer.step(review_message, engineer)
        feedback = reviewer_reply.get("content", "")
        print("Reviewer feedback:\n", feedback[:500])

        # Optional human break
        cont = input("Continue iteration? (y/n): ").strip().lower()
        if cont != "y":
            print("Stopping iteration.")
            break
        prompt = feedback

    print(f"\n✅ Final app saved at: {app_path}\nRun with:\n  streamlit run {app_path}")

if __name__ == "__main__":
    main()
