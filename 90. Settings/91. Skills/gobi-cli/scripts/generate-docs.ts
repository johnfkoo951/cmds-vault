import { execSync } from "node:child_process";
import {
  readFileSync,
  writeFileSync,
  mkdirSync,
  existsSync,
  readdirSync,
  unlinkSync,
} from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SKILL_DIR = join(__dirname, "..");
const REFERENCES_DIR = join(SKILL_DIR, "references");
const TEMPLATE_PATH = join(SKILL_DIR, "SKILL.template.md");
const OUTPUT_PATH = join(SKILL_DIR, "SKILL.md");
const PROJECT_ROOT = join(SKILL_DIR, "..", "..");
// Read version from package.json
const require = createRequire(import.meta.url);
const { version } = require(join(PROJECT_ROOT, "package.json")) as {
  version: string;
};

// Use the built dist/index.js so this works in CI without global install
const GOBI_BIN = join(PROJECT_ROOT, "dist", "index.js");

if (!existsSync(GOBI_BIN)) {
  console.error(
    "Error: dist/index.js not found. Run 'npm run build' first."
  );
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function runHelp(args: string[]): string {
  const cmd = `node ${GOBI_BIN} ${args.join(" ")} --help`;
  return execSync(cmd, {
    encoding: "utf-8",
    env: { ...process.env, NO_COLOR: "1" },
    timeout: 10_000,
  }).trim();
}

interface CommandInfo {
  name: string;
  description: string;
}

/**
 * Parse Commander.js help output to extract the Commands section.
 * Commander format:
 *   Commands:
 *     name [options]  description
 *     help [command]  display help for command
 */
function parseCommands(helpText: string): CommandInfo[] {
  const commands: CommandInfo[] = [];
  const lines = helpText.split("\n");
  let inCommands = false;

  for (const line of lines) {
    if (line.trim() === "Commands:") {
      inCommands = true;
      continue;
    }
    if (inCommands) {
      // Match: leading whitespace, command name, possible args, 2+ spaces, description
      const match = line.match(/^\s{2,}(\S+)\s+.*?\s{2,}(.+)$/);
      if (match) {
        const [, name, desc] = match;
        if (name !== "help") {
          commands.push({ name, description: desc.trim() });
        }
      } else if (line.trim() === "") {
        break;
      } else if (commands.length > 0 && line.match(/^\s{10,}\S/)) {
        // Continuation line of the previous command's wrapped description
        commands[commands.length - 1].description += " " + line.trim();
      }
    }
  }

  return commands;
}

// ---------------------------------------------------------------------------
// Generate reference docs
// ---------------------------------------------------------------------------

function generateReferenceDoc(
  commandPath: string[],
  helpText: string,
  subcommands: { name: string; helpText: string }[]
): string {
  const lines: string[] = [];
  const fullCommand = ["gobi", ...commandPath].join(" ");

  lines.push(`# ${fullCommand}`);
  lines.push("");
  lines.push("```");
  lines.push(helpText);
  lines.push("```");

  for (const sub of subcommands) {
    lines.push("");
    lines.push(`## ${sub.name}`);
    lines.push("");
    lines.push("```");
    lines.push(sub.helpText);
    lines.push("```");
  }

  return lines.join("\n") + "\n";
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

// Ensure references directory exists
if (!existsSync(REFERENCES_DIR)) {
  mkdirSync(REFERENCES_DIR, { recursive: true });
}

// Clean existing generated reference files
for (const file of readdirSync(REFERENCES_DIR)) {
  if (file.endsWith(".md")) {
    unlinkSync(join(REFERENCES_DIR, file));
  }
}

// 1. Get top-level commands
const topHelp = runHelp([]);
const topCommands = parseCommands(topHelp);

// 2. Generate reference files for each command group
const referenceFiles: { name: string; path: string; title: string }[] = [];
const commandLines: string[] = [];

for (const cmd of topCommands) {
  let cmdHelp: string;
  try {
    cmdHelp = runHelp([cmd.name]);
  } catch {
    // Leaf command with no subcommands — use top-level help
    cmdHelp = `${cmd.description}`;
  }

  const subCommands = parseCommands(cmdHelp);

  // Build command listing
  commandLines.push(`- \`gobi ${cmd.name}\` — ${cmd.description}`);

  const subHelpTexts: { name: string; helpText: string }[] = [];
  for (const sub of subCommands) {
    try {
      const subHelp = runHelp([cmd.name, sub.name]);
      subHelpTexts.push({ name: sub.name, helpText: subHelp });
      commandLines.push(
        `  - \`gobi ${cmd.name} ${sub.name}\` — ${sub.description}`
      );
    } catch {
      // Skip commands that fail (e.g. interactive-only)
    }
  }

  const refContent = generateReferenceDoc([cmd.name], cmdHelp, subHelpTexts);
  const refFile = `${cmd.name}.md`;
  writeFileSync(join(REFERENCES_DIR, refFile), refContent);
  referenceFiles.push({
    name: refFile,
    path: `references/${refFile}`,
    title: `gobi ${cmd.name}`,
  });
}

// 3. Build placeholders
const COMMANDS = commandLines.join("\n");
const REFERENCE_TOC = referenceFiles
  .map((ref) => `- [${ref.title}](${ref.path})`)
  .join("\n");

// 4. Read template and fill placeholders
let template = readFileSync(TEMPLATE_PATH, "utf-8");
template = template.replace(/\{\{VERSION\}\}/g, version);
template = template.replace("{{COMMANDS}}", COMMANDS);
template = template.replace("{{REFERENCE_TOC}}", REFERENCE_TOC);

// 5. Write generated SKILL.md
writeFileSync(OUTPUT_PATH, template);

console.log(`Generated SKILL.md (v${version})`);
console.log(`Generated ${referenceFiles.length} reference files`);
