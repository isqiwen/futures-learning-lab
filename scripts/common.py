"""Shared, standard-library-only helpers. No credentials are read or printed."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MARKER_RE = re.compile(r"<!-- futures-learning-lab:(QF-(?:GOV|M[1-8]|W\d{2})) -->")


class LabError(RuntimeError):
    pass


class CommandError(LabError):
    def __init__(self, command: list[str], returncode: int, stderr: str):
        # Never print stdin or raw HTTP headers. gh itself owns authentication.
        safe = re.sub(r"(?:gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+)", "[REDACTED]", stderr)
        self.returncode = returncode
        self.stderr = safe
        super().__init__(f"Command failed ({returncode}): {' '.join(command[:4])}\n{safe[-1600:]}")


def run(command: list[str], *, input_text: str | None = None, cwd: Path = ROOT,
        check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    # Avoid pager/editor interaction; do not change the user's persisted gh settings.
    env.update(GH_PAGER="cat", GH_PROMPT_DISABLED="1", GH_HOST="github.com")
    try:
        result = subprocess.run(command, input=input_text, capture_output=True, text=True,
                                cwd=cwd, env=env, timeout=timeout, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        raise LabError(f"无法运行 {command[0]}；请检查安装/网络后重试。") from exc
    if check and result.returncode:
        raise CommandError(command, result.returncode, result.stderr)
    return result


class GitHub:
    """Authenticated transport using a user's existing local gh session."""
    def __init__(self, write_delay: float = 1.1):
        if not shutil.which("gh"):
            raise LabError("缺少 gh。请在本机安装 GitHub CLI 并通过浏览器登录；不要发送 token。")
        self.write_delay = write_delay

    def cli(self, args: list[str], *, json_output: bool = True, write: bool = False) -> Any:
        out = run(["gh", *args]).stdout
        if write:
            time.sleep(self.write_delay)
        return json.loads(out) if json_output else out.strip()

    def api(self, endpoint: str, *, method: str = "GET", payload: dict | None = None,
            paginate: bool = False) -> Any:
        args = ["gh", "api", "--hostname", "github.com", "--method", method, endpoint]
        if paginate:
            args += ["--paginate", "--slurp"]
        if payload is not None:
            args += ["--input", "-"]
        out = run(args, input_text=json.dumps(payload, ensure_ascii=False) if payload is not None else None).stdout
        if method != "GET" and endpoint != "graphql":
            time.sleep(self.write_delay)
        return json.loads(out) if out.strip() else None

    def graphql(self, query: str, variables: dict | None = None, *, write: bool = False) -> dict:
        response = self.api("graphql", method="POST", payload={"query": query, "variables": variables or {}})
        if response.get("errors"):
            raise LabError("GraphQL 返回错误；可能已有部分写入，请修正后重跑：\n" + json.dumps(response["errors"], ensure_ascii=False))
        if write:
            time.sleep(self.write_delay)
        if not isinstance(response.get("data"), dict):
            raise LabError("GraphQL 未返回 data；停止，不能假定写入成功。")
        return response["data"]

    def all(self, endpoint: str) -> list[dict]:
        pages = self.api(endpoint, paginate=True)
        if not isinstance(pages, list) or any(not isinstance(p, list) for p in pages):
            raise LabError("分页返回形状异常；停止，不能把不完整结果当成全部。")
        return [item for page in pages for item in page]

    def assert_owner(self, owner: str) -> dict:
        user = self.api("user")
        if user.get("login", "").lower() != owner.lower():
            raise LabError(f"当前 gh 用户是 {user.get('login')}，目标 owner 是 {owner}；请先切换到正确账户。")
        return user


def load_plan(root: Path = ROOT) -> dict:
    return json.loads((root / "planning/plan.json").read_text(encoding="utf-8"))


def atomic_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def task_specs(plan: dict) -> list[dict]:
    tasks = [{"id": "QF-GOV", "title": "学习范围、证据规则与两条学习路线的时间预算", "kind": "Operations",
              "phase": "Planning", "priority": "P1", "effort": "S", "target": "W01 / 每阶段复盘",
              "depends_on": [], "resources": ["GH-REPO", "GH-PROJECT"],
              "deliverables": ["notes/time-budget.md"],
              "acceptance": ["确认每周总预算和 WIP", "学习与 Northstar 工程分开", "不把远端初始化或 AI 产物当掌握证据"],
              "oral_question": "你如何判断某周应减范围而不是降低验收标准？"}]
    for p in plan["phases"]:
        tasks.append({"id": f"QF-{p['id']}", "title": p["name"], "kind": "Epic", "phase": p["id"],
                      "priority": "P1", "effort": "XL", "target": f"W{p['start']:02d}–W{p['end']:02d}",
                      "depends_on": [], "resources": [], "deliverables": [f"reports/{p['id']}-review.md"],
                      "acceptance": [p["gate"], "子工作包证据可定位；未完成项明确标注", "本人能力验收，不以课程/CI完成代替"],
                      "children": [w["id"] for w in plan["weeks"] if w["phase"] == p["id"]],
                      "oral_question": "本阶段最重要的失败案例与能力缺口是什么？"})
    return tasks + plan["weeks"]


