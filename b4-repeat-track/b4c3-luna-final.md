# B4-A0 — Ventralis Monolith Architecture Audit

## 1. State map

Comparison route: judgment/audit slice, candidate design evaluated against the same owner rubric.

| Binding | Evidence | Classification | Proposed ownership |
|---|---:|---|---|
| `tickCount` | `main.ts:72` | Component data | `ClockState` |
| `hp` | `main.ts:73` | Component data | `Vitals` |
| `maxHp` | `main.ts:74` | Component data | `Vitals` |
| `wood` | `main.ts:75` | Component data, legacy resource mirror | `ResourceMirrors`; preserve independently from inventory |
| `stone` | `main.ts:76` | Component data, legacy resource mirror | `ResourceMirrors`; preserve independently from inventory |
| `inventory` | `main.ts:77` | Component data | `Inventory` |
| `equippedWeapon` | `main.ts:78` | Component data | `Equipment` |
| `attackBonus` | `main.ts:79` | Component data | `CombatModifiers` |
| `torchBuffTicks` | `main.ts:80` | Component data | `CombatModifiers` |
| `alive` | `main.ts:81` | Component data | `Vitals`/`LifeState` |
| `log` | `main.ts:82` | Retained runtime/session state | `SessionLog`; it affects spawn behavior and persistence |
| `worldRef` | `main.ts:83` | Retained runtime state | Bootstrap-owned `RuntimeContext`; never a component |
| `rngState` | `main.ts:84` | Retained runtime state | Seeded `RandomSource`; snapshot/restore-visible |
| `pendingEvents` | `main.ts:85` | Retained runtime state | Event-queue service; not ECS data |
| `saveCounter` | `main.ts:86` | Retained runtime state | Persistence adapter/session metrics |
| `monsters` | `main.ts:297` | Component/entity data | `MonsterStore` or entity collection; preserve exported observable array semantics |

Derived on read:

- `totalWeight()` — `main.ts:126-133`
- `carryCapacity()` — `main.ts:135-137`
- `canCarry()` — `main.ts:139-141`
- `debugDump()` — derived presentation, not stored state

Dead/redundant state: none. The apparent redundant resource mirrors are behaviorally live and must not be removed.

## 2. Function map

| Function | Destination |
|---|---|
| `lcgNext` | Seeded RNG adapter |
| `rollInt` | Seeded RNG adapter |
| `say` | Session-log service |
| `emit` | Output/debug surface adapter |
| `emitPanel` | Debug/HUD surface |
| `totalWeight` | Inventory domain query |
| `carryCapacity` | Inventory domain query |
| `canCarry` | Inventory domain query |
| `attackRoll` | Combat system/query |
| `pickup` | Gathering/inventory system |
| `craft` | Crafting system |
| `consumeRation` | Consumable system |
| `equip` | Equipment system |
| `spawnMonster` | Monster entity factory |
| `attack` | Combat system |
| `schedule` | Event-queue service |
| `onKey` | Input/router system |
| `tick` | Retained bootstrap/system orchestrator |
| `runTicks` | Retained bootstrap/test clock driver |
| `decideUseStorage` | Persistence adapter policy |
| `persist` | Persistence adapter |
| `snapshot` | Persistence serializer |
| `restore` | Persistence deserializer |
| `debugDump` | Debug/HUD surface |
| `resetGame` | Bootstrap/session reset |
| `initGame` | Bootstrap wiring and restore |
| `gameLoop` export | Bootstrap facade |
| `keys` export | Input facade |
| `api.state` getter facade | Public read-only state facade |

## 3. Side effects and dependencies

