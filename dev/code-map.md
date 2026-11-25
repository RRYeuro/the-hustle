# Code map (rebuilt automatically on every deploy by tools/codemap.py)

index.html = the main game code, then each feature as a `<script id="skinNjs">` block, loaded in number order. Later features run on top of earlier ones. All feature styles live in one `<style id="game-css">` block, marked per feature.

Feature source copies: dev/skins/. Tests: dev/tests/ (crash test: dev/tests/t_fuzz.py).

## Phone & texts

| Feature | Size | Wraps | Note |
|---|---|---|---|
| skin3 | 1k | panePhone, phoneMsg |  |
| skin11 | 5k | panePhone |  |
| skin12 | 14k | - |  |
| skin22 | 3k | - |  |
| skin46 | 11k | busted, devPanel, phoneMsg, plugPrice, w4Court, w4Verdict | ---------- callbacks: people remember ---------- |
| skin50 | 5k | render | friends are contacts |
| skin63 | 1k | modal, render | stay where you were after tapping something: keep scroll spots across a redraw |
| skin70 | 1k | - | thread buttons for recruited plug workers now come from the phone builder (skin91) |
| skin91 | 2k | - |  |

## Plugs & buying

| Feature | Size | Wraps | Note |
|---|---|---|---|
| skin20 | 2k | render |  |
| skin31 | 23k | busted, devPanel, jsBudget, nextDay, paneBlock, paneMove, plugPrice, qtyModal, render | story ties: Lucky's ex or cousin's homeboy, and a plug you are dating, treat you like family |
| skin40 | 4k | devPanel, paneBlock, render, teenStart | New player help: a first-day guide on the Block tab, teens start with plugs they can afford, and hidden rules say why. |
| skin45 | 11k | modal, phoneMsg, say, w4Counsel, wCard | ---------- clean language ---------- |
| skin51 | 10k | paneBlock, plugActions, render, w4Phone | every plug you know is a contact |
| skin55 | 6k | - | ---------- Contacts: one A-Z list, search, groups, contact cards ---------- |
| skin65 | 2k | connectOrder | The connect texts like a person: chat bubbles and reply chips in the phone thread, a chat-style header and bubbles on the order screen. |
| skin66 | 1k | - | skin66: age gate on plugs. Big plugs 18+, 16-17 buy caps smaller |
| skin67 | 4k | - | skin67: multi-buy. Text-order screen: amount stepper per product, running total, one Buy all = one deal |
| skin69 | 1k | nextDay | skin69: "you can order again" pings: plug drops reset, connects back from laying low, new runner orders |
| skin78 | 4k | connectOrder, connectPrice, devPanel | 10% extra promised: bump the next order's price once |

## Crew, workers & runners

| Feature | Size | Wraps | Note |
|---|---|---|---|
| skin2 | 1k | paneBeef |  |
| skin5 | 1k | devPanel |  |
| skin10 | 19k | act, cmResolve, crewHTML, custoPrice, devPanel, mdBody, placeAct, raid, render, serveCusto | random street events |
| skin35 | 14k | cmResolve, devPanel, heist, paneLicks | Licks app: a door to the heists |
| skin38 | 5k | devPanel, openPlace, paneBag | daily: respect from crews and your own crew's loyalty |
| skin48 | 5k | addXP, devPanel, paneCrew, teenStart, w5bOrderDay, w5bOrders | mark the rank-up so the ladder shows NEW for 2 days |
| skin49 | 5k | devPanel, paneSchool, w5bDealers, w5bOrders | runners are recruited, never handed out |
| skin54 | 4k | render | who is this thread with |
| skin57 | 2k | render | fold: apps that moved out of the phone live here (burners+licks: mall/map, trap: in person, crew/family/orders: Your Circle/Contacts) |
| skin68 | 15k | devPanel, nextDay, paneBeef, paneBlock, render | move n of gid into worker w: stash house first, then your stash |
| skin74 | 20k | devPanel, nextDay, paneBeef, paneBlock | ---- the daily run ---- |
| skin89 | 7k | nextDay, paneBlock, render | ---- 3-tap re-up ---- |

## Licks & heists

| Feature | Size | Wraps | Note |
|---|---|---|---|
| skin15 | 1k | - |  |
| skin34 | 1k | openPlace | Home button on the Move map: tap it to head home, or open your place when you are already there |
| skin59 | 8k | openPlace, paneLicks, render | where each lick is today |
| skin64 | 1k | render | skip time is one tap away: a Skip button next to Next day / Lay low / Nap |
| skin71 | 1k | paneRob | skin71: Heists tab lists today's licks (car, house tip, strap tip, store, pharmacy) with a button that opens the lick card |
| skin77 | 8k | devPanel, nextDay, openPlace, paneBlock, plugPrice | ---- Unc ---- |
| skin82 | 4k | devPanel, lickDone, nextDay, render, spendEn, street |  |
| skin83 | 2k | mainMenu | the menu's How to play button opens the list |
| skin86 | 11k | devPanel, lick, lickDone, nextDay, openPlace, paneRob, safeGame | --- which lick is running --- |

## Map, places & moving

| Feature | Size | Wraps | Note |
|---|---|---|---|
| skin4 | 1k | paneMove |  |
| skin33 | 2k | act, clCarry, openPlace, placeAct | logic gaps closed: age limits, do it where you are, ankle monitor, stolen goods on a plane |
| skin58 | 2k | openPlace | moving asks first: pick how you get there, so a mis-tap does not cost the day |

## Rap & social

