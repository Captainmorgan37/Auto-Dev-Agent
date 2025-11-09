from autogen import AssistantAgent, UserProxyAgent
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def init_agents():
    cfg = load_config()
    mode = cfg.get("mode", "general")

    if mode == "aviation":
        system_dev = (
            "You are a senior Python developer at AirSprint, specializing in Streamlit "
            "tools for flight operations. Use modular code with clear headers like 'Inputs', "
            "'Outputs', and 'Compliance Notes'. Assume access to CSVs or APIs such as Fl3xx, "
            "TAF/METAR, or CBSA data. Prioritize clarity, regulatory compliance, and usability "
            "for operations control staff."
        )
        system_rev = (
            "You are a reviewer checking an aviation operations Streamlit app. Ensure logic is "
            "sound, layout follows company style (multi-tab, clean inputs, AgGrid tables), "
            "and avoid hardcoding real API keys."
        )
    else:
        system_dev = (
            "You are an expert Streamlit developer. Write clean, efficient apps with comments, "
            "and demonstrate best practices for layout, interactivity, and data visualization."
        )
        system_rev = (
            "You are a code reviewer. Provide concise, constructive feedback on readability, "
            "efficiency, and UX."
        )

    engineer = AssistantAgent("Engineer", llm=cfg["model"], system_message=system_dev)
    reviewer = AssistantAgent("Reviewer", llm=cfg["model"], system_message=system_rev)

    user = UserProxyAgent("Morgan")
    return engineer, reviewer, user, cfg
