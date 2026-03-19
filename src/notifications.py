import requests
import yaml

with open('config/config.yaml') as f:
    config = yaml.safe_load(f)

def notify(message, channel='slack'):
    """Send notification to configured webhook."""
    if channel == 'slack':
        webhook = config['notifications'].get('slack_webhook')
        if webhook:
            requests.post(webhook, json={'text': message})
    elif channel == 'discord':
        webhook = config['notifications'].get('discord_webhook')
        if webhook:
            requests.post(webhook, json={'content': message})
