"""Refresh profile cards from GitHub's API; no third-party statistics service."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import json, math, os, subprocess, urllib.request
from html import escape

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
LOGIN='Hashamjavedofficial'

def graphql(query, variables):
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if token:
        payload=json.dumps({'query':query,'variables':variables}).encode()
        req=urllib.request.Request('https://api.github.com/graphql',data=payload,headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','User-Agent':'hasham-profile-cards'})
        with urllib.request.urlopen(req,timeout=30) as response:
            result=json.load(response)
    else:
        args=['gh','api','graphql','-f','query='+query]
        args.extend(item for key,value in variables.items() if value is not None for item in ('-f',key+'='+str(value)))
        result=json.loads(subprocess.check_output(args,text=True,encoding='utf-8'))
    if result.get('errors'):
        raise RuntimeError('GitHub GraphQL returned an error; previous cards are preserved.')
    return result['data']

def svg(title,w,h,body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title><style>text{{font-family:Segoe UI,Arial,sans-serif}}.mono{{font-family:ui-monospace,Consolas,monospace}}</style><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="20" fill="#10182b" stroke="#29344f"/>{body}</svg>'''

q='''query($login:String!){user(login:$login){followers{totalCount}contributionsCollection{startedAt endedAt contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}'''
user=graphql(q,{'login':LOGIN})['user']
collection=user['contributionsCollection']
calendar=collection['contributionCalendar']
repos=[]
cursor=None
while True:
    q='''query($login:String!,$cursor:String){user(login:$login){repositories(first:100,after:$cursor,privacy:PUBLIC,isFork:false,ownerAffiliations:OWNER){nodes{stargazerCount primaryLanguage{name color}}pageInfo{hasNextPage endCursor}}}}'''
    page=graphql(q,{'login':LOGIN,'cursor':cursor})['user']['repositories']
    repos.extend(page['nodes'])
    if not page['pageInfo']['hasNextPage']:
        break
    cursor=page['pageInfo']['endCursor']
updated=datetime.now(timezone.utc).strftime('%Y-%m-%d')
source={'username':LOGIN,'updated_on_utc':updated,'window_start':collection['startedAt'][:10],'window_end':collection['endedAt'][:10],
        'total_contributions':calendar['totalContributions'],'public_nonfork_repositories':len(repos),
        'followers':user['followers']['totalCount'],'stars_on_public_nonfork_repositories':sum(r['stargazerCount'] for r in repos),
        'weeks':calendar['weeks']}
counts=Counter(r['primaryLanguage']['name'] for r in repos if r['primaryLanguage'])
colors={r['primaryLanguage']['name']:r['primaryLanguage']['color'] or '#b5a4ff' for r in repos if r['primaryLanguage']}
source['primary_languages']=[{'name':name,'repositories':count,'color':colors[name]} for name,count in counts.most_common()]
assert len(calendar['weeks'])<=54 and calendar['totalContributions']>=0
palette={'NONE':'#202b40','FIRST_QUARTILE':'#28594f','SECOND_QUARTILE':'#388974','THIRD_QUARTILE':'#5bb99d','FOURTH_QUARTILE':'#8ff0d2'}

def contribution_cells(x,y,width,cell_size,gap):
    weeks=calendar['weeks']
    pitch=width/len(weeks)
    out=[]
    for col,week in enumerate(weeks):
        for day in week['contributionDays']:
            weekday=(datetime.fromisoformat(day['date']).weekday()+1)%7
            fill=palette[day['contributionLevel']]
            out.append(f'<rect x="{x+col*pitch:.2f}" y="{y+weekday*(cell_size+gap)}" width="{min(cell_size,pitch-2):.2f}" height="{cell_size}" rx="2" fill="{fill}"><title>{day["date"]}: {day["contributionCount"]} contributions</title></rect>')
    return ''.join(out)

total=source['total_contributions']
body=f'''<text x="32" y="44" fill="#7ce7ca" font-size="26" font-weight="600">A year of building.</text><text x="32" y="143" fill="#eef3ff" font-size="68" font-weight="700">{total:,}</text><text x="35" y="177" fill="#bbc8e3" font-size="20">contributions</text><text class="mono" x="32" y="234" fill="#9dacc9" font-size="12">GITHUB / LAST 12 MONTHS</text>'''
body+=contribution_cells(265,77,800,12,6)
body+=f'<text x="265" y="234" fill="#9dacc9" font-size="14">{source["window_start"]} → {source["window_end"]}</text><text x="1085" y="281" text-anchor="end" fill="#9dacc9" font-size="12">Updated {updated} UTC · GitHub API</text>'
activity=svg(f'{total} contributions in the last year, from GitHub. Updated {updated}.',1120,310,body)
body=f'''<text x="30" y="47" fill="#7ce7ca" font-size="30" font-weight="600">A year of building.</text><text x="30" y="115" fill="#eef3ff" font-size="54" font-weight="700">{total:,}</text><text x="155" y="112" fill="#bbc8e3" font-size="23">contributions</text>'''
body+=contribution_cells(30,151,560,8,5)
body+=f'<text x="30" y="281" fill="#9dacc9" font-size="17">Updated {updated} UTC · GitHub API</text>'
mobile=svg(f'{total} contributions in the last year, from GitHub. Updated {updated}.',620,310,body)
body='<text x="28" y="43" fill="#7ce7ca" font-size="27" font-weight="600">Around GitHub</text>'
for x,value,label in [(100,len(repos),'Public repos'),(280,source['followers'],'Followers'),(460,source['stars_on_public_nonfork_repositories'],'Stars earned')]:
    body+=f'<text x="{x}" y="137" text-anchor="middle" fill="#edefff" font-size="58" font-weight="700">{value}</text><text x="{x}" y="175" text-anchor="middle" fill="#b9aae9" font-size="20">{label}</text>'
body+=f'<text x="28" y="235" fill="#9dacc9" font-size="13">Public repositories exclude forks · Updated {updated}</text>'
stats=svg(f'{len(repos)} public non-fork repositories, {source["followers"]} followers, {source["stars_on_public_nonfork_repositories"]} stars earned.',560,260,body)
body='<text x="28" y="43" fill="#7ce7ca" font-size="27" font-weight="600">My public code</text>'
ordered=counts.most_common()
items=ordered[:5]
if len(ordered)>5:
    items.append(('Other',sum(n for _,n in ordered[5:])))
start=-math.pi/2
sum_count=sum(counts.values()) or 1
for i,(name,n) in enumerate(items):
    frac=n/sum_count
    color=colors.get(name,'#90a2c3')
    end=start+frac*2*math.pi
    if frac==1:
        body+=f'<circle cx="139" cy="145" r="66" fill="none" stroke="{color}" stroke-width="20"/>'
    else:
        x1,y1=139+66*math.cos(start),145+66*math.sin(start)
        x2,y2=139+66*math.cos(end),145+66*math.sin(end)
        body+=f'<path d="M{x1:.3f},{y1:.3f} A66,66 0 {int(frac>0.5)},1 {x2:.3f},{y2:.3f}" fill="none" stroke="{color}" stroke-width="20"/>'
    body+=f'<circle cx="256" cy="{79+i*25}" r="5" fill="{color}"/><text x="271" y="{85+i*25}" fill="#c7d2ed" font-size="18">{escape(name)} <tspan fill="#9dacc9">({n})</tspan></text>'
    start=end
body+='<text x="28" y="235" fill="#9dacc9" font-size="13">Primary language per public repo · Not a proficiency score</text>'
languages=svg('Primary languages across public, non-fork repositories; not professional proficiency.',560,260,body)

# Write only after all API requests and rendering succeeded, preserving prior cards on failure.
files={'github-activity.svg':activity,'github-activity-mobile.svg':mobile,'github-stats.svg':stats,'github-languages.svg':languages,'github-data.json':json.dumps(source,indent=2)+'\n'}
for name,content in files.items():
    (ASSETS/name).write_text(content.rstrip()+'\n',encoding='utf-8')
print(f'Refreshed {len(files)} assets from GitHub: {total} contributions, {len(repos)} public non-fork repos.')
