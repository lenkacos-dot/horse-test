#!/usr/bin/env python3
"""
horse_test.py — Horse Test v4.0
Hermes Agent Tuning Scoring Engine
v4.0 = v1.0 skeleton + v3.0 essence (frontmatter quality analysis / structured description evaluation / actual config detection / unit tests)

Core principle: pure stdlib, zero external dependencies, read-only evaluation with no side effects.
"""

import os
import re
import json
import math
import datetime
import shutil
import subprocess
from pathlib import Path

# ============================================================
# Constants
# ============================================================
HERMES_HOME = Path.home() / ".hermes"
HISTORY_FILE = HERMES_HOME / "horse-test-history.json"
HERMES_MD = Path.home() / ".hermes.md"
SCRIPT_DIR = Path(__file__).resolve().parent

# ============================================================
# YAML Frontmatter Parsing (pure re, no PyYAML)
# ============================================================
FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n(?:---|\.\.\.)\s*\n', re.DOTALL)

def _parse_simple_yaml(text):
    """Parse simple YAML key:value pairs and lists using re (no PyYAML needed)"""
    result = {}
    for line in text.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'^(\w[\w_-]*)\s*:\s*(.*)', line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            elif val.lower() == 'true':
                val = True
            elif val.lower() == 'false':
                val = False
            elif val == '' or val == '{}':
                val = {}
            result[key] = val
    return result if result else None

def extract_frontmatter(content):
    """Extract YAML frontmatter, return (dict_or_None, remaining_text)"""
    if not content or not content.startswith('---'):
        return None, content
    m = FRONTMATTER_RE.match(content)
    if not m:
        return None, content
    fm = _parse_simple_yaml(m.group(1))
    return fm, content[m.end():]

# ============================================================
# Six-Dimension Scoring Model
# ============================================================
DIMENSIONS = [
    {"id":"skills","icon":"🧠","name":"Skills","weight":0.25,"items":[
        {"id":"skill_count","label":"Skill Count","max":25},
        {"id":"skill_desc","label":"Skill Description Quality","max":25},
        {"id":"skill_coverage","label":"Domain Coverage","max":20},
        {"id":"skill_org","label":"Category Management","max":15},
        {"id":"skill_community","label":"Community Utilization","max":15},
    ]},
    {"id":"config","icon":"⚙️","name":"Config Tuning","weight":0.15,"items":[
        {"id":"cfg_provider","label":"Provider Configuration","max":20},
        {"id":"cfg_fallback","label":"Fallback Mechanism","max":20},
        {"id":"cfg_profile","label":"Profile Management","max":15},
        {"id":"cfg_token","label":"Token Optimization","max":15},
        {"id":"cfg_memory","label":"Memory Management","max":15},
        {"id":"cfg_proxy","label":"Network Configuration","max":15},
    ]},
    {"id":"prompt","icon":"📝","name":"Prompt Engineering","weight":0.15,"items":[
        {"id":"pr_sysprompt","label":"System Prompt","max":25},
        {"id":"pr_skilldesc","label":"Skill Description Quality","max":25},
        {"id":"pr_context","label":"Context Management","max":20},
        {"id":"pr_lang","label":"Multilingual Support","max":15},
        {"id":"pr_clarity","label":"Instruction Precision","max":15},
    ]},
    {"id":"tools","icon":"🔌","name":"Tool Ecosystem","weight":0.20,"items":[
        {"id":"tool_plugins","label":"Plugin Integration","max":20},
        {"id":"tool_gateway","label":"Gateway","max":15},
        {"id":"tool_cron","label":"Cron Tasks","max":20},
        {"id":"tool_external","label":"External Toolchain","max":25},
        {"id":"tool_api","label":"API Integration","max":20},
    ]},
    {"id":"operations","icon":"📊","name":"Operations","weight":0.10,"items":[
        {"id":"op_memory","label":"Memory Quality","max":25},
        {"id":"op_iteration","label":"Iterative Optimization","max":20},
        {"id":"op_community","label":"Community Engagement","max":20},
        {"id":"op_docs","label":"Documentation","max":20},
        {"id":"op_automation","label":"Automation Level","max":15},
    ]},
    {"id":"security","icon":"🛡️","name":"Security & Privacy","weight":0.15,"items":[
        {"id":"sec_privacy_rules","label":"Privacy Rules","max":25},
        {"id":"sec_rule_quality","label":"Rule Quality","max":25},
        {"id":"sec_cross_profile","label":"Cross-Profile Protection","max":20},
        {"id":"sec_data_isolate","label":"Data Isolation","max":15},
        {"id":"sec_awareness","label":"Security Awareness","max":15},
    ]},
]

