"""Templates service - manage mission templates"""

import uuid
from typing import List, Dict
from ..models import MissionTemplate, TemplateCategory, BUILTIN_TEMPLATES
from ..services import StorageService
from ..loops import ActionLoop


class TemplatesService:
    """
    Manages mission templates and instantiation.
    """

    def __init__(self, storage: StorageService):
        self.storage = storage

    def get_all_templates(self) -> Dict[str, List[MissionTemplate]]:
        """
        Get all templates (built-in + custom).

        Returns:
            Dict with 'builtin' and 'custom' keys
        """
        custom = self.storage.get_templates()
        builtin = list(BUILTIN_TEMPLATES.values())

        return {
            'builtin': builtin,
            'custom': custom
        }

    def instantiate_template(
        self,
        template_id: str,
        skill_ids: List[str],
        action_loop: ActionLoop
    ) -> List:
        """
        Create missions from a template.

        Args:
            template_id: Template to use
            skill_ids: Skills to assign missions to
            action_loop: ActionLoop for creating missions

        Returns:
            List of created missions
        """
        # Try builtin first
        template = BUILTIN_TEMPLATES.get(template_id)

        # If not builtin, try custom
        if not template:
            template = self.storage.get_template(template_id)

        if not template:
            raise ValueError(f"Template {template_id} not found")

        # Create missions
        created_missions = []
        for mission_def in template.missions:
            mission = action_loop.create_mission(
                title=mission_def['title'],
                skill_ids=skill_ids,
                difficulty=mission_def.get('difficulty', 1),
                energy=mission_def.get('energy', 1),
                note=mission_def.get('note')
            )
            created_missions.append(mission)

        # Increment usage count
        template.increment_usage()
        if template_id not in BUILTIN_TEMPLATES:
            self.storage.save_template(template)

        return created_missions

    def create_custom_template(
        self,
        name: str,
        description: str,
        category: TemplateCategory,
        missions: List[Dict[str, any]]
    ) -> MissionTemplate:
        """
        Create a custom template.

        Args:
            name: Template name
            description: Template description
            category: Template category
            missions: List of mission definitions

        Returns:
            Created template
        """
        template = MissionTemplate(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            category=category,
            missions=missions
        )

        self.storage.save_template(template)
        return template

    def delete_template(self, template_id: str):
        """Delete a custom template"""
        # Can't delete builtin templates
        if template_id in BUILTIN_TEMPLATES:
            raise ValueError("Cannot delete builtin template")

        template = self.storage.get_template(template_id)
        if template:
            # In SQLite, we'll just not fetch it anymore
            # Or we could add an is_deleted flag
            pass
