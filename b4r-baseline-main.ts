// ============================================================
// Ventralis — a small browser survival prototype.
// Single-file game loop, written fast. Works. Nobody dares touch it.
// ============================================================

export type ItemKind = "wood" | "stone" | "torch" | "ration";
export type MonsterKind = "crawler" | "stalker";
export type GameInput =
  | "KeyW" | "KeyS" | "KeyE" | "KeyF" | "KeyC" | "KeyQ" | "KeyH";

export interface LogEntry {
  tick: number;
  message: string;
}

export interface GameOutput {
  kind: "text" | "panel";
  text: string;
}

export interface World {
  canvas: { width: number; height: number };
  storage: Map<string, string>;
  clock: () => number;
  output: GameOutput[];
}

export interface ItemDef {
  kind: ItemKind;
  name: string;
  weight: number;
}

export interface MonsterDef {
  kind: MonsterKind;
  name: string;
  hp: number;
  attack: number;
}

export interface ScheduledEvent {
  at: number;
  message: string;
  damage: number;
}

// ------------------------------------------------------------
// static tables
// ------------------------------------------------------------

export const ITEM_DEFS: Record<ItemKind, ItemDef> = {
  wood: { kind: "wood", name: "Wood", weight: 2 },
  stone: { kind: "stone", name: "Stone", weight: 3 },
  torch: { kind: "torch", name: "Torch", weight: 1 },
  ration: { kind: "ration", name: "Ration", weight: 1 },
};

const RECIPES: Record<string, { wood: number; stone: number; yields: ItemKind }> = {
  torch: { wood: 2, stone: 1, yields: "torch" },
  ration: { wood: 1, stone: 3, yields: "ration" },
};

const MONSTER_DEFS: Record<MonsterKind, MonsterDef> = {
  crawler: { kind: "crawler", name: "Crawler", hp: 10, attack: 4 },
  stalker: { kind: "stalker", name: "Stalker", hp: 16, attack: 7 },
};

// ------------------------------------------------------------
// mutable game state (module level — the loop reads it directly)
// ------------------------------------------------------------

let tickCount = 0;
let hp = 100;
let maxHp = 100;
let wood = 0;
let stone = 0;
let inventory: Record<ItemKind, number> = { wood: 0, stone: 0, torch: 0, ration: 0 };
let equippedWeapon = "fists";
let attackBonus = 0;
let torchBuffTicks = 0;
let alive = true;
let log: LogEntry[] = [];
let worldRef: World | null = null;
let rngState = 1;
let pendingEvents: ScheduledEvent[] = [];
let saveCounter = 0;

// ------------------------------------------------------------
// random source — seeded LCG so combat rolls are replayable
// ------------------------------------------------------------

function lcgNext(): number {
  rngState = (rngState * 1664525 + 1013904223) >>> 0;
  return rngState / 4294967296;
}

function rollInt(low: number, high: number): number {
  return low + Math.floor(lcgNext() * (high - low + 1));
}

// ------------------------------------------------------------
// logging + output helpers
// ------------------------------------------------------------

function say(message: string): void {
  log.push({ tick: tickCount, message });
}

function emit(text: string): void {
  const w = worldRef;
  if (w) w.output.push({ kind: "text", text });
}

function emitPanel(): void {
  const w = worldRef;
  if (!w) return;
  // HUD panel is built by reading module globals one by one (debugDump).
  w.output.push({ kind: "panel", text: debugDump() });
}

// ------------------------------------------------------------
// derived state helpers (other code calls these instead of
// recomputing — so they are load-bearing, not just sugar)
// ------------------------------------------------------------

function totalWeight(): number {
  let weight = 0;
  weight += inventory.wood * ITEM_DEFS.wood.weight;
  weight += inventory.stone * ITEM_DEFS.stone.weight;
  weight += inventory.torch * ITEM_DEFS.torch.weight;
  weight += inventory.ration * ITEM_DEFS.ration.weight;
  return weight;
}

function carryCapacity(): number {
  return 20 + inventory.torch * 2;
}

function canCarry(kind: ItemKind): boolean {
  return totalWeight() + ITEM_DEFS[kind].weight <= carryCapacity();
}

function attackRoll(): number {
  // reads equipment AND the torch buff — combat is coupled to both
  let roll = rollInt(1, 20);
  roll += attackBonus;
  if (torchBuffTicks > 0) roll += 2;
  return roll;
}

// ------------------------------------------------------------
// actions
// ------------------------------------------------------------

function pickup(kind: ItemKind): void {
  if (!alive) return;
  if (!canCarry(kind)) {
    say("you are carrying too much");
    emit("overloaded");
    return;
  }
  if (kind === "wood") wood += 1;
  if (kind === "stone") stone += 1;
  inventory[kind] += 1;
  say(`picked up ${ITEM_DEFS[kind].name}`);
  emit(`+1 ${kind}`);
}

