"""Run-specific delivery receipt and configured Looker Studio URL construction.

No remote calls: URL construction does not verify the report's filters or rendering.
"""
import json
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def validate_looker_config(config):
    if config is None:
        return None
    fields = {'schema_version', 'report_url', 'url_parameter_names'}
    if not isinstance(config, dict) or set(config) != fields:
        raise ValueError('Looker config requires schema_version, report_url and url_parameter_names')
    if type(config['schema_version']) is not int or config['schema_version'] != 1:
        raise ValueError('Unsupported Looker config schema_version')
    if not isinstance(config['report_url'], str):
        raise ValueError('Looker report_url must be a string')
    url = urlsplit(config['report_url'])
    if (url.scheme != 'https' or url.netloc != 'lookerstudio.google.com'
            or not re.fullmatch(r'/reporting/[A-Za-z0-9_-]+(?:/page/[A-Za-z0-9_-]+)?/?', url.path)
            or url.fragment or any(k == 'params' for k, _ in parse_qsl(url.query))):
        raise ValueError('Use a Looker Studio HTTPS reporting URL without existing params or fragment')
    names = config['url_parameter_names']
    if (not isinstance(names, dict) or not {'entity', 'run_id'} <= set(names)
            or set(names) - {'entity', 'run_id', 'mode'}):
        raise ValueError('Looker URL parameters require entity and run_id; mode is optional')
    if any(not isinstance(v, str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,200}', v) for v in names.values()):
        raise ValueError('Invalid Looker URL parameter name')
    if len(set(names.values())) != len(names):
        raise ValueError('Looker URL parameter names must be unique')
    return dict(config, url_parameter_names=dict(names))


def delivery_receipt(manifest, config=None):
    """Describe this run only. Never provide a previous run or unfiltered fallback."""
    config = validate_looker_config(config)
    outputs = manifest.get('outputs', {})
    local = {key: outputs[key] for key in (
        'report_path', 'report_data_path', 'excel_path', 'dashboard_path', 'acceptance_path'
    ) if key in outputs}
    remote = {'status': 'not_configured', 'url': None, 'render_verified': False}
    if config is not None:
        if manifest.get('status') != 'accepted' or not manifest.get('final_report_accepted'):
            remote.update(status='blocked', reason='This run did not complete with accepted financial delivery')
        elif manifest.get('execution') != 'cloud' or manifest.get('cloud_status') != 'published':
            remote.update(status='blocked', reason='This run was not successfully published to BigQuery')
        else:
            values = {'entity': manifest['entity'], 'run_id': manifest['run_id'], 'mode': manifest.get('mode')}
            if any(not isinstance(values[k], str) or not values[k] for k in config['url_parameter_names']):
                raise ValueError('Missing run context for Looker URL parameters')
            params = {name: values[key] for key, name in config['url_parameter_names'].items()}
            url = urlsplit(config['report_url'])
            query = parse_qsl(url.query, keep_blank_values=True)
            query.append(('params', json.dumps(params, ensure_ascii=False, separators=(',', ':'))))
            remote.update(status='link_ready', url=urlunsplit((url.scheme, url.netloc, url.path,
                urlencode(query), '')), reason='Configured URL generated; report wiring, refresh and rendering require verification')
    return dict(run_id=manifest['run_id'], entity=manifest['entity'], mode=manifest.get('mode'),
        periods=manifest.get('periods', []), scope=manifest.get('scope'),
        currency=manifest.get('currency'), scale=manifest.get('scale'),
        status=manifest['status'], final_report_accepted=manifest.get('final_report_accepted', False),
        cloud_status=manifest.get('cloud_status'), local=local, looker_studio=remote)
