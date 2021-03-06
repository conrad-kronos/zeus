from datetime import timedelta
from flask import current_app

from zeus.config import db, metrics
from zeus.constants import Result
from zeus.models import Build, Job, User
from zeus.utils import timezone

from .base import Resource


class InstallIndexResource(Resource):
    auth_required = False

    def get(self):
        """
        Return various details about the installation.
        """
        one_day_ago = timezone.now() - timedelta(days=1)
        thirty_days_ago = timezone.now() - timedelta(days=30)

        return {
            "process": {
                "id": str(metrics.guid),
                "uptime": metrics.uptime,
                "connections": metrics.connections.value,
                "hits": {
                    "5m": metrics.hits.count(300),
                    "15m": metrics.hits.count(900),
                    "1h": metrics.hits.count(3600),
                },
            },
            "config": {
                "debug": current_app.debug,
                "environment": current_app.config["SENTRY_ENVIRONMENT"],
                "release": current_app.config["SENTRY_RELEASE"],
                "pubsubEndpoint": current_app.config["PUBSUB_ENDPOINT"],
            },
            "stats": {
                "builds": {
                    "created": {
                        "24h": (
                            Build.query.unrestricted_unsafe()
                            .filter(Build.date_created > one_day_ago)
                            .count()
                        ),
                        "30d": (
                            Build.query.unrestricted_unsafe()
                            .filter(Build.date_created > thirty_days_ago)
                            .count()
                        ),
                    },
                    "errored": {
                        "24h": (
                            Build.query.unrestricted_unsafe()
                            .filter(
                                Build.date_created > one_day_ago,
                                Build.result == Result.errored,
                            )
                            .count()
                        ),
                        "30d": (
                            Build.query.unrestricted_unsafe()
                            .filter(
                                Build.date_created > thirty_days_ago,
                                Build.result == Result.errored,
                            )
                            .count()
                        ),
                    },
                },
                "jobs": {
                    "created": {
                        "24h": (
                            Job.query.unrestricted_unsafe()
                            .filter(Job.date_created > one_day_ago)
                            .count()
                        ),
                        "30d": (
                            Job.query.unrestricted_unsafe()
                            .filter(Job.date_created > thirty_days_ago)
                            .count()
                        ),
                    },
                    "errored": {
                        "24h": (
                            Job.query.unrestricted_unsafe()
                            .filter(
                                Job.date_created > one_day_ago,
                                Job.result == Result.errored,
                            )
                            .count()
                        ),
                        "30d": (
                            Job.query.unrestricted_unsafe()
                            .filter(
                                Job.date_created > thirty_days_ago,
                                Job.result == Result.errored,
                            )
                            .count()
                        ),
                    },
                },
                "repos": {
                    "active": {
                        "24h": (
                            db.session.query(Build.repository_id)
                            .distinct()
                            .filter(Build.date_created > one_day_ago)
                            .distinct()
                            .count()
                        ),
                        "30d": (
                            db.session.query(Build.repository_id)
                            .distinct()
                            .filter(Build.date_created > thirty_days_ago)
                            .distinct()
                            .count()
                        ),
                    }
                },
                "users": {
                    "active": {
                        "24h": User.query.filter(
                            User.date_active > one_day_ago
                        ).count(),
                        "30d": User.query.filter(
                            User.date_active > thirty_days_ago
                        ).count(),
                    }
                },
            },
        }