def issue_body(task: dict, plan: dict, known: dict[str, dict] | None = None) -> str:
    known = known or {}
    base = f"https://github.com/{plan['owner']}/{plan['repository']}"
    refs = {s["id"]: s for s in plan["sources"]}
    def task_link(key: str) -> str:
        return f"[{key}]({known[key]['html_url']})" if key in known else f"`{key}`"
    parent = f"QF-{task['phase']}" if task["kind"] != "Epic" and task["phase"] != "Planning" else None
    lines = [f"<!-- futures-learning-lab:{task['id']} -->", "", f"# {task['id']} · {task['title']}", "",
             f"Phase: {task['phase']} | Kind: {task['kind']} | Priority: {task['priority']} | Effort: {task['effort']} | Target: {task['target']}", "",
             "这是待执行学习任务，不表示实验或本人学习已经完成。", ""]
    if "week" in task:
        lines += ["预算：6–8h（含选读、实践、分析和复盘，尚需本人确认；与 LLM 学习共用总预算）。", ""]
    if parent:
        lines += [f"父阶段：{task_link(parent)}。", ""]
    lines += ["前置：" + ("、".join(task_link(x) for x in task["depends_on"]) or "按阶段安排；个人执行从 QF-W01 开始") + "。", "",
              "## 选读材料"]
    lines += [f"- [{r}: {refs[r]['title']}]({refs[r]['url']}) — {refs[r]['scope']}" for r in task["resources"]]
    if not task["resources"]:
        lines += [f"参见 [执行计划]({base}/blob/main/docs/weekly-plan.md) 中本阶段工作包。"]
    lines += ["", "## 待交付产物", *[f"- `{x}`" for x in task["deliverables"]], "", "## 验收标准",
              *[f"- [ ] {x}" for x in task["acceptance"]],
              "- [ ] 提供真实运行命令/推导、来源和局限；不伪造结果。",
              "- [ ] 本人能独立解释，并确认是否达到目标能力。", "", "## 独立问答", task["oral_question"], "",
              "## 边界", "不上传密钥、账号、受限数据；不连接真实发单通道。不以收益为必须为正的验收条件。"]
    if task.get("children"):
        lines += ["", "## 阶段工作包（文本关系，不是原生 Sub-issues）", *[f"- [ ] {task_link(x)}" for x in task["children"]]]
    lines += ["", f"规范：[研究协议]({base}/blob/main/docs/research-protocol.md) · [计划]({base}/blob/main/docs/weekly-plan.md)",
              "", "## 执行记录", "实际开始后补充证据；现有记录不会被初始化脚本覆盖。", ""]
    return "\n".join(lines)


def index_issues(rows: list[dict]) -> dict[str, dict]:
    indexed: dict[str, dict] = {}
    for row in rows:
        if "pull_request" in row:
            continue
        matches = MARKER_RE.findall(row.get("body") or "")
        if len(matches) > 1:
            raise LabError(f"Issue #{row.get('number')} 有多个计划身份标记；请人工确认。")
        if matches:
            key = matches[0]
            if key in indexed:
                raise LabError(f"计划身份 {key} 重复；停止，避免创建或关联错误任务。")
            indexed[key] = row
    return indexed


def validate_plan(plan: dict) -> list[str]:
    errors = []
    if plan.get("schema_version") != 1:
        errors.append("Unsupported schema_version")
    if plan.get("lab") != "futures-learning-lab":
        errors.append("Unexpected lab identity")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*", plan.get("owner", "")):
        errors.append("Invalid GitHub owner")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", plan.get("repository", "")):
        errors.append("Invalid repository name")
    weeks = plan.get("weeks", [])
    if [w.get("week") for w in weeks] != list(range(1, 53)):
        errors.append("Expected ordered relative weeks 1..52")
    phase_ids = [p.get("id") for p in plan.get("phases", [])]
    if phase_ids != [f"M{i}" for i in range(1, 9)]:
        errors.append("Expected eight phases M1..M8")
    refs = [r.get("id") for r in plan.get("sources", [])]
    if len(refs) != len(set(refs)):
        errors.append("Duplicate resource IDs")
    tasks = task_specs(plan)
    ids = [t["id"] for t in tasks]
    if len(ids) != 61 or len(ids) != len(set(ids)):
        errors.append("Expected 61 unique governance/epic/weekly tasks")
    visited: set[str] = set()
    for t in tasks:
        for dependency in t.get("depends_on", []):
            if dependency not in visited:
                errors.append(f"{t['id']}: missing/forward/cyclic dependency {dependency}")
        if not set(t.get("resources", [])).issubset(refs):
            errors.append(f"{t['id']}: unknown resource")
        if len(t.get("acceptance", [])) < 3 or not t.get("deliverables"):
            errors.append(f"{t['id']}: insufficient acceptance/deliverables")
        visited.add(t["id"])
    for w in weeks:
        matches = [p for p in plan["phases"] if p["start"] <= w["week"] <= p["end"]]
        if len(matches) != 1 or matches[0]["id"] != w["phase"]:
            errors.append(f"{w['id']}: invalid phase window")
        if w.get("estimated_hours") != [6, 8]:
            errors.append(f"{w['id']}: hours do not match baseline")
    if plan.get("budget", {}).get("start_date") is not None:
        errors.append("No calendar start date was authorized")
    return errors


def check_manifest(root: Path = ROOT) -> list[str]:
    """Initial seed integrity only; not required for ongoing study edits."""
    path = root / "MANIFEST.json"
    if not path.is_file():
        return ["Missing initial MANIFEST.json"]
    manifest = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    for name, expected in manifest["files"].items():
        p = root / name
        if not p.resolve().is_relative_to(root.resolve()) or p.is_symlink():
            errors.append(f"Unsafe seed path: {name}")
        elif not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
            errors.append(f"Seed content changed or missing: {name}")
    return errors
