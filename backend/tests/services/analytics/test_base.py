from services.analytics.base import BaseAnalytics


def test_queries_exist() -> None:
    all_analytic_services = BaseAnalytics.__subclasses__()
    for service in all_analytic_services:
        if service.query_template is not None:
            assert service.query_template.exists()
