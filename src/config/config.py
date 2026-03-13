import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_KEY")

SCORE_COLORS = {
    "Very Weak": "#EF4444",
    "Weak": "#F97316",
    "Moderate": "#FACC15",
    "Good": "#10B981",
    "Excellent": "#2563EB"
}

EDUCATION_COLORS = {
    "High School": "#F97316",
    "Technical Degree": "#14B8A6",
    "Associate Degree": "#06B6D4",
    "Bachelor's Degree": "#3B82F6",
    "Postgraduate": "#8B5CF6",
    "Master's Degree": "#6366F1",
    "Doctorate": "#7C3AED",
    "Course / Certification": "#FACC15",
    "Not Informed": "#9CA3AF"
}

METRIC_COLORS = {
    "col1": "#2563EB",
    "col2": "#10B981",
    "col3": "#F59E0B",
    "col4": "#EF4444"
}