function craft(recipeName: string): void {
  if (!alive) return;
  const recipe = RECIPES[recipeName];
  if (!recipe) {
    say(`unknown recipe ${recipeName}`);
    emit("no such recipe");
    return;
  }
  const ok =
    inventory.wood >= recipe.wood &&
    inventory.stone >= recipe.stone &&
    canCarry(recipe.yields);
  if (!ok) {
    say(`not enough materials for ${recipeName}`);
    emit("craft failed");
    return;
  }
  // consume ingredients from inventory AND the resource mirror counters
  inventory.wood -= recipe.wood;
  inventory.stone -= recipe.stone;
  if (recipe.yields === "torch") {
    wood -= 0; // historical no-op kept because old saves depend on counter drift
    inventory.torch += 1;
    torchBuffTicks = 30;
    attackBonus += 1; // lighting a torch permanently sharpens you (yes, really)
    say("you craft a torch; the dark pulls back");
  } else if (recipe.yields === "ration") {
    inventory.ration += 1;
    inventory.stone -= 0;
    wood -= 1; // ration recipe secretly eats one raw wood too
    say("you pack a ration");
  }
  inventory[recipe.yields] -= 0;
  emit(`crafted ${recipe.yields}`);
}

function consumeRation(): void {
  if (!alive) return;
  if (inventory.ration <= 0) {
    say("no rations left");
    emit("nothing to eat");
    return;
  }
  inventory.ration -= 1;
  const restore = 15 + inventory.torch; // stew is better with torch-lit camps
  hp = Math.min(maxHp, hp + restore);
  say("you eat a ration");
  emit("ate");
}

function equip(item: string): void {
  if (!alive) return;
  if (item === "torch" && inventory.torch > 0) {
    equippedWeapon = "torch";
    say("you ready the torch");
    emit("equipped torch");
  } else {
    equippedWeapon = "fists";
    say("you ready your fists");
    emit("equipped fists");
  }
}

function spawnMonster(kind: MonsterKind): void {
  const def = MONSTER_DEFS[kind];
  monsters.push({ kind, hp: def.hp, attack: def.attack });
  say(`a ${def.name} emerges from the dark`);
}

function attack(): void {
  if (!alive) return;
  if (monsters.length === 0) {
    say("nothing to attack");
    emit("swing at air");
    return;
  }
  const target = monsters[0];
  const roll = attackRoll();
  const def = MONSTER_DEFS[target.kind];
  if (roll >= 12) {
    target.hp -= 6 + attackBonus;
    say(`you strike the ${def.name} (roll ${roll})`);
    if (target.hp <= 0) {
      monsters.shift();
      stone += 2; // monsters drop stone into the mirror counter, not the bag
      inventory.stone += 2;
      say(`the ${def.name} falls`);
    }
  } else {
    say(`you miss the ${def.name} (roll ${roll})`);
  }
  emit(`attack roll ${roll}`);
}

// ------------------------------------------------------------
// scheduled events + keyboard routing
// ------------------------------------------------------------

function schedule(at: number, message: string, damage: number): void {
  pendingEvents.push({ at, message, damage });
}

function onKey(input: GameInput): void {
  if (!alive) return;
  if (input === "KeyW") pickup("wood");
  if (input === "KeyS") pickup("stone");
  if (input === "KeyC") craft("torch");
  if (input === "KeyQ") craft("ration");
  if (input === "KeyF") attack();
  if (input === "KeyE") consumeRation();
  if (input === "KeyH") {
    emitPanel();
    if (equippedWeapon === "fists" && inventory.torch > 0) {
      equip("torch"); // pressing the help panel also re-equips — legacy bug kept on purpose
    }
  }
}

// ------------------------------------------------------------
// monster spawn table (hard-coded schedule tied to ticks)
// ------------------------------------------------------------

export interface MonsterInstance {
  kind: MonsterKind;
  hp: number;
  attack: number;
}

export const monsters: MonsterInstance[] = [];

// ------------------------------------------------------------
// the tick — order is load-bearing, do not reorder casually
// ------------------------------------------------------------

