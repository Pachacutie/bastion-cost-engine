"""WSGI entry point for production deployment."""

from bastion_cost.web import create_app

app = create_app()
