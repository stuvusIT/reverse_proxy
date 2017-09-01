#!/usr/bin/env python3
# This script generates reverse proxy facts out of the hostvars
import json
import optparse


def main():
  p = optparse.OptionParser(
      description='Outputs the relevant ansible facts needed for the reverse proxy.',
      usage='%prog [reverse_proxy hostname] [path to file containing hostvars in json]')
  options, arguments = p.parse_args()
  if len(arguments) == 2:
    reverse_proxy_host = arguments[0]
    original_facts = json.loads(open(arguments[1]).read())
    facts = generateFacts(original_facts, reverse_proxy_host)
    print(json.dumps(facts))
  else:
    p.print_help()


def generateFacts(original_facts, reverse_proxy_host):
  # Facts are the hostvars of the reverse proxy
  facts = original_facts[reverse_proxy_host] if reverse_proxy_host in original_facts else {}

  # List of hostnames that have missing vars
  failed_names = {'description': [], 'ip': []}

  # Create dicts and prefix if not already set
  if 'proxy_domains' not in facts:
    facts['proxy_domains'] = []

  # Traverse every host defined in hostvars
  for host in original_facts.keys():

    config = original_facts[host]

    # Skip if this host has no served domains
    if 'served_domains' not in config:
      continue

    # Skip and report if no description is set
    if 'description' not in config:
      failed_names['description'].append(host)
      continue

    # Skip and report error if no connection IP is set
    if 'ansible_host' not in config:
      failed_names['ip'].append(host)
      continue

    # Skip this host if it is already configured
    if any(d['target_host'] == host for d in facts['proxy_domains']):
      continue

    served_domains = {
        'target_host': host,
        'target_description': config['description'],
        'target_ip': config['ansible_host'],
        'served_domains': config['served_domains']
    }

    facts['proxy_domains'].append(served_domains)

  # Return the result, consisting of the failed hosts and the extended hostvars
  result = {'failed_hosts': failed_names, 'new_hostvars': facts}
  return result


if __name__ == "__main__":
  main()