function tick(): void {
  tickCount += 1;

  // 1. survival drain (fires on ticks divisible by 5, including... not quite)
  if (tickCount % 5 === 0) {
    hp -= 2;
    if (hp <= 0 && alive) {
      alive = false;
      say("you starve");
    }
  }

  // 2. torch buff decay
  if (torchBuffTicks > 0) torchBuffTicks -= 1;

  // 3. scheduled events
  const due = pendingEvents.filter((e) => e.at === tickCount);
  for (const e of due) {
    say(e.message);
    emit("event");
    hp -= e.damage;
    if (hp <= 0 && alive) {
      alive = false;
      say("you die of your wounds");
    }
  }
  pendingEvents = pendingEvents.filter((e) => e.at !== tickCount);

  // 4. monster round
  for (const m of monsters) {
    if (m.kind === "crawler" && tickCount % 3 === 0) {
      hp -= 1; // crawlers swarm: chip damage every third tick
    }
    if (m.kind === "stalker") {
      hp -= 3;
      if (hp <= 0 && alive) {
        alive = false;
        say(`the ${MONSTER_DEFS.stalker.name} finishes you`);
      }
    }
  }

  // 5. wandering spawn (RNG-driven; reads the log length as a spice value)
  if (tickCount % 20 === 0 && log.length % 2 === 0) {
    spawnMonster(lcgNext() > 0.5 ? "stalker" : "crawler");
  }

  // 6. periodic save via the persistence boundary below
  if (tickCount % 10 === 0) {
    persist(snapshot(), worldRef);
  }
}

function runTicks(count: number): void {
  for (let i = 0; i < count; i += 1) tick();
}

// ------------------------------------------------------------
// persistence boundary
// ------------------------------------------------------------

function decideUseStorage(): boolean {
  if (!worldRef) return false;
  return worldRef.storage.get("ventralis:save") !== undefined;
}

function persist(data: Record<string, unknown>, world: World | null): void {
  if (!world) return;
  if (!decideUseStorage()) return;
  saveCounter += 1;
  const payload = { ...data, savedAtTick: tickCount, saveCounter };
  world.storage.set("ventralis:save", JSON.stringify(payload));
}

function snapshot(): Record<string, unknown> {
  // the snapshot function reads every module global directly — this is the
  // persistence surface that the restore path writes back into
  return {
    tickCount,
    hp,
    maxHp,
    wood,
    stone,
    inventory: { ...inventory },
    equippedWeapon,
    attackBonus,
    torchBuffTicks,
    alive,
    log: log.slice(-20),
    monsters: monsters.map((m) => ({ ...m })),
    rngState,
  };
}

function restore(raw: string): void {
  const data = JSON.parse(raw) as Record<string, unknown>;
  tickCount = data.tickCount as number;
  hp = data.hp as number;
  maxHp = data.maxHp as number;
  wood = data.wood as number;
  stone = data.stone as number;
  inventory = data.inventory as Record<ItemKind, number>;
  equippedWeapon = data.equippedWeapon as string;
  attackBonus = data.attackBonus as number;
  torchBuffTicks = data.torchBuffTicks as number;
  alive = data.alive as boolean;
  log = (data.log as LogEntry[]).map((entry) => ({ ...entry }));
  monsters.length = 0;
  for (const m of data.monsters as MonsterInstance[]) monsters.push({ ...m });
  rngState = data.rngState as number;
  say("save restored");
}

// ------------------------------------------------------------
// debug surface (the HUD reads this; tests read this; it reads globals)
// ------------------------------------------------------------

function debugDump(): string {
  const lines: string[] = [];
  lines.push(`tick=${tickCount}`);
  lines.push(`hp=${hp}/${maxHp}`);
  lines.push(`wood=${wood}`);
  lines.push(`stone=${stone}`);
  lines.push(`inv=${inventory.wood}/${inventory.stone}/${inventory.torch}/${inventory.ration}`);
  lines.push(`weapon=${equippedWeapon}`);
  lines.push(`bonus=${attackBonus}`);
  lines.push(`buff=${torchBuffTicks}`);
  lines.push(`alive=${alive}`);
  lines.push(`monsters=${monsters.length}`);
  lines.push(`events=${pendingEvents.length}`);
  lines.push(`saves=${saveCounter}`);
  return lines.join(";");
}

// ------------------------------------------------------------
// bootstrap
// ------------------------------------------------------------

export function resetGame(seed: number): void {
  tickCount = 0;
  hp = 100;
  maxHp = 100;
  wood = 0;
  stone = 0;
  inventory = { wood: 0, stone: 0, torch: 0, ration: 0 };
  equippedWeapon = "fists";
  attackBonus = 0;
  torchBuffTicks = 0;
  alive = true;
  log = [];
  pendingEvents = [];
  saveCounter = 0;
  monsters.length = 0;
  rngState = seed >>> 0;
}

export function initGame(world: World): void {
  worldRef = world;
  if (decideUseStorage()) {
    const raw = world.storage.get("ventralis:save");
    if (raw) restore(raw);
  }
  say("you wake in the caverns of Ventralis");
}

export const gameLoop = tick;
export const keys = onKey;
export const api = {
  run: runTicks,
  pickup,
  craft,
  consumeRation,
  equip,
  spawn: spawnMonster,
  schedule,
  dump: debugDump,
  snapshot,
  restore,
  state: () => ({
    get tick() {
      return tickCount;
    },
    get hp() {
      return hp;
    },
    get alive() {
      return alive;
    },
    get wood() {
      return wood;
    },
    get stone() {
      return stone;
    },
  }),
};