| Function | Reads | Writes / effects |
|---|---|---|
| `lcgNext` | `rngState` | Mutates RNG state; consumes one RNG value |
| `rollInt` | RNG | Consumes RNG through `lcgNext` |
| `say` | `tickCount` | Appends `log`; no output/storage |
| `emit` | `worldRef` | Appends text to `world.output` |
| `emitPanel` | `worldRef`, `debugDump` | Appends panel output |
| `totalWeight` | `inventory`, `ITEM_DEFS` | None |
| `carryCapacity` | `inventory` | None |
| `canCarry` | inventory queries and item definitions | None |
| `attackRoll` | `attackBonus`, `torchBuffTicks` | Consumes RNG |
| `pickup` | `alive`, carry queries, item definitions | Mutates mirrors/inventory; log/output |
| `craft` | `alive`, recipes, inventory, carry query | Mutates inventory, mirrors, buffs, bonus; log/output |
| `consumeRation` | `alive`, inventory, `maxHp` | Mutates inventory/hp; log/output |
| `equip` | `alive`, inventory | Mutates equipment; log/output |
| `spawnMonster` | monster definitions | Mutates `monsters`; log |
| `attack` | `alive`, monsters, combat state, RNG | Mutates monster/hp/resources; log/output; consumes RNG |
| `schedule` | None | Mutates event queue |
| `onKey` | `alive`, equipment, inventory | Routes actions; may emit panel and re-equip |
| `tick` | all core state, queue, log, RNG, world | Ordered state mutation; events/output; periodic persistence; possible RNG consumption |
| `runTicks` | None directly | Repeats `tick` |
| `decideUseStorage` | `worldRef.storage` | None; gates saving/restoring |
| `persist` | world, `tickCount`, `saveCounter` | Storage write; increments save counter |
| `snapshot` | all serialized state, monsters | Returns copy; no mutation |
| `restore` | serialized payload | Replaces state, monsters, RNG; appends restore log |
| `debugDump` | all display state, queue length, save counter | Returns formatted string |
| `resetGame` | seed | Resets state, queue, monsters, RNG; retains `worldRef` |
| `initGame` | world storage | Sets runtime world; may restore; appends boot log |
| `api.state` | selected state | Read-only getters |

The `tick` phase order must remain: survival drain, torch decay, scheduled events, monster round, wandering spawn, periodic save.

## 4. Ownership and mutation boundaries

- World state is owned by a `WorldState` aggregate containing vitals, inventory, resource mirrors, equipment, modifiers, monsters, and tick state.
- The event queue is owned by an `EventQueue` service. Systems may enqueue events and the tick coordinator drains due events.
- Persistence is owned by a `PersistenceAdapter`, receiving a serializer and runtime save policy. It alone accesses `World.storage`.
- The clock is owned by a clock interface injected into bootstrap. Existing tick-count semantics remain authoritative; `World.clock` is retained as an available runtime dependency but must not silently replace tick progression.
- Randomness is owned by an injected seeded `RandomSource` wrapping the LCG. It remains snapshot/restore-visible.

Mutation strategy: controlled direct mutation inside systems, with the world aggregate passed through a narrow `GameContext`. This is preferable here to returned command-only systems because the existing behavior depends on exact mutation order, shared resource-mirror drift, mutable monster references, log length, and RNG consumption order. Systems should expose narrow interfaces and only mutate owned domains; the coordinator controls sequencing.

## 5. Not-ECS list

- Persistence boundary: storage I/O, save gating, serialization, and `saveCounter` are infrastructure concerns, not entities or components.
- Debug/HUD surface: `debugDump`, panel emission, and output formatting are presentation adapters reading state; turning them into components would pollute gameplay state with UI concerns.
- Scheduled-event queue: it is an ordered temporal service with due-event filtering, not an entity collection. A queue abstraction preserves exact-tick semantics more clearly.
- Seeded RNG: the RNG is a deterministic infrastructure dependency and replay resource. It must not become a component attached to gameplay entities.
- Input routing and bootstrap: keyboard mapping and lifecycle wiring are application boundaries, not ECS systems containing domain state.
- Static definitions (`ITEM_DEFS`, `RECIPES`, `MONSTER_DEFS`): immutable configuration/type data, not runtime components.

ECS remains useful for monster instances, inventory/vitals/equipment components, and ordered gameplay systems. A justified hybrid is safer than forcing every concern into ECS.

## 6. Hidden-coupling register

