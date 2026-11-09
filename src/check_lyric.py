#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐句核填词：字数 == 拍数、断点、韵脚部、韵脚重字。

输入文件格式（UTF-8，每行一句，TAB 分隔）：
  no-bo-ru-tsu-ki-wo|se-o-i-te<TAB>身负初升之月|霜落双肩
拍以 - 分隔，断点用 |。无断点的句子两侧都不写 |。

用法: python check_lyric.py lyric.tsv
"""
import sys
from collections import defaultdict

# 词韵粗分（够用即可，必要时自行增补）
GROUPS = {
    "言前": "an ian uan van".split(),
    "中东": "eng ing ong iong".split(),
    "油求": "ou iou".split(),
    "江阳": "ang iang uang".split(),
    "发花": "a ia ua".split(),
    "梭波": "o uo e".split(),
    "灰堆": "ei uei".split(),
    "姑苏": "u".split(),
    "衣期": "i v er".split(),
    "遥条": "ao iao".split(),
    "怀来": "ai uai".split(),
}

def group_of(fin):
    for g, fs in GROUPS.items():
        if fin in fs:
            return g
    return fin

def main(path):
    bad, seen, finals = [], defaultdict(list), {}
    HAVE_PINYIN = True
    for ln, row in enumerate(open(path, encoding="utf-8"), 1):
        row = row.strip()
        if not row or row.startswith("#"):
            continue
        jp, zh = row.split("\t")[:2]
        halves_jp = [h for h in jp.split("|") if h]
        halves_zh = [h for h in zh.split("|") if h]
        if len(halves_jp) != len(halves_zh):
            bad.append((ln, "断点数不同", jp, zh)); continue
        for j, z in zip(halves_jp, halves_zh):
            m = len([x for x in j.split("-") if x])
            n = len([c for c in z if c not in "，、。！？ "])
            if m != n:
                bad.append((ln, f"{m}拍 vs {n}字", j, z))
        last = [c for c in zh if c not in "|，、。！？ "][-1]
        fin = None
        try:
            from pypinyin import lazy_pinyin, Style
            fin = lazy_pinyin(last, style=Style.FINALS)[0]
        except ImportError:
            HAVE_PINYIN = False
        if fin:
            g = group_of(fin)
            seen[g].append((ln, last))
            finals[ln] = (last, fin, g)
            print(f"{ln:3d}  {m:2d}拍/{n:2d}字  末字 {last} ({fin}/{g})   {zh}")
    print("\n不符：", bad if bad else "无")
    if not HAVE_PINYIN:
        print("⚠ 未装 pypinyin：韵脚与韵部两项未检查，本次结果不完整（退出码 2）")
        return 2
    dup = {g: v for g, v in seen.items() if len(v) > 1}
    print("同部多句（正常，词韵通押）：", {g: len(v) for g, v in dup.items()})
    same = defaultdict(list)
    for ln, (ch, fin, g) in finals.items():
        same[ch].append(ln)
    rep = {c: v for c, v in same.items() if len(v) > 1}
    print("韵脚重字：", rep if rep else "无")
    return 0 if not bad and not rep else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
