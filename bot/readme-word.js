// README activity bot: deletes one word from README.md and commits, then adds the
// same word back and commits, so the file ends unchanged. Run: node bot/readme-word.js [--test]
const fs = require("fs");
const path = require("path");
const assert = require("assert");
const { execFileSync } = require("child_process");

const README = path.resolve(__dirname, "..", "README.md");

const ts = () => new Date().toISOString().replace("T", " ").slice(0, 19);
const log = {
  info: (m) => console.log(`\x1b[36m[${ts()}] [INFO]\x1b[0m ${m}`),
  ok: (m) => console.log(`\x1b[32m[${ts()}] [ OK ]\x1b[0m ${m}`),
  fail: (m) => console.error(`\x1b[31m[${ts()}] [FAIL]\x1b[0m ${m}`),
};

// Runs one step; on error rethrows with the step name so the log says where it broke.
function step(name, fn) {
  log.info(`${name}...`);
  try {
    const result = fn();
    log.ok(name);
    return result;
  } catch (err) {
    throw new Error(`${name} failed: ${err.message}`);
  }
}

const git = (...args) => execFileSync("git", args, { encoding: "utf8" }).trim();

// Removes the last plain word (3+ letters) in the text, together with the space before it.
// Skips headings and lines with HTML, links or code so the README never breaks between the two commits.
function removeLastWord(text) {
  const lines = text.split("\n");
  for (let i = lines.length - 1; i >= 0; i--) {
    if (/^#|[<`]|https?:/.test(lines[i])) continue;
    const m = [...lines[i].matchAll(/ ([A-Za-z]{3,})\b/g)].pop();
    if (!m) continue;
    lines[i] = lines[i].slice(0, m.index) + lines[i].slice(m.index + m[0].length);
    return { word: m[1], text: lines.join("\n") };
  }
  throw new Error("no word found to remove");
}

function main() {
  const original = step("Read README.md", () => fs.readFileSync(README, "utf8"));
  const { word, text } = step("Pick word", () => removeLastWord(original));
  log.info(`Word: "${word}"`);

  step("Delete word + commit", () => {
    fs.writeFileSync(README, text);
    git("commit", "-am", "docs: tidy README wording");
  });
  step("Add word back + commit", () => {
    fs.writeFileSync(README, original);
    git("commit", "-am", "docs: refine README wording");
  });
  step("Push", () => {
    git("pull", "--rebase");
    git("push");
  });

  log.ok("Done — 2 commits pushed, README unchanged");
}

function selfTest() {
  const r = removeLastWord("Built by **Manyu Shetty** at home.");
  assert.deepStrictEqual(r, { word: "home", text: "Built by **Manyu Shetty** at." });
  assert.strictEqual(removeLastWord('plain words here\n<a href="x">link text</a>').word, "here");
  assert.throws(() => removeLastWord("<br/>"));
  log.ok("Self-test passed");
}

try {
  process.argv.includes("--test") ? selfTest() : main();
} catch (err) {
  log.fail(err.message);
  process.exitCode = 1;
}