| Coupling | Evidence | Preservation requirement |
|---|---:|---|
| Resource mirrors and inventory are double-accounted | `main.ts:162-164`, `186-188` | Pickup increments both; crafting decrements inventory only. Do not normalize them. |
| Torch crafting leaves mirror counters unchanged | `main.ts:189-194` | Preserve `wood -= 0`, inventory consumption, `attackBonus += 1`, and `torchBuffTicks = 30`. |
| Ration crafting secretly consumes raw mirror wood | `main.ts:195-199` | Preserve `wood -= 1`; stone mirror remains unchanged. |
| Monster death gives stone to both mirror and bag | `main.ts:251-255` | Preserve the double stone drop. |
| RNG consumption order is observable | `main.ts:92-99`, `143-148`, `246`, `346-347` | Preserve one LCG stream and call order; seed 7 must produce attack roll 5 first. |
| Spawn behavior depends on log length | `main.ts:345-348` | Preserve `log.length % 2 === 0` gating and exact log append order. |
| Periodic saves are gated by existing save key | `main.ts:364-374` | Preserve `decideUseStorage`; tick 10 is a no-op without the key. |
| Save counter is hidden mutable state | `main.ts:372-374`, `432-433` | Preserve increment timing and debug output. |
| Snapshot/restore touches nearly all state | `main.ts:377-414` | Serialize and restore mirrors, modifiers, log tail, monsters, and RNG. |
| Restore appends a log entry | `main.ts:409-413` | Preserve post-restore log mutation. |
| KeyH has a re-equip side effect | `main.ts:279-283` | Emit panel first, then equip torch when fists plus torch are present. |
| KeyH output ordering is observable | `main.ts:280-282`; tests | Preserve panel-before-equip output. |
| Tick order is load-bearing | `main.ts:303-353` | Do not reorder survival, buffs, events, monsters, spawn, save. |
| Death blocks actions | `main.ts:155-156`, `169-170`, `205-206`, `219-220`, `238-239`, `271-272` | Preserve early returns after death. |
| `resetGame` does not clear `worldRef` | `main.ts:441-456` | Preserve unless an explicit compatibility decision is made; current tests rely on subsequent init behavior. |
| `debugDump` exposes queue/save counts | `main.ts:420-434` | Preserve exact field order and formatting. |
| Storage presence, not payload validity, enables persistence | `main.ts:364-366` | Preserve gating semantics and avoid eager storage creation. |
| Stalker/crawler attack values in definitions are not used for damage | `main.ts:63-66`, `331-342` | Preserve actual hard-coded damage behavior. |
| `World.clock` is currently unused | `main.ts:21-25` | Do not introduce clock-driven behavior during migration. |

## 7. Proposed dependency graph

```mermaid
graph TD
  Main[main.ts bootstrap facade]
  Input[input-router.ts]
  Systems[systems/*]
  Components[components/*]
  Entities[entities/monster-factory.ts]
  Queries[domain/inventory-queries.ts]
  Events[runtime/event-queue.ts]
  RNG[runtime/random-source.ts]
  Session[runtime/session-log.ts]
  Persist[persistence/persistence-adapter.ts]
  Debug[debug/debug-surface.ts]
  Types[types/domain.ts]
  Config[config/game-definitions.ts]

  Main --> Input
  Main --> Systems
  Main --> Events
  Main --> RNG
  Main --> Session
  Main --> Persist
  Main --> Debug

  Input --> Systems
  Systems --> Components
  Systems --> Entities
  Systems --> Queries
  Systems --> Events
  Systems --> RNG
  Systems --> Session
  Systems --> Debug

  Entities --> Types
  Systems --> Types
  Queries --> Types
  Config --> Types
  Persist --> Types
  Debug --> Types

  Persist -. reads/writes World.storage .-> World[World runtime adapter]
  Debug -. writes World.output .-> World

  Components --> Types
  Events --> Types
  RNG --> Types
  Session --> Types
```

No arrows point back from persistence/debug into gameplay systems, so the graph remains acyclic.

## 8. Proposed file tree

