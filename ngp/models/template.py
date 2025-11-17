"""Mission Template model - predefined mission sets"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any
from enum import Enum


class TemplateCategory(Enum):
    """Template categories"""
    WRITING = "writing"
    FITNESS = "fitness"
    CODING = "coding"
    LEARNING = "learning"
    CREATIVITY = "creativity"
    HEALTH = "health"
    PRODUCTIVITY = "productivity"
    CUSTOM = "custom"


@dataclass
class MissionTemplate:
    """
    Represents a mission template that can be instantiated.

    Attributes:
        id: Unique identifier
        name: Template name
        description: Template description
        category: Template category
        missions: List of mission definitions
        created_at: When template was created
        times_used: How many times instantiated
    """
    id: str
    name: str
    description: str
    category: TemplateCategory
    missions: List[Dict[str, Any]]  # List of mission definitions
    created_at: datetime = field(default_factory=datetime.now)
    times_used: int = 0

    def increment_usage(self):
        """Increment usage counter"""
        self.times_used += 1


# Predefined templates
BUILTIN_TEMPLATES = {
    "writing_starter": MissionTemplate(
        id="template_writing_starter",
        name="Writing Starter Pack",
        description="Essential writing missions to get started",
        category=TemplateCategory.WRITING,
        missions=[
            {"title": "Write 250 words", "difficulty": 1, "energy": 2},
            {"title": "Write 500 words", "difficulty": 2, "energy": 2},
            {"title": "Write 1000 words", "difficulty": 3, "energy": 3},
            {"title": "Edit previous work", "difficulty": 2, "energy": 3},
            {"title": "Brainstorm ideas for 15 minutes", "difficulty": 1, "energy": 2},
            {"title": "Read and analyze good writing", "difficulty": 2, "energy": 2},
            {"title": "Outline a chapter", "difficulty": 2, "energy": 3},
            {"title": "Research topic for article", "difficulty": 2, "energy": 2},
            {"title": "Write morning pages", "difficulty": 1, "energy": 1},
            {"title": "Revise one section", "difficulty": 3, "energy": 3},
        ]
    ),
    "fitness_beginner": MissionTemplate(
        id="template_fitness_beginner",
        name="Fitness Beginner Pack",
        description="Beginner-friendly fitness missions",
        category=TemplateCategory.FITNESS,
        missions=[
            {"title": "10 minute walk", "difficulty": 1, "energy": 1},
            {"title": "20 minute walk", "difficulty": 2, "energy": 2},
            {"title": "15 push-ups", "difficulty": 2, "energy": 2},
            {"title": "30 second plank", "difficulty": 2, "energy": 2},
            {"title": "10 squats", "difficulty": 1, "energy": 2},
            {"title": "Stretch for 10 minutes", "difficulty": 1, "energy": 1},
            {"title": "Run for 5 minutes", "difficulty": 2, "energy": 3},
            {"title": "20 jumping jacks", "difficulty": 1, "energy": 2},
            {"title": "Yoga session (15 min)", "difficulty": 2, "energy": 2},
            {"title": "Bodyweight workout (20 min)", "difficulty": 3, "energy": 3},
        ]
    ),
    "coding_daily": MissionTemplate(
        id="template_coding_daily",
        name="Coding Daily Practice",
        description="Daily coding practice missions",
        category=TemplateCategory.CODING,
        missions=[
            {"title": "Code for 30 minutes", "difficulty": 2, "energy": 3},
            {"title": "Solve one coding challenge", "difficulty": 2, "energy": 3},
            {"title": "Read documentation for 20 minutes", "difficulty": 1, "energy": 2},
            {"title": "Debug a tricky issue", "difficulty": 3, "energy": 4},
            {"title": "Write tests for feature", "difficulty": 2, "energy": 3},
            {"title": "Refactor old code", "difficulty": 2, "energy": 3},
            {"title": "Learn new library/framework", "difficulty": 3, "energy": 3},
            {"title": "Code review someone's work", "difficulty": 2, "energy": 2},
            {"title": "Write technical blog post", "difficulty": 3, "energy": 3},
            {"title": "Contribute to open source", "difficulty": 3, "energy": 4},
        ]
    ),
    "learning_routine": MissionTemplate(
        id="template_learning_routine",
        name="Learning Routine",
        description="Structured learning missions",
        category=TemplateCategory.LEARNING,
        missions=[
            {"title": "Read for 20 minutes", "difficulty": 1, "energy": 2},
            {"title": "Watch educational video", "difficulty": 1, "energy": 1},
            {"title": "Take notes on lesson", "difficulty": 2, "energy": 2},
            {"title": "Practice exercises", "difficulty": 2, "energy": 3},
            {"title": "Review flashcards", "difficulty": 1, "energy": 1},
            {"title": "Teach concept to someone", "difficulty": 3, "energy": 3},
            {"title": "Complete course module", "difficulty": 2, "energy": 3},
            {"title": "Research new topic", "difficulty": 2, "energy": 2},
            {"title": "Quiz yourself", "difficulty": 1, "energy": 2},
            {"title": "Apply learning to project", "difficulty": 3, "energy": 4},
        ]
    ),
    "productivity_basics": MissionTemplate(
        id="template_productivity_basics",
        name="Productivity Basics",
        description="Core productivity habits",
        category=TemplateCategory.PRODUCTIVITY,
        missions=[
            {"title": "Plan your day", "difficulty": 1, "energy": 1},
            {"title": "Complete #1 priority task", "difficulty": 3, "energy": 3},
            {"title": "Clear inbox to zero", "difficulty": 2, "energy": 2},
            {"title": "Organize workspace", "difficulty": 1, "energy": 1},
            {"title": "Review weekly goals", "difficulty": 1, "energy": 2},
            {"title": "Time block tomorrow", "difficulty": 1, "energy": 1},
            {"title": "Eliminate one distraction", "difficulty": 2, "energy": 2},
            {"title": "Batch similar tasks", "difficulty": 2, "energy": 2},
            {"title": "Take proper breaks", "difficulty": 1, "energy": 1},
            {"title": "Weekly review session", "difficulty": 2, "energy": 3},
        ]
    ),
}
