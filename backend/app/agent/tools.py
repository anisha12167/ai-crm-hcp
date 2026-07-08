from langchain_core.tools import tool
from typing import Optional
import datetime
import json


# ============================================================
# TOOL 1: LOG INTERACTION (Mandatory)
# ============================================================
@tool
def log_interaction(
    hcp_name: str,
    interaction_type: Optional[str] = "Meeting",
    date: Optional[str] = None,
    time: Optional[str] = None,
    attendees: Optional[str] = None,
    topics_discussed: Optional[str] = None,
    sentiment: Optional[str] = None,
    materials: Optional[str] = None,
    notes: Optional[str] = None,
) -> str:
    """Log a new HCP interaction. Use this when the user describes a meeting,
    call, email, or any interaction with a healthcare professional.
    Extract ALL available details from the user's message.

    Args:
        hcp_name: Name of the healthcare professional (e.g., "Dr. Smith")
        interaction_type: Type of interaction - one of: Meeting, Call, Email, Video Conference
        date: Date of interaction in YYYY-MM-DD format. Use today if not specified.
        time: Time of interaction in HH:MM format (24h). Use current time if not specified.
        attendees: Other people who attended, comma-separated
        topics_discussed: Key discussion points
        sentiment: Overall sentiment - one of: Positive, Negative, Neutral
        materials: Materials/brochures shared, comma-separated
        notes: Additional notes about the interaction
    """
    # Use today's date and current time if not provided
    if not date:
        date = datetime.date.today().isoformat()
    if not time:
        time = datetime.datetime.now().strftime("%H:%M")

    form_data = {
        "hcp_name": hcp_name,
        "interaction_type": interaction_type or "Meeting",
        "date": date,
        "time": time,
        "attendees": attendees or "",
        "topics_discussed": topics_discussed or "",
        "sentiment": sentiment or "",
        "materials": [m.strip() for m in materials.split(",")] if materials else [],
        "notes": notes or "",
    }

    return json.dumps({
        "status": "success",
        "action": "log_interaction",
        "form_data": form_data,
        "message": f"Logged interaction with {hcp_name}"
    })


# ============================================================
# TOOL 2: EDIT INTERACTION (Mandatory)
# ============================================================
@tool
def edit_interaction(
    hcp_name: Optional[str] = None,
    interaction_type: Optional[str] = None,
    date: Optional[str] = None,
    time: Optional[str] = None,
    attendees: Optional[str] = None,
    topics_discussed: Optional[str] = None,
    sentiment: Optional[str] = None,
    materials: Optional[str] = None,
    notes: Optional[str] = None,
) -> str:
    """Edit/update specific fields of the current interaction.
    Use this when the user wants to correct or change specific details.
    ONLY include the fields that need to change — omit fields that should stay the same.

    Args:
        hcp_name: Updated HCP name (only if changing)
        interaction_type: Updated type (only if changing)
        date: Updated date in YYYY-MM-DD (only if changing)
        time: Updated time in HH:MM (only if changing)
        attendees: Updated attendees (only if changing)
        topics_discussed: Updated topics (only if changing)
        sentiment: Updated sentiment (only if changing)
        materials: Updated materials, comma-separated (only if changing)
        notes: Updated notes (only if changing)
    """
    updates = {}
    if hcp_name is not None:
        updates["hcp_name"] = hcp_name
    if interaction_type is not None:
        updates["interaction_type"] = interaction_type
    if date is not None:
        updates["date"] = date
    if time is not None:
        updates["time"] = time
    if attendees is not None:
        updates["attendees"] = attendees
    if topics_discussed is not None:
        updates["topics_discussed"] = topics_discussed
    if sentiment is not None:
        updates["sentiment"] = sentiment
    if materials is not None:
        updates["materials"] = [m.strip() for m in materials.split(",")]
    if notes is not None:
        updates["notes"] = notes

    changed_fields = list(updates.keys())

    return json.dumps({
        "status": "success",
        "action": "edit_interaction",
        "form_data": updates,
        "message": f"Updated fields: {', '.join(changed_fields)}"
    })


