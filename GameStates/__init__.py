import os

__all__ = [file[:-3] for file in os.listdir('GameStates') if file.endswith('.py') and file != '__init__.py']