TIERS = [
    {"min":0,"max":199,"icon":"🐣","name":"Stable Boy","en":"Stable Boy","desc":"New to Hermes, basic setup complete"},
    {"min":200,"max":349,"icon":"🐴","name":"Rider","en":"Rider","desc":"Mastered basic skills, can handle daily tasks"},
    {"min":350,"max":499,"icon":"🏇","name":"Horse Trainer","en":"Horse Trainer","desc":"Relatively complete skill system, multi-profile management"},
    {"min":500,"max":649,"icon":"🦄","name":"Master Trainer","en":"Master Trainer","desc":"Deeply customized Agent, proficient with Cron/Gateway"},
    {"min":650,"max":799,"icon":"🐉","name":"Dragon Knight","en":"Dragon Knight","desc":"Custom skills, community contributions, multi-toolchain integration"},
    {"min":800,"max":1000,"icon":"👑","name":"Horse God","en":"Horse God","desc":"Ultimate tuning, near-automated agent workflows"},
]

# ============================================================
# Utility Functions
# ============================================================
def _get_username():
    """Cross-platform username retrieval (macOS: USER, Windows: USERNAME)"""
    return os.environ.get("USER") or os.environ.get("USERNAME") or "User"

def _find_process(name_pattern):
    """Cross-platform process detection (macOS: pgrep, Windows: tasklist)"""
    try:
        if os.name == 'nt':  # Windows
            r = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {name_pattern}"],
                               capture_output=True, text=True, timeout=5)
            return name_pattern.lower() in r.stdout.lower()
        else:  # macOS / Linux
            r = subprocess.run(["pgrep", "-f", name_pattern],
                               capture_output=True, text=True, timeout=3)
            return r.returncode == 0
    except: return False

def safe_read(path, max_lines=200):
    """Safely read a file without crashing"""
    if not path: return ""
    try:
        with open(path,'r',encoding='utf-8') as f:
            lines = []
            for _ in range(max_lines):
                line = f.readline()
                if not line: break
                lines.append(line.rstrip())
            return '\n'.join(lines)
    except: return ""

def safe_read_all(path):
    """Safely read full file contents"""
    if not path: return ""
    try:
        with open(path,'r',encoding='utf-8') as f:
            return f.read()
    except: return ""

def analyze_frontmatter_quality(fm):
    """Analyze frontmatter field completeness (v4.0: adopted from v3.0)"""
    if not fm or not isinstance(fm,dict):
        return 0,{}
    score = 3
    for field,pts in [("name",3),("description",3),("version",2),("author",1),("license",1),("metadata",2)]:
        if fm.get(field): score += pts
    score += min(len(fm)*2,10)
    return min(score,25),{"has_frontmatter":True,"field_count":len(fm)}

