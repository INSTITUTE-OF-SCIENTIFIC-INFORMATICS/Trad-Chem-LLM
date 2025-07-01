#!/usr/bin/env python3
"""
Contributors Handler for Trad-Chem LLM
Manages contributor information and displays them in the UI

@author Anu Gamage
LinkedIn: https://www.linkedin.com/in/anu-gamage-62192b201/
"""

import json
import os
from typing import Dict, List, Any

class ContributorsHandler:
    """Handler for managing and displaying project contributors"""
    
    def __init__(self):
        """Initialize contributors handler"""
        self.contributors_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'contributors.json'
        )
        self.contributors_data = self.load_contributors()
    
    def load_contributors(self) -> Dict[str, Any]:
        """Load contributors data from JSON file"""
        try:
            if os.path.exists(self.contributors_file):
                with open(self.contributors_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._get_default_contributors()
        except Exception as e:
            print(f"Error loading contributors: {e}")
            return self._get_default_contributors()
    
    def _get_default_contributors(self) -> Dict[str, Any]:
        """Return default contributors data if file not found"""
        return {
            "project_info": {
                "name": "Trad-Chem LLM",
                "description": "Traditional Chemistry Large Language Model Assistant",
                "version": "1.0.0"
            },
            "lead_developer": {
                "name": "Anu Gamage",
                "role": "Lead Developer",
                "linkedin": "https://www.linkedin.com/in/anu-gamage-62192b201/"
            },
            "core_contributors": [],
            "acknowledgments": []
        }
    
    def get_project_info(self) -> Dict[str, Any]:
        """Get project information"""
        return self.contributors_data.get('project_info', {})
    
    def get_lead_developer(self) -> Dict[str, Any]:
        """Get lead developer information"""
        return self.contributors_data.get('lead_developer', {})
    
    def get_core_contributors(self) -> List[Dict[str, Any]]:
        """Get core contributors list"""
        return self.contributors_data.get('core_contributors', [])
    
    def get_acknowledgments(self) -> List[Dict[str, Any]]:
        """Get acknowledgments list"""
        return self.contributors_data.get('acknowledgments', [])
    
    def get_special_thanks(self) -> List[Dict[str, Any]]:
        """Get special thanks list"""
        return self.contributors_data.get('special_thanks', [])
    
    def get_contribution_guide(self) -> Dict[str, Any]:
        """Get how to contribute information"""
        return self.contributors_data.get('how_to_contribute', {})
    
    def get_all_contributors(self) -> Dict[str, Any]:
        """Get all contributors data"""
        return self.contributors_data
    
    def add_contributor(self, contributor_data: Dict[str, Any], category: str = 'core_contributors'):
        """Add a new contributor to the specified category"""
        if category in self.contributors_data:
            if isinstance(self.contributors_data[category], list):
                self.contributors_data[category].append(contributor_data)
            else:
                self.contributors_data[category] = contributor_data
        else:
            self.contributors_data[category] = [contributor_data]
    
    def save_contributors(self) -> bool:
        """Save contributors data back to JSON file"""
        try:
            with open(self.contributors_file, 'w', encoding='utf-8') as f:
                json.dump(self.contributors_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving contributors: {e}")
            return False
    
    def get_contributors_count(self) -> Dict[str, int]:
        """Get count of contributors by category"""
        return {
            'lead_developer': 1 if self.contributors_data.get('lead_developer') else 0,
            'core_contributors': len(self.contributors_data.get('core_contributors', [])),
            'acknowledgments': len(self.contributors_data.get('acknowledgments', [])),
            'special_thanks': len(self.contributors_data.get('special_thanks', []))
        }
    
    def get_highlighted_team_members(self) -> List[Dict[str, Any]]:
        """Get highlighted team members from core contributors"""
        highlighted_members = []
        core_contributors = self.get_core_contributors()
        
        for contributor in core_contributors:
            team_members = contributor.get('team_members', [])
            for member in team_members:
                if member.get('highlighted', False):
                    highlighted_members.append(member)
        
        return highlighted_members
    
    def get_all_team_members(self) -> List[Dict[str, Any]]:
        """Get all team members from core contributors"""
        all_members = []
        core_contributors = self.get_core_contributors()
        
        for contributor in core_contributors:
            team_members = contributor.get('team_members', [])
            all_members.extend(team_members)
        
        return all_members

# Initialize the handler instance
contributors_handler = ContributorsHandler() 