# ============================================================
# TOOL 3: SUGGEST FOLLOW-UP (Custom)
# ============================================================
@tool
def suggest_followup(
    hcp_name: str,
    topics_discussed: str,
    sentiment: str,
) -> str:
    """Suggest follow-up actions after an interaction with an HCP.
    Use this when the user asks for next steps, follow-up suggestions,
    or what to do after a meeting.

    Args:
        hcp_name: Name of the HCP from the current interaction
        topics_discussed: What was discussed in the interaction
        sentiment: The sentiment of the interaction (Positive, Negative, Neutral)
    """
    # Generate contextual follow-up based on sentiment and topics
    suggestions = []

    if sentiment and sentiment.lower() == "positive":
        suggestions = [
            f"Schedule a follow-up meeting with {hcp_name} within 2 weeks to maintain momentum",
            f"Send a thank-you email summarizing key discussion points about {topics_discussed}",
            "Prepare additional clinical data or case studies for the next meeting",
            "Share relevant materials that were discussed but not provided",
        ]
    elif sentiment and sentiment.lower() == "negative":
        suggestions = [
            f"Prepare counterpoints addressing {hcp_name}'s concerns about {topics_discussed}",
            "Consult with medical affairs team for additional data support",
            "Consider inviting a Key Opinion Leader for the next interaction",
            f"Schedule an informal check-in with {hcp_name} in 1 week",
        ]
    else:
        suggestions = [
            f"Follow up with {hcp_name} via email within 3 days",
            f"Send additional resources related to {topics_discussed}",
            "Update CRM with interaction notes and set a reminder for follow-up",
            "Discuss outcomes with sales manager for strategic guidance",
        ]

    return json.dumps({
        "status": "success",
        "action": "suggest_followup",
        "suggestions": suggestions,
        "message": f"Here are recommended follow-up actions for your interaction with {hcp_name}"
    })


# ============================================================
# TOOL 4: SEARCH HCP (Custom)
# ============================================================
@tool
def search_hcp(
    query: str,
) -> str:
    """Search the HCP database by name or specialty.
    Use this when the user wants to look up an HCP, check if an HCP exists,
    or find HCPs by specialty.

    Args:
        query: Search term — an HCP name, partial name, or specialty
    """
    # This will be called with DB access in the graph wrapper
    # Returns placeholder that the graph node will fill with real DB results
    return json.dumps({
        "status": "search_requested",
        "action": "search_hcp",
        "query": query,
        "message": f"Searching for HCPs matching '{query}'"
    })


# ============================================================
# TOOL 5: SUMMARIZE INTERACTION (Custom)
# ============================================================
@tool
def summarize_interaction(
    hcp_name: str,
    interaction_type: str,
    date: str,
    topics_discussed: str,
    sentiment: str,
    materials: Optional[str] = None,
    attendees: Optional[str] = None,
) -> str:
    """Generate a professional summary of the current interaction.
    Use this when the user asks to summarize, create a report, or
    generate a recap of the interaction.

    Args:
        hcp_name: Name of the HCP
        interaction_type: Type of interaction (Meeting, Call, etc.)
        date: Date of the interaction
        topics_discussed: Key discussion points
        sentiment: Sentiment of the interaction
        materials: Materials shared (if any)
        attendees: Other attendees (if any)
    """
    summary_parts = [
        f"**Interaction Summary**",
        f"- **HCP:** {hcp_name}",
        f"- **Type:** {interaction_type}",
        f"- **Date:** {date}",
        f"- **Sentiment:** {sentiment}",
        f"- **Topics:** {topics_discussed}",
    ]

    if attendees:
        summary_parts.append(f"- **Attendees:** {attendees}")
    if materials:
        summary_parts.append(f"- **Materials Shared:** {materials}")

    summary = "\n".join(summary_parts)

    return json.dumps({
        "status": "success",
        "action": "summarize_interaction",
        "summary": summary,
        "message": "Here is the professional summary of the interaction"
    })


# Export all tools
ALL_TOOLS = [
    log_interaction,
    edit_interaction,
    suggest_followup,
    search_hcp,
    summarize_interaction,
]