Each migrated implementation file should remain under 120 lines; `main.ts` should remain under approximately 80 lines.

```text
src/
  main.ts                         # bootstrap/facade, <=80 lines
  types/
    domain.ts                     # shared interfaces and input types
  config/
    game-definitions.ts           # item, recipe, monster tables
  components/
    world-state.ts                # aggregate and component types
    inventory.ts
    vitals.ts
    equipment.ts
    combat-modifiers.ts
    monster-store.ts
  runtime/
    random-source.ts
    event-queue.ts
    session-log.ts
    runtime-context.ts
  domain/
    inventory-queries.ts
  entities/
    monster-factory.ts
  systems/
    pickup-system.ts
    crafting-system.ts
    consumable-system.ts
    equipment-system.ts
    combat-system.ts
    survival-system.ts
    event-system.ts
    spawn-system.ts
    tick-coordinator.ts
  persistence/
    snapshot.ts
    persistence-adapter.ts
  debug/
    debug-surface.ts
  input/
    input-router.ts
```

The exact split can be adjusted if individual files exceed the line budget, but no migrated source file should exceed 120 lines.

## 9. Migration order

1. Add type/config modules and adapters without changing behavior. Keep `main.ts` as the sole caller; run the characterization suite.
2. Extract immutable definitions and pure inventory queries. Verify capacity and pickup tests.
3. Introduce a `WorldState` aggregate while retaining compatibility facades for existing API reads. Verify boot/debug and resource-mirror tests.
4. Extract session logging and output/debug adapters. Verify exact output ordering and dump formatting.
5. Extract RNG as a seeded adapter and snapshot its state. Verify seed-7 attack behavior.
6. Extract pickup, crafting, ration, and equipment systems one at a time. Verify each corresponding characterization group after each slice, including secret wood consumption and torch side effects.
7. Extract monster factory and combat system. Verify double stone drops, monster damage, and death behavior.
8. Extract event queue and survival/event systems without changing tick ordering. Verify exact-tick event behavior and death gating.
9. Extract spawn logic while retaining the log-length condition. Verify RNG/log-dependent spawn behavior.
10. Extract snapshot/restore and persistence adapter. Preserve storage-key gating, save counter, saved tick, log tail, monsters, and RNG. Verify all persistence tests.
11. Extract input routing and retained tick coordinator. Verify KeyH panel/re-equip ordering and all public API facades.
12. Reduce `main.ts` to bootstrap wiring and exports, then run the complete suite and typecheck.

`tests/characterization.test.ts` is the acceptance oracle and must not be edited.

## 10. Risk and verification plan

Behavioral verification must use the existing characterization suite unchanged after every migration slice. The implementer should also:

- Run `pnpm run test` and `pnpm run typecheck` after each slice.
- Compare exact `api.dump()` strings, output-array ordering, storage payloads, save counters, and RNG-derived values.
- Use `git diff --check` and inspect `git diff` after each slice.
- Confirm no test, fixture, or package file changes.
- Add no new test assertions to the acceptance suite; temporary local diagnostics, if needed, must not be committed or left in the worktree.
- Treat any changed RNG call count, log append order, save-gating result, mirror counter, or KeyH output sequence as a migration failure.

Abandon ECS for a concern when ECS introduces observable ordering changes, requires infrastructure state to be represented as gameplay data, makes persistence/debug dependencies cyclic, or cannot preserve deterministic RNG and event semantics without hidden global state. In those cases retain the concern as a service or adapter in the hybrid architecture.

## Verification and handoff

- `git status --short` — exit code `0`; empty output.
- `git diff --check` — exit code `0`; clean.
- `pnpm run test` — exit code `0`; 1 test file passed, 21 tests passed.
- `pnpm run typecheck` — exit code `0`; clean.

Model/provider: GPT-5 / Codex provider; exact provider identifier not exposed.  
Session/thread ID: not visible in the environment.  
Attempts: 1.  
Repairs: none required.  
Changed paths: none.  
Scope drift: none.  
Initial failures: none.  
Remaining blockers: none.