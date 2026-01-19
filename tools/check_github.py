import os
import sys
import json
import urllib.request
import subprocess
import re

# Load token from environment or .env
token = os.environ.get('GITHUB_TOKEN')
if not token:
    # try to read .env
    try:
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GITHUB_TOKEN='):
                    token = line.split('=', 1)[1].strip()
                    break
    except Exception:
        pass

if not token:
    print('No GITHUB_TOKEN found in environment or .env')
    sys.exit(2)

# determine GitHub login from git remote
gh_login = None
try:
    r = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip():
        remote = r.stdout.strip()
        m = re.search(r"[:/](?P<owner>[^/]+)/[^/]+(?:\.git)?$", remote)
        if m:
            gh_login = m.group('owner')
except Exception:
    pass

if not gh_login:
    gh_login = 'Gr00ss'

print('Using GitHub login:', gh_login)

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def run_graphql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode('utf-8')
    req = urllib.request.Request('https://api.github.com/graphql', data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print('HTTPError', e.code, e.reason)
        try:
            print(e.read().decode())
        except Exception:
            pass
        return None
    except Exception as e:
        print('Request error:', e)
        return None

# Try to get the authenticated user's login (viewer) and prefer it
viewer_res = run_graphql('query { viewer { login } }')
if viewer_res:
    try:
        vlogin = viewer_res.get('data', {}).get('viewer', {}).get('login')
        if vlogin:
            gh_login = vlogin
            print('Detected viewer login from token, using:', gh_login)
    except Exception:
        pass

# Allow overriding target username via first CLI arg (e.g., PRIVACYCHILD)
target_login = gh_login
if len(sys.argv) > 1:
    target_login = sys.argv[1]
    print('Overriding target login with CLI arg:', target_login)

# Query contributionsCollection
q1 = '''query($login: String!, $from: DateTime!) { user(login: $login) { contributionsCollection(from: $from) { totalCommitContributions totalIssueContributions totalPullRequestContributions totalPullRequestReviewContributions totalRepositoryContributions contributionCalendar { totalContributions } } } }'''
res1 = run_graphql(q1, {"login": target_login, "from": "1970-01-01T00:00:00Z"})
if res1 and 'errors' in res1:
    print('GraphQL errors for contributions query:', res1.get('errors'))

print('\nContributions query result:')
if not res1:
    print('No response')
else:
    try:
        cc = res1.get('data', {}).get('user', {}).get('contributionsCollection', {})
        print('totalCommitContributions:', cc.get('totalCommitContributions'))
        print('totalIssueContributions:', cc.get('totalIssueContributions'))
        print('totalPullRequestContributions:', cc.get('totalPullRequestContributions'))
        print('totalPullRequestReviewContributions:', cc.get('totalPullRequestReviewContributions'))
        print('totalRepositoryContributions:', cc.get('totalRepositoryContributions'))
        cal = cc.get('contributionCalendar') or {}
        print('contributionCalendar.totalContributions:', cal.get('totalContributions'))
    except Exception as e:
        print('Error reading contributions:', e)

# Query repositories for commit counts and primary languages
q2 = '''query($login: String!) { user(login: $login) { repositories(first: 100, ownerAffiliations: OWNER, isFork: false) { nodes { name primaryLanguage { name } defaultBranchRef { target { ... on Commit { history { totalCount } } } } } } } }'''
res2 = run_graphql(q2, {"login": target_login})
if res2 and 'errors' in res2:
    print('GraphQL errors for repos query:', res2.get('errors'))

print('\nRepositories summary:')
if not res2:
    print('No response')
else:
    try:
        nodes = res2.get('data', {}).get('user', {}).get('repositories', {}).get('nodes', [])
        total_commits_sum = 0
        lang_counts = {}
        for n in nodes:
            name = n.get('name')
            lang = n.get('primaryLanguage', {}).get('name') if n.get('primaryLanguage') else None
            try:
                h = n.get('defaultBranchRef', {}).get('target', {}).get('history', {}).get('totalCount')
                if isinstance(h, int):
                    total_commits_sum += h
            except Exception:
                pass
            if lang:
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
        print('repos counted:', len(nodes))
        print('sum of default-branch commit counts (first 100 repos):', total_commits_sum)
        print('top repo languages (by repo count):')
        for k,v in sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f'  {k}: {v}')
    except Exception as e:
        print('Error reading repos:', e)

print('\nDone')

# Additionally: fetch commitContributionsByRepository to sum user's commits across all repos
q3 = '''query { viewer { contributionsCollection(from: "1970-01-01T00:00:00Z") { commitContributionsByRepository(maxRepositories: 100) { contributions { totalCount } repository { name } } } } }'''
res3 = run_graphql(q3)
print('\ncommitContributionsByRepository (viewer):')
if not res3:
    print('No response')
else:
    try:
        items = res3.get('data', {}).get('viewer', {}).get('contributionsCollection', {}).get('commitContributionsByRepository', [])
        total = 0
        for it in items:
            # contributions may be a list-like node
            contribs = it.get('contributions') or {}
            # contributions might be a connection with totalCount
            if isinstance(contribs, dict):
                tc = contribs.get('totalCount')
                if isinstance(tc, int):
                    total += tc
                else:
                    # try get as list of nodes
                    try:
                        nodes = contribs.get('nodes', [])
                        for node in nodes:
                            if isinstance(node.get('totalCount'), int):
                                total += node.get('totalCount')
                    except Exception:
                        pass
            elif isinstance(contribs, list):
                for c in contribs:
                    if isinstance(c.get('totalCount'), int):
                        total += c.get('totalCount')
        print('sum of commitContributionsByRepository.totalCount (first 100 repos):', total)
    except Exception as e:
        print('Error reading commitContributionsByRepository:', e)