def analyze_description_quality(content):
    """Analyze description text structural quality (v4.0: adopted from v3.0)"""
    if not content: return 0,{"length":0}
    text = content.lower()
    score = min(max(len(content)-50,0)//150+1,5)
    for kw,pts in [("usage",4),("parameter",4),("example",4),("depend",3),("install",2)]:
        if kw in text: score += pts
    headers = len(re.findall(r'^#{1,3}\s+',content,re.MULTILINE))
    lists = len(re.findall(r'^\s*[-*]\s+',content,re.MULTILINE))
    code = len(re.findall(r'```',content))//2
    score += min(headers+lists+code,7)
    return min(score,25),{"length":len(content),"headers":headers,"lists":lists,"code_blocks":code}

def analyze_config_token_optimization(text):
    """Analyze config.yaml for token optimization settings (v4.0: adopted from v3.0)"""
    has_max_tk = bool(re.search(r'max_tokens?\s*[:=]',text,re.I)) if text else False
    has_ctx = bool(re.search(r'context[_\\s]?window|max_turns?\s*[:=]',text,re.I)) if text else False
    has_cmp = bool(re.search(r'compress|精减|摘要|summar',text,re.I)) if text else False
    has_dis = bool(re.search(r'disabl|禁用|排除|exclud',text,re.I)) if text else False
    score = (5 + (4 if has_max_tk else 0) + (3 if has_ctx else 0)
             + (2 if has_cmp else 0) + (1 if has_dis else 0))
    return {"has_max_tokens":has_max_tk,"has_context_window":has_ctx,
            "has_skill_compress":has_cmp,"has_tool_disable":has_dis,"token_score":min(score,15)}

def analyze_security_rules(content):
    """Analyze .hermes.md security rule quality"""
    if not content: return {"count":0,"quality":0,"has_forbidden_paths":False,"has_sensitive_files":False,
                           "has_operation_restrict":False,"has_confirm":False}
    text = content.lower()
    count = len(re.findall(r'(?:forbidden|do not|禁止|不允许|不要|拒绝|不能)',text,re.I))
    return {"count":count,"quality":min(count*3,15),
            "has_forbidden_paths":bool(re.search(r'[/\\\\]',content)),
            "has_sensitive_files":bool(re.search(r'(?:\.env|\.git|\.ssh|\.aws|secret|token|key)',text,re.I)),
            "has_operation_restrict":bool(re.search(r'\b(?:rm|del|exec|eval|sudo)\b',text,re.I)),
            "has_confirm":bool(re.search(r'confirm|二次|ask|确认',text,re.I))}

# ============================================================
# HTS Calculation
# ============================================================
def calculate_hts(dim_scores, previous_score=None):
    """Weighted geometric mean HTS = prod(S_i^W_i) × 1000, with trend correction β"""
    hts = 1.0
    for d in DIMENSIONS:
        s = max(dim_scores.get(d["id"],50)/100.0,0.001)
        hts *= math.pow(s,d["weight"])
    base = round(hts*1000,1)
    beta = 1.0
    if previous_score is not None:
        delta = base - previous_score
        if delta > 30: beta = 1.05
        elif delta < -30: beta = 0.95
    return min(round(base*beta,1),1000.0),base,beta

def get_tier(score):
    for t in TIERS:
        if t["min"] <= score <= t["max"]: return t
    return TIERS[-1]

# ============================================================
# History
# ============================================================
def load_history():
    if HISTORY_FILE.is_file():
        try: return json.loads(safe_read_all(HISTORY_FILE))
        except: return []
    return []

def save_history(hts, dim_scores):
    h = load_history()
    h.append({"date":datetime.datetime.now().isoformat(),"hts":hts,"dimensions":dim_scores})
    h = h[-30:]
    HISTORY_FILE.parent.mkdir(parents=True,exist_ok=True)
    with open(HISTORY_FILE,'w',encoding='utf-8') as f:
        json.dump(h,f,ensure_ascii=False,indent=2)
    return h

# ============================================================
# Scanner
# ============================================================
class Scanner:
    def __init__(self):
        self.data = {}
        self._scan_all()
    def _scan_all(self):
        self._skills(); self._config(); self._memory(); self._cron()
        self._plugins(); self._tools(); self._security(); self._operations()

    def _skills(self):
        d={"dirs":[],"count":0,"descriptions":[],"coverage":set(),"fm_scores":[],"dq_scores":[]}
        sk = HERMES_HOME/"skills"
        if sk.is_dir():
            for e in sorted(os.listdir(sk)):
                fp = sk/e
                if not fp.is_dir() or e.startswith('.'): continue
                d["dirs"].append(e)
                for md in ['SKILL.md','DESCRIPTION.md','README.md']:
                    mp = fp/md
                    if mp.is_file():
                        c = safe_read(mp,80)
                        d["descriptions"].append({"dir":e,"file":md,"content":c})
                        fm,_ = extract_frontmatter(c)
                        if fm:
                            sc,_ = analyze_frontmatter_quality(fm)
                            d["fm_scores"].append(sc)
                        sc,_ = analyze_description_quality(c)
                        d["dq_scores"].append(sc)
                        txt = c.lower()
                        for kw,cat in [("code","coding"),("research","research"),("web","web"),
                                       ("productivity","productivity"),("data","data-science"),
                                       ("social","social-media"),("security","security")]:
                            if kw in txt: d["coverage"].add(cat)
                        break
            d["count"]=len(d["dirs"])
        self.data["skills"]=d

    def _config(self):
        c={"provider_count":0,"has_fallback":False,"fb_ok":False,"profiles":[],"profile_count":0,
           "proxy":False,"token_opt":{},"has_cross_profile":False,"text":""}
        for p in [HERMES_HOME/"config.yaml",HERMES_HOME/"config.yml"]:
            if p.is_file():
                c["text"]=safe_read(p,400); break
        if c["text"]:
            t=c["text"]
            c["provider_count"]=len(re.findall(r'provider\s*:',t,re.I))
            c["has_fallback"]='fallback' in t.lower()
            c["fb_ok"]=not bool(re.search(r'fallback_providers\s*:\s*\[',t)) and c["has_fallback"]
            c["has_cross_profile"]=bool(re.search(r'cross[_\\s]?profile',t,re.I))
            c["token_opt"]=analyze_config_token_optimization(t)
        pd = HERMES_HOME/"profiles"
        if pd.is_dir():
            c["profiles"]=[d for d in os.listdir(pd) if (pd/d).is_dir() and not d.startswith('.')]
            c["profile_count"]=len(c["profiles"])
        gc = safe_read(Path.home()/".gitconfig",100)
        c["proxy"]='proxy' in gc.lower() or '7897' in gc
        for ev in ["HTTP_PROXY","HTTPS_PROXY","http_proxy","https_proxy"]:
            if os.environ.get(ev): c["proxy"]=True; break
        self.data["config"]=c

    def _memory(self):
        m={"has_memory":False,"entries":[]}
        md = HERMES_HOME/"memory"
        if md.is_dir():
            m["entries"]=[f for f in os.listdir(md) if f.endswith(('.json','.yaml','.yml'))]
        if (HERMES_HOME/".usage.json").is_file(): m["has_memory"]=True
        self.data["memory"]=m

    def _cron(self):
        c={"tasks":[],"count":0,"has_watchdog":False,"scripts":[]}
        jp = HERMES_HOME/"cron"/"jobs.json"
        if jp.is_file():
            try:
                jd=json.loads(safe_read_all(jp))
                c["tasks"]=list(jd.keys()) if isinstance(jd,dict) else []
                c["count"]=len(c["tasks"])
                for n in c["tasks"]:
                    if 'dns' in n.lower() or 'watchdog' in n.lower(): c["has_watchdog"]=True
            except: pass
        # Cross-platform script detection (macOS: .sh, Windows: .bat/.ps1)
        sd = HERMES_HOME / "scripts"
        script_exts = ('.sh', '.bat', '.ps1', '.cmd')
        if sd.is_dir():
            c["scripts"]=[f for f in os.listdir(sd) if f.lower().endswith(script_exts) and not f.startswith('.')]
        self.data["cron"]=c

    def _plugins(self):
        p={"installed":[],"count":0,"has_useful":False}
        pd = HERMES_HOME/"plugins"
        if pd.is_dir():
            p["installed"]=[e for e in os.listdir(pd) if (pd/e).is_dir() and not e.startswith('.')]
            p["count"]=len(p["installed"])
            p["has_useful"]=any(u in p["installed"] for u in ['disk-cleanup','security-guidance','rtk-rewrite'])
        self.data["plugins"]=p

    def _tools(self):
        t={"installed":[],"gateway":False}
        for p in [Path.home()/".local"/"bin",Path.home()/".hermes"/"node"/"bin",
                  Path.home()/".hermes"/"node","/opt/homebrew/bin","/usr/local/bin"]:
            if str(p) not in os.environ.get("PATH",""):
                os.environ["PATH"]=f"{p}:"+os.environ.get("PATH","")
        for cmd in ["pipx","ffmpeg","gbrain","crush","node","bun","playwright","python3"]:
            if shutil.which(cmd): t["installed"].append(cmd)
        if (Path.home()/".cache"/"ms-playwright").is_dir() and "playwright" not in t["installed"]:
            t["installed"].append("playwright")
        # Gateway process detection (cross-platform)
        if _find_process("hermes.*gateway"): t["gateway"]=True; t["installed"].append("gateway")
        self.data["tools"]=t

    def _security(self):
        s={"has_hermes_md":HERMES_MD.is_file(),"content":"","rules_count":0,"quality":0,
           "cross_profile":False,"data_isolate":0,"has_confirm":False}
        if s["has_hermes_md"]:
            c=safe_read(HERMES_MD,150)
            s["content"]=c
            ar=analyze_security_rules(c)
            s["rules_count"]=ar["count"]
            s["quality"]=ar["quality"]
            s["has_confirm"]=ar["has_confirm"]
            iso=0
            if ar["has_forbidden_paths"]: iso+=5
            if ar["has_sensitive_files"]: iso+=5
            if ar["has_operation_restrict"]: iso+=3
            if ar["has_confirm"]: iso+=2
            s["data_isolate"]=iso
        s["cross_profile"]=self.data.get("config",{}).get("has_cross_profile",False)
        self.data["security"]=s

    def _operations(self):
        o={"history":HISTORY_FILE.is_file(),"notes":False,"community":False,"notes_count":0}
        sk=HERMES_HOME/"skills"
        if sk.is_dir():
            o["notes_count"]=len(list(sk.glob("*/使用笔记.md")))+len(list(sk.glob("*/notes.md")))
            o["notes"]=o["notes_count"]>0
            o["community"]=any(
                ('tap' in d.lower() or 'community' in d.lower() or 'github.com' in (safe_read(sk/d/"SKILL.md",20)).lower())
                for d in os.listdir(sk) if (sk/d).is_dir() and not d.startswith('.') and (sk/d/"SKILL.md").is_file()
            )
        self.data["operations"]=o

# ============================================================
# Scorer
# ============================================================
class Scorer:
    def __init__(self,scanner):
        self.d=scanner.data; self.scores={}; self.dim_scores={}
    def run(self):
        for dim in DIMENSIONS:
            fn=getattr(self,f"_s_{dim['id']}",None)
            self.scores[dim["id"]]=fn() if fn else {"score":0,"details":{i["id"]:0 for i in dim["items"]}}
            tot=sum(self.scores[dim["id"]]["details"].values())
            mx=sum(i["max"] for i in dim["items"])
            self.dim_scores[dim["id"]]=round(tot/mx*100,1) if mx else 0

    def _s_skills(self):
        s=self.d["skills"]; fm=s.get("fm_scores",[]); dq=s.get("dq_scores",[])
        det={}
        c=s["count"]
        det["skill_count"]=10 if c<=3 else 15 if c<=9 else 20 if c<=20 else 25
        if fm and dq: det["skill_desc"]=round(min(sum(fm)/len(fm)*0.4+sum(dq)/len(dq)*0.6,25))
        elif dq: det["skill_desc"]=round(min(sum(dq)/len(dq),25))
        else: det["skill_desc"]=5
        det["skill_coverage"]=min(len(s.get("coverage",set()))*4,20)
        has_desc=any(d.get("file")=="DESCRIPTION.md" for d in s.get("descriptions",[]))
        det["skill_org"]=(10 if has_desc else 5)+min(sum(1 for d in s.get("dirs",[]) if '/' in d)*3,10)
        det["skill_community"]=15 if any(
            any(kw in d.get("content","").lower() for kw in ['tap','community','wondelai','witt3rd','github'])
            for d in s.get("descriptions",[])
        ) else 8
        return {"score":sum(det.values()),"details":det}

    def _s_config(self):
        c=self.d["config"]; det={}
        det["cfg_provider"]=min(c.get("provider_count",0)*5,20)
        if c.get("has_fallback"): det["cfg_fallback"]=20 if c.get("fb_ok") else 12
        else: det["cfg_fallback"]=0
        det["cfg_profile"]=min(c.get("profile_count",0)*7,15)
        to=c.get("token_opt",{})
        det["cfg_token"]=to.get("token_score",10) if to else 10
        det["cfg_memory"]=10 if self.d.get("memory",{}).get("has_memory") else 7
        det["cfg_proxy"]=15 if c.get("proxy") else 5
        return {"score":sum(det.values()),"details":det}

    def _s_prompt(self):
        s=self.d["skills"]; fm=s.get("fm_scores",[]); dq=s.get("dq_scores",[]); det={}
        det["pr_sysprompt"]=round(min((sum(fm)/len(fm) if fm else 0),25)) if fm else 5
        det["pr_skilldesc"]=round(min((sum(dq)/len(dq) if dq else 0),25)) if dq else 10
        cfg=self.d.get("config",{}).get("text","")
        det["pr_context"]=18 if re.search(r'max_turns?\s*[:=]',cfg,re.I) else 10
        descs=s.get("descriptions",[])
        has_cn=any('chinese' in d.get("content","").lower() or '中文' in d.get("content","") for d in descs)
        has_en=any(len(re.findall(r'[a-zA-Z]{10,}',d.get("content","")))>0 for d in descs)
        det["pr_lang"]=15 if has_cn and has_en else 8
        has_ex=any('example' in d.get("content","").lower() or '示例' in d.get("content","") for d in descs)
        det["pr_clarity"]=15 if has_ex else 8
        return {"score":sum(det.values()),"details":det}

    def _s_tools(self):
        det={}
        pl=self.d.get("plugins",{})
        det["tool_plugins"]=20 if pl.get("has_useful") else (10 if pl.get("count",0)>0 else 0)
        # Gateway (cross-platform process detection)
        det["tool_gateway"]=15 if _find_process("hermes.*gateway") else 5
        cr=self.d.get("cron",{})
        det["tool_cron"]=min(cr.get("count",0)*7,20)
        tools=self.d.get("tools",{})
        inst=[t for t in tools.get("installed",[]) if t!="gateway"]
        det["tool_external"]=min(len(inst)*5,25)
        det["tool_api"]=min(self.d.get("config",{}).get("provider_count",0)*4,20)
        return {"score":sum(det.values()),"details":det}

    def _s_operations(self):
        det={}
        ops=self.d.get("operations",{})
        det["op_memory"]=18 if ops.get("history") else 10
        det["op_iteration"]=18 if len(load_history())>=2 else 12
        det["op_community"]=20 if ops.get("community") else 8
        det["op_docs"]=min(20+(ops.get("notes_count",0)),20) if ops.get("notes") else 8
        det["op_automation"]=min(self.d.get("cron",{}).get("count",0)*3,15)
        return {"score":sum(det.values()),"details":det}

    def _s_security(self):
        det={}
        sec=self.d.get("security",{})
        det["sec_privacy_rules"]=25 if sec.get("has_hermes_md") else 0
        det["sec_rule_quality"]=min(sec.get("quality",0)+sec.get("rules_count",0),25)
        det["sec_cross_profile"]=20 if sec.get("cross_profile") else 8
        det["sec_data_isolate"]=min(sec.get("data_isolate",0),15)
        det["sec_awareness"]=min(sec.get("rules_count",0)*3,15)
        return {"score":sum(det.values()),"details":det}

# ============================================================
# Suggestion Generation
# ============================================================
def gen_suggestions(scorer):
    SUG = {
        "skills":["Add complete YAML frontmatter to every skill (name/description/version/author)",
                   "Install high-quality community skills from Skill Tap to cover more domains",
                   "Organize skills by category in directories, add DESCRIPTION.md",
                   "Add CHANGELOG.md to skills to track iterations"],
        "config":["Configure primary + backup Providers with properly formatted fallback_providers in config.yaml",
                   "Create multiple Profiles to separate work/personal scenarios",
                   "Configure cross_profile for data isolation between different Profiles",
                   "Optimize Tokens: set max_tokens, context_window, disable infrequently used tools"],
        "prompt":["Write complete frontmatter for each SKILL.md (name/description/version/metadata)",
                  "Add Usage / Parameters / Examples sections to descriptions",
                  "Configure max_turns to optimize context window utilization",
                  "Add Few-shot examples to improve instruction precision"],
        "tools":["Install useful plugins: disk-cleanup, security-guidance, rtk-rewrite",
                 "Configure Gateway (iMessage/Telegram/Discord) to extend reach",
                 "Install external tools: playwright, ffmpeg, gbrain, crush",
                 "Create Cron scheduled tasks (watchdog, daily report, health check)"],
        "operations":["Optimize memory: periodically clean expired entries, keep it lean and high-signal",
                       "Engage with the community: share skills on Skill Tap, submit PRs",
                       "Write usage notes and best practice records",
                       "Configure automated ops scripts and monitoring tasks"],
        "security":["Add specific privacy rules to ~/.hermes.md (forbidden paths/sensitive files/operation restrictions/confirmation mechanisms)",
                    "Configure cross_profile protection in config.yaml",
                    "Add sensitive file isolation policies",
                    "Establish a two-step confirmation mechanism for dangerous operations"],
    }
    out=[]
    for dim in DIMENSIONS:
        ds=scorer.dim_scores.get(dim["id"],0)
        if ds<60:
            items=SUG.get(dim["id"],["Keep optimizing"])
            idx=0 if ds<30 else 1 if ds<50 else 2
            out.append({"priority":"high" if ds<40 else "medium","dimension":dim["name"],
                        "icon":dim["icon"],"score":ds,"suggestion":items[min(idx,len(items)-1)]})
    out.sort(key=lambda x:0 if x["priority"]=="high" else 1)
    return out

# ============================================================
# Report Output
# ============================================================
def print_report(scorer, hts, base, beta, tier, suggestions, history):
    user=_get_username(); now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"\n{'='*60}")
    print(f"  🐎 Horse Test Results — Hermes Agent Tuning Report  v4.0")
    print(f"{'='*60}")
    print(f"  User: {user}        Date: {now}")
    print(f"  HTS Score: {hts}/1000  |  Rank: {tier['icon']} {tier['name']} ({tier['en']})")
    print(f"{'='*60}\n")
    print(f"  📊 Six-Dimension Score Breakdown:")
    print(f"  {'─'*58}")
    for dim in DIMENSIONS:
        ds=scorer.dim_scores.get(dim["id"],0)
        bar="█"*int(ds/100*30)+"░"*(30-int(ds/100*30))
        print(f"  {dim['icon']} {dim['name']:<15s} {bar} {ds:5.1f}/100 (weight {dim['weight']*100:.0f}%)")
    print(f"  {'─'*58}")
    print(f"  📐 Algorithm: Weighted Geometric Mean HTS = ∏(Sᵢ^Wᵢ)")
    print(f"     Base HTS: {base}  |  Trend Correction β: {beta:.2f}  |  Final Score: {hts}")
    if history:
        p=history[-1].get("hts",0); d=hts-p
        print(f"     Previous Score: {p}  {'📈' if d>0 else '📉' if d<0 else '➖'} {d:+.1f}")
    print(f"\n  🏆 Current Rank: {tier['icon']} {tier['name']} (Rank {TIERS.index(tier)+1}/{len(TIERS)})")
    print(f"     {tier['desc']}")
    nxt=TIERS.index(tier)+1
    if nxt<len(TIERS):
        need=TIERS[nxt]["min"]-hts; print(f"     {need:.1f} points needed for next rank '{TIERS[nxt]['icon']}{TIERS[nxt]['name']}'")
    if suggestions:
        print(f"\n  💡 Suggestions:")
        for i,s in enumerate(suggestions[:5],1):
            tag="🔴" if s["priority"]=="high" else "🟡"
            print(f"  {i}. {tag} {s['icon']} {s['dimension']} ({s['score']:.0f}/100)")
            print(f"     → {s['suggestion']}")
    print(f"\n{'='*60}")