| Feature | Size | Wraps | Note |
|---|---|---|---|
| skin9 | 3k | modal |  |
| skin17 | 0k | paneBlock |  |
| skin61 | 3k | paneBlock | the trap house is run in person, on one of your blocks |
| skin62 | 1k | mgrBtn, render | manager button always shows, and says what is missing |
| skin79 | 5k | devPanel, mdBody, render | stash spots |
| skin80 | 2k | devPanel, jsBudget, nextDay |  |
| skin81 | 9k | bizMul, devPanel, nextDay, render | majors |
| skin85 | 5k | devPanel, lickDone, nextDay, rapTour | block rep follows real rep |

## Law, heat & beef

| Feature | Size | Wraps | Note |
|---|---|---|---|
| skin18 | 17k | devPanel, nextDay, paneBiz | day tick |
| skin32 | 0k | - | a car means moving between blocks does not eat the day: a little gas and energy instead |
| skin36 | 10k | devPanel, lickDone, openPlace, paneMove, raid, render, srvTick | what patrols do (scanner or not) |
| skin43 | 11k | devPanel, livingDay, paneExp | ---------- Bills that bite ---------- |
| skin53 | 3k | devPanel, paneExp | the more street money you sit on, the more eyes on you |
| skin75 | 7k | devPanel, nextDay, phoneMsg, render, say, srvTick, street | --- oversold blocks --- |
| skin84 | 4k | devPanel, paneBlock, paneRob | Block tab before robbery opens; Heists tab list after |
| skin87 | 8k | bizMul, connectLand, devPanel, nextDay, render, shipRisk | Right Hand picks up loads |
| skin88 | 4k | connectOrder, devPanel, endStory, nextDay, shipRisk, w6Path, wMax | loads home |
| skin90 | 5k | - | deep copy + restore in place (keeps object identity so the real click still works) |

## Look, layout & art

| Feature | Size | Wraps | Note |
|---|---|---|---|
| skin1 | 1k | render |  |
| skin6 | 10k | paneBeef, paneBiz, paneCrew, paneMoney, paneMove, panePhone, paneSpots | Move: board, here sections, rest |
| skin7 | 1k | paneBlock |  |
| skin8 | 2k | newsHTML, newsPush, paneBlock, render | street news with a source + pop-up on new news |
| skin13 | 7k | paneBeef, paneCards, paneCrew, paneExp | Cards |
| skin14 | 14k | talkDown | ---------- football: lane runner ---------- |
| skin16 | 3k | modal, render |  |
| skin21 | 3k | render |  |
| skin23 | 10k | - |  |
| skin24 | 20k | modal, openPlace, render | pan / zoom |
| skin25 | 22k | render |  |
| skin26 | 4k | modal |  |
| skin27 | 27k | busted, devPanel, lick, openPlace, paneLicks, raid, safeGame | ---------- Sort: tap 1 to 16 in order ---------- |
| skin28 | 0k | - | pictures live in art/ now. After the game is up, quietly save them all for offline play. |
| skin30 | 1k | - | loading screen: title art + bar while the first pictures come in |
| skin37 | 11k | act, devPanel, mdBiz, w4Biz | ---------- lane run: delivery and taxi ---------- |
| skin39 | 16k | chase, devPanel, lick, lickDone | Three self-contained mini games: Lockpick (back doors), Vault logic (safes), Roof run (rooftop getaway on foot). |
| skin41 | 2k | - |  |
| skin42 | 4k | cmResolve, devPanel, openPlace, render | crew heist result gets its picture |
| skin44 | 2k | - |  |
| skin47 | 1k | modal, streetEvent, wCard | long cards: picture becomes a thin strip |
| skin56 | 0k | render |  |
| skin60 | 0k | openPlace | Javi and Mateo cards in texts: face thumbnail instead of the whole collage |
| skin73 | 10k | devPanel, render | {steps,i,t0,base,miss} |
| skin76 | 3k | devPanel, render, sfx | popups slide in + panel reveal |
| skin92 | 13k | devPanel, nextDay, paneBlock, render, serveCusto | skin92: UI set. Block fold, phone tab count, day recap, break down (bag up), tap sizes |

## Other

| Feature | Size | Wraps | Note |
|---|---|---|---|
| skin29 | 0k | - | one name = one face, everywhere. Same-name people in different lists now share a picture. |
| skin52 | 0k | - |  |

## Functions wrapped by 4+ features (change these carefully)

- devPanel (34): skin5, skin10, skin18, skin27, skin31, skin35, skin36, skin37, skin38, skin39, skin40, skin42, skin43, skin46, skin48, skin49, skin53, skin68, skin73, skin74, skin75, skin76, skin77, skin78, skin79, skin80, skin81, skin82, skin84, skin85, skin86, skin87, skin88, skin92
- render (31): skin1, skin8, skin10, skin16, skin20, skin21, skin24, skin25, skin31, skin36, skin40, skin42, skin50, skin51, skin54, skin56, skin57, skin59, skin62, skin63, skin64, skin68, skin73, skin75, skin76, skin79, skin81, skin82, skin87, skin89, skin92
- nextDay (16): skin18, skin31, skin68, skin69, skin74, skin75, skin77, skin80, skin81, skin82, skin85, skin86, skin87, skin88, skin89, skin92
- paneBlock (13): skin7, skin8, skin17, skin31, skin40, skin51, skin61, skin68, skin74, skin77, skin84, skin89, skin92
- openPlace (12): skin24, skin27, skin33, skin34, skin36, skin38, skin42, skin58, skin59, skin60, skin77, skin86
- modal (7): skin9, skin16, skin24, skin26, skin45, skin47, skin63
- paneBeef (5): skin2, skin6, skin13, skin68, skin74
- lickDone (5): skin36, skin39, skin82, skin85, skin86
- phoneMsg (4): skin3, skin45, skin46, skin75
- paneMove (4): skin4, skin6, skin31, skin36
