# -*- coding: utf-8 -*-
"""由 TSV 生成逐拍对照表：罗马音一拍 ↔ 中文一字，上下对齐。

输入同 check_lyric.py：每行 `罗马音\t中文`，拍以 - 分隔，断点用 |。
输出：
  第1句（6+4）
    no-bo-ru-tsu-ki-wo｜se-o-i-te
    身-负-初-升-之-月｜霜-落-双-肩

用法: python pair_table.py lyric.tsv > 对照.txt
"""
import sys


def main(path):
    out = []
    for ln, row in enumerate(open(path, encoding="utf-8"), 1):
        row = row.rstrip("\n")
        if not row.strip() or row.startswith("#"):
            continue
        jp, zh = row.split("\t")[:2]
        jh = [h for h in jp.split("|") if h]
        zh2 = zh.replace("|", "｜")
        zh2 = "｜".join("-".join(list(h.strip())) for h in zh2.split("｜") if h.strip())
        counts = "+".join(str(len([x for x in h.split("-") if x])) for h in jh)
        out.append(f"第{ln}句（{counts}）")
        out.append("  " + jp.replace("|", "｜"))
        out.append("  " + zh2)
        out.append("")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
