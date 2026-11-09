# zh-lyric-adaptation

[简体中文](README.md)

Write Chinese lyrics that fit a Japanese song. Character count comes from the mora count, phrase breaks come from the ear, register comes from the original.

A straight translation of a Japanese lyric crowds the line. Adaptation is rewriting: seven morae in the original means seven characters in Chinese. One extra character and the line will not sit on the melody; one missing and it goes slack. These two scripts handle the mechanical half — split the morae, align the characters, check the result.

## What it is

Japanese morae map roughly onto Chinese characters. Contracted sounds (しょ, ちゃ) count as one mora. The long vowel mark ー, ん and っ each take a mora without producing a new character. The working rule: one romanised syllable per Chinese character, with phrase breaks falling on word boundaries.

Rhymes are sorted loosely into the thirteen rhyme groups (十三辙): yan-qian, zhong-dong, you-qiu, jiang-yang, fa-hua, suo-bo, hui-dui, gu-su, yi-qi, yao-tiao, huai-lai. These names follow the traditional rhyme categories. The coarse grouping is enough for most adaptation work; for finer sets, edit the `GROUPS` table in the script.

## How to use

Both scripts read the same TSV: one line per lyric line, two TAB-separated columns, romanisation first and Chinese second. Morae are separated by `-`, phrase breaks by `|`.

### Alignment table

`src/pair_table.py` sets romanisation beside Chinese, one mora to one character, line for line:

```
$ python3 src/pair_table.py 词.tsv
第1句（6+4）
  no-bo-ru-tsu-ki-wo｜se-o-i-te
  身-负-初-升-之-月｜霜-落-双-肩
```

### Check

`src/check_lyric.py` checks character count, phrase breaks and rhyme line by line. A count that does not match the morae, a break that splits a word, a repeated rhyme character — each one is reported, and the exit code is non-zero:

```
$ python3 src/check_lyric.py 词.tsv
```

### Install

As a Hermes skill:

```bash
rsync -a --exclude .git ./ ~/.hermes/skills/creative/zh-lyric-adaptation/
```

## Layout

```
.
├── README.md
├── README.en.md      English version
├── SKILL.md          adaptation workflow and acceptance rules
├── LICENSE
└── src/
    ├── check_lyric.py   per-line check: syllables, breaks, rhymes
    └── pair_table.py    build the per-mora alignment table
```

## Requirements

Python 3 and `pypinyin`:

```bash
pip install pypinyin
```

If the dependency is missing, `check_lyric.py` says so and exits with code 2. It does not pretend to pass.

## Scope

### A few hard rules

- An LRC line boundary is not a musical phrase boundary. On one 33-line song, two lines were shifted by a whole phrase — the tail of one line belonged to the head of the next. Adapt against LRC timing and one line will always land early and the next late.
- Do not look for beats with a script. Spectral-flux onset detection returned 843 onsets against 381 morae in the song, 2.2× over; autocorrelation gave a 2:1 double peak and no usable beat. The scripts check character count, breaks, rhyme and tone. They do not analyse rhythm.
- Phrase breaks land on word boundaries. A two-character word must not be split by `|`, or the breath cuts the word in half. The singer places the breaks; the machine does not guess them.
- Do not break the one-character-per-mora rule casually. Any algorithm that drops a character by letting the final mora absorb it will be overruled by the ear: the dropped mora does not disappear, it leaves a hole in the middle of the line. If a cut is needed, ask first, and cut only at the end of a line.
- A line that feels wrong usually has the wrong words, not the wrong rhythm. In a lyric written throughout in classical diction, one 「好好地」 or 「指尖」 or 「谎话」 and the voice stops belonging to the character. Keep the mora count and change the register instead.

Further details live in SKILL.md: contracted sounds count as one mora, ー/ん/っ each take one, hand-typed romanisation tends to lose hyphens, the last character before a cut has to be singable on a long note, and the tone at the end of a line follows the melody.

## License

MIT. See [LICENSE](LICENSE).
