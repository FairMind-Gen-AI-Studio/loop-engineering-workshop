#!/usr/bin/env bash
# Prove every exercise works before a delivery. Facilitator only; runs offline in
# scratch clones, never in this checkout.
#
#   bash tools/verify.sh
#   FM_SCRIPTS=/path/to/plugins/fairmind-coding/scripts bash tools/verify.sh
#
# FM_SCRIPTS defaults to the installed fairmind-coding plugin. Point it at the
# public plugin to verify what participants install.
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOL="$ROOT/tools/solutions"
fail() { echo "VERIFY FAIL: $1" >&2; exit 1; }
pass() { echo "  ✓ $1"; }

if [ -z "${FM_SCRIPTS:-}" ]; then
  FM_SCRIPTS="$(python3 -c "import json,os;print(json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json')))['plugins']['fairmind-coding@fairmind-plugins'][0]['installPath'])")/scripts"
fi
[ -f "$FM_SCRIPTS/admit_check.py" ] || fail "no admit_check.py under FM_SCRIPTS=$FM_SCRIPTS"

work="$(mktemp -d "${TMPDIR:-/tmp}/workshop-verify-XXXXXX")" || fail "no temp dir"
trap 'rm -rf "$work"' EXIT

clone() {  # clone <branch> <dir>
  git clone -q --branch "$1" "$ROOT" "$2" || fail "cannot clone $1"
  git -C "$2" config user.email verify@example.invalid
  git -C "$2" config user.name verify
}
tests_pass() { (cd "$1" && PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider >/dev/null 2>&1); }

echo "main"
clone main "$work/main"
tests_pass "$work/main" || fail "tests are red on main"
pass "tests green"
(cd "$work/main" && python3 -m shop | grep -q "24.5 EUR") || fail "receipt no longer shows the exercise 1 bug"
pass "receipt shows 24.5 EUR (the exercise 1 task)"
cp -R "$SOL/ex1/." "$work/main/"
tests_pass "$work/main" || fail "exercise 1 solution is red"
pass "exercise 1 solution green"

echo "ex2-start"
clone ex2-start "$work/ex2"
tests_pass "$work/ex2" && fail "tests are green on ex2-start; the seeded bug is gone"
pass "tests red on the seeded VAT bug"
cp -R "$SOL/ex2/." "$work/ex2/"
tests_pass "$work/ex2" || fail "exercise 2 solution is red"
pass "exercise 2 solution green"
(cd "$work/ex2" && python3 scripts/fake_deploy.py --interval 0 --minutes 10 --out d.log >/dev/null \
  && grep -q "status=degraded" d.log) || fail "fake deploy never regresses"
pass "fake deploy log regresses"

echo "ex3-goal-start"
clone ex3-goal-start "$work/goal"
[ -f "$work/goal/TICKET.md" ] || fail "no TICKET.md"
[ -e "$work/goal/.fairmind" ] && fail "the /goal starting point carries .fairmind/; /goal would see the checks"
pass "ticket present, no contract in sight"

echo "ex3-loop-start"
repo="$work/loop"
clone ex3-loop-start "$repo"
state="$repo/.fairmind/loop-state.json"
[ -f "$repo/.fairmind/design/DISC-1.md" ] || fail "no design brief"
python3 "$FM_SCRIPTS/admit_check.py" --state "$state" --cwd "$repo" >"$work/admit.log" 2>&1 \
  || fail "admission errored: $(tail -5 "$work/admit.log")"
python3 - "$state" <<'PY' || fail "admission did not quarantine exactly the bad check"
import json, sys
s = json.load(open(sys.argv[1]))
quarantined = sorted(q["id"] for q in s["quarantine"])
admitted = sorted(c["id"] for c in s["checks"] if c["admission"]["status"] == "passed" and c["id"] not in quarantined)
assert quarantined == ["module-exists"], quarantined
assert admitted == ["ac1-percent-off", "ac2-case-insensitive", "ac3-unknown-code", "ac4-free-keeps-shipping"], admitted
PY
pass "admission: 4 admitted, module-exists quarantined"
python3 "$FM_SCRIPTS/run_gate_checks.py" --state "$state" --cwd "$repo" --validate-contract >"$work/validate.log" 2>&1 \
  || fail "contract does not validate: $(tail -5 "$work/validate.log")"
pass "--validate-contract: armable"
python3 "$FM_SCRIPTS/run_gate_checks.py" --state "$state" --cwd "$repo" --arm >"$work/arm.log" 2>&1 \
  || fail "--arm refused: $(tail -5 "$work/arm.log")"
pass "--arm: running"
python3 "$FM_SCRIPTS/run_gate_checks.py" --state "$state" --cwd "$repo" >"$work/red.log" 2>&1
[ $? -eq 10 ] || fail "the first evaluation did not block red (exit 10): $(tail -5 "$work/red.log")"
pass "first evaluation blocks red"
cp -R "$SOL/ex3/." "$repo/"
python3 - "$state" "$repo" <<'PY' || fail "a check is still red on the exercise 3 solution"
import json, subprocess, sys
s = json.load(open(sys.argv[1]))
for c in s["checks"]:
    if c["id"] == "module-exists":
        continue
    r = subprocess.run(c["exec"]["command"], shell=True, cwd=sys.argv[2], capture_output=True, text=True)
    assert r.returncode == 0, (c["id"], r.stdout[-400:], r.stderr[-400:])
PY
pass "exercise 3 solution: every admitted check green"
# Green once is not done: the gate keeps the turn open (exit 10) until three greens
# in a row and a completeness review. The exercise ends here, at confirmation 1/3.
python3 "$FM_SCRIPTS/run_gate_checks.py" --state "$state" --cwd "$repo" >"$work/green.log" 2>&1; code=$?
[ "$code" -eq 10 ] && grep -q "confirmation 1/3" "$work/green.log" \
  || fail "the gate is not green 1/3 on the solution (exit $code): $(tail -5 "$work/green.log")"
pass "gate green on the solution: confirmation 1/3, where the exercise ends"
tests_pass "$repo" || fail "the unit tests break on the exercise 3 solution"
pass "unit tests still green"

echo "ex4-start"
clone ex4-start "$work/ex4"
tests_pass "$work/ex4" || fail "tests are red on ex4-start; the review exercise needs a green branch"
pass "tests green (the flaws are untested on purpose)"
cp "$SOL/ex4/tests/test_shipping.py" "$work/ex4/tests/"
tests_pass "$work/ex4" && fail "the boundary tests pass on ex4-start; the flaws are gone"
pass "the solution's tests catch both flaws"
cp -R "$SOL/ex4/." "$work/ex4/"
tests_pass "$work/ex4" || fail "exercise 4 solution is red"
pass "exercise 4 solution green"

echo "workshop reset, in a copy made from the template"
origin="$work/copy-origin.git"; copy="$work/copy"
git init -q --bare -b main "$origin"
mkdir "$copy" && git -C "$ROOT" archive main | tar -x -C "$copy"
git -C "$copy" init -q -b main && git -C "$copy" add -A
git -C "$copy" -c user.email=v@example.invalid -c user.name=v commit -qm "Initial commit"
git -C "$copy" remote add origin "$origin" && git -C "$copy" push -q origin main
git -C "$copy" config user.email v@example.invalid && git -C "$copy" config user.name v
for ex in ex2 ex3-loop ex4; do
  (cd "$copy" && WORKSHOP_UPSTREAM="$ROOT" ./workshop reset "$ex" </dev/null >/dev/null 2>"$work/reset.err") \
    || fail "reset $ex failed in a template copy: $(cat "$work/reset.err")"
  git -C "$copy" merge-base --is-ancestor origin/main HEAD || fail "reset $ex is not built on the copy's main"
done
grep -q FREE_SHIPPING_FROM "$copy/shop/pricing.py" || fail "reset ex4 did not bring the exercise 4 change"
[ -e "$copy/.fairmind" ] && fail "the exercise 3 contract leaked into exercise 4"
pass "reset builds ex2, ex3-loop, ex4 on the copy's own main, and nothing leaks between them"

echo "ALL VERIFIED"
