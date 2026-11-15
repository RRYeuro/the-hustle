# Code map (auto-made Nov 15)

Each feature is a <script id="skinNjs"> block near the end of index.html, loaded in this order. "Wraps" = old functions it adds behavior to. Later skins run on top of earlier ones.

| Skin | Size | Wraps | Adds (window.*) | Notes |
|---|---|---|---|---|
| skin1 | 1k | render | - | - |
| skin2 | 1k | paneBeef | - | - |
| skin3 | 1k | panePhone, phoneMsg | - | - |
| skin4 | 1k | paneMove | - | - |
| skin5 | 1k | devPanel | _rph | - |
| skin6 | 9k | - | _SR, _rph, _rtick | Move: board, here sections, rest; phone; character card replaces Bag |
| skin7 | 1k | paneBlock | _rideI | - |
| skin8 | 2k | newsPush, paneBlock, render | - | street news with a source + pop-up on new news; street business + stay on Block; appended after the block pane |
| skin9 | 3k | modal | shareImg, shareRun | - |
| skin10 | 18k | act, cmResolve, crewHTML, custoPrice, devPanel, mdBody, placeAct, raid, render, serveCusto | _reok, crewJobs, custoMood, streetEvent | random street events; customer moods; real estate office |
| skin11 | 5k | - | _phLock, _rph | - |
| skin12 | 14k | - | _KB, _MS, _mcomp, _mth | - |
| skin13 | 7k | paneBeef, paneCards, paneCrew, paneExp | _AP13 | Cards; Expenses stub; Me; Your Circle gangs |
| skin14 | 14k | - | sportGame, sportMeet | football: lane runner; basketball: angle + power shot; track: stride pulse; talk it down: de-escalation meter |
| skin15 | 1k | - | - | - |
| skin16 | 3k | modal, render | - | - |
| skin17 | 0k | paneBlock | - | - |
| skin18 | 16k | devPanel, nextDay, paneBiz | _MK | day tick; actions; dev menu |
| skin20 | 2k | - | _blkMore | - |
| skin21 | 3k | - | - | - |
| skin22 | 3k | - | _AP13, _AVX, _MC, _rph | - |
| skin23 | 10k | - | shootoutGame0 | - |
| skin24 | 20k | modal, openPlace, render | _sk24 | pan / zoom; clicks: swallow drags, handle switch; keyboard on the map; tire shop = the gun dealer, opened as a normal place with numbered cards |
| skin25 | 22k | render | _sk25, _tp26 | - |
| skin26 | 4k | modal | _sk26 | - |
| skin27 | 27k | busted, devPanel, lick, openPlace, paneLicks, raid, safeGame | __pcDbg, __srDbg, _l27al, _l27force, _l27q, _sk27, l27Alarm, l27Car | Sort: tap 1 to 16 in order; Pin Cracker: 4 digits, green = right spot, yellow = wrong spot; real loot; pawn shop rows |
| skin28 | 0k | - | _sk28 | - |
| skin29 | 0k | - | _sk29 | - |
| skin30 | 1k | - | _sk30 | loading screen: title art + bar while the first pictures come in |
| skin31 | 22k | busted, devPanel, jsBudget, nextDay, paneMove, plugPrice, qtyModal, render | _sk31, l31Call, l31End, l31Go, l31Intro, l31Meet, l31PullUp, l31Spots | bulk units: what each level sells by; size follows the plug's level; the price of that size follows the quality; the meet; Move map: plug spots |
| skin32 | 0k | - | _sk32, l32Drive | - |
| skin33 | 2k | act, clCarry, l32Drive, openPlace, placeAct | _sk33, l32Drive | - |
| skin34 | 1k | openPlace | _sk34 | - |
| skin35 | 14k | cmResolve, devPanel, heist, paneLicks | __hcAfter, __hcB, __hcCut, __hcP, _sk35, l35Plan, l35Resolve | Licks app: a door to the heists |
| skin36 | 10k | devPanel, lickDone, openPlace, paneMove, raid, render, srvTick | _sk36, l36HTML, l36On, l36Pat | what patrols do (scanner or not); the scanner gives a heads-up on some raids; what the scanner shows; 🚓 on the block tabs and the map |
| skin37 | 11k | act, devPanel, mdBiz, w4Biz | __gig37, _sk37, l37Lane, l37Shift, l37Tow | lane run: delivery and taxi; hook timing: tow truck; running a shift; Business tab: the taxi row, and both delivery buttons share one slot |
| skin38 | 5k | devPanel, openPlace, paneBag | _sk38, l38, l38Fake, l38HTML, l38Sn | daily: respect from crews and your own crew's loyalty; status shows where you look at your fit (character card) and at the mall |
| skin39 | 16k | chase, devPanel, lick, lickDone | __lpDbg, __rfDbg, __vcDbg, _m39force, _m39roof, _sk39, chaseWho, l27Alarm | Lockpick: stop the needle in the green zone, pin by pin; Vault logic: work the code out from the clues; Roof run: jump the gaps and the AC units, rooftop to rooftop; hooks |
| skin40 | 4k | devPanel, paneBlock, render, teenStart | __l39say, _sk40, l39Guide | first-day guide; hidden rules say why |
| skin41 | 2k | - | _sk41 | - |
| skin42 | 4k | cmResolve, devPanel, openPlace, render | _sk42, _t42, l42a, l42q | crew heist result gets its picture; jewelry picture at the pawn shop; dev |
| skin43 | 11k | devPanel, livingDay, paneExp | _l43b, _sk43, l32Drive, l43BailOpts, l43CatchUp, l43Cuts, l43Fee, l43HTML | Bills that bite; lights off: less energy each morning; no insurance: a stop can tow the car; Bail and lawyer choice |
| skin44 | 2k | - | _sk44, l44Ready | - |
| skin45 | 12k | mainMenu, modal, phoneMsg, say, w4Counsel, wCard | _sk45, l45Clean, l45cl, l45greet, l45pl, l45voice | clean language; who is talking; plug lines by level and trust; phone texts rewritten in each person's voice |
| skin46 | 11k | busted, devPanel, l43PhoneOff, l45greet, phoneMsg, plugPrice, w4Court, w4Verdict | _sk46, l43PhoneOff, l45greet, l46bat, l46dodge, l46miss, l46ring, l46sb | callbacks: people remember; plug meet: greeting, callback, pick a tone; texting: voiced replies, haggling, typing dots; battery + signal |
| skin47 | 1k | modal, streetEvent, wCard | _sk47, l47Busy | long cards: picture becomes a thin strip; random street events wait for big moments to finish |
| skin48 | 5k | addXP, devPanel, paneCrew, teenStart, w5bDealers, w5bOrderDay, w5bOrders | _sk48, l48ladder, l48new, l48rk | mark the rank-up so the ladder shows NEW for 2 days; runner orders follow your rank: none at Corner Boy, small at first; starting fresh: nobody begins with a Big plug, whatever their age; runners (Dre, Moe, Tasha) only show up once you reach Petty Dealer |
| skin49 | 5k | devPanel, paneSchool, w5bOrders | _mf49w, _sk49 | runners are recruited, never handed out; school: meet people at lunch; tutorial + dev |
| skin50 | 5k | _AVX, _MC, render | _AVX, _MC, _mcomp, _mth, _rph, _sk50 | friends are contacts |
| skin51 | 10k | _MC, l45greet, paneBlock, plugActions, render | _MC, _mt51h, _sk51, l45greet | every plug you know is a contact; plug card: one Text button instead of a menu; what you can text a plug, built from the old buttons; stood up |
| skin52 | 0k | l32Drive | _sk52, l32Drive | - |
| skin53 | 3k | devPanel, paneExp | _sk53, l53 | the more street money you sit on, the more eyes on you; shows on the Money tab |
| skin54 | 5k | render | _sk54 | who is this thread with; render: thread options + tidy app pages; plain words in the leftover generic replies |
| skin55 | 6k | - | _ct55, _ctg55, _ctq55, _rph, _sk55, l31Text | Contacts: one A-Z list, search, groups, contact cards; Maps; clicks |
| skin56 | 0k | render | _sk56 | - |
| skin57 | 2k | render | _sk57, l57open | opening a locked app another way (old saves, links) says why |

## Functions wrapped by 4+ skins (change these carefully)

- devPanel: skin5, skin10, skin18, skin27, skin31, skin35, skin36, skin37, skin38, skin39, skin40, skin42, skin43, skin46, skin48, skin49, skin53
- render: skin1, skin8, skin10, skin16, skin24, skin25, skin31, skin36, skin40, skin42, skin50, skin51, skin54, skin56, skin57
- openPlace: skin24, skin27, skin33, skin34, skin36, skin38, skin42
- modal: skin9, skin16, skin24, skin26, skin45, skin47
- paneBlock: skin7, skin8, skin17, skin40, skin51
