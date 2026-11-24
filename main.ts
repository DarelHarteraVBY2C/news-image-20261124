// Dunia Hari Ini — Selasa, 24 November 2026
// Entry news-image-20261124: menulis ulang entry.png ke direktori output
// make.fun. Node 22, stdlib saja, tanpa network, hasil byte-identik.
//
// Alur: baca entry.png -> validasi penuh (signature, IHDR, IEND, ukuran,
// dimensi 1024x1024) -> tulis ke $MAKEFUN_OUTPUT_DIR/entry.png -> baca
// ulang dan pastikan hash + byte sama persis dengan sumber.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join, resolve } from "node:path";

const SOURCE_NAME = "entry.png";
const LIMIT_BYTES = 1_048_576;
const EXPECT_W = 1024;
const EXPECT_H = 1024;

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const IEND_TAIL = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44,
  0xae, 0x42, 0x60, 0x82,
]);

function abort(reason: string): never {
  console.error(`[dunia-hari-ini] gagal: ${reason}`);
  process.exit(1);
}

function digest(buf: Buffer): string {
  return createHash("sha256").update(buf).digest("hex");
}

// Validasi struktur PNG secara menyeluruh sebelum berkas dipakai.
function validatePng(buf: Buffer): void {
  if (buf.length < 33) abort(`berkas terlalu kecil (${buf.length} byte)`);
  if (buf.length > LIMIT_BYTES) {
    abort(`berkas ${buf.length} byte melebihi batas ${LIMIT_BYTES} byte`);
  }
  if (!buf.subarray(0, 8).equals(PNG_MAGIC)) {
    abort("signature PNG tidak cocok");
  }
  // Chunk pertama harus IHDR (panjang 13, tipe di offset 12).
  if (buf.readUInt32BE(8) !== 13 || buf.toString("latin1", 12, 16) !== "IHDR") {
    abort("chunk pertama bukan IHDR");
  }
  const w = buf.readUInt32BE(16);
  const h = buf.readUInt32BE(20);
  if (w !== EXPECT_W || h !== EXPECT_H) {
    abort(`dimensi ${w}x${h}, diharapkan ${EXPECT_W}x${EXPECT_H}`);
  }
  if (!buf.subarray(buf.length - 12).equals(IEND_TAIL)) {
    abort("chunk penutup IEND tidak ditemukan");
  }
}

function main(): void {
  const repoRoot = resolve(new URL(".", import.meta.url).pathname);
  const sourcePath = join(repoRoot, SOURCE_NAME);
  let source: Buffer;
  try {
    source = readFileSync(sourcePath);
  } catch {
    abort(`tidak bisa membaca ${sourcePath}`);
  }
  validatePng(source);

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(repoRoot, "out");
  mkdirSync(outDir, { recursive: true });
  const destPath = join(outDir, SOURCE_NAME);
  writeFileSync(destPath, source);

  const written = readFileSync(destPath);
  if (written.length !== source.length) {
    abort(
      `ukuran hasil tulis ${written.length} byte != sumber ${source.length} byte`,
    );
  }
  if (!written.equals(source)) {
    abort("hasil tulis tidak sama persis dengan sumber");
  }
  console.log(
    `[dunia-hari-ini] ok: ${destPath} (${written.length} byte, sha256 ${digest(written)})`,
  );
}

main();
