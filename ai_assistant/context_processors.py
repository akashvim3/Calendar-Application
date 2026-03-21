"""
Context processors for global template variables.
"""

def global_context(request):
    """Add global context variables to all templates."""
    return {
        'app_name': 'AI Assistant',
        'app_version': '1.0.0',
        'current_year': 2026,
    }
