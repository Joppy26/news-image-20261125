// SPDX-License-Identifier: MIT
// Copies entry.png to the output directory.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const here = fileURLToPath(new URL(".", import.meta.url));
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
