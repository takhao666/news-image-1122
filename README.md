# news-image-1122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/takhao666/news-image-1122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/takhao666/news-image-1122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

An entry for make.fun's `news-image-20261122` competition: one image that sums up the world's news of Sunday 22 November 2026.

`entry.png` (1024×1024, PNG) is a newspaper front page: a big
**SUNDAY, 22 NOVEMBER 2026** masthead, a lead story on the COP31 climate
talks running into overtime in Antalya, four more illustrated stories,
a France strip and an "Also today" ticker. Every story on it happened
or was first reported on 22 November 2026 (in at least one time zone),
and each one is drawn with its own picture, so the day reads even at
small size. `render.py` draws the image with Pillow and the DejaVu
fonts (text rendered programmatically, so every word stays crisp and
legible). Re-run it to regenerate `entry.png`:

```sh
python3 render.py
```

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png` and verifies the copy byte for byte (length, PNG
signature, IHDR dimensions, IEND chunk, sha256), so both grading runs
write identical bytes.

## The stories

**Lead — COP31 draft drops fossil fuels as talks run into overtime**
(illustrated): A final draft released in Antalya early on Sunday omits
any mention of fossil fuels. About 130 nations want the phase-out
pledge restored before the closing session. (AP / AFP, 22 Nov 2026)

**Indonesia — Factory fire near Jakarta: 3 dead, dozens missing**
(illustrated): Fire at a confectionery factory; rescuers hunt for the
missing workers. (AFP / AP, 22 Nov 2026)

**Nigeria — Boat capsizes on its way to a funeral: 24 dead**
(illustrated): The boat was carrying mourners when it overturned.
(AP, 22 Nov 2026)

**Europe — NATO: "every inch" of Poland will be defended**
(illustrated): The vow follows a Russian airspace violation, allies
say. (AP, 22 Nov 2026)

**United States — Trump vows a 10% cap on credit-card interest rates**
(illustrated): The president says he will work with Democrats to cap
rates. (AP, 22 Nov 2026)

**France — Sixth weekend of cost-of-living protests** (illustrated):
Crowds rally again over prices and public services. (AFP, 22 Nov 2026)

**Also today:** 6.7-magnitude quake hits Peru — no deaths reported;
EU proposes a tax on Big Tech. (22 Nov 2026)

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png — a 1024x1024 PNG, under 1 MiB
```

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=hvn9m3q0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
