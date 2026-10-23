
import json
import os
from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from pydantic import BaseModel, Field, ValidationError


# Load the API key from the local .env file.
load_dotenv()

MODEL_NAME = "gemini-3.6-flash"


class InterviewQuestion(BaseModel):
    """Structure of one interview question."""

    question: str = Field(min_length=5)
    difficulty: Literal["Easy", "Medium", "Hard"]
    answer: str = Field(min_length=5)
    explanation: str = Field(min_length=5)
    example: str = Field(min_length=5)
    follow_up_questions: list[str] = Field(min_length=1, max_length=3)


class InterviewResponse(BaseModel):
    """Structure of the complete interview response."""

    role: str = Field(min_length=2)
    questions: list[InterviewQuestion] = Field(min_length=1, max_length=10)


def validate_inputs(
    role: str,
    experience: str,
    skills: list[str],
    number_of_questions: int,
) -> None:
    """Check user inputs before calling the AI."""

    if not role or not role.strip():
        raise ValueError("Please enter a Job Role.")

    if len(role.strip()) > 100:
        raise ValueError("Job Role must be 100 characters or fewer.")

    if not experience or not experience.strip():
        raise ValueError("Please select your Experience Level.")

    if not skills or not any(skill.strip() for skill in skills):
        raise ValueError("Please enter at least one Skill.")

    if len(skills) > 20:
        raise ValueError("Please enter no more than 20 Skills.")

    if any(len(skill.strip()) > 60 for skill in skills):
        raise ValueError("Each Skill must be 60 characters or fewer.")

    if not 1 <= number_of_questions <= 10:
        raise ValueError("Choose between 1 and 10 questions.")


def generate_interview_questions(
    role: str,
    experience: str,
    skills: list[str],
    number_of_questions: int = 5,
) -> dict:
    """Generate structured interview questions using Gemini."""

    validate_inputs(role, experience, skills, number_of_questions)

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY was not found. Check your local .env file."
        )

    clean_role = role.strip()
    clean_experience = experience.strip()
    clean_skills = [skill.strip() for skill in skills if skill.strip()]

    prompt = f"""
You are an experienced technical interviewer and interview coach.

Create exactly {number_of_questions} useful interview questions.

Candidate details:
- Job role: {clean_role}
- Experience level: {clean_experience}
- Skills: {", ".join(clean_skills)}

Requirements:
1. Match the questions to the role and experience level.
2. Cover the provided skills where appropriate.
3. Include a clear, accurate sample answer for each question.
4. Explain why the answer is correct in beginner-friendly language.
5. Give a practical example for each answer.
6. Include 1 to 3 relevant follow-up questions per question.
7. Use Easy, Medium, or Hard as the difficulty.
8. Avoid duplicate questions.
9. Return only data matching the requested JSON schema.
"""

    try:
        with genai.Client(api_key=api_key) as client:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": InterviewResponse,
                },
            )

        if not response.text or not response.text.strip():
            raise RuntimeError("Gemini returned an empty response.")

        # Parse and validate the AI response.
        result = InterviewResponse.model_validate_json(response.text)

        # Ensure the AI generated the requested number of questions.
        if len(result.questions) != number_of_questions:
            raise RuntimeError(
                "The AI returned an unexpected number of questions. "
                "Please try again."
            )

        # Return ordinary Python data for the Streamlit UI.
        return result.model_dump()

    except ValidationError as exc:
        raise RuntimeError(
            "The AI response did not match the expected format. "
            "Please try again."
        ) from exc

    except errors.APIError as exc:
        status_code = getattr(exc, "code", None)

        if status_code == 429:
            message = (
                "Gemini usage limit reached. Check your available quota "
                "and try again later."
            )
        elif status_code == 503:
            message = (
                "Gemini is temporarily busy. Please try again later."
            )
        elif status_code == 401 or status_code == 403:
            message = (
                "Gemini API access failed. Check your API key and "
                "available API access."
            )
        else:
            message = (
                "Gemini API request failed. Check your connection, "
                "model availability, and quota."
            )

        raise RuntimeError(message) from exc

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Could not read the AI response. Please try again."
        ) from exc