def gen_word_report(scorer, hts, base, beta, tier, suggestions, dim_scores, sdata):
    try:
        from docx import Document
        from docx.shared import Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement
    except ImportError:
        print("  ⚠️ python-docx is not installed, skipping Word report")
        return None
    doc=Document()
    def sf(run,sz=Pt(10),color=None,bold=False):
        run.font.name='Arial'; run.font.size=sz; run.bold=bold
        if color: run.font.color.rgb=color
        r=run._element; rPr=r.get_or_add_rPr(); rFonts=rPr.get_or_add_rFonts()
        rFonts.set(qn('w:eastAsia'),'Arial')
    def sch(cell,color):
        s=OxmlElement('w:shd'); s.set(qn('w:fill'),color); s.set(qn('w:val'),'clear')
        cell._element.get_or_add_tcPr().append(s)
    def hdr(tbl,texts):
        for i,t in enumerate(texts):
            tbl.rows[0].cells[i].text=t; sch(tbl.rows[0].cells[i],'1A3C6E')
            for p in tbl.rows[0].cells[i].paragraphs:
                for r in p.runs: sf(r,Pt(10),RGBColor(0xFF,0xFF,0xFF),True)
    # Cover page
    for _ in range(4): doc.add_paragraph()
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run('🐎 Horse Test Report v4.0'); sf(r,Pt(30),RGBColor(0x8B,0x45,0x13),True)
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run(f'HTS: {hts}/1000  |  {tier["icon"]} {tier["name"]} ({tier["en"]})'); sf(r,Pt(16))
    doc.add_paragraph()
    p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run(f'Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}'); sf(r,Pt(10),RGBColor(0x66,0x66,0x66))
    doc.add_page_break()
    # Score overview
    doc.add_heading('📊 Score Overview',level=1)
    tbl=doc.add_table(rows=7,cols=4); tbl.style='Light Grid Accent 1'
    hdr(tbl,['Dimension','Score','Weight','Evaluation'])
    for ri,dim in enumerate(DIMENSIONS):
        ds=dim_scores.get(dim["id"],0); tbl.rows[ri+1].cells[0].text=f'{dim["icon"]} {dim["name"]}'
        tbl.rows[ri+1].cells[1].text=f'{ds:.1f}/100'; tbl.rows[ri+1].cells[2].text=f'{dim["weight"]*100:.0f}%'
        tbl.rows[ri+1].cells[3].text='⭐ Excellent' if ds>=80 else '✅ Good' if ds>=60 else '🔧 Fair' if ds>=40 else '🔴 Needs Improvement'
    tbl.rows[6].cells[0].text='🏆 Overall (HTS)'; tbl.rows[6].cells[1].text=f'{hts}/1000'
    tbl.rows[6].cells[2].text='100%'; tbl.rows[6].cells[3].text=f'{tier["icon"]} {tier["name"]}'
    doc.add_paragraph(f'Algorithm: Weighted Geometric Mean | Base HTS: {base} | β: {beta:.2f}')
    doc.add_page_break()
    # Score details
    doc.add_heading('📋 Dimension Score Details',level=1)
    for dim in DIMENSIONS:
        did=dim["id"]; ds=dim_scores.get(did,0)
        doc.add_heading(f'{dim["icon"]} {dim["name"]} — {ds:.1f}/100 (weight {dim["weight"]*100:.0f}%)',level=2)
        dets=scorer.scores.get(did,{}).get("details",{})
        items=dim["items"]
        t=doc.add_table(rows=len(items)+1,cols=4); t.style='Light Grid Accent 1'
        hdr(t,['Item','Score','Max','Criteria'])
        for ri,item in enumerate(items):
            sc=dets.get(item["id"],0)
            t.rows[ri+1].cells[0].text=item["label"]
            t.rows[ri+1].cells[1].text=str(sc)
            t.rows[ri+1].cells[2].text=str(item["max"])
            # Criteria mapping
            criteria_map={
                "skill_count":"0-3:10, 4-9:15, 10-20:20, 20+:25",
                "skill_desc":"frontmatter completeness + description structure analysis",
                "skill_coverage":"domain coverage count × 4",
                "skill_org":"DESCRIPTION.md(10)+subdirectories(3)+CHANGELOG(3)",
                "skill_community":"contains community/tap/github keywords",
                "cfg_provider":"Provider count × 5",
                "cfg_fallback":"present & correct format(20)/present but wrong format(12)/none(0)",
                "cfg_profile":"Profile count × 7",
                "cfg_token":"actual detection of max_tokens/context/compress/disable",
                "cfg_memory":"has memory file(10)/none(7)",
                "cfg_proxy":"has proxy config(15)/none(5)",
                "pr_sysprompt":"average frontmatter score (0-25)",
                "pr_skilldesc":"average description quality score (0-25)",
                "pr_context":"has max_turns(18)/none(10)",
                "pr_lang":"bilingual(15)/monolingual(8)",
                "pr_clarity":"has examples(15)/none(8)",
                "tool_plugins":"useful plugins(20)/has plugins(10)/none(0)",
                "tool_gateway":"running(15)/not running(5)",
                "tool_cron":"Cron count × 7",
                "tool_external":"external tools count × 5",
                "tool_api":"Provider count × 4",
                "op_memory":"has history(18)/none(10)",
                "op_iteration":"≥2 runs(18)/single run(12)",
                "op_community":"yes(20)/no(8)",
                "op_docs":"has notes(20+)/none(8)",
                "op_automation":"Cron count × 3",
                "sec_privacy_rules":"has .hermes.md(25)/none(0)",
                "sec_rule_quality":"quality+rules_count(0-25)",
                "sec_cross_profile":"configured(20)/not configured(8)",
                "sec_data_isolate":".hermes.md 4-dimension analysis (0-15)",
                "sec_awareness":"rule count × 3 (0-15)",
            }
            t.rows[ri+1].cells[3].text=criteria_map.get(item["id"],item.get("criteria",""))
        doc.add_paragraph()
    # Suggestions
    doc.add_heading('💡 Suggestions',level=1)
    if suggestions:
        for i,s in enumerate(suggestions[:8],1):
            tag='🔴' if s["priority"]=="high" else '🟡'
            p=doc.add_paragraph(); r=p.add_run(f'{i}. {tag} {s["icon"]} {s["dimension"]}'); sf(r,bold=True)
            doc.add_paragraph(f'   → {s["suggestion"]}')
    else: doc.add_paragraph('✅ All dimensions are performing well!')
    path=Path.home()/"Desktop"/f'Horse_Test_Report_v4_{datetime.date.today().strftime("%Y%m%d")}.docx'
    doc.save(path); return str(path)

# ============================================================
# Main Entry
# ============================================================
def main():
    print("🔍 Horse Test v4.0 — Scanning Hermes Agent environment...")
    sc=Scanner(); sr=Scorer(sc); sr.run()
    h=load_history(); prev=h[-1].get("hts") if h else None
    hts,base,beta=calculate_hts(sr.dim_scores,prev)
    tier=get_tier(hts); sug=gen_suggestions(sr) if hts<800 else []
    print_report(sr,hts,base,beta,tier,sug,h)
    save_history(hts,sr.dim_scores)
    wp=gen_word_report(sr,hts,base,beta,tier,sug,sr.dim_scores,sc.data)
    if wp: print(f"\n  📄 Word Report: {wp}")
    print(f"\n💬 SUMMARY|HTS={hts}|TIER={tier['name']}|DIMS=",end="")
    for dim in DIMENSIONS: print(f"{dim['id']}={sr.dim_scores.get(dim['id'],0):.0f}",end=",")
    print()

if __name__=="__main__":
    main()
